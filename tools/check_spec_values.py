"""Check that fixed design values exist in the fortune SKILL.md.

The expected values are the mechanizable items of the fixed list
V-01..V-43 (design tokens and definition strings), transcribed from
the run record C-015.md. Each value is anchored by context (e.g. the
token-table row) so ambiguous bare values cannot false-match.

Target: the canonical SKILL.md by default, or the file given as the
single argument.

Exit codes:
    0: every expected value exists
    1: at least one expected value is missing
    2: error (missing file, unreadable, bad arguments, ...)

Usage:
    python3 tools/check_spec_values.py
    python3 tools/check_spec_values.py <path>
"""

from __future__ import annotations

import sys
from pathlib import Path

# (label, expected string) pairs, in the order of the C-015 list.
EXPECTED: list[tuple[str, str]] = [
    # Colours
    ("bg", "`bg` | #F5F7FA"),
    ("text", "`text` | #000000"),
    ("navy", "`navy` | #14324A"),
    ("accent", "`accent` | #FF7A1A"),
    ("label-blue", "`label-blue` | #1C7FB8"),
    ("header-gray", "`header-gray` | #8CA0B0"),
    ("card-shadow", "`card-shadow` | 0 1px 4px rgba(20,50,74,.10)"),
    ("quote-author", "`quote-author` | #FFB37E"),
    ("family-green", "`family-green` | #2E8B6E"),
    ("gym-orange", "`gym-orange` | #E08A2E"),
    ("caution-red", "`caution-red` | #B54434"),
    ("week-normal", "`week-normal` | #C9A227"),
    ("rest-purple", "`rest-purple` | #8E6BC8"),
    ("panel-grad-from", "`panel-grad-from` | #EAF1F7"),
    ("panel-grad-to", "`panel-grad-to` | #FDF0E4"),
    ("panel-border", "`panel-border` | #D8E4EE"),
    ("ctxnote-color", "`ctxnote-color` | #444444"),
    # Font sizes
    ("date-size", "`date-size` | 35px"),
    ("body-size", "`body-size` | 16.5px（行間 1.56）"),
    ("mb-size", "`mb-size` | 16.2px"),
    ("box-p-size", "`box-p-size` | 15.9px"),
    ("fb-size", "`fb-size` | 15.4px"),
    ("wb-size", "`wb-size` | 15.1px"),
    ("ctxnote-size", "`ctxnote-size` | 15.3px"),
    ("qn-size", "`qn-size` | 16px"),
    ("mt-size", "`mt-size` | 15px"),
    ("ft-wt-size", "`ft-wt-size` | 14.5px"),
    ("slabel-size", "`slabel-size` | 14px（太字 900）"),
    ("tl-size", "`tl-size` | 11px"),
    # Margins and shapes
    ("page-margin", "`page-margin` | 8mm/9mm（週間は 7mm/9mm）"),
    ("midgrid-gap", "`midgrid-gap` | 4px"),
    ("icard-padding", "`icard-padding` | 3px 9px"),
    ("overview-padding", "`overview-padding` | 4px 11px 5px"),
    ("flow-padding", "`flow-padding` | 4px 11px 0"),
    ("box-padding", "`box-padding` | 2px 9px 6px"),
    ("quote-padding", "`quote-padding` | 13px 15px"),
    ("slabel-margin", "`slabel-margin` | 6px 0 3px"),
    (
        "slabel-bar",
        "`slabel-bar` | 6px | `.slabel` 左の縦バー幅"
        "（色は `accent`、padding-left 9px）",
    ),
    ("vbody-padding-bottom", "`vbody-padding-bottom` | 1px"),
    ("crow-margin-bottom", "`crow-margin-bottom` | 4px"),
    ("card-radius", "`card-radius` | 14〜16px"),
    ("panel-radius", "`panel-radius` | 14px"),
    ("panel-border-width", "`panel-border-width` | 1px"),
    ("header-rule", "`header-rule` | 1px"),
    ("section-underline", "`section-underline` | 3px"),
    ("m3-bar", "`m3-bar` | 5px"),
    # Definition strings
    ("version-v2", "日次占いは v2 を使う"),
    (
        "template-daily",
        "`~/workspace/goals/goal-4/hidden_files/"
        "fortune-template-v2.html`",
    ),
    ("template-weekly", "fortune-template-v2-weekly.html"),
    ("design-plan", "案D「クリア・モダン」＋H4ヘッダー"),
    ("page-count", "通常 4ページ、月曜は週間1ページを足して 5ページ"),
    ("middle-items", "仕事・家族・ジム運・今日の注意・今日の天気"),
    (
        "quote-authors",
        "ニーチェ／シオラン／ストア派"
        "（セネカ・マルクス・アウレリウス・エピクテトス）"
        "／ペシミズム系（ショーペンハウアー等）"
        "／吉田松陰／有名な禅僧（一休・道元・良寛・白隠など）の6系統",
    ),
    ("quote-source-rule", "実在の有名な言葉のみ。出典（著作名）を併記し"),
    ("adjust-by-margin", "文字ではなく余白で調整する（文字を小さくしない）"),
]


def default_target_path() -> Path:
    return (
        Path.home()
        / "workspace"
        / "custom-skills"
        / "fortune-pdf-design"
        / "SKILL.md"
    )


def check(path: Path) -> int:
    if not path.is_file():
        print(f"error: file not found: {path}")
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: failed to read file: {exc}")
        return 2

    print(f"target: {path}")
    missing = 0
    for label, expected in EXPECTED:
        if expected in text:
            print(f"OK {label}: {expected}")
        else:
            print(f"MISSING {label}: {expected}")
            missing += 1

    total = len(EXPECTED)
    print(f"summary: total {total} checks, {total - missing} ok, "
          f"{missing} missing")
    return 1 if missing else 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 0:
        path = default_target_path()
    elif len(args) == 1:
        path = Path(args[0]).expanduser()
    else:
        print(
            "usage: check_spec_values.py [path]",
            file=sys.stderr,
        )
        return 2
    return check(path)


if __name__ == "__main__":
    raise SystemExit(main())
