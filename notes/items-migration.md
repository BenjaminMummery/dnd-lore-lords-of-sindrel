# Items → wiki pages migration

OP **inventory/item** pages do not sync via the lore bridge. New home: `lore/wiki/wiki/*.textile` with tag `item`.

## Identified from wiki links (19 colon-slugs → 18 wiki pages)

| `op_slug` | Wiki title | Link refs |
|---|---|---|
| `the-amulet-of-stars` | The Amulet of Stars | first-of-mabon, the-octarion-circle |
| `the-cel-s` | Celæs | general-alicia-meness |
| `the-crown-of-shadows` | The Crown of Shadows | high-summoner-nial-beltus |
| `the-gladius` | Gladius | lord-ablas-oestra, osteomantic-archives |
| `the-gun` | The Gun | world-history |
| `the-red-mourning` | The Red Mourning | mistress-lucretia-samhain, quarantine-zone |
| `the-shadow-s-vestment` | The Shadow's Vestment | ambassador-thrawne-lithra |
| `the-shaper-s-hands` | The Shaper's Hands | hytham-grimbolg |
| `peaches-of-immortality` | Peaches of Immortality | first-of-mabon, mistress-lucretia-samhain |
| `sindrel-coach` | Sindrel Coach | 9 refs (sessions, characters, home-page) |
| `anasthetic-scalpel` | Anasthetic Scalpel | wilrin-racenglade (PC assets) |
| `pipes-of-faunal-calling` | Pipes of Faunal Calling | session-4 |
| `spoon-of-digging` | Spoon of Digging | session-4 |
| `fallowhurst-college-master-key` | Fallowhurst College Master Key | fallowhurst-college |
| `letter-from-lord-oestra-to-embren-oestra` | Letter from Lord Oestra to Embren Oestra | fallowhurst-college |
| `map-of-fallowhurst-college` | Map of Fallowhurst College | fallowhurst-college, session-2 (`map-of-fallowhurst-college-1` alias) |
| `notes-on-triffid-research` | Notes on Triffid Research | fallowhurst-college |
| `private-warwick-s-report` | Private Warwick's Report | sebastian-warwick, hielaman |

## Link format

- **Before:** `[[:the-gladius | Gladius]]` (OP item / character colon link)
- **After:** `[[Gladius | Gladius]]` (wiki page; matches `name` / `title` frontmatter)

## Remaining on OP (manual)

- Copy item body text into each stub.
- Delete old item pages on Obsidian Portal.
- Publish new wiki pages; run sync.

## Not linked yet (Octarion table plain text)

Founder key items named in `the-octarion-circle.textile` without colon links: Mask of Foreknowledge, etc. Add wiki pages when item OP pages exist or when linking those rows.
