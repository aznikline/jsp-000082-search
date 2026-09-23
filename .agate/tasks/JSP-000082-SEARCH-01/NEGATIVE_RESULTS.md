# NEGATIVE_RESULTS — JSP-000082-SEARCH-01 (in progress)

All results below are *finite-scope* statements. None is a proof or
disproof of Erdős–Gyárfás.

## Extremal-layer min-degree audits (McKay .s6, downloaded 2026-09-23
## from users.cecs.anu.edu.au/~bdm/data/extremal.html, re-decoded and
## min-degree-audited by tools/mindeg_audit.py, cross-checked vs nauty
## copyg 2.9.3)

| file | graphs | edges | min-deg hist | delta>=3? |
|---|---|---|---|---|
| c48_n18e27.s6 | 570 | 27 | all 2 | 0 |
| c48_n19e29.s6 | 304 | 29 | all 2 | 0 |
| c48_n20e31.s6 | 94 | 31 | all 2 | 0 |
| c48_n21e33.s6 | 12 | 33 | all 2 | 0 |
| c48_n22e34.s6 | 13644 | 34 | 1:224, 2:13420 | 0 |
| c48_n23e36.s6 | 3257 | 36 | all 2 | 0 |
| c48_n24e38.s6 | 980 | 38 | all 2 | 0 |

Consequence (combined with ex-table strictness n<=17): every delta>=3
{C4,C8}-free graph at n=18..24 would have to be non-extremal, i.e. live
in layers ceil(3n/2) <= m < ex(n). At n=18,19 there is no such layer
(equality) -> n<=19 fully closed: no delta>=3 graph without a 2-power
cycle exists on <=19 vertices (this re-derives rosharma719's theorem
from the primary data source, independently of their code).

## Generation shards (geng 2.9.3 -> check_g6, own checker)

| shard | layer | outcome |
|---|---|---|
| S8 n=20 m=30 cubic | 36,101 C4-free cubic graphs | 0 survivors: every one has C8 (hitL: C4=0, C8=36101, C16=0). Reproduces rosharma719. |

=> n=20 fully closed (m=30 by S8, m=31 by extremal audit).

## Running / pending

- S2 n=21 m=32 (seq 4,3^20): generating
- S10 n=22 m=33 cubic: generating
- S9 n=24 m=36 cubic: generating
- S7 CEGAR cubic n=30 lottery: 90-min cap
- planned if time: n=23 m=35, n=24 m=37, n=22 cubic check cross-run

## Explicitly NOT covered this round

- n=25..29 general layers, cubic n=26/28 (published bound covers
  cubic <30 anyway), cubic n>=30 exhaustive
- Any claim about the infinite/open problem itself
