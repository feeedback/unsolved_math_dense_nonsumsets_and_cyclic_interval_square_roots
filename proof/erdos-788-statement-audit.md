# Erdős 788 formal-statement audit

Audit date: 2026-08-26

Source commit: `d28713ac8245ca86a686b8c67370a8d19d81b242`

This audit checks that the theorem imported by the prime-cyclic transfer is
actually present in the pinned Lean development. It does not audit every proof
term in the 43-file development and does not assert external acceptance.

## Canonical finite definition

`Erdos788/Definitions.lean` defines

- `I n = Finset.Ioo n (2*n)`;
- `J n = Finset.Ioo (2*n) (4*n)`;
- `Admissible n B C` as `C subset I n` with `c+c' notin B` for every two
  distinct members `c,c'` of `C`;
- `Guarantees n t` with quantifier order
  `forall B subset J n, exists C, Admissible n B C and t <= |B|+|C|`;
- `fNat n` as the greatest natural number satisfying `Guarantees n`;
- `f n` as the integer coercion of `fNat n`.

Theorems `fNat_guarantees`, `le_fNat`, and
`f_isGreatestIntegerGuarantee` prove the intended maximum property. Equal
summands are excluded only in the independent-set condition, exactly as in
Erdős Problem 788. This is the convention needed for a simple sum graph.

## Exact graph min--max identity

`Erdos788/GraphFormulation.lean` defines `paletteGraph n B` on the subtype
`I n`, with adjacency

`x != y and x.val + y.val in B`.

It then defines

`graphScore n B = |B| + indepNum(paletteGraph n B)`

and minimizes that score over every `B subset J n`. The theorem
`fNat_eq_minGraphScore` proves equality with `fNat n`; the theorem
`exists_graphScore_eq_minGraphScore` supplies an actual minimizing palette.
Thus the formal theorem is not merely a one-sided guarantee or an infimum over
an unrelated class.

## Exact interval normalization

`Erdos788/Normalization.lean` supplies all endpoint and graph facts required
for the import:

- `vertexEquivFin n : Vertex n equiv Fin (n-1)` translates an original vertex
  by `n+1`;
- `attainableNormalizedSums N = Finset.Icc 1 (2*N-3)`;
- `isAttainableNormalizedSum_iff_mem` proves that this is exactly the set of
  sums of two distinct vertices of `Fin N`, including the small degenerate
  orders;
- `normalizePalette n B` keeps precisely the attainable colors whose translate
  by `2*n+2` lies in `B`;
- `paletteGraphIso` proves the original and normalized graphs are isomorphic;
- `indepNum_paletteGraph_eq_sumGraph` proves exact equality of independence
  numbers;
- `graphScore_activePalette_le` deletes colors that label no edge without
  increasing the score;
- `graphScore_activePalette_eq_normalized` identifies the remaining original
  score with normalized palette cardinality plus normalized independence
  number.

The normalized graph `sumGraph N A` is simple: its adjacency theorem is

`x != y and x.val + y.val in A`.

## Identity with the interval score used here

Define outside Lean

`g(N) = min_{Q subset {1,...,2N-3}} (|Q| + alpha(H_Q))`,

where `H_Q` is the simple sum graph on `{0,...,N-1}`. Then

`g(N) = fNat(N+1)`.

To check both directions, first let `Q` be any attainable normalized palette.
The theorem `fNat_le_of_normalized_palette` in
`Erdos788/EveryNFinite.lean` gives

`fNat(N+1) <= |Q| + indepNum(sumGraph N Q)`.

Minimizing over `Q` gives `fNat(N+1) <= g(N)`.

Conversely, choose `B subset J(N+1)` with score `fNat(N+1)` using
`exists_graphScore_eq_minGraphScore` and `fNat_eq_minGraphScore`. Replace it
by `activePalette (N+1) B`, then normalize. The active score cannot exceed the
minimum score, but it is itself an allowed original score, so it equals that
minimum. `graphScore_activePalette_eq_normalized` then gives an attainable
normalized palette with score `fNat(N+1)`. Hence `g(N) <= fNat(N+1)`.

This proves the exact identity, including the `N+1` shift recorded in the
project transfer proof.

## Asymptotic theorem extracted

`Erdos788/Statement.lean` defines `HasExponentOneHalf` with explicit epsilon
quantifiers:

`forall epsilon>0, eventually n^(1/2-epsilon) <= f(n) <= n^(1/2+epsilon)`.

`Erdos788/FinalTheorem.lean` proves

`Erdos788.erdos788 : MainTheorem`,

and `MainTheorem` contains both `PaperMainTheorem` and the exact original
upper question. In particular it contains `HasExponentOneHalf`.

Combining that conclusion with `g(N)=fNat(N+1)` gives

`g(N)=N^(1/2+o(1))`.

The shift is harmless with full quantifiers: apply the external estimate at
`n=N+1`; for any fixed positive epsilon, `N+1<=2N` and the constant factor
`2^(1/2+epsilon)` is at most `N^epsilon` for all sufficiently large `N`.
The lower bound transfers in the same way. The prime-cyclic construction only
needs the upper direction.

## Audit decision

The formal statement and normalization are faithful to the interval-palette
theorem used in `interval-palette-transfer.md`. No assumption about cyclic
groups or nonsumsets is hidden in the import; those are separate project
lemmas.

The pinned project passed a clean local build of all 7,936 jobs on 2026-08-26.
The local axiom audit reported exactly `[propext, Classical.choice,
Quot.sound]`, and the three normalization entry points used above type-checked
in the same run. The reproducible manifest, checker, hashes, and exact output
are in `experiments/general-nonsumset/erdos-788-rebuild/`.

This closes the local build and statement-fidelity gates. It does not turn the
recent external proposal into a peer-reviewed or community-accepted theorem;
that evidence boundary remains stated in the status audit.
