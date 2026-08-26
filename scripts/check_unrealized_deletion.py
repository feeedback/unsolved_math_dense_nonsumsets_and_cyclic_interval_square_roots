#!/usr/bin/env python3
"""Independently check an exact-output deletion witness by root enumeration."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path


PROBLEM_ID = "AIM-COMBINATORICS-0232"
SCHEMA_VERSION = 1


class CertificateError(ValueError):
    """Raised when a deletion certificate is invalid."""


def require_residue_list(value: object, prime: int, label: str) -> list[int]:
    if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
        raise CertificateError(f"{label} must be an integer list")
    if value != sorted(set(value)) or any(not 0 <= item < prime for item in value):
        raise CertificateError(f"{label} must contain unique canonical residues")
    return value


def verify(document: dict[str, object]) -> dict[str, object]:
    if document.get("schema_version") != SCHEMA_VERSION:
        raise CertificateError("unsupported schema version")
    if document.get("problem_id") != PROBLEM_ID:
        raise CertificateError("wrong problem identifier")
    prime = document.get("prime")
    if not isinstance(prime, int) or prime < 2:
        raise CertificateError("invalid prime")
    if any(prime % divisor == 0 for divisor in range(2, int(prime**0.5) + 1)):
        raise CertificateError("field order is composite")

    palette = require_residue_list(document.get("palette"), prime, "palette")
    deletion = require_residue_list(document.get("deletion"), prime, "deletion")
    claimed = require_residue_list(document.get("nonsumset"), prime, "nonsumset")
    if set(palette) & set(deletion):
        raise CertificateError("palette and deletion must be disjoint")
    if document.get("deletion_size") != len(deletion):
        raise CertificateError("deletion_size does not match deletion")

    universe = set(range(prime))
    candidate = universe - set(palette) - set(deletion)
    if candidate != set(claimed):
        raise CertificateError("nonsumset is not the complement of E union T")

    represented = False
    roots_checked = 0
    for size in range(prime + 1):
        for root_tuple in combinations(range(prime), size):
            roots_checked += 1
            sums = {(left + right) % prime for left, right in product(root_tuple, repeat=2)}
            if sums == candidate:
                represented = True
                break
        if represented:
            break
    if represented:
        raise CertificateError("claimed nonsumset has a self-sumset root")
    if document.get("roots_enumerated") != roots_checked:
        raise CertificateError("roots_enumerated does not match independent enumeration")

    payload_document = dict(document)
    claimed_hash = payload_document.pop("payload_sha256", None)
    payload = json.dumps(payload_document, sort_keys=True, separators=(",", ":")).encode()
    if claimed_hash != hashlib.sha256(payload).hexdigest():
        raise CertificateError("payload checksum mismatch")
    return {
        "status": "verified",
        "prime": prime,
        "roots_checked": roots_checked,
        "nonsumset_size": len(candidate),
        "implementation_independence": {
            "imports_generator": False,
            "root_enumeration": "itertools.combinations by cardinality",
            "sum_operation": "itertools.product over residue tuples",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    try:
        raw = parse_args().certificate.read_text(encoding="utf-8")
        report = verify(json.loads(raw))
    except (CertificateError, json.JSONDecodeError, OSError) as error:
        print(f"certificate rejected: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
