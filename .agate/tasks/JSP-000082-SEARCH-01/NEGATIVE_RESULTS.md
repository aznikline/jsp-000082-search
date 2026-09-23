# NEGATIVE_RESULTS — JSP-000082-SEARCH-01 (final, 2026-09-23 ~23:20)

All statements are finite-scope. Nothing here bears on the truth of the
Erdős–Gyárfás conjecture beyond the stated ranges.

## Certified coverage this round (own pipeline)

**No counterexample exists on <= 20 vertices.** Chain:

1. n<=17: ex(n,{C4,C8}) < ceil(3n/2) strictly for every n in 4..17
   (McKay extremal table values; file names encode ex). A delta>=3
   graph needs >=ceil(3n/2) edges > ex, so it cannot be {C4,C8}-free.
   (For n<=15, C16 needs no check since 16>n; for n=16,17 the bound
   alone already excludes {C4,C8}-free delta>=3 graphs.)
2. n=18,19: ex = ceil(3n/2) equality. Any delta>=3 {C4,C8}-free graph
   would be extremal. McKay files audited by tools/mindeg_audit.py
   (sparse6 decoder cross-checked against nauty copyg 2.9.3):
   all 570 (n=18) and 304 (n=19) extremal graphs have min-degree 2.
3. n=20, m=30 (forces cubic): geng -c -f -d3 -D3 generated all 36,101
   connected C4-free cubic graphs; check_g6 (own C DFS, complete, no
   budget) found C8 in EVERY one. 0 survivors. Matches rosharma719's
   manifest count and result independently.
4. n=20, m=31 (extremal): all 94 extremal graphs min-degree 2.

n=20 is additionally closed for disconnected graphs via (1)-(3):
components have <20 vertices, all covered by the chain.

## n=22 (single-order statements, connectivity caveat noted)

- m=33 cubic: 553,227 C4-free cubic graphs generated (geng count
  matches rosharma719 exactly), check_g6: every one contains C8.
  0 survivors.
- m=34 extremal: 13,644 graphs, min-degree 1 (224) or 2 (13,420).
- => no CONNECTED delta>=3 graph on 22 vertices avoids all of
  {C4,C8,C16}. A disconnected n=22 counterexample would need a
  counterexample component on <=21 vertices; n<=20 is closed but
  n=21 is NOT (see below), so "no n=22 counterexample" is conditional
  on the open n=21 layer.

## Open layers encountered (not closed)

- n=21 m=32 (seq 4,3^20): geng -c -f -d3 -D4 generation did not
  complete: ~177 CPU-min count-only attempt + ~108 CPU-min piped
  attempt, both killed at wall deadline. Layer OPEN.
- n=23 m=35 (seq 4,3^22): not started (budget).
- n=24 m=36 cubic: ~122 CPU-min generation, no output before kill.
  Layer OPEN. m=37 layer not started; m=38 extremal audit shows all
  min-deg 2 (980 graphs).
- Cubic n=30 CEGAR (edge-minimal encoding, Glucose3): ~33min wall,
  no candidate; stats lost on kill. Bounded probe only -- NOT coverage.

## Audited but non-conclusive

- McKay extremal files at n=21,22,23,24 (m=ex layers): all min-deg<=2
  -- closes only the top edge-count layer at each order.
- Prior-art audits: rosharma719 reports (not re-derived by me): Z3/Z5
  lifts of the four 24v {C4,C8}-free bases exhausted, 0 survivors;
  order-30 cubic quotient census t>=4 closed (52.6B markings).
  Status: SOURCE_VERIFIED claims, COMPUTATION_NOT_REPRODUCED by me.

## Honest summary

Smallest possible counterexample order: >=21 (this round) -- published
floor is >=17 (Royle-Markstrom); rosharma719 had reached 19.
The genuinely open near-frontier: n=21 m=32, n=23 m=35, all of
n=24..29 non-cubic, cubic n=30.
