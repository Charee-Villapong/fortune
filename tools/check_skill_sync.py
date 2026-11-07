"""Check that the canonical SKILL.md and its synced copy are identical.

Canonical: ~/workspace/custom-skills/fortune-pdf-design/SKILL.md
Synced copy: <repo>/skill/SKILL.md

Exit codes:
    0: files are byte-identical
    1: files differ
    2: error (missing file, unreadable, bad arguments, ...)

Usage:
    python3 tools/check_skill_sync.py
    python3 tools/check_skill_sync.py <path-a> <path-b>
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def default_canonical_path() -> Path:
    return (
        Path.home()
        / "workspace"
        / "custom-skills"
        / "fortune-pdf-design"
        / "SKILL.md"
    )


def default_synced_path() -> Path:
    repo_root = Path(__file__).resolve().parent.parent
    return repo_root / "skill" / "SKILL.md"


def file_info(path: Path) -> tuple[int, str]:
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def check(path_a: Path, path_b: Path) -> int:
    for path in (path_a, path_b):
        if not path.is_file():
            print(f"error: file not found: {path}")
            return 2
    try:
        size_a, hash_a = file_info(path_a)
        size_b, hash_b = file_info(path_b)
    except OSError as exc:
        print(f"error: failed to read file: {exc}")
        return 2

    print(f"a: {path_a} size={size_a} sha256={hash_a}")
    print(f"b: {path_b} size={size_b} sha256={hash_b}")

    if size_a == size_b and hash_a == hash_b:
        print("result: match")
        return 0
    print("result: mismatch")
    return 1


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 0:
        path_a = default_canonical_path()
        path_b = default_synced_path()
    elif len(args) == 2:
        path_a = Path(args[0]).expanduser()
        path_b = Path(args[1]).expanduser()
    else:
        print(
            "usage: check_skill_sync.py [path-a path-b]",
            file=sys.stderr,
        )
        return 2
    return check(path_a, path_b)


if __name__ == "__main__":
    raise SystemExit(main())
