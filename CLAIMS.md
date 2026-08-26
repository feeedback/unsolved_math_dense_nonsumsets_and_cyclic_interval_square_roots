# Claim boundary

## Main claim

For primes `p -> infinity`,

`M(p) = p - p^(1/2+o(1))`,

where `M(p)` is the maximum size of a subset of `F_p` that is not an
unrestricted self-sumset `B+B`.

## Dependency chain

1. **Canonical statement.** The AIM wording and all conventions are frozen in
   `problem/statement.md` and `problem/definitions.md`.
2. **Known lower boundary.** Alon's 2007 theorem gives the required lower
   exponent for the strict complement threshold after an explicit integer
   endpoint conversion.
3. **Imported theorem.** Wang's pinned Erdős 788 development supplies an
   interval palette of score `N^(1/2+o(1))` for every sufficiently large `N`.
4. **New transfer.** Two consecutive interval charts produce a cyclic palette
   in `F_p` with the same exponent-scale score.
5. **New exact-output layer.** A strict binomial count selects a second deletion
   set that is not the complement of any exact self-sumset output.
6. **Squeeze.** The lower and upper complement exponents match.

## Evidence labels

- Item 2 is a cited published theorem.
- Item 3 is an external machine-checked proposal, independently rebuilt and
  statement-audited, but not peer-reviewed or community-accepted.
- Items 4 and 5 are project proofs presented in full in the manuscript and
  checked on exhaustive finite fixtures.
- The assembled result is a candidate complete proof, not a novelty or
  community-acceptance claim.

The critical review questions are whether the imported theorem is faithful and
correct, whether the interval charts cover every residue without adding an
uncontrolled edge, and whether the exact-output root count is injective in the
direction used. `REVIEW_CHECKLIST.md` makes these attacks explicit.
