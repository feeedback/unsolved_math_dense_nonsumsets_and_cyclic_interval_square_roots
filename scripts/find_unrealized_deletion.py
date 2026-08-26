#!/usr/bin/env python3
"""Find a finite exact-output deletion witness for the nonsumset construction."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path


PROBLEM_ID = "AIM-COMBINATORICS-0232"
SCHEMA_VERSION = 1


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor for divisor in range(2, int(value**0.5) + 1)
    )


def elements_to_mask(elements: set[int]) -> int:
    return sum(1 << element for element in elements)


def mask_to_elements(mask: int, prime: int) -> list[int]:
    return [element for element in range(prime) if mask & (1 << element)]


def self_sumset_mask(root_mask: int, prime: int) -> int:
    root = mask_to_elements(root_mask, prime)
    result = 0
    for left in root:
        for right in root:
            result |= 1 << ((left + right) % prime)
    return result


def independence_number(prime: int, palette_mask: int) -> int:
    best = 0
    for root_mask in range(1 << prime):
        root = mask_to_elements(root_mask, prime)
        independent = all(
            not (palette_mask & (1 << ((left + right) % prime)))
            for index, left in enumerate(root)
            for right in root[index + 1 :]
        )
        if independent:
            best = max(best, len(root))
    return best


def realized_deletions(prime: int, palette_mask: int, deletion_size: int) -> set[int]:
    """Return eligible T for which G \\ (E union T) is a self-sumset."""
    universe_mask = (1 << prime) - 1
    realized: set[int] = set()
    for root_mask in range(1 << prime):
        sumset_mask = self_sumset_mask(root_mask, prime)
        if sumset_mask & palette_mask:
            continue
        deletion_mask = (universe_mask ^ sumset_mask) & ~palette_mask
        if bin(deletion_mask).count("1") == deletion_size:
            realized.add(deletion_mask)
    return realized


def generate_certificate(
    prime: int, palette: set[int], deletion_size: int
) -> dict[str, object]:
    if not is_prime(prime):
        raise ValueError(f"prime must be prime, got {prime}")
    if prime > 23:
        raise ValueError("exhaustive witness generation is limited to prime <= 23")
    if any(element < 0 or element >= prime for element in palette):
        raise ValueError("palette elements must be canonical residues")

    palette_mask = elements_to_mask(palette)
    available = [element for element in range(prime) if element not in palette]
    if not 0 <= deletion_size <= len(available):
        raise ValueError("deletion size exceeds the complement of the palette")

    realized = realized_deletions(prime, palette_mask, deletion_size)
    witness_mask = None
    for deletion in combinations(available, deletion_size):
        candidate = elements_to_mask(set(deletion))
        if candidate not in realized:
            witness_mask = candidate
            break
    if witness_mask is None:
        raise ValueError("every eligible deletion is realized by a self-sumset root")

    universe_mask = (1 << prime) - 1
    nonsumset_mask = universe_mask ^ (palette_mask | witness_mask)
    alpha = independence_number(prime, palette_mask)
    eligible_count = comb(prime - len(palette), deletion_size)
    candidate_upper_bound = sum(comb(prime, size) for size in range(alpha + 1))
    certificate: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "problem_id": PROBLEM_ID,
        "method": "lexicographic exhaustive exact-output deletion search",
        "prime": prime,
        "palette": sorted(palette),
        "deletion_size": deletion_size,
        "deletion": mask_to_elements(witness_mask, prime),
        "nonsumset": mask_to_elements(nonsumset_mask, prime),
        "independence_number": alpha,
        "palette_score": len(palette) + alpha,
        "roots_enumerated": 1 << prime,
        "eligible_deletion_count": eligible_count,
        "realized_deletion_count": len(realized),
        "candidate_root_upper_bound": candidate_upper_bound,
        "counting_criterion_holds": eligible_count > candidate_upper_bound,
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    certificate["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    return certificate


def parse_palette(raw: str, prime: int) -> set[int]:
    if not raw.strip():
        return set()
    return {int(element) % prime for element in raw.split(",")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--palette", default="")
    parser.add_argument("--deletion-size", type=int, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    certificate = generate_certificate(
        args.prime, parse_palette(args.palette, args.prime), args.deletion_size
    )
    output = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
