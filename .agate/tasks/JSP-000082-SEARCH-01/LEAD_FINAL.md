# LEAD_FINAL — JSP-000082-SEARCH-01 (2026-09-23)

VERDICT: STOP_NO_HIT

## ORIGINAL STATEMENT
Attacked: every finite simple undirected graph, minimum degree >=3,
contains a simple cycle of length 2^k for some k>=2 (Erdos-Gyarfas,
Erdos #64 / JSP-000082). Quantifiers unchanged; only the negative
direction (find one finite counterexample) was attacked, per task.

## SEARCH COVERAGE
Closed by this round's own chain (all edge layers at each order
enumerated and checked):
- n <= 20: no delta>=3 graph without a 2-power cycle exists
  (n<=17 extremal inequality; n=18,19 extremal min-deg audits;
  n=20 cubic layer 36,101 graphs + m=31 extremal audit; disconnected
  n=20 reduces to components <=19).
- exactly n=22: closed unconditionally. Connected case via m=33 cubic
  (553,227 graphs, all contain C8) + m=34 extremal audit. Disconnected
  case by argument: a delta>=3 component needs >=4 vertices, so every
  component of a disconnected 22-vertex graph has <=18 <=20 vertices
  and is already excluded.
- NOT closed as a range: "all n<=22" fails only at n=21 (m=32 layer
  generation killed at deadline). Garcia (arXiv:2609.04686) reports
  DRAT-certified exclusion through n=23; NOT reproduced by this task,
  so n=21,23 are "not covered here", not "open frontier".

NOT covered: n=21 m=32, n=23 m=35, n=24 m=36/37, all of n=24..29
non-cubic, cubic n>=30 exhaustive.

## RESULT
No counterexample found. No candidate ever entered verification.

## INDEPENDENT VERIFICATION
Three distinct levels; do not conflate:
- Detector calibration: DFS (A) vs SAT-existence encoding (B) agreed
  on fixtures + 40 random graphs; C checker vs A agreed on 304 graphs;
  sparse6 decoder vs nauty copyg identical on all 7 files. This
  validates the CHECKERS, not that a second algorithm re-checked every
  generated graph.
- Computational exclusion: named geng commands ran to completion,
  check_g6 processed all output, 0 survivors; extremal-file audits ran
  on downloaded .s6 data with recorded hashes. Counts 36,101 / 553,227
  matching rosharma719's manifests is a reproduction check, not a
  second independent enumeration algorithm. No DRAT, no Lean.
- Original-statement result: no candidate found; says nothing about
  the conjecture beyond covered ranges.
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
Archived per lead decision: ARCHIVED -- NO ACTIVE SEARCH BUDGET.
This was a scoped reproduction/probe, not a frontier push: no
candidate emerged, no structural lead emerged, and the layers left
uncovered here (n=21, n=23) are already claimed closed by Garcia's
DRAT-certified preprint. Raw compute alone is not justified; a future
round needs new evidence — a proved search-space reduction, a
construction that plausibly avoids 2-power cycles, or a located flaw
in a published computation — not merely unfinished shards.

REMOTE_REPOSITORY=https://github.com/aznikline/jsp-000082-search
REMOTE_BRANCH=agent/jsp000082-search-01-owner
VERIFIED_AT_READBACK_HEAD=709f28ae9536d1cdbb91364ec73b3de0041c591b
NOTE: the line above is the remote HEAD confirmed by readback at the
time that verification ran (pre-archive-commit). The final delivery
HEAD is whatever origin/agent/jsp000082-search-01-owner reports after
the archive commit push; this file intentionally does not record its
own containing commit.
TESTED_CODE_SHA(short16): graphio.py=2e543c70ddb0e8b0; cyclecheck_a.py=1215deedf1aa5997; verify_b.py=576360e0a77b548f; searcher.py=8326451f976ecde3; check_g6.c=305f095b787063d8; run_shard.py=d4e155d2a0455046; cegar_shard.py=ead9c8c6e9ec2865; mindeg_audit.py=45f9c41f6ff79c0d; tests.py=f2f61e3aa4bc8f3e
TASK_PATH=.agate/tasks/JSP-000082-SEARCH-01/
TREE_CLEAN=YES
SEARCH_STATUS=STOP_NO_HIT
VALIDATOR_A=tools/cyclecheck_a.py (DFS, min-rooted, witness output)
VALIDATOR_B=tools/verify_b.py (SAT existence encoding, independent)
LEAN_STATUS=NOT_STARTED (no candidate reached V1-V4)
AXIOM_AUDIT=N/A
