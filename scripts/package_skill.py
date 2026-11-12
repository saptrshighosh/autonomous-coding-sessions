#!/usr/bin/env python3
"""Build dist/autonomous-coding-sessions.skill, a reproducible archive of the main skill.

The archive is a zip with one top-level folder (the skill name). It is built
byte-for-byte reproducibly (sorted entries, fixed timestamps, no compression)
so CI can rebuild it and check it matches what is committed.

    python3 scripts/package_skill.py
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = "autonomous-coding-sessions"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def build_bytes(skill_dir: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        files = sorted(
            p for p in skill_dir.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
        )
        for path in files:
            name = f"{skill_dir.name}/{path.relative_to(skill_dir).as_posix()}"
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            executable = path.stat().st_mode & 0o111
            info.external_attr = (0o755 if executable else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    return buffer.getvalue()


def main() -> int:
    skill_dir = ROOT / "skills" / SKILL
    if not (skill_dir / "SKILL.md").is_file():
        print(f"error: {skill_dir}/SKILL.md not found", file=sys.stderr)
        return 1
    out = ROOT / "dist" / f"{SKILL}.skill"
    out.parent.mkdir(exist_ok=True)
    out.write_bytes(build_bytes(skill_dir))
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
