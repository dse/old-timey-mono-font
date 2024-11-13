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
	$(FONTSVG) --expand-stroke 96 --ignore-svg-stroke-width $(FONT_SRC) `find src/chars -type f -name '*.svg'`

metrics: FORCE
	glyphbearings src/ReproTypewrA.sfd > data/orig-metrics.txt
	glyphbearings src/ReproTypewr.sfd > data/new-metrics.txt

braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

.PHONY: FORCE
