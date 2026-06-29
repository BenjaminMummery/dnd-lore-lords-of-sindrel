# Obsidian Portal styling (local backup)

Repo-only copies of **Custom CSS** and **Custom Character Layout** for [The Lords of Sindrel](https://thelordsofsindrel.obsidianportal.com/). Not synced to OP.

## Files

| File | OP destination | Notes |
|------|----------------|-------|
| `custom-css-cos-grey-palette.css` | Campaign Settings → Advanced → **Custom CSS** | **Current live theme** - grey read-aloud blockquotes, index name sizing (`20px` on list items), table header fix. |
| `custom-css-cos-theme-safe.css` | Same | Alternate CoS theme (`.campaign-public-layout` scoped, parchment tables). Compare before replacing live CSS. |
| `custom-css-index-tile-borders.css` | Append to Custom CSS | Deceased / Undead tile borders (state tags, not separate index sections). |
| `character-index-layout.html` | Campaign Settings → Characters → **Custom Layout** | Tag-driven index sections (party, houses, Black Cats, City Cats, etc.). |

## Refreshing from live OP

The lore bridge does **not** export Custom CSS or character layout. To update these files:

1. **Custom CSS** - copy from OP Settings, or from `/themes/custom_css.css` on the live site (User Custom CSS section only). Bot protection may block automated fetch.
2. **Character layout** - copy from OP Settings → Characters → Custom Layout.

After editing locally, paste back into OP to apply.

## OP CSS sanitizer (known blockers)

Avoid in Custom CSS or OP rejects the save:

- `>` anywhere (including comments)
- the word `description`
- `@import`
- CSS variables (`:root`, `var()`)
- Unicode in comments (em dashes, curly quotes)
- `content:` in `:before` / `:after`

See [OP custom CSS basics](https://help.obsidianportal.com/article/183-custom-css-basics).

## Character layout conventions

- Tags slugify to classes: `House Oestra` → `.tag-house-oestra`, `in-party` → `.tag-in-party`.
- Player characters use the **Player Character** flag → `.pc` (not a tag).
- **Deceased** / **Undead** are styling tags only; characters stay in house/party buckets.
- **City Cats** section uses `.tag-city-cats`; extend the **OTHERS** `:not()` chain with `:not(.tag-city-cats)`.
- Do **not** add a separate Undead index section (use tile border CSS instead).

Agent conventions for tags and layout: `.cursor/rules/lore-assistant.mdc`.
