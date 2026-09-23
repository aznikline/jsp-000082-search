# VALIDATOR_TESTS

Components (three separated):

1. `tools/graphio.py` — edge-list/graph6 IO, normalization, SHA-256,
   structural validation (rejects self-loops, out-of-range endpoints,
   odd token counts; dedups mirrored pairs).
2. `tools/cyclecheck_a.py` — detector A: DFS simple-cycle existence per
   target length, minimum-vertex-rooted canonicalization, returns a
   concrete witness vertex list. `check_witness` is an independent
   small checker (distinct vertices, consecutive edges exist, correct
   length). `all_cycles_of_length` enumerates all cycles of a length
   (cap-guarded) for batch blocking.
3. `tools/verify_b.py` — verifier B: SAT existence encoding
   (position-vertex vars, one-per-position, all-different, adjacency,
   root-is-minimum canonicalization). Different algorithm class from A.
4. `tools/check_g6.c` — streaming C checker for geng pipelines:
   verifies min degree and absence of all requested 2-power lengths
   by complete DFS (no budget). Survivors echoed to stdout.
5. `tools/searcher.py` — CEGAR searcher (Cadical): edge vars,
   deg>=3 via CardEnc.totalizer, edge-minimality clauses
   (e_uv -> ~(deg u>=4 and deg v>=4)), lazy forbidden-cycle blocking.

## Regression results (tools/tests.py, all PASS, 2026-09-23)

- K4 -> C4 witness (validated by check_witness)
- C8 + chord 0-4 -> no C4, C8 found (chorded simple cycle counted)
- C16 + chord 0-8 -> no C4, no C8, C16 found
- C16 + chords 0-8 & 4-12 -> no C4, no C8, C16 still found
  (chords do not hide a simple cycle)
- empty graph / single vertex -> no cycles; C5 fails delta>=3; K4 passes
- K3,3 -> C4
- A vs B agreement: 40 random graphs x all forbidden lengths, 0 mismatch;
  every B witness validated by check_witness
- C checker vs detector A: 304 graphs (incl. all fixtures), 0 mismatches
- totalizer rhs semantics verified empirically (sum>=k entails rhs[k-1];
  one-directional -- the direction edge-minimality needs)
- CEGAR smoke: n=4 UNSAT (K4 has C4), n=5 UNSAT, unrestricted n=4 UNSAT

## Calibration

| run | outcome |
|---|---|
| CEGAR n=8 edge-minimal | UNSAT, 62 iters, 0.04 s |
| CEGAR n=10 edge-minimal | UNSAT, 5577 iters, 62k clauses, 35.9 s |
| CEGAR n=12 edge-minimal | TIMEOUT 240 s, 34,832 iters, 512k clauses -- CEGAR-to-UNSAT does not scale; not used for layer closure |
| geng -c -f -d3 -D3 20 30:30 | 36,101 graphs in 35 s (matches rosharma719 manifest exactly) |

Conclusion: generation+checker (geng 2.9.3 + check_g6) is the closure
pipeline; CEGAR retained as an open-ended search tool only.
