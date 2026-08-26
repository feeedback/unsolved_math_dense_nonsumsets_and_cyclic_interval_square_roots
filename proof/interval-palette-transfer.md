# Prime-cyclic transfer from an interval sum palette

Status: candidate complete upper-bound proof. The pinned external Lean rebuild
and statement audit passed; independent adversarial review remains pending.

Audit date: 2026-08-26

Linear issue: `RIS-560`

## Result to transfer

For an integer `N >= 1` and a palette

`Q subset {1, ..., 2N-3}`,

let `H_Q` be the simple graph on `{0, ..., N-1}` in which distinct vertices
`x,y` are adjacent when `x+y in Q`. Define

`g(N)=min_Q (|Q|+alpha(H_Q))`.

Wang's solution of Erdős Problem 788 proves

`g(N)=N^(1/2+o(1))`.

The paper uses the parameter `n=N+1`, and its exact min--max identity identifies
`g(N)` with its function `f(N+1)`. Its upper bound is enough below; the lower
bound only confirms that the displayed exponent notation is two-sided. The
source, commit, checksums, and Lean entry points are pinned in
`problem/sources.md`.

## Lemma 1: interval palettes give a prime-cyclic palette

Let `P` tend to infinity through the primes and write the standard
representatives of `G=F_P` as the disjoint union of two consecutive intervals

`V_0={0,...,N_0-1}`

and

`V_1={N_0,...,P-1}`,

where `N_0=ceil(P/2)` and `N_1=floor(P/2)`.

For `i in {0,1}`, choose a minimizing interval palette `Q_i` for `g(N_i)`.
If `V_i=a_i+{0,...,N_i-1}`, put

`E_i={2a_i+q mod P:q in Q_i}`

and `E=E_0 union E_1`. Let `Gamma_E` be the simple Cayley-sum graph on `G`,
where distinct `x,y` are adjacent when `x+y in E`.

Then

`|E|+alpha(Gamma_E) <= g(N_0)+g(N_1)=P^(1/2+o(1))`.

In fact the left side is itself `P^(1/2+o(1))`, not merely bounded above
at that scale.

### Proof

The image defining `E_i` cannot have more elements than `Q_i`, so

`|E| <= |Q_0|+|Q_1|`.

Let `R` be independent in `Gamma_E`. For `x=a_i+u` and `y=a_i+v` in
`R intersect V_i`, with `x != y`, membership `u+v in Q_i` would imply

`x+y = 2a_i+u+v in E_i subset E`

in `F_P`, contradicting independence. Translation by `a_i` therefore sends
`R intersect V_i` to an independent set in `H_(Q_i)`. Hence

`|R| <= alpha(H_(Q_0))+alpha(H_(Q_1))`.

Maximizing over `R` and adding the palette bound proves the first inequality.
Since both `N_i=(1/2+o(1))P` and `g(N)=N^(1/2+o(1))`, the right side is
`P^(1/2+o(1))`. Modular collisions between translated palettes only decrease
`|E|` and can only add edges, so wraparound causes no loss. QED.

For the claimed two-sided exponent, put `e=|E|`. Every vertex of
`Gamma_E` has degree at most `e`: for each selected sum there is at most one
possible neighbor. The greedy independence bound therefore gives

`alpha(Gamma_E) >= P/(e+1)`.

Consequently

`e+alpha(Gamma_E) >= e+P/(e+1) >= 2 sqrt(P)-1`.

Together with the constructed upper bound, this proves
`|E|+alpha(Gamma_E)=P^(1/2+o(1))`. The lower estimate is not needed by the
nonsumset construction, but it makes the score statement in `RIS-560`
literally two-sided.

## Lemma 2: a square-root palette gives a dense nonsumset

Suppose that `E subset G` satisfies

`|E|+alpha(Gamma_E) <= h(P)`,

where `h(P)=P^(1/2+o(1))`. Then, for all sufficiently large `P`, there is a
set `T subset G\E` such that

`|T|=4h(P)`

and `G\(E union T)` is not a self-sumset. Floors may be inserted if `h(P)` is
not initially integer-valued.

### Proof

Put `e=|E|`, `r=alpha(Gamma_E)`, and `t=4h(P)`. For large `P`,
`e+t<P`. The number of possible `t`-element sets `T subset G\E` is

`binom(P-e,t)`.

For every root candidate `B subset G` with `|B|<=r`, equality

`B+B=G\(E union T)`

determines at most one `T`, namely

`T=(G\E)\(B+B)`.

There are at most

`sum_(j=0)^r binom(P,j) <= (P+1)P^h`

such candidates. On the other hand,

`binom(P-e,t) >= ((P-e)/t)^t`.

Because `h=P^(1/2+o(1))`, the logarithm of the latter lower bound is

`(2+o(1))h log P`,

whereas the logarithm of `(P+1)P^h` is `(1+o(1))h log P`. Thus the number of
choices for `T` is strictly larger for all sufficiently large `P`; fix one
which is not determined by any candidate root of size at most `r`.

Set `A=G\(E union T)`. If `A=B+B`, then for every two distinct elements
`b,b' in B`, their sum lies outside `E`. Therefore `B` is independent in the
simple graph `Gamma_E`, so `|B|<=r`. Equality would then make `T` the excluded
choice determined by this `B`, a contradiction. The use of a simple graph is
safe: diagonal sums are not needed to bound `|B|`, while the assumed equality
still determines all of `T`. QED.

## Corollary: the AIM exponent

Apply Lemma 1 and then Lemma 2. The constructed nonsumset has complement size

`|E|+|T| <= 5h(P)=P^(1/2+o(1))`.

In the strict Alon--Pham convention `d(P)=P-M(P)`, this proves

`d(P) <= P^(1/2+o(1))`.

Alon's 2007 theorem proves

`d(P) >= Omega(sqrt(P/log P))=P^(1/2-o(1))`.

Consequently

`d(P)=P^(1/2+o(1))`

and, in the canonical AIM notation,

`M(P)=P-P^(1/2+o(1))`.

## Evidence boundary

The two transfer lemmas above are elementary and written in full. The only
substantial imported theorem is the interval palette result. Its public Lean
development is unusually strong evidence, but this project will not label the
AIM problem resolved until all of the following hold:

1. the pinned Lean development builds locally;
2. its formal statement is checked against the paper's interval min--max
   definition;
3. the prime-cyclic transfer is reviewed independently, including simple-graph
   diagonals, modular wraparound, and the second-layer counting inequality;
4. a full proof artifact cites the external theorem at its exact pinned
   version and records its MIT license and checksum;
5. a final novelty/status search checks whether this transfer has already been
   published or publicly claimed.
