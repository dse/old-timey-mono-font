MAKEFILE = Makefile
FONTCONVERT = bin/fontconvert
FONTSVG = bin/fontsvg
FONT_SRC = src/ReproTypewr.sfd
FONT_TTF = dist/ttf/ReproTypewr.ttf

default: $(FONT_TTF)

dist/ttf/%.ttf: src/%.sfd $(FONTCONVERT) $(MAKEFILE)
	$(FONTCONVERT) "$<" "$@.tmp.ttf"
	mv "$@.tmp.ttf" "$@"

fontsvg: FORCE
	$(FONTSVG) --clockwise $(FONT_SRC) src/chars/96-px-outlines/*.svg
	$(FONTSVG) --expand-stroke 84 $(FONT_SRC) src/chars/12-px-outlines/*.svg

.PHONY: FORCE
