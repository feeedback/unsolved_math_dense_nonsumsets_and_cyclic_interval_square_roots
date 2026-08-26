import importlib.util
import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "verify_interval_palette_transfer.py"
    spec = importlib.util.spec_from_file_location("verify_interval_palette_transfer", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TRANSFER = load_script()


def palettes(elements):
    elements = tuple(elements)
    for mask in range(1 << len(elements)):
        yield frozenset(
            element for index, element in enumerate(elements) if mask & (1 << index)
        )


class IntervalPaletteTransferTest(unittest.TestCase):
    def test_every_palette_pair_through_order_nine(self):
        for order in range(2, 10):
            lower_order = (order + 1) // 2
            upper_order = order // 2
            palette_pairs = itertools.product(
                palettes(range(1, max(1, 2 * lower_order - 2))),
                palettes(range(1, max(1, 2 * upper_order - 2))),
            )
            for lower, upper in palette_pairs:
                report = TRANSFER.verify_transfer(order, lower, upper)
                self.assertLessEqual(
                    report["cyclic_score"], report["interval_score_sum"]
                )
                self.assertGreaterEqual(
                    report["greedy_independence_product"], order
                )

    def test_modular_collisions_only_shrink_palette(self):
        report = TRANSFER.verify_transfer(
            7, frozenset(range(1, 6)), frozenset(range(1, 4))
        )
        self.assertEqual(report["cyclic_palette"], [1, 2, 3, 4, 5])
        self.assertLess(
            len(report["cyclic_palette"]),
            sum(len(palette) for palette in report["input_palettes"]),
        )

    def test_exact_second_layer_counting_inequality(self):
        report = TRANSFER.verify_counting_inequality(10_000, 40, 60, 400)
        self.assertGreater(report["added_set_choices"], report["candidate_roots"])

    def test_failed_counting_inequality_is_rejected(self):
        with self.assertRaises(TRANSFER.VerificationError):
            TRANSFER.verify_counting_inequality(20, 2, 8, 4)

    def test_out_of_range_interval_color_is_rejected(self):
        with self.assertRaises(TRANSFER.VerificationError):
            TRANSFER.verify_transfer(7, frozenset({0}), frozenset())


if __name__ == "__main__":
    unittest.main()
