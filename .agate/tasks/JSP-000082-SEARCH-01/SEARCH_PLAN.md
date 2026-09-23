# SEARCH_PLAN — frozen 2026-09-23

Target: general finite simple graph, delta>=3, no simple cycle of
length 2^k (k>=2, 2^k<=N). No unconditional restriction to a graph
class. Connectivity restriction is sound (a connected component of a
counterexample is a counterexample); used only in generation, flagged
where it matters for layer-closure claims.

## Certified frontier used as floor

- n<=17: ex(n,{C4,C8}) < ceil(3n/2) strictly -> no delta>=3 {C4,C8}-free
  graph exists (McKay extremal values, SOURCE_VERIFIED).
- n=18,19: equality; extremal files all min-deg 2 (re-audit planned;
  files downloaded from McKay's page directly).
- Cubic n<30: Royle-Markstrom published bound (SOURCE_VERIFIED, not
  reproduced); rosharma719 verified cubic C4-free at n=20,22 all have
  C8 (36,101 / 553,227; 36,101 count reproduced by me).

Consequence: the lowest genuinely-open orders are the non-extremal
delta>=3 layers at n=20..23 plus everything at n=24..29 (non-cubic),
cubic n=30.

## Shards (generation pipeline: geng -> check_g6; survivors get
## detector-A + verifier-B + hash-locked V1-V4)

S0  n=18,19 extremal-file min-degree audit (McKay .s6, direct download)
S1  n=20 m=31, -c -f -d3 (-D5 forced by degree sum): extremal layer.
    Direct .s6 audit substitutes if generation too slow.
S2  n=21 m=32, -c -f -d3 -D4  (seq 4,3^20; rosharma-flagged unfinished)
S3  n=21 m=33, -c -f -d3 -D6  (extremal layer; .s6 audit substitute)
S4  n=22 m=34, -c -f -d3 -D5  (extremal layer; .s6 audit substitute)
S5  n=23 m=35, -c -f -d3 -D4  (4,3^22; rosharma-flagged unfinished)
S6  n=23 m=36, -c -f -d3 -D6  (extremal layer; .s6 audit substitute)
S7  cubic n=30 CEGAR lottery (time-capped; RESTRICTED_FAMILY: cubic,
    3-connected not assumed -- unrestricted cubic CEGAR)
S8  reproduction: n=20 cubic m=30 through my checker (36,101 expected)

Completeness claims per shard: a shard closed with 0 survivors +
verified generation count = "no connected delta>=3 {C4,C8,C16}-free
graph in that layer"; combined with the floor this becomes "no
counterexample on <= N vertices" only for fully covered (n,m) ranges.
n<=23 needs every m in [ceil(3n/2), ex(n)].

## What may be missed (explicit)

- geng -f generation is trusted for completeness of the C4-free class;
  check_g6 independently re-verifies C4 absence on generated output,
  but completeness of enumeration is nauty's theorem, not mine.
- Disconnected delta>=3 graphs at n are covered only via the floor
  (their components have <n vertices).
- Orders n=24..29 general and cubic n=30 are not exhaustively covered
  by this plan; S7 is a bounded lottery, not coverage.
