#!/usr/bin/env python3
"""Fail if lore Textile wiki or character links do not resolve in-repo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LORE = ROOT / "lore"

WIKI_LINK = re.compile(r"\[\[([^\]|#]+?)(?:\s*\|\s*[^\]]+)?\]\]")
CHAR_LINK = re.compile(r"\[\[:([^\]|#]+?)(?:\s*\|\s*[^\]]+)?\]\]")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 2:
        return {}
    fm: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^(\w+):\s*(.+)$", line)
        if not match:
            continue
        value = match.group(2).strip()
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            value = value[1:-1]
        fm[match.group(1)] = value
    return fm


def build_index() -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}

    def add_key(key: str, path: str) -> None:
        if key:
            index.setdefault(key.strip().lower(), set()).add(path)

    for path in LORE.rglob("*.textile"):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        rel = str(path.relative_to(ROOT))
        for field in ("op_slug", "name", "title"):
            if fm.get(field):
                add_key(fm[field], rel)
        add_key(path.stem, rel)
    return index


def find_broken_links(index: dict[str, set[str]]) -> list[tuple[str, str, str, str]]:
    broken: list[tuple[str, str, str, str]] = []

    for path in sorted(LORE.rglob("*.textile")):
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT))

        for match in CHAR_LINK.finditer(text):
            slug = match.group(1).strip()
            if slug.lower() not in index:
                broken.append((rel, match.group(0), slug, "character slug"))

        for match in WIKI_LINK.finditer(text):
            raw = match.group(0)
            if raw.lower().startswith("[[file:"):
                continue
            target = match.group(1).strip()
            if target.startswith(":"):
                continue
            if target.lower() not in index:
                broken.append((rel, raw, target, "wiki target"))

    broken.sort(key=lambda row: (row[2].lower(), row[0], row[1]))
    return broken


def main() -> int:
    if not LORE.is_dir():
        print("check_wiki_links: lore/ not found", file=sys.stderr)
        return 1

    index = build_index()
    broken = find_broken_links(index)

    if not broken:
        print(f"Wiki links OK ({len(index)} indexed names/slugs).")
        return 0

    print(f"Broken wiki links ({len(broken)}):", file=sys.stderr)
    for rel, link, target, kind in broken:
        print(f"  {rel}: {link}  ({kind}: {target!r})", file=sys.stderr)
    print(
        "\nTargets must match op_slug, name, or title on a lore/**/*.textile page.",
        file=sys.stderr,
    )
    print("Character links use [[:slug | Label]] matching lore/characters/.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
