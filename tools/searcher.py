"""CEGAR searcher: SAT + lazy forbidden-cycle separation.

Encoding (given N):
  - one boolean per undirected edge pair e_{u,v}, u<v
  - per-vertex totalizer (ubound 4) over incident edge lits:
      obj[2] forced true  => deg(v) >= 3
      obj[3] is reified deg(v)>=4 (bidirectional, verified by tests)
  - edge-minimality (sound reduction): for every pair {u,v}:
      e_{u,v} -> not(deg(u)>=4 and deg(v)>=4)
      i.e. clause (-e_uv, -ge4_u, -ge4_v)
    Justification: deleting an edge whose deletion keeps delta>=3 cannot
    create any cycle; iterating yields an edge-minimal counterexample on
    the same vertex set. So restricting to edge-minimal graphs is complete
    for EXISTENCE of a counterexample at every N.
  - optional degree cap, optional fixed degree sequences
    (RESTRICTED_SEARCH_FAMILY when used -- recorded per shard)

Loop: solve -> extract graph -> detector A over forbidden lengths ->
  found forbidden simple cycle C: add clause OR_{e in C} -e  (block that
  exact cycle instance; never removes other graphs)
  no forbidden cycle: emit CANDIDATE and stop.
"""
import signal
import time

from pysat.solvers import Cadical195
from pysat.card import ITotalizer, CardEnc, EncType
from pysat.formula import IDPool

import cyclecheck_a
from graphio import adjacency


class TimeoutInterrupt(Exception):
    pass


def build_base(n, edge_minimal=True, deg_cap=None, forced_seq=None,
               exact_edges=None):
    """Build (cnf, pool, edge_var) with structural constraints.

    forced_seq: optional sorted tuple degree sequence (restriction).
    exact_edges: optional exact edge count.
    Returns (cnf_clauses, edge_vars dict (u,v)->lit, ge4 dict v->lit).
    """
    pool = IDPool()
    cnf = []
    ev = {}
    for u in range(n):
        for v in range(u + 1, n):
            ev[(u, v)] = pool.id(f"e_{u}_{v}")

    ge4 = {}
    for v in range(n):
        inc = [ev[(min(u, v), max(u, v))] for u in range(n) if u != v]
        if len(inc) < 3:
            cnf.append([])  # deg>=3 impossible for this vertex
            f = pool.id("false4_%d" % v)
            ge4[v] = f
            continue
        if len(inc) < 4:
            # deg>=3 forces all incident edges; deg>=4 impossible
            for e in inc:
                cnf.append([e])
            f = pool.id("false4_%d" % v)
            cnf.append([-f])
            ge4[v] = f
            continue
        cnf.extend(CardEnc.atleast(lits=inc, bound=3, vpool=pool,
                                   encoding=EncType.totalizer).clauses)
        ub = deg_cap if deg_cap else 4
        ub = max(ub, 4)
        tot = ITotalizer(lits=inc, ubound=ub, top_id=pool.top)
        pool.top = tot.top_id
        cnf.extend(tot.cnf.clauses)
        ge4[v] = tot.rhs[3]                 # entailed when deg >= 4
        if deg_cap is not None:
            cnf.append([-tot.rhs[deg_cap]])  # deg <= deg_cap

    if edge_minimal:
        for (u, v), e in ev.items():
            cnf.append([-e, -ge4[u], -ge4[v]])

    if forced_seq is not None:
        # pin exact degrees via equality to each value
        for v in range(n):
            target = forced_seq[v]
            inc = [ev[(min(u, v), max(u, v))] for u in range(n) if u != v]
            cnf.extend(CardEnc.atleast(lits=inc, bound=target,
                                       vpool=pool,
                                       encoding=EncType.totalizer).clauses)
            tot = ITotalizer(lits=inc, ubound=target + 1,
                             top_id=pool.top)
            pool.top = tot.top_id
            cnf.extend(tot.cnf.clauses)
            cnf.append([-tot.rhs[target]])          # deg <= target

    if exact_edges is not None:
        all_e = list(ev.values())
        cnf.extend(CardEnc.atleast(lits=all_e, bound=exact_edges,
                                   vpool=pool,
                                   encoding=EncType.totalizer).clauses)
        tot = ITotalizer(lits=all_e, ubound=exact_edges + 1,
                         top_id=pool.top)
        pool.top = tot.top_id
        cnf.extend(tot.cnf.clauses)
        cnf.append([-tot.rhs[exact_edges]])

    return cnf, ev, ge4, pool


def model_to_edges(n, ev, model):
    ms = set(model)
    return [(u, v) for (u, v), lit in ev.items() if lit in ms]


def cegar_search(n, cnf_base, ev, time_cap=600, iter_cap=None,
                 per_solve_cap=300, cycle_cap=20000, seed=0, log=print):
    """Run the lazy-separation loop. Returns dict with status and stats."""
    solver = Cadical195(bootstrap_with=cnf_base)
    stats = {"iterations": 0, "blocked_cycles": {L: 0 for L in
             cyclecheck_a.forbidden_lengths(n)}, "solve_status": None}
    t0 = time.time()
    result = {"status": "TIMEOUT", "graph": None}

    def handler(signum, frame):
        solver.interrupt()

    old = signal.signal(signal.SIGALRM, handler)
    try:
        while True:
            if time.time() - t0 > time_cap:
                result["status"] = "TIMEOUT"
                break
            if iter_cap is not None and stats["iterations"] >= iter_cap:
                result["status"] = "ITER_CAP"
                break
            remaining = max(1, int(time_cap - (time.time() - t0)))
            signal.alarm(min(per_solve_cap, remaining))
            r = solver.solve_limited()
            signal.alarm(0)
            stats["iterations"] += 1
            if r is None:
                result["status"] = "UNKNOWN_INTERRUPTED"
                break
            if not r:
                result["status"] = "UNSAT"
                break
            g = model_to_edges(n, ev, solver.get_model())
            blocked_any = False
            for L in cyclecheck_a.forbidden_lengths(n):
                cycs, capped = cyclecheck_a.all_cycles_of_length(
                    n, g, L, cap=cycle_cap)
                for wit in cycs:
                    clause = [-ev[(min(wit[i], wit[(i + 1) % L]),
                                   max(wit[i], wit[(i + 1) % L]))]
                              for i in range(L)]
                    solver.add_clause(clause)
                    stats["blocked_cycles"][L] += 1
                    blocked_any = True
                stats["cycle_enum_capped"] = stats.get(
                    "cycle_enum_capped", 0) + (1 if capped else 0)
            if not blocked_any:
                result["status"] = "SAT_CANDIDATE"
                result["graph"] = g
                break
    finally:
        signal.signal(signal.SIGALRM, old)
        solver.delete()
    result["stats"] = stats
    result["elapsed"] = time.time() - t0
    return result
