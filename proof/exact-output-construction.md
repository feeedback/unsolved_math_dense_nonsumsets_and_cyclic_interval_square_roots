# Exact-output construction of a dense nonsumset

Status: proved project lemma, independently checked by QED and finite regression.

Audit date: 2026-08-26

## Input

Let `p` be prime, `G=F_p`, and let `E subset G`. Define the simple graph
`Gamma_E` on `G` by joining distinct `x,y` when `x+y in E`. Put

`e=|E|`, `r=alpha(Gamma_E)`, and `H=e+r`.

The preceding interval-to-cyclic transfer supplies such palettes for all
sufficiently large primes with

`2 sqrt(p)-1 <= H <= p^(1/2+eta_p)`, where `eta_p -> 0`.

No random-Cayley assumption is used below.

## Exact finite counting lemma

For every sufficiently large `p`, put `k=4H`. Then

`k <= p-e`

and

`binom(p-e,k) > sum_(j=0)^r binom(p,j)`.

### Proof

Take `p` large enough that

`eta_p <= 1/16`, `log(8)/log(p) <= 1/16`, and `5p^(9/16) <= p`.

Then `3 <= H <= p^(9/16)`. Since `e <= H`,

`e+4H <= 5H <= p`,

so `k=4H <= p-e`. Also `p-e >= p/2` for large `p`. For integers
`0<k<=n`, each factor in the product for `binom(n,k)` is at least `n/k`, so

`binom(n,k) >= (n/k)^k`.

With `n=p-e` and `k=4H`, this yields

`log binom(p-e,4H) >= 4H log(p/(8H))`.

The chosen thresholds and `H<=p^(9/16)` give

`log(p/(8H)) >= (1-9/16-1/16)log(p) = (3/8)log(p)`.

Consequently

`binom(p-e,4H) >= p^(3H/2)`.

On the other hand,

`sum_(j=0)^r binom(p,j) <= sum_(j=0)^r p^j <= p^(r+1)`.

Since `r<=H` and `H>=3`,

`p^(r+1) <= p^(H+1) <= p^(4H/3) < p^(3H/2)`.

This proves the strict finite inequality. No asymptotic equivalence is used
inside the pigeonhole step.

## Construction

Let `T` range over the `k`-element subsets of `G\E`. Call `T` realized if

`B+B = G\(E union T)`

for some `B subset G`, with equal summands allowed.

Every root of a realized output is independent in `Gamma_E`: if distinct
`x,y in B` had `x+y in E`, then their sum would belong both to `B+B` and to
the deleted palette. Hence `|B|<=r`. There are at most

`sum_(j=0)^r binom(p,j)`

possible roots. A fixed root determines at most one deletion set, because

`T=(G\(B+B))\E`.

The exact counting lemma therefore shows that not all `k`-element deletion
sets are realized. Choose an unrealized `T` and set

`A=G\(E union T)`.

By construction `A` is not `B+B` for any `B`. Since `E` and `T` are disjoint,

`|G\A|=e+4H <= 5H <= 5p^(1/2+eta_p)=p^(1/2+o(1))`.

This proves the missing upper bound for the strict complement threshold.

## Edge cases and conventions

- The empty root is counted among the candidates.
- Equal summands remain allowed in the target self-sumset. The loopless graph
  is used only for the necessary condition on distinct pairs.
- Diagonal sums cannot invalidate the argument: a realized equality still
  forces all of `B+B` to avoid `E`, and it still determines `T` uniquely.
- Palette collisions were already absorbed into the actual integer `e=|E|`.
- The deletion size is the integer `4H`; no floor or ceiling is hidden.

## Deterministic finite witness mode

`scripts/find_unrealized_deletion.py` enumerates roots and eligible deletion
sets in lexicographic order for small primes. It emits the first unrealized
`T` as a checksum-protected certificate. `scripts/check_unrealized_deletion.py`
does not import the generator: it independently enumerates roots by cardinality
using immutable tuples and Cartesian products.

Example:

```bash
python3 scripts/find_unrealized_deletion.py \
  --prime 5 --palette '' --deletion-size 1 \
  --output /tmp/unrealized-deletion.json
python3 scripts/check_unrealized_deletion.py \
  --certificate /tmp/unrealized-deletion.json
```

This finite mode validates the exact-output mechanism, not the asymptotic
existence of the imported interval palettes.
