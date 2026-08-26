# Pinned dependencies

## Imported mathematical theorem

The only recent, nonstandard critical input is Shouqiao Wang's proposed
solution of Erdős Problem 788:

- repository: `https://github.com/ShouqiaoW/erdos.git`;
- commit: `d28713ac8245ca86a686b8c67370a8d19d81b242`;
- proof directory: `788/lean`;
- Lean: `4.27.0`;
- Mathlib: `a3a10db0e9d66acbebf76c5e6a135066525ac900`;
- terminal theorem: `Erdos788.erdos788`;
- license at the pin: MIT.

The exact source hashes and the public independent review links are in
`problem/sources.md`. The local rebuild result is in `external/erdos-788/`.

## Optional full Lean reproduction

The default package verification does not clone or build external code. To
repeat the heavyweight imported proof check separately:

```bash
git clone https://github.com/ShouqiaoW/erdos.git
git -C erdos checkout d28713ac8245ca86a686b8c67370a8d19d81b242
cp external/erdos-788/AxiomCheck.lean erdos/788/lean/AxiomCheck.lean
cd erdos/788/lean
lake build
lake env lean AxiomCheck.lean
```

The recorded clean run completed 7,936 build jobs and printed exactly
`[propext, Classical.choice, Quot.sound]` for the terminal theorem. The build
is reproducible but not minimal: external reviewers have requested a more
reviewable boundary before accepting it into `formal-conjectures`.

## Local package requirements

- Python 3.11 or newer for the one-command finite checks;
- no third-party Python packages;
- a standard LaTeX installation or Tectonic 0.17.0 only if rebuilding the PDF.
