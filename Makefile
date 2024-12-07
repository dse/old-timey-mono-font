MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONTCONVERT_SCRIPT := bin/fontconvert
FONTSVG_SCRIPT := bin/fontsvg
FONTUNHINT_SCRIPT := bin/fontunhint
SETFONTMETAS_SCRIPT := bin/setfontmetas

FONT_TTF := dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF := dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF := dist/ttf/ReproTypewr-Light.ttf
LIGHT_CODING_FONT_TTF := dist/ttf/ReproTypewrCode-Light.ttf
SEMI_LIGHT_FONT_TTF := dist/ttf/ReproTypewr-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_TTF := dist/ttf/ReproTypewrCode-SemiLight.ttf

FONT_COND_TTF := dist/ttf/ReproTypewr-Cond.ttf
CODING_FONT_COND_TTF := dist/ttf/ReproTypewrCode-Cond.ttf
LIGHT_FONT_COND_TTF := dist/ttf/ReproTypewr-CondLight.ttf
LIGHT_CODING_FONT_COND_TTF := dist/ttf/ReproTypewrCode-CondLight.ttf
SEMI_LIGHT_FONT_COND_TTF := dist/ttf/ReproTypewr-CondSemiLight.ttf
SEMI_LIGHT_CODING_FONT_COND_TTF := dist/ttf/ReproTypewrCode-CondSemiLight.ttf

FONT_SEMICOND_TTF := dist/ttf/ReproTypewr-SemiCond.ttf
CODING_FONT_SEMICOND_TTF := dist/ttf/ReproTypewrCode-SemiCond.ttf
LIGHT_FONT_SEMICOND_TTF := dist/ttf/ReproTypewr-SemiCondLight.ttf
LIGHT_CODING_FONT_SEMICOND_TTF := dist/ttf/ReproTypewrCode-SemiCondLight.ttf
SEMI_LIGHT_FONT_SEMICOND_TTF := dist/ttf/ReproTypewr-SemiCondSemiLight.ttf
SEMI_LIGHT_CODING_FONT_SEMICOND_TTF := dist/ttf/ReproTypewrCode-SemiCondSemiLight.ttf

CHARGRID_TPL := website/chargrid.mustache
CHARGRID_HTML := website/chargrid.html
CHARLIST_TPL := website/charlist.mustache
CHARLIST_HTML := website/charlist.html

ORIGINAL_FONTS := \
	$(FONT_TTF) \
	$(LIGHT_FONT_TTF) \
	$(SEMI_LIGHT_FONT_TTF) \
	$(FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) \
	$(SEMI_LIGHT_FONT_COND_TTF) \
	$(FONT_SEMICOND_TTF) \
	$(LIGHT_FONT_SEMICOND_TTF) \
	$(SEMI_LIGHT_FONT_SEMICOND_TTF) 

CODING_FONTS := \
	$(CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(SEMI_LIGHT_CODING_FONT_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF) \
	$(SEMI_LIGHT_CODING_FONT_COND_TTF) \
	$(CODING_FONT_SEMICOND_TTF) \
	$(LIGHT_CODING_FONT_SEMICOND_TTF) \
	$(SEMI_LIGHT_CODING_FONT_SEMICOND_TTF)

CONDENSED_FONTS := \
	$(FONT_COND_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF) \
	$(SEMI_LIGHT_FONT_COND_TTF) \
	$(SEMI_LIGHT_CODING_FONT_COND_TTF)

SEMICONDENSED_FONTS := \
	$(FONT_SEMICOND_TTF) \
	$(CODING_FONT_SEMICOND_TTF) \
	$(LIGHT_FONT_SEMICOND_TTF) \
	$(LIGHT_CODING_FONT_SEMICOND_TTF) \
	$(SEMI_LIGHT_FONT_SEMICOND_TTF) \
	$(SEMI_LIGHT_CODING_FONT_SEMICOND_TTF)

FONTS := $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTSVG__REGULAR    := --expand-stroke 96
FONTSVG__SEMI_LIGHT := --expand-stroke 72 # --translate-y -12  --scale-y 1344 --scale-y-from 1320  --scale-x 1008 --scale-x-from 984
FONTSVG__LIGHT      := --expand-stroke 48 # --translate-y -24  --scale-y 1344 --scale-y-from 1296  --scale-x 1008 --scale-x-from 960
#                                                                        ^^^^     ascent     ^^^^

FONTSVG__SEMICONDENSED := --aspect 0.833333 # Pica => 12cpi
FONTSVG__CONDENSED     := --aspect 0.606060 # 15cpi => 16.5cpi

default: $(FONTS) $(CHARGRID_HTML) $(CHARLIST_HTML)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
condensed: $(CONDENSED_FONTS)
semicondensed: $(SEMICONDENSED_FONTS)

.SUFFIXES: .sfd .ttf

# update source font fron SVG files
fontsvg: FORCE
	$(FONTSVG_SCRIPT) --expand-stroke 96 $(FONT_SRC) `find src/chars -type f -name '*.svg'`

braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter" \
		--ps-name     "ReproTypewr" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Semi-Light" \
		--ps-name     "ReproTypewr-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Light" \
		--ps-name     "ReproTypewr-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code" \
		--ps-name     "ReproTypewrCode" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
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
		--ps-name     "ReproTypewrCode-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
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
		--ps-name     "ReproTypewrCode-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Condensed" \
		--ps-name     "ReproTypewr-Cond" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Condensed Semi-Light" \
		--ps-name     "ReproTypewr-CondSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Condensed Light" \
		--ps-name     "ReproTypewr-CondLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Condensed" \
		--ps-name     "ReproTypewrCode-Cond" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_CODING_FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Condensed Semi-Light" \
		--ps-name     "ReproTypewrCode-CondSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_COND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $(FONTSVG__CONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Condensed Light" \
		--ps-name     "ReproTypewrCode-CondLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Semicondensed" \
		--ps-name     "ReproTypewr-SemiCond" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Semicondensed Semi-Light" \
		--ps-name     "ReproTypewr-SemiCondSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter" \
		--full-name   "Reproducing Typewriter Semicondensed Light" \
		--ps-name     "ReproTypewr-SemiCondLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__REGULAR) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Semicondensed" \
		--ps-name     "ReproTypewrCode-SemiCond" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_CODING_FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__SEMI_LIGHT) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Semicondensed Semi-Light" \
		--ps-name     "ReproTypewrCode-SemiCondSemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_SEMICOND_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) $(FONTSVG__SEMICONDENSED) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Reproducing Typewriter Code" \
		--full-name   "Reproducing Typewriter Code Semicondensed Light" \
		--ps-name     "ReproTypewrCode-SemiCondLight" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

chargrid: FORCE $(CHARGRID_HTML)
charlist: FORCE $(CHARLIST_HTML)

$(CHARGRID_HTML): $(FONT_SRC) $(CHARGRID_TPL) $(MAKEFILE)
	bin/fontdata $(FONT_SRC) > temp.json
	chevron -d temp.json $(CHARGRID_TPL) > $@
	rm temp.json

$(CHARLIST_HTML): $(FONT_SRC) $(CHARLIST_TPL) $(MAKEFILE)
	bin/fontdata $(FONT_SRC) > temp2.json
	chevron -d temp2.json $(CHARLIST_TPL) > $@
	rm temp2.json

clean: FORCE
	/bin/rm $(FONTS) $(CHARGRID_HTML) $(CHARLIST_HTML) || true
	find . -type f \( -name '*.tmp' -o -name '*.tmp.*' -o -name '*.featfreeze.otf' -o -name '*~' -o -name '#*#' \) -exec rm {} + || true

.PHONY: FORCE

# resetting DisplaySize: ___ doesn't break
# resetting Weight: Regular breaks
