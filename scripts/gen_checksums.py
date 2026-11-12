#!/usr/bin/env python3
"""Write or verify CHECKSUMS.sha256 for everything that runs or ships as code.

    python3 scripts/gen_checksums.py          # rewrite CHECKSUMS.sha256
    python3 scripts/gen_checksums.py --check  # verify, exit 1 on mismatch

The file lists scripts, hook examples, manifests, the installer and the packaged
skill. A checksum catches an accidental or partial change; it does not prove who
made it. Verify the release tag you install.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "CHECKSUMS.sha256"
PATTERNS = [
    "install.sh",
    ".claude-plugin/*.json",
    "scripts/*.py",
    "skills/*/scripts/**/*",
    "examples/hardened-project/.claude/hooks/*",
    "dist/*.skill",
]


def tracked_files() -> list[Path]:
    found = set()
    for pattern in PATTERNS:
        for path in ROOT.glob(pattern):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                found.add(path)
    return sorted(found)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    lines = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in tracked_files()]
    if "--check" in argv:
        expected = MANIFEST.read_text(encoding="utf-8").splitlines() if MANIFEST.is_file() else []
        if expected != lines:
            print("CHECKSUMS.sha256 is out of date. Run: make checksums", file=sys.stderr)
            for line in sorted(set(lines) ^ set(expected)):
                print(f"  differs: {line}", file=sys.stderr)
            return 1
        print(f"checksums ok ({len(lines)} files)")
        return 0
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote CHECKSUMS.sha256 ({len(lines)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
