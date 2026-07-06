#!/usr/bin/env python3
"""Regenerate items index tiles and optional item-page portraits from wiki item pages."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "lore" / "wiki" / "wiki"
ITEMS_PAGE = WIKI / "items.textile"

MARKER_START = "<!-- ITEMS_INDEX_AUTO_START -->"
MARKER_END = "<!-- ITEMS_INDEX_AUTO_END -->"
LEGACY_TEXTILE_MARKER_START = "###. ITEMS_INDEX_AUTO_START"
LEGACY_TEXTILE_MARKER_END = "###. ITEMS_INDEX_AUTO_END"
IMAGE_MARKER_START = "<!-- ITEM_IMAGE_AUTO_START -->"
IMAGE_MARKER_END = "<!-- ITEM_IMAGE_AUTO_END -->"

# Category tag on item pages -> index section heading (first match wins).
CATEGORY_SECTIONS: list[tuple[str, str]] = [
    ("document", "Documents"),
    ("jewelry", "Jewelry"),
    ("musical instrument", "Musical instruments"),
    ("key", "Keys"),
    ("clothing", "Clothing"),
    ("consumable", "Other"),
    ("vehicle", "Vehicle"),
    ("shield", "Shield"),
    ("weapon", "Weapon"),
    ("wondrous", "Other"),
    ("other", "Other"),
]

SECTION_ORDER: list[str] = []
_seen: set[str] = set()
for _, heading in CATEGORY_SECTIONS:
    if heading not in _seen:
        SECTION_ORDER.append(heading)
        _seen.add(heading)

# Party-relevant gear on the public index; founder regalia and op_gm_only pages in GM block.
FOUNDER_SIGNATURE_SLUGS = {
    "cel-s",
    "mask-of-foreknowledge",
    "the-amulet-of-stars",
    "the-crown-of-shadows",
    "the-gladius",
    "the-red-mourning",
    "the-shaper-s-hands",
    "the-shadow-s-vestment",
}

# GM index tiles for pages that stay public but should not appear on the player index.
GM_INDEX_SLUGS: set[str] = set()


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 2:
        return {}
    fm: dict = {"tags": []}
    in_tags = False
    for line in parts[1].splitlines():
        if line.startswith("tags:"):
            in_tags = True
            rest = line[5:].strip()
            if rest and rest != "[]":
                fm["tags"].append(rest.strip("'\""))
            continue
        if in_tags:
            if line.strip().startswith("- "):
                fm["tags"].append(line.strip()[2:].strip("'\""))
            elif line.strip():
                in_tags = False
        match = re.match(r"^([\w]+):\s*(.+)$", line)
        if match and not in_tags:
            val = match.group(2).strip()
            if (val.startswith("'") and val.endswith("'")) or (
                val.startswith('"') and val.endswith('"')
            ):
                val = val[1:-1]
            fm[match.group(1)] = val
    return fm


def category_for(tags: list[str]) -> str:
    tag_set = {t.lower() for t in tags}
    for cat_tag, heading in CATEGORY_SECTIONS:
        if cat_tag in tag_set:
            return heading
    return "Other"


def load_items() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(WIKI.glob("*.textile")):
        if path.stem == "items":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        tags = [t.lower() for t in fm.get("tags") or []]
        if "item" not in tags:
            continue
        name = fm.get("name") or fm.get("title") or path.stem
        op_gm_only = fm.get("op_gm_only") == "true"
        gm_index = op_gm_only or path.stem in GM_INDEX_SLUGS
        image_url = (fm.get("image_url") or "").strip() or None
        rows.append(
            {
                "path": path,
                "slug": path.stem,
                "op_slug": fm.get("op_slug") or path.stem,
                "name": name,
                "category": category_for(tags),
                "gm_index": gm_index,
                "image_url": image_url,
            }
        )
    return rows


def escape_text(s: str) -> str:
    """Visible tile text - do not encode apostrophes (OP shows &#x27; literally)."""
    return html.escape(s, quote=False)


def escape_attr(s: str) -> str:
    """HTML attribute values in double-quoted attributes."""
    return html.escape(s, quote=False).replace('"', "&quot;")


def render_tile(item: dict) -> str:
    href = f"/wikis/{escape_attr(item['op_slug'])}"
    name_text = escape_text(item["name"])
    name_attr = escape_attr(item["name"])
    if item.get("image_url"):
        img = (
            f'<img class="item-wiki-tile-img" src="{escape_attr(item["image_url"])}" '
            f'alt="{name_attr}">'
        )
        tile_class = "item-wiki-tile"
    else:
        img = '<span class="item-wiki-tile-placeholder" aria-hidden="true"></span>'
        tile_class = "item-wiki-tile item-wiki-tile-no-img"
    return (
        f'<div class="{tile_class}">\n'
        f'  <a class="item-wiki-tile-link" href="{href}" title="{name_attr}">\n'
        f"    {img}\n"
        f'    <span class="item-wiki-tile-name">{name_text}</span>\n'
        f"  </a>\n"
        f"</div>"
    )


def render_section(heading: str, section_items: list[dict]) -> str:
    if not section_items:
        return ""
    ordered = sorted(section_items, key=lambda i: i["name"].casefold())
    tiles = "\n".join(render_tile(item) for item in ordered)
    return f"h2. {heading}\n\n<div class=\"item-wiki-grid\">\n{tiles}\n</div>\n\n"


def render_index(items: list[dict]) -> str:
    public = [i for i in items if not i["gm_index"]]
    gm = [i for i in items if i["gm_index"]]

    body: list[str] = []
    for heading in SECTION_ORDER:
        section = [i for i in public if i["category"] == heading]
        body.append(render_section(heading, section))

    public_text = "".join(body).rstrip() + "\n"

    gm_body: list[str] = []
    for heading in SECTION_ORDER:
        section = [i for i in gm if i["category"] == heading]
        gm_body.append(render_section(heading, section))
    gm_text = "".join(gm_body).rstrip()

    return (
        f"{MARKER_START}\n"
        f"{public_text}\n"
        f"<!-- GM_INFO_START -->\n"
        f"{gm_text}\n"
        f"<!-- GM_INFO_END -->\n"
        f"{MARKER_END}\n"
    )


def render_item_image_block(name: str, image_url: str) -> str:
    safe_name = escape_attr(name)
    safe_url = escape_attr(image_url)
    return (
        f"{IMAGE_MARKER_START}\n"
        f'<div class="item-portrait"><img src="{safe_url}" alt="{safe_name}"></div>\n'
        f"{IMAGE_MARKER_END}\n"
    )


def update_item_page_image(item: dict) -> bool:
    path: Path = item["path"]
    text = path.read_text(encoding="utf-8")
    block_pattern = re.compile(
        re.escape(IMAGE_MARKER_START) + r".*?" + re.escape(IMAGE_MARKER_END) + r"\n?",
        re.S,
    )
    image_url = item.get("image_url")
    if image_url:
        block = render_item_image_block(item["name"], image_url)
        if block_pattern.search(text):
            new_text = block_pattern.sub(block, text)
        elif text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                new_text = f"---{parts[1]}---\n\n{block}\n{parts[2].lstrip()}"
            else:
                new_text = block + text
        else:
            new_text = block + text
    else:
        if not block_pattern.search(text):
            return False
        new_text = block_pattern.sub("", text)

    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def strip_index_blocks(text: str) -> str:
    """Remove generated index blocks (current Textile markers and legacy HTML comments)."""
    for start, end in (
        (MARKER_START, MARKER_END),
        (LEGACY_TEXTILE_MARKER_START, LEGACY_TEXTILE_MARKER_END),
    ):
        pattern = re.compile(
            re.escape(start) + r".*?" + re.escape(end) + r"\n?",
            re.S,
        )
        text = pattern.sub("", text)
    return text.rstrip() + "\n"


def update_items_page(items: list[dict]) -> bool:
    if not ITEMS_PAGE.exists():
        print("generate_items_index: items.textile not found", file=sys.stderr)
        return False

    text = ITEMS_PAGE.read_text(encoding="utf-8")
    generated = render_index(items)

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = strip_index_blocks(parts[2])
            intro = body.strip()
            if intro:
                new_text = f"---{parts[1]}---\n\n{intro}\n\n{generated}"
            else:
                new_text = f"---{parts[1]}---\n\n{generated}"
        else:
            new_text = strip_index_blocks(text) + "\n" + generated
    else:
        new_text = strip_index_blocks(text) + "\n" + generated

    if new_text == text:
        return False
    ITEMS_PAGE.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    items = load_items()
    if not items:
        print("generate_items_index: no wiki pages tagged item", file=sys.stderr)
        return 1

    index_changed = update_items_page(items)
    image_changes = sum(1 for item in items if update_item_page_image(item))

    public_n = sum(1 for i in items if not i["gm_index"])
    gm_n = sum(1 for i in items if i["gm_index"])
    with_images = sum(1 for i in items if i.get("image_url"))
    action = "Updated" if index_changed or image_changes else "Unchanged"
    print(
        f"{action} {ITEMS_PAGE.relative_to(ROOT)} "
        f"({public_n} public, {gm_n} GM index, {with_images} with image_url)"
    )
    if image_changes:
        print(f"  item portraits synced on {image_changes} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
