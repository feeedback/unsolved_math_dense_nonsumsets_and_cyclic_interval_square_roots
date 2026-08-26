# Sources and exact pins

Checked: 2026-08-26. SHA-256 values identify the exact bytes inspected.
Third-party PDFs are not redistributed in this package.

## Canonical AIM problem

- E. Croot and V. F. Lev (collectors), *Problems Presented at the Workshop on
  Recent Trends in Additive Combinatorics*, Problem 2.7 (B. Green), page 7.
- URL: <https://aimath.org/WWN/additivecomb/additivecomb.pdf>
- inspected PDF SHA-256:
  `7b1d12368aaf38bf6787ff0d3750d03e08c8ec95c78424d1f2c232a2a3c182d5`.

## Published lower-bound input

- Noga Alon, “Large sets in finite fields are sumsets,” *Journal of Number
  Theory* 126 (2007), 110–118.
- DOI: <https://doi.org/10.1016/j.jnt.2006.11.007>
- author PDF: <https://web.math.princeton.edu/~nalon/PDFS/sumset.pdf>
- inspected PDF SHA-256:
  `e9d4670e3d5ee07162d581fe9f28930dfb16f146686b9551994c4d4c981b19cd`.

The manuscript uses Alon's inclusive theorem and displays the conversion to
the strict threshold `d(p)` explicitly.

## Imported interval theorem

- Shouqiao Wang, proposed solution of Erdős Problem 788.
- repository: <https://github.com/ShouqiaoW/erdos>
- pinned commit: `d28713ac8245ca86a686b8c67370a8d19d81b242`.
- paper TeX SHA-256:
  `23a67830fc417649992a6c247b441ee79fb50d5e51db8f39a5c9b5f4db907b17`.
- paper PDF SHA-256:
  `9450d86d06f1439a8a7702bc0aed6f8915239153ba26de19985fe5c22a5dd2f9`.
- `Statement.lean` SHA-256:
  `66f4950df5d2db6856fcd5720b86bb1931c9131e619789c33eb5783b83ec3b76`.
- `FinalTheorem.lean` SHA-256:
  `50f2ffb56595ce8f60dc117bc344f8c19a0a1a99d1c2d39035b8fda958bb8c6f`.
- Mathlib commit:
  `a3a10db0e9d66acbebf76c5e6a135066525ac900`.
- public independent rebuild:
  <https://github.com/ShouqiaoW/erdos/issues/3>.
- external review record:
  <https://github.com/google-deepmind/formal-conjectures/pull/4587>.

The pinned Lean tree has an MIT license and built cleanly in the recorded local
and public independent checks. The external pull request was closed pending a
more reviewable proof boundary and mathematical vetting, explicitly without a
negative claim about correctness.

## UnsolvedMath record identity

- dataset: `ulamai/UnsolvedMath` v1.6.0;
- revision: `c5d16bab227526df173907935b21c39c28d16b94`;
- record: `AIM-COMBINATORICS-0232`;
- canonicalized record SHA-256:
  `39175d651a6131617733fcec22dec0aa4a47cc323873c22a95c4cb0ddbed1b78`.

The dataset is selection metadata, not authority for correctness, novelty, or
problem status.
