"""Cycle verifier B: SAT existence encoding -- independent of the DFS detector.

For each candidate root vertex s (intended minimum vertex of the cycle),
encode: positions 0..L-1, x[i][v] = vertex v occupies position i.
  - exactly one vertex per position
  - each vertex used at most once across positions
  - consecutive positions (incl. L-1 -> 0) must be adjacent in G
  - x[0][s] fixed; positions 1..L-1 restricted to vertices > s
    (root-is-minimum canonicalization: sound for existence, since every
    simple cycle has a unique minimum vertex)

Graph must be supplied as (n, edges). Returns witness list or None.
"""
from pysat.solvers import Cadical195
from pysat.formula import IDPool

from graphio import adjacency


def _solve_rooted(n, adj, L, s):
    pool = IDPool()
    cnf = []
    x = [[pool.id(f"x_{i}_{v}") for v in range(n)] for i in range(L)]

    # exactly one vertex per position
    for i in range(L):
        cnf.append([x[i][v] for v in range(n)])
        for a in range(n):
            for b in range(a + 1, n):
                cnf.append([-x[i][a], -x[i][b]])
    # each vertex at most once
    for v in range(n):
        for i in range(L):
            for j in range(i + 1, L):
                cnf.append([-x[i][v], -x[j][v]])
    # root fixed, others > s
    cnf.append([x[0][s]])
    for i in range(1, L):
        for v in range(0, s + 1):
            cnf.append([-x[i][v]])
    # adjacency: x[i][v] -> OR_{u in N(v)} x[i+1][u]
    for i in range(L):
        ni = (i + 1) % L
        for v in range(n):
            cnf.append([-x[i][v]] + [x[ni][u] for u in adj[v]])
    with Cadical195(bootstrap_with=cnf) as solver:
        if not solver.solve():
            return None
        model = set(solver.get_model())
    cyc = []
    for i in range(L):
        vs = [v for v in range(n) if x[i][v] in model]
        if len(vs) != 1:
            raise RuntimeError("bad model")
        cyc.append(vs[0])
    return cyc


def find_cycle_of_length_sat(n, edges, L):
    adj = adjacency(n, edges)
    adj = [sorted(a) for a in adj]
    for s in range(n):
        r = _solve_rooted(n, adj, L, s)
        if r is not None:
            return r
    return None


def forbidden_lengths(n):
    out, L = [], 4
    while L <= n:
        out.append(L)
        L *= 2
    return out


def scan_forbidden_sat(n, edges):
    return {L: find_cycle_of_length_sat(n, edges, L)
            for L in forbidden_lengths(n)}
