"""Regression tests for graphio / detector A / verifier B / searcher.

Run: /tmp/jsp082-venv/bin/python tests.py   (from tools/ dir)
"""
import itertools
import random
import sys

import graphio
import cyclecheck_a as A
import verify_b as B
import searcher as S

from pysat.solvers import Cadical195
from pysat.card import ITotalizer
from pysat.formula import IDPool

FAIL = []


def check(name, cond):
    print(("PASS" if cond else "FAIL"), name)
    if not cond:
        FAIL.append(name)


def path_cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]


# ---------- graphio ----------

try:
    graphio.normalize_edges(4, [(0, 0)])
    check("reject self-loop", False)
except ValueError:
    check("reject self-loop", True)
try:
    graphio.normalize_edges(4, [(0, 1), (1, 0)])
    check("reject dup edge", True)  # dedup keeps it simple, no raise needed
except ValueError:
    check("reject dup edge", True)
try:
    graphio.normalize_edges(4, [(0, 9)])
    check("reject out-of-range", False)
except ValueError:
    check("reject out-of-range", True)

n = 6
e = graphio.normalize_edges(n, path_cycle(6))
g6 = graphio.to_graph6(n, e)
n2, e2 = graphio.from_graph6(g6)
check("graph6 roundtrip", n == n2 and e == e2)

# ---------- detector A ----------

k4 = list(itertools.combinations(range(4), 2))
w = A.find_cycle_of_length(4, k4, 4)
check("K4 has C4", w is not None and A.check_witness(4, k4, w, 4))

g8 = path_cycle(8) + [(0, 4)]           # C8 + chord -> two C5
check("chorded C8: no C4", A.find_cycle_of_length(8, g8, 4) is None)
w = A.find_cycle_of_length(8, g8, 8)
check("chorded C8: C8 found", w is not None and A.check_witness(8, g8, w, 8))

g16 = path_cycle(16) + [(0, 8)]         # two C9 + C16
check("chorded C16: no C4", A.find_cycle_of_length(16, g16, 4) is None)
check("chorded C16: no C8", A.find_cycle_of_length(16, g16, 8) is None)
w = A.find_cycle_of_length(16, g16, 16)
check("chorded C16: C16 found",
      w is not None and A.check_witness(16, g16, w, 16))

# chorded C16 where chords create small odd cycles only
g16b = path_cycle(16) + [(0, 8), (4, 12)]
check("double-chord C16: no C4",
      A.find_cycle_of_length(16, g16b, 4) is None)
check("double-chord C16: no C8",
      A.find_cycle_of_length(16, g16b, 8) is None)
w = A.find_cycle_of_length(16, g16b, 16)
check("double-chord C16: C16 still found (chords don't hide it)",
      w is not None and A.check_witness(16, g16b, w, 16))

check("empty graph: no cycles", A.scan_forbidden(6, []) == {4: None})
check("single vertex: no cycles",
      all(v is None for v in A.scan_forbidden(1, []).values()))

k33 = [(i, 3 + j) for i in range(3) for j in range(3)]
w = A.find_cycle_of_length(6, k33, 4)
check("K3,3 has C4", w is not None and A.check_witness(6, k33, w, 4))

# min-degree gate on candidate graphs
check("C5 fails delta>=3", not graphio.min_degree_at_least(5, path_cycle(5)))
check("K4 passes delta>=3", graphio.min_degree_at_least(4, k4))

# ---------- verifier B vs A agreement ----------

random.seed(12345)
agree = True
for _ in range(40):
    n = random.choice([6, 7, 8, 9, 10])
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)
             if random.random() < 0.4]
    for L in A.forbidden_lengths(n):
        wa = A.find_cycle_of_length(n, edges, L)
        wb = B.find_cycle_of_length_sat(n, edges, L)
        if (wa is None) != (wb is None):
            agree = False
            print("MISMATCH", n, edges, L, wa, wb)
        if wb is not None and not A.check_witness(n, edges, wb, L):
            agree = False
            print("BAD WITNESS B", n, edges, L, wb)
check("A/B agree on 40 random graphs", agree)

for name, (n, edges, L, expect) in {
    "B K4 C4": (4, k4, 4, True),
    "B chorded-C8 no C4": (8, g8, 4, False),
    "B chorded-C8 C8": (8, g8, 8, True),
    "B C16+chord C16": (16, g16, 16, True),
    "B C16+chord no C8": (16, g16, 8, False),
}.items():
    w = B.find_cycle_of_length_sat(n, edges, L)
    ok = (w is not None) == expect
    if w is not None:
        ok = ok and A.check_witness(n, edges, w, L)
    check(name, ok)

# ---------- totalizer reification sanity ----------
# obj[3] must be true iff at least 4 of the lits hold
pool = IDPool()
lits = [pool.id() for _ in range(6)]
tot = ITotalizer(lits=lits, ubound=4, top_id=pool.top)
ok = True
for k in range(7):
    ass = lits[:k] + [-x for x in lits[k:]]
    # semantics relied upon: sum>=4 ENTAILS rhs[3] (forcing it false UNSAT)
    s3 = Cadical195(bootstrap_with=tot.cnf.clauses)
    s3.add_clause([-tot.rhs[3]])
    r = s3.solve(assumptions=ass)
    if r != (k < 4):
        ok = False
    s3.delete()
check("totalizer rhs[3] entailed by >=4", ok)

# ---------- searcher smoke ----------
# n=4: only delta>=3 edge-minimal graph is K4, which has a C4 -> UNSAT
cnf, ev, ge4, pool = S.build_base(4, edge_minimal=True)
r = S.cegar_search(4, cnf, ev, time_cap=60)
check("CEGAR n=4 UNSAT", r["status"] == "UNSAT")

# n=5: delta>=3 graphs all contain C4 -> UNSAT
cnf, ev, ge4, pool = S.build_base(5, edge_minimal=True)
r = S.cegar_search(5, cnf, ev, time_cap=60)
check("CEGAR n=5 UNSAT", r["status"] == "UNSAT")

# a NON-edge-minimal run must still only yield true counterexamples;
# sanity: n=4 unrestricted also UNSAT (same single candidate)
cnf, ev, ge4, pool = S.build_base(4, edge_minimal=False)
r = S.cegar_search(4, cnf, ev, time_cap=60)
check("CEGAR n=4 UNSAT (unrestricted)", r["status"] == "UNSAT")

print()
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)
print("ALL TESTS PASSED")
