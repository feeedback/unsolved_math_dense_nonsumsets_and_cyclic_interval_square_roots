# AI assistance disclosure

This proof package is substantially AI-assisted.

- Language models were used for proof search, literature triage, code, proof
  revision, and adversarial review.
- The final project proof passed an internal QED run using `gpt-5.6-sol` at
  `xhigh` reasoning with the recorded limits `8/4/4`.
- The interval theorem imported from Shouqiao Wang's Erdős 788 repository is
  itself presented by that repository as an AI-assisted proposed solution.
- Lean kernel checking establishes the pinned formal theorem relative to its
  definitions and standard axioms. It does not establish informal-statement
  fidelity, novelty, attribution, importance, or peer review.
- The finite Python checks in this package were independently implemented at
  the code level, but they do not prove the asymptotic theorem.

No independent human expert has yet accepted the complete chain. Reviewers
should treat every prose proof step as requiring ordinary mathematical
scrutiny and should report any ambiguity in statement normalization before
reviewing downstream deductions.
