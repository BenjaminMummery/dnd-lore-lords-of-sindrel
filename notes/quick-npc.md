# Quick NPC cheat sheet

Repo-only. Agent rule: `.cursor/rules/npc-generation.mdc` (prefer that for generation).

## One-line prompts

```
Quick NPC: Leageur, Silas Oestra attendant
Quick NPC: Wallarch, Grimbolg adjutant porter
Quick NPC: Dockward, refugee dock labourer (silver)
Quick NPC: Fulcrum, Grimbolg adjutant registry clerk
Quick NPC: Fulcrum, visitor Factor, human ambassador
```

Even shorter (agent applies defaults): `NPC: Fulcrum clerk` · `NPC: Leageur attendant`

## Affiliation

**Permanent residents must have house patronage** — gold bracelet (Adjutant) or house tattoo (Factor). No long-term unaffiliated city jobs.

| Who | Affiliation |
|-----|-------------|
| Fulcrum clerks, Wallarch porters, house staff | **Adjutant** (pick house) |
| Hexine delegates, foreign merchants in town | **Visitor** — silver bracelet, Factor if senior |
| Traders, diplomats, new arrivals, refugees without patronage | **Unaffiliated** (silver) |
| Criminals off the books | Unaffiliated (illegal) |

**Fulcrum desk work:** Grimbolg, Lithra, or Goela. **Security:** Meness or Oestra.

## Location → population

| Where | Default |
|-------|---------|
| Leageur / house staff | **Native** |
| House salon guests | **Visitor** |
| Merchant's Quarter | Visitor guests; native clerks |
| Fulcrum / Merrylane | Native **Adjutant**; visitors = delegates |
| Dockward | Mix; refugee/native labour often **silver** |
| Wallarch | Native adjutants (poor postings) or visitor traders |
| Outside Sindrel | **Visitor** (Artresh) |

Staff in a house → native. Dignitary in the salon → visitor.

## Species (population first, then tier)

**Bias away from Human** on new improvisations (~1 in 4–5 may still be Human). Pick **population** first, then species from that profile. See the [lore bridge dashboard](https://obsidianportal-git-sync.onrender.com/) for race counts.

**Native:** Core human/elf/half-elf/dwarf/gnome/halfling · Common tiefling/aasimar/dragonborn/genasi/half-orc — prefer Common/non-human Core for native staff.

**Visitor (Artresh):** Core human/orc/dwarf/halfling/goblin · Rare tiefling/aasimar/fey — Human OK more often; still vary.

**Refugee:** Core tiefling/aasimar/genasi/half-elf/elf · Uncommon human/dwarf/halfling — Human should be uncommon here.

## Names by house

Pick one or riff on the pattern. Minor canon names included as style anchors.

| House | Example names (adjutant tier) |
|-------|-------------------------------|
| **Oestra** | Cassia Drusken, Marco Valer, Livia Corin |
| **Beltus** | Rostam Darvish, Shirin Anahita, Parviz Khorshid |
| **Meness** | Eirik Tryke, Astrid Volva, Brokkr Stegg |
| **Goela** | Nikias Orestes, Calliope Thessaly, Phaedra Mnemos |
| **Lithra** | Senet Amunet, Kebi Neferu, Nashira Seti |
| **Mabon** | Ren Kurogane, Yuki Matsura, Hana Mori |
| **Grimbolg** | Sena Ott, Thistle Goodbarley, Bramwell Cobb |
| **Visitor** (silver) | Bran Holloway, Mira Dunwick, Tomas Greymark |

Oestra Latinate · Beltus Persian · Meness Norse · Goela Greek · Lithra Egyptian · Mabon Japanese · Grimbolg Houdian

## House tells (one line each)

| House | Tell |
|-------|------|
| Oestra | Armour, crimson/black/bronze, sword visible, blunt |
| Meness | White watch-coat, black trim, lawful |
| Goela | Purple, veils, oracular |
| Grimbolg | Moss green, apron, work-stained |
| Beltus | Black/gold, layered, servants |
| Mabon | Indigo/grey, maker's marks |
| Lithra | Grey/silver, performance poise |

## Output checklist

1. Population (one line why)
2. Name · Species · Pronouns · House · Role (Adjutant/Factor?)
3. *You see…* (2–4 sentences)
4. House tells (1–2 details)
5. Hook (optional; GM-only if secret)

## Gender

Target 45/45/10 he/she/nb — bias underrepresented when improvising. See the [lore bridge dashboard](https://obsidianportal-git-sync.onrender.com/).

## Persist

Walk-ons: chat only. To keep: ask agent to save → `lore/characters/<slug>.textile`.
