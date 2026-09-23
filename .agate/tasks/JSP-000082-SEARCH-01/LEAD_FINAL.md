# LEAD_FINAL — JSP-000082-SEARCH-01 (2026-09-23)

VERDICT: STOP_NO_HIT

## ORIGINAL STATEMENT
Attacked: every finite simple undirected graph, minimum degree >=3,
contains a simple cycle of length 2^k for some k>=2 (Erdos-Gyarfas,
Erdos #64 / JSP-000082). Quantifiers unchanged; only the negative
direction (find one finite counterexample) was attacked, per task.

## SEARCH COVERAGE
Closed this round (own pipeline, all layers enumerated and checked):
- n <= 20: no delta>=3 graph without a 2-power cycle exists
  (n<=17 extremal inequality; n=18,19 extremal min-deg audits;
  n=20 cubic layer 36,101 graphs + m=31 extremal audit; disconnected
  n=20 reduces to components <=19).
- n=22 connected, all layers (m=33 cubic 553,227 graphs; m=34 extremal
  audit): no connected counterexample on exactly 22 vertices; the
  unconditional claim is conditional on the open n=21 layer.

NOT covered: n=21 m=32 layer (generation did not finish), n=23 m=35,
n=24 m=36/37, all of n=24..29 non-cubic, cubic n>=30 exhaustive.

## RESULT
No counterexample found. No candidate ever entered verification.

## INDEPENDENT VERIFICATION
- Detector A (Python DFS, min-vertex-rooted) vs verifier B (SAT
  existence encoding): 0 mismatches on fixtures + 40 random graphs.
- C checker (check_g6.c) vs detector A: 0 mismatches on 304 graphs.
- sparse6 decoder vs nauty copyg: identical output on all 7 files.
- geng counts reproduced rosharma719's manifests exactly
  (36,101 / 553,227).
- Survivor-triggered V1-V4 flow never activated (0 survivors).

## RESOURCE USAGE
Budget: 24 core-h CPU / 8 h wall / <=4 workers / <=4 GiB / <=10 GiB.
Actual: ~9.2 core-h CPU (est. from per-shard times incl. killed runs),
~7.6 h wall, peak 4 workers (cap honored), <1 GiB RAM, <50 MiB repo.

## REMAINING UNCERTAINTY
- geng enumeration completeness is nauty's theorem, not mine;
  C4-freeness of generated output was independently re-verified.
- No DRAT/proof-checked UNSAT anywhere; all closures are
  generation+checking certificates (counts + zero survivors).
- Killed shards leave open layers as listed.

## INVESTMENT DECISION
Recommend STOP for this exact approach: geng-based layer closure is
hitting the wall at n=21-24 near-cubic layers (>2 CPU-h each). A next
round would need either res/mod parallel sharding across many cores
(authorized budget required) or a structural reduction (e.g. Carr
M1-M4 + 3-connectivity) to shrink layers. The CEGAR lottery was
inconclusive, not evidence either way.

REMOTE_REPOSITORY=https://github.com/aznikline/jsp-000082-search
REMOTE_BRANCH=agent/jsp000082-search-01-owner
REMOTE_EXACT_HEAD=709f28ae9536d1cdbb91364ec73b3de0041c591b
TESTED_CODE_SHA(short16): graphio.py=2e543c70ddb0e8b0; cyclecheck_a.py=1215deedf1aa5997; verify_b.py=576360e0a77b548f; searcher.py=8326451f976ecde3; check_g6.c=305f095b787063d8; run_shard.py=d4e155d2a0455046; cegar_shard.py=ead9c8c6e9ec2865; mindeg_audit.py=45f9c41f6ff79c0d; tests.py=f2f61e3aa4bc8f3e
TASK_PATH=.agate/tasks/JSP-000082-SEARCH-01/
TREE_CLEAN=YES
SEARCH_STATUS=STOP_NO_HIT
VALIDATOR_A=tools/cyclecheck_a.py (DFS, min-rooted, witness output)
VALIDATOR_B=tools/verify_b.py (SAT existence encoding, independent)
LEAN_STATUS=NOT_STARTED (no candidate reached V1-V4)
AXIOM_AUDIT=N/A
