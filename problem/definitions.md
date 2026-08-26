# Definitions and scope

## Field and subsets

For prime `p`, identify `F_p` with `{0,1,...,p-1}` under addition modulo `p`.
Subsets are extensional; ordering and multiplicity do not matter. Both the
empty set and the full field are allowed choices for `A` and `B`.

## Unrestricted self-sumset

For `B subset F_p`,

`B+B = {(x+y) mod p : x in B, y in B}`.

The same set `B` occurs twice. Equal summands are allowed, so `{b}+{b}={2b}`.
The empty root has the empty self-sumset.

## Extremal and complement functions

`A` is a nonsumset if no `B subset F_p` satisfies `A=B+B`. Define

`M(p) = max{|A| : A is a nonsumset in F_p}`

and the strict complement threshold

`d(p) = p-M(p)`.

The word *strict* matters: every set with complement smaller than `d(p)` is a
self-sumset, while at complement exactly `d(p)` at least one nonsumset exists.

## Excluded interpretations

- restricted sums requiring `x != y`;
- two independently chosen roots `B+C`;
- containment or covering instead of equality;
- nonempty, proper, large, or structured root restrictions;
- composite cyclic groups or extension fields;
- a subsequence of primes in place of all sufficiently large primes.
