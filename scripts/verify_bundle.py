#!/usr/bin/env python3
"""Verify packaged bytes and run the dependency-free finite checks."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
IGNORED_NAMES = {".DS_Store"}
IGNORED_PARTS = {".git", "__pycache__"}


class VerificationError(ValueError):
    """Raised when package content differs from its manifest."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest() -> dict[str, str]:
    try:
        lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise VerificationError(f"cannot read manifest: {error}") from error
    entries: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        digest, separator, raw_path = line.partition("  ")
        if separator != "  " or len(digest) != 64:
            raise VerificationError(f"malformed manifest line {number}")
        relative = PurePosixPath(raw_path)
        if relative.is_absolute() or ".." in relative.parts or "." in relative.parts:
            raise VerificationError(f"unsafe manifest path: {raw_path}")
        if raw_path in entries:
            raise VerificationError(f"duplicate manifest path: {raw_path}")
        entries[raw_path] = digest
    if not entries:
        raise VerificationError("manifest is empty")
    return entries


def visible_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == MANIFEST:
            continue
        relative = path.relative_to(ROOT)
        if path.name in IGNORED_NAMES or path.suffix == ".pyc":
            continue
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        files.add(relative.as_posix())
    return files


def verify_checksums() -> dict[str, object]:
    entries = parse_manifest()
    actual_files = visible_files()
    expected_files = set(entries)
    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    if missing or extra:
        raise VerificationError(f"file set mismatch: missing={missing}, extra={extra}")

    mismatches = [
        relative
        for relative, expected in sorted(entries.items())
        if sha256(ROOT / relative) != expected
    ]
    if mismatches:
        raise VerificationError(f"checksum mismatch: {mismatches}")
    return {"status": "verified", "files": len(entries)}


def run_tests() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checksums-only", action="store_true", help="skip executable fixtures"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = verify_checksums()
        print(f"checksums: verified {report['files']} files")
        if not args.checksums_only:
            run_tests()
            print("finite checks: passed")
    except (VerificationError, OSError, subprocess.CalledProcessError) as error:
        print(f"reviewer package rejected: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
