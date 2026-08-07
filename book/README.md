# Guide to the Worlds of Sindrel

LaTeX source for a D&D-style lore guide, typeset with the [DND 5e LaTeX Template](https://github.com/rpgtex/DND-5e-LaTeX-Template) (vendored in `lib/dnd/`).

## Prerequisites

Install a TeX distribution. On macOS:

```sh
# Full install (~4 GB), recommended if you typeset often
brew install --cask mactex-no-gui

# Or minimal install (~100 MB); add packages as needed
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk collection-fontsrecommended tcolorbox environ trimspaces
```

After installing MacTeX or BasicTeX, ensure binaries are on your `PATH`:

```sh
export PATH="/Library/TeX/texbin:$PATH"
```

Verify:

```sh
pdflatex --version
latexmk --version
```

## Build

From this directory:

```sh
make          # build main.pdf
make watch    # rebuild on save
make clean    # remove build artifacts
```

Or directly:

```sh
TEXINPUTS=./lib//: latexmk -pdf main.tex
```

Output: `main.pdf`

## Project layout

```
book/
├── main.tex              # Root document; add \input{} for chapters here
├── chapters/             # One .tex file per chapter/section
├── lib/dnd/              # DND-5e-LaTeX-Template (git clone)
├── Makefile
└── .latexmkrc
```

## Adding content

1. Create `chapters/your-topic.tex`.
2. Add `\input{chapters/your-topic}` to `main.tex` under the appropriate `\part{}`.
3. Run `make`.

Source lore lives in `../lore/` (Textile). Rewrite or adapt it into LaTeX as you go.

## Updating the template

```sh
cd lib/dnd && git pull
```

## Template options

Common `dndbook` class options (see [template README](https://github.com/rpgtex/DND-5e-LaTeX-Template)):

| Option | Effect |
|--------|--------|
| `bg=none` | No parchment background (faster preview, less ink) |
| `bg=print` | Footer art only |
| `justified` | Justify column text |

Example: `\documentclass[letterpaper,twocolumn,openany,bg=none,nodeprecatedcode]{dndbook}`
