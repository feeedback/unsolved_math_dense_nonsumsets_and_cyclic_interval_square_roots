# Pinned Erdős 788 Lean rebuild

Date: 2026-08-26

## Outcome

The pinned external development at commit
`d28713ac8245ca86a686b8c67370a8d19d81b242` completed a clean local
`lake build`: 7,936 of 7,936 jobs passed. The remote `HEAD` and `main` still
pointed to the same commit at the end of the run.

The source tree contains 47 tracked files under `788/lean`, including 43 Lean
files. A targeted scan found no occurrences of `sorry`, `admit`, `axiom`,
`unsafe`, or `native_decide` in those Lean sources.

## Environment

- macOS 26.6.2 build 25G83, arm64;
- Lean 4.27.0, commit
  `db93fe1608548721853390a10cd40580fe7d22ae`;
- Lake `5.0.0-src+db93fe1`;
- Mathlib commit `a3a10db0e9d66acbebf76c5e6a135066525ac900`.

## Axiom and bridge check

The repository-local `AxiomCheck.lean` had the same bytes as
`axiom-check.lean` in this directory and was run with:

```text
lake env lean AxiomCheck.lean
```

It exited successfully and printed:

```text
Erdos788.fNat_eq_minGraphScore (n : ℕ) : Erdos788.fNat n = Erdos788.minGraphScore n
Erdos788.graphScore_activePalette_eq_normalized (n : ℕ) (B : Finset ℕ) :
  Erdos788.graphScore n (Erdos788.activePalette n B) =
    (Erdos788.normalizePalette n B).card + (Erdos788.sumGraph (n - 1) (Erdos788.normalizePalette n B)).indepNum
Erdos788.fNat_le_of_normalized_palette (n : ℕ) (A : Finset ℕ) (hA : A ⊆ Erdos788.attainableNormalizedSums (n - 1)) :
  Erdos788.fNat n ≤ A.card + (Erdos788.sumGraph (n - 1) A).indepNum
'Erdos788.erdos788' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are the exact bridge declarations used in the separate formal-statement
audit. The axiom set is the standard classical quotient/propositional set
reported by the prior public independent rebuild; no project-specific axiom
appears.

## Evidence boundary

This run establishes reproducible local compilation and the declared axiom
boundary. It does not independently re-prove the 43-file formal development
on paper, establish publication priority, or imply peer review. The external
repository has an MIT license at the pinned commit (SHA-256
`b0777d8a7d69f639b78fecad8e394f04561c21048f2b5e4c46c49d468d37625f`).
No external source file is copied here; only this project-authored check,
hashes, commands, and output are retained.
