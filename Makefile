MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONTCONVERT_SCRIPT := bin/fontconvert
FONTSVG_SCRIPT := bin/fontsvg
FONTUNHINT_SCRIPT := bin/fontunhint
FONTNAMES_SCRIPT := bin/fontnames

FONT_TTF := dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF := dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF := dist/ttf/ReproTypewrLight.ttf
LIGHT_CODING_FONT_TTF := dist/ttf/ReproTypewrCodeLight.ttf

FONTS := $(FONT_TTF) $(LIGHT_FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_CODING_FONT_TTF)

FONTSVG__LIGHT := --expand-stroke 72 --translate-y -12 --scale-y 1056 --scale-y-from 1032 --scale-x 1008 --scale-x-from 984

default: $(FONTS)

.SUFFIXES: .sfd .ttf

dist/ttf/%.ttf: src/%.sfd $(FONTCONVERT_SCRIPT) $(MAKEFILE) $(FONTUNHINT_SCRIPT)
	$(FONTCONVERT_SCRIPT) "$<" "$@"
	$(FONTUNHINT_SCRIPT) "$@"

# update source font fron SVG files
fontsvg: FORCE
	$(FONTSVG_SCRIPT) --expand-stroke 96 --ignore-svg-stroke-width $(FONT_SRC) `find src/chars -type f -name '*.svg'`
braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(LIGHT_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(FONTNAMES_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	$(FONTNAMES_SCRIPT) --ps-name ReproTypewrLight --ps-weight Light "$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(FONTNAMES_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) --expand-stroke 96 --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(FONTNAMES_SCRIPT) --append-ps-name Code --append-family-name Code --append-full-name Code "$@"
	$(FONTUNHINT_SCRIPT) "$@"

$(LIGHT_CODING_FONT_TTF): $(FONT_SRC) $(FONTSVG_SCRIPT) $(MAKEFILE) $(FONTNAMES_SCRIPT) $(FONTUNHINT_SCRIPT)
	$(FONTSVG_SCRIPT) $(FONTSVG__LIGHT) --ignore-svg-stroke-width $< -o $@ `find src/chars -type f -name '*.svg'`
	mv "$@" "$@.tmp.ttf"	# tmp file required for featfreeze to work
	pyftfeatfreeze -f code -S -U Code "$@.tmp.ttf" "$@"
	rm "$@.tmp.ttf"
	$(FONTNAMES_SCRIPT) --ps-weight Light --append-ps-name "CodeLight" --append-family-name "Code" --append-full-name "Code Light" "$@"
	$(FONTUNHINT_SCRIPT) "$@"

clean: FORCE
	/bin/rm $(FONT_TTF) $(CODING_FONT_TTF) $(LIGHT_FONT_TTF) $(LIGHT_CODING_FONT_TTF) || true
	find . -type f \( -name '*.tmp' -o -name '*.tmp.*' -o -name '*.featfreeze.otf' -o -name '*~' -o -name '#*#' \) -exec rm {} + || true

.PHONY: FORCE
