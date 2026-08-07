MAIN = main
TEXINPUTS = ./lib//:
LATEX = latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -file-line-error
GLOSSARIES = makeglossaries
export PATH := /Library/TeX/texbin:$(PATH)

.PHONY: all pdf clean distclean watch

all: pdf

pdf:
	TEXINPUTS="$(TEXINPUTS)" $(LATEX) $(LATEXFLAGS) $(MAIN).tex

watch:
	TEXINPUTS="$(TEXINPUTS)" $(LATEX) $(LATEXFLAGS) -pvc $(MAIN).tex

clean:
	TEXINPUTS="$(TEXINPUTS)" $(LATEX) -C $(MAIN).tex

distclean: clean
	rm -rf $(MAIN).synctex.gz
