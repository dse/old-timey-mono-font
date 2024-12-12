MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONTCONVERT_SCRIPT := bin/fontconvert
FONTTOOL_SCRIPT := bin/fonttool
FONTUNHINT_SCRIPT := bin/fontunhint
SETFONTMETAS_SCRIPT := bin/setfontmetas

FONT_TTF                                := dist/ttf/ReproTypewr.ttf
CODING_FONT_TTF                         := dist/ttf/ReproTypewrCode.ttf
LIGHT_FONT_TTF                          := dist/ttf/ReproTypewr-Light.ttf
LIGHT_CODING_FONT_TTF                   := dist/ttf/ReproTypewrCode-Light.ttf
SEMI_LIGHT_FONT_TTF                     := dist/ttf/ReproTypewr-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_TTF              := dist/ttf/ReproTypewrCode-SemiLight.ttf
FONT_NARROW_TTF                         := dist/ttf/ReproTypewr17Pitch.ttf
CODING_FONT_NARROW_TTF                  := dist/ttf/ReproTypewrCode17Pitch.ttf
LIGHT_FONT_NARROW_TTF                   := dist/ttf/ReproTypewr17Pitch-Light.ttf
LIGHT_CODING_FONT_NARROW_TTF            := dist/ttf/ReproTypewrCode17Pitch-Light.ttf
SEMI_LIGHT_FONT_NARROW_TTF              := dist/ttf/ReproTypewr17Pitch-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_NARROW_TTF       := dist/ttf/ReproTypewrCode17Pitch-SemiLight.ttf
FONT_PICA_TTF                           := dist/ttf/ReproTypewrPica.ttf
CODING_FONT_PICA_TTF                    := dist/ttf/ReproTypewrCodePica.ttf
LIGHT_FONT_PICA_TTF                     := dist/ttf/ReproTypewrPica-Light.ttf
LIGHT_CODING_FONT_PICA_TTF              := dist/ttf/ReproTypewrCodePica-Light.ttf
SEMI_LIGHT_FONT_PICA_TTF                := dist/ttf/ReproTypewrPica-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_PICA_TTF         := dist/ttf/ReproTypewrCodePica-SemiLight.ttf

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

FONTTOOL__PICA       := --aspect 0.833333 # Pica => 12cpi
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

# Stage 1: import SVGs and set basic metas
src/build/ReproTypewr.stage1.sfd: src/ReproTypewr.sfd Makefile bin/importsvg
	mkdir -p src/build
	bin/importsvg "$<" -o "$@" src/chars/*.svg
	bin/setfontmetas -v \
		--family-name 'Repro Typewr' \
		--full-name 'Repro Typewr' \
		--ps-name 'ReproTypewr' \
		--ps-weight 'Medium' \
		--os2-weight 400 \
		--panose=2,0,5,9,3,0,-,-,-,3 \
		"$@"

# Stage 2: unroll references
src/build/ReproTypewr.stage2.sfd: src/build/ReproTypewr.stage1.sfd Makefile bin/fontunref
	mkdir -p src/build
	bin/fontunref "$<" -o "$@"

# Stage 3: make Pica and 17Pitch outlines
src/build/ReproTypewrPica.stage2.sfd: src/build/ReproTypewr.stage2.sfd Makefile bin/fontaspect
	mkdir -p src/build
	bin/fontaspect --aspect 0.833333333333 "$<" -o "$@"
	bin/setfontmetas -v \
		--family-name 's/Repro Typewr/Repro Typewr Pica/' \
		--full-name 's/Repro Typewr/Repro Typewr Pica/' \
		--ps-name 's/ReproTypewr/ReproTypewrPica/' \
		"$@"
src/build/ReproTypewr17Pitch.stage2.sfd: src/build/ReproTypewr.stage2.sfd Makefile bin/fontaspect
	mkdir -p src/build
	bin/fontaspect --aspect 0.606060606060 "$<" -o "$@"
	bin/setfontmetas -v \
		--family-name 's/Repro Typewr/Repro Typewr 17 Pitch/' \
		--full-name 's/Repro Typewr/Repro Typewr 17 Pitch/' \
		--ps-name 's/ReproTypewr/ReproTypewr17Pitch/' \
		"$@"

# Stage 4: make weights
dist/ttf/%.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes
	bin/expandstrokes -x 96 "$<" -o "$@"
	bin/setfontmetas -v \
		--ps-weight "Medium" \
		--os2-weight 400 \
		"$@"
dist/ttf/%-SemiLight.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes
	bin/expandstrokes -x 72 "$<" -o "$@"
	bin/setfontmetas -v \
		--full-name '+ Semi-Light' \
		--ps-name '+-SemiLight' \
		--ps-weight "Semi-Light" \
		--os2-weight 350 \
		--panose=-,-,4,-,-,-,-,-,-,- \
		"$@"
dist/ttf/%-Light.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes
	bin/expandstrokes -x 48 "$<" -o "$@"
	bin/setfontmetas -v \
		--full-name '+ Light' \
		--ps-name '+-Light' \
		--ps-weight "Light" \
		--os2-weight 300 \
		--panose=-,-,3,-,-,-,-,-,-,- \
		"$@"

# Stage 5: make code variants
dist/ttf/ReproTypewrCode%ttf: dist/ttf/ReproTypewr%ttf Makefile
	pyftfeatfreeze -f code "$<" "$@" # -U "" because we do that later
	bin/setfontmetas -v \
		--family-name 's/Repro Typewr/Repro Typewr Code/' \
		--full-name   's/Repro Typewr/Repro Typewr Code/' \
		--ps-name     's/ReproTypewr/ReproTypewrCode/' \
		"$@"

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
	/bin/rm -fr src/build || true

.PHONY: FORCE

# resetting DisplaySize: ___ doesn't break
# resetting Weight: Regular breaks
