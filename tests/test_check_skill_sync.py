"""Characterization tests for tools/check_skill_sync.py.

Spec (decided):
- Canonical SKILL.md is
  ~/workspace/custom-skills/fortune-pdf-design/SKILL.md.
- Synced copy is <fortune repo>/skill/SKILL.md.
- The two must be byte-identical; drift must be detectable.

Exit codes fixed by these tests:
- match -> 0
- mismatch -> 1
- missing / error -> 2

Real files are only read, never modified.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "check_skill_sync.py"
CANONICAL = (
    Path.home()
    / "workspace"
    / "custom-skills"
    / "fortune-pdf-design"
    / "SKILL.md"
)
SYNCED = REPO_ROOT / "skill" / "SKILL.md"


def run_check(*args: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )


def test_match_returns_zero(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    content = b"# same\ncontent\n"
    a.write_bytes(content)
    b.write_bytes(content)

    result = run_check(a, b)

    assert result.returncode == 0
    assert "match" in result.stdout


def test_mismatch_returns_one(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_bytes(b"# version A\n")
    b.write_bytes(b"# version B\n")

    result = run_check(a, b)

    assert result.returncode == 1
    assert "mismatch" in result.stdout


def test_mismatch_same_length_returns_one(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_bytes(b"aaaa")
    b.write_bytes(b"bbbb")

    result = run_check(a, b)

    assert result.returncode == 1


def test_missing_first_file_returns_two(tmp_path: Path) -> None:
    a = tmp_path / "missing.md"
    b = tmp_path / "b.md"
    b.write_bytes(b"present\n")

    result = run_check(a, b)

    assert result.returncode == 2


def test_missing_second_file_returns_two(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "missing.md"
    a.write_bytes(b"present\n")

    result = run_check(a, b)

    assert result.returncode == 2


def test_missing_both_files_returns_two(tmp_path: Path) -> None:
    result = run_check(tmp_path / "x.md", tmp_path / "y.md")

    assert result.returncode == 2


def test_real_files_are_byte_identical() -> None:
    """Current state: canonical and synced copy must match."""
    assert CANONICAL.is_file(), f"canonical not found: {CANONICAL}"
    assert SYNCED.is_file(), f"synced copy not found: {SYNCED}"

    result = run_check(CANONICAL, SYNCED)

    assert result.returncode == 0
    assert CANONICAL.read_bytes() == SYNCED.read_bytes()


def test_default_invocation_matches_real_files() -> None:
    """With no arguments the script compares the real pair."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "match" in result.stdout
