# Manuscript verification

Verified: 2026-08-26

## Build

The included PDF was compiled from `aim-nonsumsets.tex` with
`SOURCE_DATE_EPOCH=0` and the official Tectonic 0.17.0 macOS arm64 release.
The release archive checksum was
`a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667`.
The build completed without unresolved references, LaTeX warnings, overfull
boxes, or underfull boxes.

Packaged PDF SHA-256:

`679f3348d88e2438e13a7c50cb037a0900c41abdad9334f8d4706b30f44310c3`.

Two clean builds in separate temporary directories produced this same digest.

The package-level `MANIFEST.sha256` independently covers both TeX and PDF.

## Assembly checks

- The canonical maximum `M(p)` and strict complement `d(p)=p-M(p)` are stated
  together.
- Alon's inclusive endpoint is converted to the strict integer bound.
- Wang's `n=N+1` normalization is stated before the cyclic transfer.
- Chart coverage, palette collisions, modular reduction, distinct-pair
  adjacency, and the two-sided score are addressed.
- The deletion proof uses a strict finite inequality and proves that a root
  determines at most one deletion set.
- Equal summands and the empty root remain in scope.
- Every exponent conversion displays its `o(1)` dependency.

## Editorial structure

The intended reader is a research mathematician familiar with elementary
additive combinatorics and graph independence numbers. The manuscript does not
re-teach those prerequisites. It instead follows the usual research-paper
sequence: concise abstract, contextual introduction, main statement, imported
results, new lemmas, assembled theorem proof, and a separate evidence appendix.

- The introduction identifies the precise contribution and imported boundary.
- A five-step roadmap exposes the role of each later section before notation
  becomes dense.
- The root-size bridge is a named lemma rather than an inference hidden inside
  the counting argument.
- Every displayed estimate used later has a semantic label and cross-reference.
- Computational and source-audit evidence is outside the mathematical proof.

Authorship and final venue-specific metadata remain deliberately unresolved in
this private review draft.

## Formalization boundary

The imported interval theorem has a pinned Lean proof. The new cyclic transfer
and deletion argument are supplied as complete prose proofs with deterministic
finite regressions; they do not yet have a Lean formalization. Accordingly,
the package is a candidate proof for expert review, not a fully formal proof of
the AIM theorem.
