# SOURCE_AUDIT — JSP-000082 / Erdős #64

Audit date: 2026-09-23. Scope: this problem only.

## Original statement (exact quantifiers)

erdosproblems.com #64 / formal-conjectures `FormalConjectures/ErdosProblems/64.lean`:

> Does every finite graph with minimum degree at least 3 contain a
> cycle of length 2^k for some k >= 2?

Lean reference statement (verbatim semantics):
`∀ (V : Type*) (G : SimpleGraph V) [Fintype V], G.minDegree ≥ 3 →
 ∃ (k) (v) (c : G.Walk v v), k ≥ 2 ∧ c.IsCycle ∧ c.length = 2^k`

- Graph: finite, simple, undirected (SimpleGraph over a Fintype).
- Minimum degree >= 3 on every vertex.
- Forbidden cycle lengths for an N-vertex counterexample:
  {2^k | k>=2, 2^k <= N} — ALL of them must be absent. Cycles are
  *simple* (closed walks with distinct internal vertices); chords do
  not disqualify a cycle.
- Known conjecture name: Erdős–Gyárfás conjecture (1995).
- teorth/erdosproblems status: `falsifiable` (open), prize $1000.
  JSP-000082 maps to Erdős #64 (NOT #82; the dcdreamy PR cited 82).

## Known mathematical/computational bounds

| claim | scope | source | status |
|---|---|---|---|
| any counterexample needs >= 17 vertices | general δ>=3 | Royle & Markström, exhaustive search | SOURCE_VERIFIED / COMPUTATION_NOT_REPRODUCED |
| cubic counterexample needs >= 30 vertices | cubic | Royle & Markström | SOURCE_VERIFIED / COMPUTATION_NOT_REPRODUCED |
| bipartite counterexample needs >= 30 | bipartite δ>=3 | reported, source TBC (rosharma L12) | UNCONFIRMED SOURCE |
| ex(n,{C4,C8}) table n=4..23 | all graphs | B. McKay extremal data (users.cecs.anu.edu.au/~bdm/data/extremal.html), transcribed by rosharma719 | SOURCE_VERIFIED via transcription; spot-check possible |
| n<=17: ex(n,{C4,C8}) < ceil(3n/2) strictly ⇒ no δ>=3 {C4,C8}-free graph ⇒ no counterexample | general | arithmetic on McKay table | DERIVED (needs only ex values) |
| n=18,19: equality; all extremal graphs have min-deg 2 ⇒ no δ>=3 {C4,C8}-free | general | McKay .s6 files + rosharma719 min-deg audit (files present in their repo, checksummed) | SOURCE_VERIFIED / not yet re-run by me |
| cubic C4-free n=20 (36,101) and n=22 (553,227): all contain C8 | cubic | rosharma719 geng pipeline, logs/p1_n20_23 | SOURCE_VERIFIED claim; 36,101 reproduced by me 2026-09-23 (geng count identical); C8-check rerun pending |
| n=21 m=32 (4,3^20) and n=23 m=35 (4,3^22) near-cubic layers | these layers only | rosharma719: started, NOT finished | OPEN LAYER — target of this task |
| minimal counterexample structure | order-minimal cex | Carr 2026: deg>=4 vertices independent, >=4/7 cubic vertices | SOURCE_VERIFIED |
| every even-order minimal cex, 17<=n<=33, is 3-connected | minimal cex | rosharma719 (via Whitney ineq. + their F-series) | PROVED_IN_MARKDOWN by them / NOT_FORMALLY_VERIFIED |
| order-30 cubic, >=4 triangles eliminated (52.6B markings) | cubic n=30, t>=4 | rosharma719 order-30 quotient census | SOURCE_VERIFIED claim / NOT REPRODUCED |
| Z3 and Z5 cyclic lifts of the 4 known order-24 {C4,C8}-free bases | lift family | rosharma719 z3_lifts/z5 audits | exhausted, 0 survivors (their runs) |
| Markström 24-vertex cubic {C4,C8}-free graphs | 4 graphs | Markström; only 2-power cycle is C16 | SOURCE_VERIFIED |

The "general >=24 vertices" and "cubic bipartite >=60" figures from the
earlier scan were leads; the sourced values are 17 (general) and 30
(cubic). Bipartite >=30 unconfirmed.

## Competition audit (this problem only)

- plby/lean-proofs: no Erdos064 file (tree checked at pinned
  8822f7dd, 2026-09-15 snapshot). Not covered.
- TheJustinSunPrize/awards PRs (all states):
  - PR #3532 (OPEN, dcdreamy-code): "register Lean formalization" —
    inspected diff: `Erdos82.lean` proves `Nat.Prime 2`,
    `2+3+5+7=17` etc. Unrelated trivialities, wrong problem number.
    Not a solution.
  - PR #667 (OPEN, CollinYuanjieRen): infinite 3-regular tree —
    the problem is finite graphs; infinite case is a misreading.
    Not a solution.
  - No award-claim issues for JSP-000082.
- rosharma719/erdos64: very large multi-branch research repo
  (consolidated/canonical). No counterexample found; extensive partial
  structure. Their research notes are leads, not trusted theorems.
- google-deepmind/formal-conjectures: statement only (`sorry`).

=> No credible complete solution or counterexample is registered.
First-counterexample investment remains legitimate.

## What was actually reproduced vs read

- Reproduced now: geng count of C4-free cubic graphs at n=20 =
  36,101 (exact match to rosharma's manifest).
- Read only (not re-run): everything else in the table above.
