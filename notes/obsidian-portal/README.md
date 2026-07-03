# Obsidian Portal styling (local backup)

Repo-only copies of **Custom CSS** and **Custom Character Layout** for [The Lords of Sindrel](https://thelordsofsindrel.obsidianportal.com/). Not synced to OP.

## Files

| File | OP destination | Notes |
|------|----------------|-------|
| **`custom-css.css`** | Campaign Settings → Advanced → **Custom CSS** | **SSOT** - paste the whole file. CoS grey palette, index tile borders, timeline, item wiki tiles. |
| `custom-css-cos-theme-safe.css` | Same (replace `custom-css.css` only if switching themes) | Alternate CoS theme (`.campaign-public-layout` scoped, parchment tables). Not combined with live CSS. |
| `timeline-showpiece-snippet.html` | New wiki page body (Textile mode) | HTML for the timeline page; paste below a short intro. |
| `character-index-layout.html` | Campaign Settings → Characters → **Custom Layout** | Tag-driven index sections (party, houses, Black Cats, City Cats, etc.). |

## Refreshing from live OP

The lore bridge does **not** export Custom CSS or character layout. To update these files:

1. **Custom CSS** - copy from OP Settings, or from `/themes/custom_css.css` on the live site (User Custom CSS section only). Bot protection may block automated fetch. Replace `custom-css.css` in one piece; do not maintain separate append files.
2. **Character layout** - copy from OP Settings → Characters → Custom Layout.

After editing locally, paste `custom-css.css` back into OP to apply.

## OP CSS sanitizer (known blockers)

OP rejects the whole paste if these appear **anywhere** in the file (including comments):

- `>` (child combinator; also avoid in comments)
- the substring `description` (including `.character-description` - use `.main-content p a` instead)
- the substring `@import` (including in comments that mention it)
- CSS variables (`:root`, `var()`)
- Unicode in comments (em dashes, arrows, curly quotes)
- `content:` in `:before` / `:after`

Also avoid if save still fails: `calc()`, `object-fit`, `:focus-within`.

Before pasting into OP, run: `scripts/check_op_custom_css.py notes/obsidian-portal/custom-css.css`

See [OP custom CSS basics](https://help.obsidianportal.com/article/183-custom-css-basics).

## Character layout conventions

- Tags slugify to classes: `House Oestra` → `.tag-house-oestra`, `in-party` → `.tag-in-party`.
- Player characters use the **Player Character** flag → `.pc` (not a tag).
- **Deceased** / **Undead** are styling tags only; characters stay in house/party buckets.
- **City Cats** section uses `.tag-city-cats`; extend the **OTHERS** `:not()` chain with `:not(.tag-city-cats)`.
- Do **not** add a separate Undead index section (use tile border CSS in `custom-css.css` instead).

Agent conventions for tags and layout: `.cursor/rules/lore-assistant.mdc`.
