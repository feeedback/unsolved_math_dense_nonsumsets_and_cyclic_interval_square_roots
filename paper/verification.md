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

`ea783041314540e9ea319235606065d277bedfd2c2488e8300c05671934315a2`.

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

## Formalization boundary

The imported interval theorem has a pinned Lean proof. The new cyclic transfer
and deletion argument are supplied as complete prose proofs with deterministic
finite regressions; they do not yet have a Lean formalization. Accordingly,
the package is a candidate proof for expert review, not a fully formal proof of
the AIM theorem.
