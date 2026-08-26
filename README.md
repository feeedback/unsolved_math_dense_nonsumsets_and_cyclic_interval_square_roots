# Dense nonsumsets and cyclic-interval square roots

Private reviewer package for
[`AIM-COMBINATORICS-0232`](https://www.unsolvedmath.com/problems/AIM-COMBINATORICS-0232),
AIM Problem 2.7 (B. Green).

## Claimed result

For primes `p -> infinity`, let `M(p)` be the largest cardinality of a subset
of `F_p` which is not `B+B` for any `B subset F_p`, with equal summands
allowed. The manuscript gives the candidate complete proof

`M(p) = p - p^(1/2+o(1))`.

The new deduction transfers an interval-palette theorem to the cyclic group
and then uses an exact-output deletion count. The interval theorem is imported
from Shouqiao Wang's proposed solution of Erdős Problem 788. Its pinned Lean
development builds without forbidden placeholders, but the theorem has not
yet been peer-reviewed or accepted by the mathematical community. This package
therefore does **not** claim novelty, peer review, or community resolution.

## Review order

1. Read `problem/statement.md` and `problem/definitions.md`.
2. Read `CLAIMS.md` and `DEPENDENCIES.md` to see the exact imported boundary.
3. Read `paper/aim-nonsumsets.pdf` or its TeX source.
4. Inspect the two new components in `proof/`.
5. Use `REVIEW_CHECKLIST.md` for an adversarial pass.
6. Run the local verification command below.

## One-command verification

Only Python's standard library is needed:

```bash
python3 scripts/verify_bundle.py
```

This command verifies every packaged byte against `MANIFEST.sha256`, exhausts
all palette pairs through cyclic order nine, checks finite counting positive
and negative fixtures, independently regenerates a small exact-output witness,
rejects tampered witnesses, and rejects internal workflow identifiers or
machine-local home paths.

These executable checks validate finite instances and package integrity. They
are sanity checks for the elementary reductions, not a formal proof of the
asymptotic theorem. The optional full imported Lean rebuild is documented in
`DEPENDENCIES.md`.

For a byte-reproducible manuscript build with Tectonic 0.17.0:

```bash
SOURCE_DATE_EPOCH=0 tectonic --outdir /tmp/nonsumset-paper paper/aim-nonsumsets.tex
```

## Deliberate omissions

This reviewer repository excludes the full research workspace, candidate
selection history, UnsolvedMath dataset snapshot, agent transcripts, QED logs,
token accounting, caches, and third-party PDFs. Primary sources are cited by
versioned URL and checksum in `problem/sources.md`. The Wang Lean tree remains
in its original MIT-licensed repository at an exact commit.

## Publication state

This is a private review draft, not an arXiv preprint. Authorship and citation
metadata must be confirmed by the repository owner before wider circulation.
See `AI_DISCLOSURE.md` and `REVIEW_TERMS.md`.
