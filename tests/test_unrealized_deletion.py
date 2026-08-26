import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load_script("find_unrealized_deletion")
CHECKER = load_script("check_unrealized_deletion")


class ExactOutputDeletionTest(unittest.TestCase):
    def test_generator_produces_independently_checked_witness(self):
        certificate = GENERATOR.generate_certificate(5, set(), 1)
        self.assertEqual(certificate["deletion"], [0])
        self.assertEqual(certificate["nonsumset"], [1, 2, 3, 4])
        report = CHECKER.verify(certificate)
        self.assertEqual(report["status"], "verified")
        self.assertEqual(report["roots_checked"], 1 << 5)

    def test_represented_tamper_is_rejected_after_rehash(self):
        certificate = GENERATOR.generate_certificate(7, set(), 4)
        certificate["deletion"] = [0, 1, 2, 3]
        certificate["nonsumset"] = [4, 5, 6]
        payload = dict(certificate)
        payload.pop("payload_sha256")
        import hashlib
        import json

        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        certificate["payload_sha256"] = hashlib.sha256(encoded).hexdigest()
        with self.assertRaises(CHECKER.CertificateError):
            CHECKER.verify(certificate)

    def test_checksum_tamper_is_rejected(self):
        certificate = GENERATOR.generate_certificate(5, set(), 1)
        tampered = copy.deepcopy(certificate)
        tampered["palette_score"] += 1
        with self.assertRaises(CHECKER.CertificateError):
            CHECKER.verify(tampered)

    def test_checker_does_not_import_generator(self):
        source = (ROOT / "scripts" / "check_unrealized_deletion.py").read_text()
        self.assertNotIn("import find_unrealized_deletion", source)
        self.assertNotIn("from find_unrealized_deletion", source)


if __name__ == "__main__":
    unittest.main()
