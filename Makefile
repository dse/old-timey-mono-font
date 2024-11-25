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
SEMI_LIGHT_FONT_TTF := dist/ttf/ReproTypewrSemiLight.ttf
SEMI_LIGHT_CODING_FONT_TTF := dist/ttf/ReproTypewrCodeSemiLight.ttf

FONTS := $(FONT_TTF) \
	$(LIGHT_FONT_TTF) \
	$(CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(SEMI_LIGHT_FONT_TTF) \
	$(SEMI_LIGHT_CODING_FONT_TTF)

FONTSVG__SEMI_LIGHT := --expand-stroke 68 --translate-y -14  --scale-y 1056 --scale-y-from 1028  --scale-x 1008 --scale-x-from 980
FONTSVG__LIGHT      := --expand-stroke 48 --translate-y -24  --scale-y 1056 --scale-y-from 1008  --scale-x 1008 --scale-x-from 960

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
		--panose      2,14,5,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

# update source font fron SVG files
fontsvg: FORCE
	$(FONTSVG_SCRIPT) --expand-stroke 96 $(FONT_SRC) `find src/chars -type f -name '*.svg'`
braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Light" \
		--ps-name     "ReproTypewrLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,14,3,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Semi-Light" \
		--ps-name     "ReproTypewrSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,14,4,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) --expand-stroke 96 $< -o $@ `find src/chars -type f -name '*.svg'`
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

$(SEMI_LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Semi-Light" \
		--ps-name     "ReproTypewrCodeSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,14,4,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Light" \
		--ps-name     "ReproTypewrCodeLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,14,3,9,-,2,-,-,-,- \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

CHARGRID_TPL := website/chargrid.mustache
CHARGRID_HTML := website/chargrid.html

chargrid: FORCE $(CHARGRID_HTML)

$(CHARGRID_HTML): $(FONT_SRC) $(CHARGRID_TPL) $(MAKEFILE)
	bin/fontdata $(FONT_SRC) > temp.json
	chevron -d temp.json $(CHARGRID_TPL) > $@
	rm temp.json

clean: FORCE
	/bin/rm $(FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_FONT_TTF) $(LIGHT_CODING_FONT_TTF) || true
	find . -type f \( -name '*.tmp' -o -name '*.tmp.*' -o -name '*.featfreeze.otf' -o -name '*~' -o -name '#*#' \) -exec rm {} + || true

.PHONY: FORCE
