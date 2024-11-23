MAKEFILE = Makefile
FONTCONVERT = bin/fontconvert
FONTSVG = bin/fontsvg
FONT_SRC = src/ReproTypewr.sfd

FONT_TTF = dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF = dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF = dist/ttf/ReproTypewrLight.ttf
LIGHT_CODING_FONT_TTF = dist/ttf/ReproTypewrCodeLight.ttf
FONTS = $(FONT_TTF) $(LIGHT_FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_CODING_FONT_TTF)

FONTSVG__LIGHT = --expand-stroke 72 --translate-y -12 --scale-y 1056 --scale-y-from 1032 --scale-x 1008 --scale-x-from 984

default: $(FONTS)

dist/ttf/%.ttf: src/%.sfd $(FONTCONVERT) $(MAKEFILE)
	$(FONTCONVERT) "$<" "$@.tmp.ttf"
	mv "$@.tmp.ttf" "$@"

# update source font fron SVG files
fontsvg: FORCE
	$(FONTSVG) --expand-stroke 96 --ignore-svg-stroke-width $(FONT_SRC) `find src/chars -type f -name '*.svg'`
braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG) $(MAKEFILE) bin/fontnames
	$(FONTSVG) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	bin/fontnames --ps-name ReproTypewrLight --ps-weight Light "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG) $(MAKEFILE) bin/fontnames
	$(FONTSVG) --expand-stroke 96 --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	bin/fontnames --append-ps-name Code --append-family-name Code --append-full-name Code "$@"

$(LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG) $(MAKEFILE) bin/fontnames
	$(FONTSVG) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	bin/fontnames --ps-weight Light --append-ps-name "CodeLight" --append-family-name "Code" --append-full-name "Code Light" "$@"

clean: FORCE
	/bin/rm $(CODING_FONT_TTF) $(LIGHT_FONT_TTF) $(LIGHT_CODING_FONT_TTF) || true

.PHONY: FORCE
