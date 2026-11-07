"""Characterization tests for tools/check_spec_values.py.

Spec (fixed by the test author from the fixed list fortune-v2.md
V-01..V-43 and the current SKILL.md token tables, BEFORE any
implementation exists; do not rewrite these tests to fit an
implementation -- implementation conveniences are judged separately):

- New tool: tools/check_spec_values.py (standard library only), in the
  same style as tools/check_skill_sync.py (loose-coupled single tool,
  result reported via exit code).
- Usage: python3 tools/check_spec_values.py [target]
    - no argument: target is the canonical
      ~/workspace/custom-skills/fortune-pdf-design/SKILL.md
    - one argument: that file is the target
    - two or more arguments: error
- Behaviour: for each entry of the tool's built-in expected-value list
  (labelled string literals, taken from the mechanizable items of
  V-01..V-43; see the run record C-015.md for the full list of 55
  checks), check that the string exists in the full text of the
  target, print one result line per check that is identifiable by its
  label, and print a summary line at the end.
- Labels are the design-token names (e.g. ``bg``, ``body-size``) for
  token checks, and the slugs listed in C-015.md for string checks
  (e.g. ``page-count``, ``middle-items``, ``template-daily``).
- Ambiguous bare values (e.g. a plain ``16px``, which is also a
  substring of ``16.5px``) must be anchored by context such as the
  token-table row (token name + value).
- Exit codes:
    - 0: every expected value exists
    - 1: at least one expected value is missing
    - 2: error (file missing / unreadable / bad arguments)

Real files are only read, never modified. Every mutation case runs on
a copy inside a temporary directory.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "check_spec_values.py"
CANONICAL = (
    Path.home()
    / "workspace"
    / "custom-skills"
    / "fortune-pdf-design"
    / "SKILL.md"
)
SYNCED = REPO_ROOT / "skill" / "SKILL.md"

# A per-check result line for a missing value must be recognizable as
# "missing" in some common wording; the label alone is not enough.
MISSING_MARKERS = (
    "missing",
    "fail",
    "absent",
    "not found",
    "欠落",
    "なし",
    "未検出",
    "ありません",
    "✗",
    "×",
)


def run_check(*args: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )


def combined(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def lines_for_label(output: str, label: str) -> list[str]:
    return [line for line in output.splitlines() if label in line]


def is_missing_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in MISSING_MARKERS) or bool(
        re.search(r"\bNG\b", line)
    )


def assert_check_missing(output: str, label: str) -> None:
    lines = lines_for_label(output, label)
    assert lines, f"no result line identifiable by label {label!r}"
    assert any(is_missing_line(line) for line in lines), (
        f"check {label!r} is not identifiable as missing: {lines!r}"
    )


def assert_check_present(output: str, label: str) -> None:
    lines = lines_for_label(output, label)
    assert lines, f"no result line identifiable by label {label!r}"
    assert any(not is_missing_line(line) for line in lines), (
        f"check {label!r} unexpectedly reported missing: {lines!r}"
    )


def assert_summary_present(output: str) -> None:
    assert any(
        token in line.lower() or "件" in line
        for line in output.splitlines()
        for token in ("total", "summary", "result")
    ), f"no summary line in output: {output!r}"


# --- (a) real canonical file, default invocation --------------------


def test_default_invocation_on_canonical_returns_zero() -> None:
    """No argument targets the canonical SKILL.md; all values exist."""
    assert CANONICAL.is_file(), f"canonical not found: {CANONICAL}"

    result = run_check()

    assert result.returncode == 0
    output = combined(result)
    for label in ("bg", "body-size", "page-count", "quote-authors"):
        assert_check_present(output, label)
    assert_summary_present(output)


def test_canonical_explicit_argument_returns_zero() -> None:
    result = run_check(CANONICAL)

    assert result.returncode == 0
    assert_check_present(combined(result), "bg")


# --- (b) real synced copy passed explicitly -------------------------


def test_repo_copy_argument_returns_zero() -> None:
    """The repo-side copy holds the same values, so it also passes."""
    assert SYNCED.is_file(), f"synced copy not found: {SYNCED}"

    result = run_check(SYNCED)

    assert result.returncode == 0
    output = combined(result)
    for label in ("bg", "body-size", "page-count"):
        assert_check_present(output, label)
    assert_summary_present(output)


# --- (c) mutations on a temporary copy ------------------------------
#
# Each case changes exactly one fixed value in a copy of the real
# file. The run must fail with exit 1, the changed check must be
# identifiable as missing by its label, and an unrelated check must
# still be reported present.

MUTATIONS = [
    # colour values
    pytest.param(
        "bg",
        "`bg` | #F5F7FA",
        "`bg` | #F5F7FB",
        id="colour-bg",
    ),
    pytest.param(
        "quote-author",
        "`quote-author` | #FFB37E",
        "`quote-author` | #FFB37F",
        id="colour-quote-author",
    ),
    # font sizes (token-anchored: a bare 16px is a substring of 16.5px,
    # so the qn-size case only works if the token row is the anchor)
    pytest.param(
        "body-size",
        "`body-size` | 16.5px",
        "`body-size` | 16.9px",
        id="size-body-size",
    ),
    pytest.param(
        "qn-size",
        "`qn-size` | 16px",
        "`qn-size` | 17px",
        id="size-qn-size",
    ),
    # string items
    pytest.param(
        "middle-items",
        "仕事・家族・ジム運・今日の注意・今日の天気",
        "仕事・家族・ジム運・今日の注意・今日の天候",
        id="string-middle-items",
    ),
    pytest.param(
        "template-daily",
        "`~/workspace/goals/goal-4/hidden_files/fortune-template-v2.html`",
        "`~/workspace/goals/goal-4/hidden_files/fortune-template-v9.html`",
        id="string-template-daily",
    ),
]


@pytest.mark.parametrize("label,old,new", MUTATIONS)
def test_mutated_value_returns_one_and_identifies_check(
    tmp_path: Path, label: str, old: str, new: str
) -> None:
    text = CANONICAL.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"mutation source not unique: {old!r}"
    mutated = tmp_path / "SKILL.md"
    mutated.write_text(text.replace(old, new, 1), encoding="utf-8")

    result = run_check(mutated)

    assert result.returncode == 1
    output = combined(result)
    assert_check_missing(output, label)
    # An unrelated check is unaffected by the single-value change.
    assert_check_present(output, "accent")


# --- (d) empty file ---------------------------------------------------


def test_empty_file_returns_one(tmp_path: Path) -> None:
    empty = tmp_path / "empty.md"
    empty.write_text("", encoding="utf-8")

    result = run_check(empty)

    assert result.returncode == 1
    assert_check_missing(combined(result), "bg")


# --- (e) missing file -------------------------------------------------


def test_missing_file_returns_two(tmp_path: Path) -> None:
    result = run_check(tmp_path / "does-not-exist.md")

    assert result.returncode == 2


def test_directory_argument_returns_two(tmp_path: Path) -> None:
    result = run_check(tmp_path)

    assert result.returncode == 2


# --- (f) bad arguments ------------------------------------------------


def test_two_arguments_returns_two() -> None:
    result = run_check(CANONICAL, SYNCED)

    assert result.returncode == 2
