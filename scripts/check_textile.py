#!/usr/bin/env python3
"""Pre-commit checks for Obsidian Portal Textile lore files."""

from __future__ import annotations

import sys
from pathlib import Path


def check_textile(path: Path) -> list[str]:
    errors: list[str] = []
    data = path.read_bytes()
    if b"\r" in data:
        errors.append(f"{path}: must use LF line endings (found CR/CRLF)")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path}: must be valid UTF-8")
        return errors

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        return errors

    end = normalized.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path}: frontmatter opening --- has no closing ---")
        return errors

    rest = normalized[end + 5 :].lstrip("\n")
    if rest.startswith("---\n"):
        errors.append(f"{path}: nested frontmatter block (duplicate --- section)")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return 0

    failed = False
    for name in argv[1:]:
        path = Path(name)
        if not path.is_file():
            continue
        for error in check_textile(path):
            print(error, file=sys.stderr)
            failed = True

    if failed:
        print(
            "\nTextile files must use LF-only line endings so the lore bridge can parse YAML frontmatter.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
