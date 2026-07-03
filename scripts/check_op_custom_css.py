#!/usr/bin/env python3
"""Fail if custom CSS contains strings Obsidian Portal is known to reject."""

from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCKED = [
    (r">", "child combinator or greater-than in comments"),
    (r"description", "substring description"),
    (r"@import", "substring @import"),
    (r":root\b", ":root"),
    (r"var\(", "var()"),
    (r"content\s*:", "content: in pseudo-elements"),
]

WARN = [
    (r"calc\(", "calc() - may be rejected"),
    (r"object-fit", "object-fit - may be rejected"),
    (r":focus-within", ":focus-within - may be rejected"),
]

NON_ASCII = re.compile(r"[^\x00-\x7F]")


def check(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for pattern, label in BLOCKED:
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(pattern, line):
                errors.append(f"  line {i}: {label}: {line.strip()[:80]}")

    for pattern, label in WARN:
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(pattern, line):
                warnings.append(f"  line {i}: {label}: {line.strip()[:80]}")

    for i, line in enumerate(text.splitlines(), 1):
        if NON_ASCII.search(line):
            errors.append(f"  line {i}: non-ASCII in comment or rule: {line.strip()[:80]}")

    if errors:
        print(f"OP Custom CSS blocked patterns in {path}:")
        print("\n".join(errors))
    if warnings:
        print(f"Warnings for {path}:")
        print("\n".join(warnings))

    if errors:
        return 1
    if warnings:
        print("OK (with warnings)")
    else:
        print(f"OK: {path}")
    return 0


def main() -> None:
    paths = [Path(p) for p in sys.argv[1:]] or [
        Path("notes/obsidian-portal/custom-css.css")
    ]
    code = 0
    for path in paths:
        if not path.is_file():
            print(f"Missing: {path}", file=sys.stderr)
            code = 1
            continue
        code = max(code, check(path))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
