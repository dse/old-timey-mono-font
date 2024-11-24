MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONTCONVERT_SCRIPT := bin/fontconvert
FONTSVG_SCRIPT := bin/fontsvg
FONTUNHINT_SCRIPT := bin/fontunhint
SETFONTMETAS_SCRIPT := bin/setfontmetas

FONT_TTF := dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF := dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF := dist/ttf/ReproTypewrLight.ttf
LIGHT_CODING_FONT_TTF := dist/ttf/ReproTypewrCodeLight.ttf

FONTS := $(FONT_TTF) $(LIGHT_FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_CODING_FONT_TTF)

FONTSVG__LIGHT := --expand-stroke 72 --translate-y -12 --scale-y 1056 --scale-y-from 1032 --scale-x 1008 --scale-x-from 984

default: $(FONTS)

.SUFFIXES: .sfd .ttf

dist/ttf/%.ttf: src/%.sfd $(FONTCONVERT_SCRIPT) $(MAKEFILE) $(FONTUNHINT_SCRIPT) $(SETFONTMETAS_SCRIPT)
	$(FONTCONVERT_SCRIPT) "$<" "$@"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter" \
		--ps-name     "ReproTypewr" \
		--ps-weight   "Book" \
		--os2-weight  400 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

# update source font fron SVG files
fontsvg: FORCE
	$(FONTSVG_SCRIPT) --expand-stroke 96 --ignore-svg-stroke-width $(FONT_SRC) `find src/chars -type f -name '*.svg'`
braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Light" \
		--ps-name     "ReproTypewrLight" \
		--ps-weight   "Light" \
		--os2-weight  250 \
		--panose      2,14,3,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) --expand-stroke 96 --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code" \
		--ps-name     "ReproTypewrCode" \
		--ps-weight   "Book" \
		--os2-weight  400 \
		--panose      2,14,5,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Light" \
		--ps-name     "ReproTypewrCodeLight" \
		--ps-weight   "Light" \
		--os2-weight  250 \
		--panose      2,14,3,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

clean: FORCE
	/bin/rm $(FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_FONT_TTF) $(LIGHT_CODING_FONT_TTF) || true
	find . -type f \( -name '*.tmp' -o -name '*.tmp.*' -o -name '*.featfreeze.otf' -o -name '*~' -o -name '#*#' \) -exec rm {} + || true

.PHONY: FORCE
