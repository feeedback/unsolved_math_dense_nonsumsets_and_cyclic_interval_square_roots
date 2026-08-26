#!/usr/bin/env python3
"""Verify finite instances of the interval-to-cyclic palette transfer.

The verifier deliberately uses exhaustive subset enumeration.  It is not an
asymptotic proof of the imported interval theorem; it checks the elementary
finite transfer and the exact counting inequality used after that theorem.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable


MAX_EXHAUSTIVE_ORDER = 24


class VerificationError(ValueError):
    """Raised when an input or claimed transfer inequality is invalid."""


def parse_palette(value: str) -> frozenset[int]:
    if not value:
        return frozenset()
    try:
        return frozenset(int(item) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "palettes must be comma-separated integers"
        ) from error


def validate_interval_palette(order: int, palette: frozenset[int]) -> None:
    if order < 1:
        raise VerificationError("interval order must be positive")
    attainable = set(range(1, max(1, 2 * order - 2)))
    if not palette <= attainable:
        raise VerificationError(
            f"palette {sorted(palette)} is outside the attainable range "
            f"{sorted(attainable)}"
        )


def exhaustive_independence_number(
    order: int, adjacent: Callable[[int, int], bool]
) -> int:
    """Return the exact independence number by a transparent full census."""
    if not 0 <= order <= MAX_EXHAUSTIVE_ORDER:
        raise VerificationError(
            f"exhaustive graph order must be in [0, {MAX_EXHAUSTIVE_ORDER}]"
        )

    edge_masks = [0] * order
    for left in range(order):
        for right in range(left + 1, order):
            if adjacent(left, right):
                edge_masks[left] |= 1 << right

    maximum = 0
    for subset in range(1 << order):
        cardinality = bin(subset).count("1")
        if cardinality <= maximum:
            continue
        if all(
            not (subset & (1 << left) and subset & edge_masks[left])
            for left in range(order)
        ):
            maximum = cardinality
    return maximum


def interval_independence_number(order: int, palette: frozenset[int]) -> int:
    validate_interval_palette(order, palette)
    return exhaustive_independence_number(
        order, lambda left, right: left + right in palette
    )


def cyclic_independence_number(order: int, palette: frozenset[int]) -> int:
    if order < 1:
        raise VerificationError("cyclic order must be positive")
    if any(not 0 <= element < order for element in palette):
        raise VerificationError("cyclic palette elements must be standard residues")
    return exhaustive_independence_number(
        order, lambda left, right: (left + right) % order in palette
    )


def transfer_palette(
    order: int, lower_palette: frozenset[int], upper_palette: frozenset[int]
) -> frozenset[int]:
    """Translate the two interval palettes into the cyclic group of given order."""
    if order < 2:
        raise VerificationError("cyclic order must be at least two")
    lower_order = (order + 1) // 2
    upper_order = order // 2
    validate_interval_palette(lower_order, lower_palette)
    validate_interval_palette(upper_order, upper_palette)

    upper_offset = lower_order
    return frozenset(
        {element % order for element in lower_palette}
        | {(2 * upper_offset + element) % order for element in upper_palette}
    )


def verify_transfer(
    order: int, lower_palette: frozenset[int], upper_palette: frozenset[int]
) -> dict[str, object]:
    lower_order = (order + 1) // 2
    upper_order = order // 2
    cyclic_palette = transfer_palette(order, lower_palette, upper_palette)

    lower_alpha = interval_independence_number(lower_order, lower_palette)
    upper_alpha = interval_independence_number(upper_order, upper_palette)
    cyclic_alpha = cyclic_independence_number(order, cyclic_palette)
    interval_score = (
        len(lower_palette) + lower_alpha + len(upper_palette) + upper_alpha
    )
    cyclic_score = len(cyclic_palette) + cyclic_alpha

    if cyclic_alpha > lower_alpha + upper_alpha:
        raise VerificationError("cyclic independence bound failed")
    if cyclic_score > interval_score:
        raise VerificationError("cyclic score bound failed")
    if cyclic_alpha * (len(cyclic_palette) + 1) < order:
        raise VerificationError("universal greedy independence bound failed")

    return {
        "cyclic_order": order,
        "interval_orders": [lower_order, upper_order],
        "input_palettes": [sorted(lower_palette), sorted(upper_palette)],
        "cyclic_palette": sorted(cyclic_palette),
        "interval_independence_numbers": [lower_alpha, upper_alpha],
        "cyclic_independence_number": cyclic_alpha,
        "interval_score_sum": interval_score,
        "cyclic_score": cyclic_score,
        "greedy_independence_product": cyclic_alpha
        * (len(cyclic_palette) + 1),
        "status": "verified",
    }


def small_root_count(order: int, maximum_size: int) -> int:
    if not 0 <= maximum_size <= order:
        raise VerificationError("maximum root size must lie in [0, order]")
    return sum(math.comb(order, size) for size in range(maximum_size + 1))


def verify_counting_inequality(
    order: int, excluded_size: int, maximum_root_size: int, added_size: int
) -> dict[str, object]:
    """Check the exact pigeonhole inequality in the second-layer construction."""
    if not 0 <= excluded_size <= order:
        raise VerificationError("excluded palette size must lie in [0, order]")
    available = order - excluded_size
    if not 0 <= added_size <= available:
        raise VerificationError(
            "added-set size must lie in [0, order - excluded_size]"
        )

    choices = math.comb(available, added_size)
    candidates = small_root_count(order, maximum_root_size)
    if choices <= candidates:
        raise VerificationError(
            "counting inequality failed: added-set choices do not outnumber roots"
        )
    return {
        "group_order": order,
        "excluded_palette_size": excluded_size,
        "maximum_root_size": maximum_root_size,
        "added_set_size": added_size,
        "added_set_choices": choices,
        "candidate_roots": candidates,
        "status": "verified",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    transfer = subparsers.add_parser("transfer", help="verify one finite transfer")
    transfer.add_argument("--order", type=int, required=True)
    transfer.add_argument("--lower-palette", type=parse_palette, required=True)
    transfer.add_argument("--upper-palette", type=parse_palette, required=True)

    counting = subparsers.add_parser(
        "counting", help="verify one exact second-layer counting inequality"
    )
    counting.add_argument("--order", type=int, required=True)
    counting.add_argument("--excluded-size", type=int, required=True)
    counting.add_argument("--maximum-root-size", type=int, required=True)
    counting.add_argument("--added-size", type=int, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "transfer":
            report = verify_transfer(args.order, args.lower_palette, args.upper_palette)
        else:
            report = verify_counting_inequality(
                args.order,
                args.excluded_size,
                args.maximum_root_size,
                args.added_size,
            )
    except VerificationError as error:
        raise SystemExit(f"verification failed: {error}") from error
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
