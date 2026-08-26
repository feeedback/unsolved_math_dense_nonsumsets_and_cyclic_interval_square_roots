# Canonical problem statement

Canonical identifier: `AIM-COMBINATORICS-0232`

Canonical source: AIM Problem 2.7, attributed to B. Green

## Original wording

> What is the size of the largest subset of F_p which is not a sumset B+B?

The source is *Problems Presented at the Workshop on Recent Trends in Additive
Combinatorics*, collected by E. Croot and V. F. Lev, PDF page 7. Exact source
metadata and the inspected PDF checksum are in `sources.md`.

## Normalized statement

Let `p` be prime and let addition be in `F_p`. For every `B subset F_p`, define
the unrestricted self-sumset

`B+B = {b_1+b_2 : b_1 in B and b_2 in B}`.

Define

`M(p) = max{|A| : A subset F_p and A != B+B for every B subset F_p}`.

Determine the asymptotic behavior of `M(p)` as `p -> infinity` through the
primes.

## Candidate answer under review

The manuscript claims

`M(p) = p - p^(1/2+o(1))`.

This is the general asymptotic question, not a finite subcase. The proof imports
the interval theorem from the pinned proposed solution of Erdős Problem 788;
the status of that dependency is stated separately in `DEPENDENCIES.md`.
