MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONTCONVERT_SCRIPT := bin/fontconvert
FONTTOOL_SCRIPT := bin/fonttool
FONTUNHINT_SCRIPT := bin/fontunhint
SETFONTMETAS_SCRIPT := bin/setfontmetas

FONT_TTF				:= dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF				:= dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF				:= dist/ttf/ReproTypewr-Light.ttf
LIGHT_CODING_FONT_TTF			:= dist/ttf/ReproTypewrCode-Light.ttf
SEMI_LIGHT_FONT_TTF			:= dist/ttf/ReproTypewr-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_TTF		:= dist/ttf/ReproTypewrCode-SemiLight.ttf

FONT_NARROW_TTF				:= dist/ttf/ReproTypewr17Pitch.ttf
CODING_FONT_NARROW_TTF			:= dist/ttf/ReproTypewrCode17Pitch.ttf
LIGHT_FONT_NARROW_TTF			:= dist/ttf/ReproTypewr17Pitch-Light.ttf
LIGHT_CODING_FONT_NARROW_TTF		:= dist/ttf/ReproTypewrCode17Pitch-Light.ttf
SEMI_LIGHT_FONT_NARROW_TTF		:= dist/ttf/ReproTypewr17Pitch-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_NARROW_TTF		:= dist/ttf/ReproTypewrCode17Pitch-SemiLight.ttf

FONT_PICA_TTF			:= dist/ttf/ReproTypewrPica.ttf
CODING_FONT_PICA_TTF		:= dist/ttf/ReproTypewrCodePica.ttf
LIGHT_FONT_PICA_TTF			:= dist/ttf/ReproTypewrPica-Light.ttf
LIGHT_CODING_FONT_PICA_TTF		:= dist/ttf/ReproTypewrCodePica-Light.ttf
SEMI_LIGHT_FONT_PICA_TTF		:= dist/ttf/ReproTypewrPica-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_PICA_TTF	:= dist/ttf/ReproTypewrCodePica-SemiLight.ttf

CHARGRID_TPL := website/chargrid.mustache
CHARGRID_HTML := website/chargrid.html
CHARLIST_TPL := website/charlist.mustache
CHARLIST_HTML := website/charlist.html

ORIGINAL_FONTS := \
	$(FONT_TTF) \
	$(LIGHT_FONT_TTF) \
	$(SEMI_LIGHT_FONT_TTF) \
	$(FONT_NARROW_TTF) \
	$(LIGHT_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_FONT_NARROW_TTF) \
	$(FONT_PICA_TTF) \
	$(LIGHT_FONT_PICA_TTF) \
	$(SEMI_LIGHT_FONT_PICA_TTF) 

CODING_FONTS := \
	$(CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(SEMI_LIGHT_CODING_FONT_TTF) \
	$(CODING_FONT_NARROW_TTF) \
	$(LIGHT_CODING_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_CODING_FONT_NARROW_TTF) \
	$(CODING_FONT_PICA_TTF) \
	$(LIGHT_CODING_FONT_PICA_TTF) \
	$(SEMI_LIGHT_CODING_FONT_PICA_TTF)

NARROW_FONTS := \
	$(FONT_NARROW_TTF) \
	$(CODING_FONT_NARROW_TTF) \
	$(LIGHT_FONT_NARROW_TTF) \
	$(LIGHT_CODING_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_CODING_FONT_NARROW_TTF)

PICA_FONTS := \
	$(FONT_PICA_TTF) \
	$(CODING_FONT_PICA_TTF) \
	$(LIGHT_FONT_PICA_TTF) \
	$(LIGHT_CODING_FONT_PICA_TTF) \
	$(SEMI_LIGHT_FONT_PICA_TTF) \
	$(SEMI_LIGHT_CODING_FONT_PICA_TTF)

FONTS := $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTTOOL__REGULAR    := --expand-stroke 96
FONTTOOL__SEMI_LIGHT := --expand-stroke 72 # --translate-y -12  --scale-y 1344 --scale-y-from 1320  --scale-x 1008 --scale-x-from 984
FONTTOOL__LIGHT      := --expand-stroke 48 # --translate-y -24  --scale-y 1344 --scale-y-from 1296  --scale-x 1008 --scale-x-from 960
#                                                                        ^^^^     ascent     ^^^^

FONTTOOL__PICA := --aspect 0.833333 # Pica => 12cpi
FONTTOOL__NARROW     := --aspect 0.606060 # 15cpi => 16.5cpi

default: $(FONTS) $(CHARGRID_HTML) $(CHARLIST_HTML)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
narrow: $(NARROW_FONTS)
pica: $(PICA_FONTS)

.SUFFIXES: .sfd .ttf

# update source font fron SVG files
fonttool: FORCE
	$(FONTTOOL_SCRIPT) --source-file --expand-stroke 96 $(FONT_SRC) `find src/chars -type f -name '*.svg'`

braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr" \
		--full-name   "Repro Typewr" \
		--ps-name     "ReproTypewr" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr" \
		--full-name   "Repro Typewr Semi-Light" \
		--ps-name     "ReproTypewr-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr" \
		--full-name   "Repro Typewr Light" \
		--ps-name     "ReproTypewr-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code" \
		--full-name   "Repro Typewr Code" \
		--ps-name     "ReproTypewrCode" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code" \
		--full-name   "Repro Typewr Code Semi-Light" \
		--ps-name     "ReproTypewrCode-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code" \
		--full-name   "Repro Typewr Code Light" \
		--ps-name     "ReproTypewrCode-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr 17 Pitch" \
		--full-name   "Repro Typewr 17 Pitch" \
		--ps-name     "ReproTypewr17Pitch" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr 17 Pitch" \
		--full-name   "Repro Typewr 17 Pitch Semi-Light" \
		--ps-name     "ReproTypewr17Pitch-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr 17 Pitch" \
		--full-name   "Repro Typewr 17 Pitch Light" \
		--ps-name     "ReproTypewr17Pitch-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code 17 Pitch" \
		--full-name   "Repro Typewr Code 17 Pitch" \
		--ps-name     "ReproTypewrCode17Pitch" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_CODING_FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code 17 Pitch" \
		--full-name   "Repro Typewr Code 17 Pitch Semi-Light" \
		--ps-name     "ReproTypewrCode17Pitch-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_NARROW_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $(FONTTOOL__NARROW) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code 17 Pitch" \
		--full-name   "Repro Typewr Code 17 Pitch Light" \
		--ps-name     "ReproTypewrCode17Pitch-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Pica" \
		--full-name   "Repro Typewr Pica" \
		--ps-name     "ReproTypewrPica" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Pica" \
		--full-name   "Repro Typewr Pica Semi-Light" \
		--ps-name     "ReproTypewrPica-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Pica" \
		--full-name   "Repro Typewr Pica Light" \
		--ps-name     "ReproTypewrPica-Light" \
		--ps-weight   "Light" \
		--os2-weight  300 \
		--panose      2,0,3,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__REGULAR) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code Pica" \
		--full-name   "Repro Typewr Code Pica" \
		--ps-name     "ReproTypewrCodePica" \
		--ps-weight   "Medium" \
		--os2-weight  400 \
		--panose      2,0,5,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(SEMI_LIGHT_CODING_FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__SEMI_LIGHT) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code Pica" \
		--full-name   "Repro Typewr Code Pica Semi-Light" \
		--ps-name     "ReproTypewrCodePica-SemiLight" \
		--ps-weight   "Semi-Light" \
		--os2-weight  350 \
		--panose      2,0,4,9,3,0,-,-,-,3 \
		"$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_PICA_TTF): $(FONT_SRC) $(FONTTOOL_SCRIPT) $(MAKEFILE) $(SETFONTMETAS_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTTOOL_SCRIPT) $(FONTTOOL__LIGHT) $(FONTTOOL__PICA) $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(SETFONTMETAS_SCRIPT) \
		--family-name "Repro Typewr Code Pica" \
		--full-name   "Repro Typewr Code Pica Light" \
		--ps-name     "ReproTypewrCodePica-Light" \
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
