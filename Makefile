MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONT_FAMILY := Repro Typewr
PS_FONT_FAMILY := ReproTypewr

IMPORTSVG_PROG     := bin/importsvg
FONTUNREF_PROG     := bin/fontunref
EXPANDSTROKES_PROG := bin/expandstrokes
FONTASPECT_PROG    := bin/fontaspect
SETFONTMETAS_PROG  := bin/setfontmetas

OPT_VERBOSE :=

IMPORTSVG     := $(IMPORTSVG_PROG)
FONTUNREF     := $(FONTUNREF_PROG)
EXPANDSTROKES := $(EXPANDSTROKES_PROG)
FONTASPECT    := $(FONTASPECT_PROG)
SETFONTMETAS  := $(SETFONTMETAS_PROG)

FONT_TTF                                := dist/ttf/$(PS_FONT_FAMILY).ttf
CODING_FONT_TTF                         := dist/ttf/$(PS_FONT_FAMILY)Code.ttf
LIGHT_FONT_TTF                          := dist/ttf/$(PS_FONT_FAMILY)-Light.ttf
LIGHT_CODING_FONT_TTF                   := dist/ttf/$(PS_FONT_FAMILY)Code-Light.ttf
SEMI_LIGHT_FONT_TTF                     := dist/ttf/$(PS_FONT_FAMILY)-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_TTF              := dist/ttf/$(PS_FONT_FAMILY)Code-SemiLight.ttf
FONT_NARROW_TTF                         := dist/ttf/$(PS_FONT_FAMILY)17Pitch.ttf
CODING_FONT_NARROW_TTF                  := dist/ttf/$(PS_FONT_FAMILY)Code17Pitch.ttf
LIGHT_FONT_NARROW_TTF                   := dist/ttf/$(PS_FONT_FAMILY)17Pitch-Light.ttf
LIGHT_CODING_FONT_NARROW_TTF            := dist/ttf/$(PS_FONT_FAMILY)Code17Pitch-Light.ttf
SEMI_LIGHT_FONT_NARROW_TTF              := dist/ttf/$(PS_FONT_FAMILY)17Pitch-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_NARROW_TTF       := dist/ttf/$(PS_FONT_FAMILY)Code17Pitch-SemiLight.ttf
FONT_ELITE_TTF                           := dist/ttf/$(PS_FONT_FAMILY)Elite.ttf
CODING_FONT_ELITE_TTF                    := dist/ttf/$(PS_FONT_FAMILY)CodeElite.ttf
LIGHT_FONT_ELITE_TTF                     := dist/ttf/$(PS_FONT_FAMILY)Elite-Light.ttf
LIGHT_CODING_FONT_ELITE_TTF              := dist/ttf/$(PS_FONT_FAMILY)CodeElite-Light.ttf
SEMI_LIGHT_FONT_ELITE_TTF                := dist/ttf/$(PS_FONT_FAMILY)Elite-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_ELITE_TTF         := dist/ttf/$(PS_FONT_FAMILY)CodeElite-SemiLight.ttf

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
	$(FONT_ELITE_TTF) \
	$(LIGHT_FONT_ELITE_TTF) \
	$(SEMI_LIGHT_FONT_ELITE_TTF) 

CODING_FONTS := \
	$(CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(SEMI_LIGHT_CODING_FONT_TTF) \
	$(CODING_FONT_NARROW_TTF) \
	$(LIGHT_CODING_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_CODING_FONT_NARROW_TTF) \
	$(CODING_FONT_ELITE_TTF) \
	$(LIGHT_CODING_FONT_ELITE_TTF) \
	$(SEMI_LIGHT_CODING_FONT_ELITE_TTF)

NARROW_FONTS := \
	$(FONT_NARROW_TTF) \
	$(CODING_FONT_NARROW_TTF) \
	$(LIGHT_FONT_NARROW_TTF) \
	$(LIGHT_CODING_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_FONT_NARROW_TTF) \
	$(SEMI_LIGHT_CODING_FONT_NARROW_TTF)

ELITE_FONTS := \
	$(FONT_ELITE_TTF) \
	$(CODING_FONT_ELITE_TTF) \
	$(LIGHT_FONT_ELITE_TTF) \
	$(LIGHT_CODING_FONT_ELITE_TTF) \
	$(SEMI_LIGHT_FONT_ELITE_TTF) \
	$(SEMI_LIGHT_CODING_FONT_ELITE_TTF)

ZIP_FILE = dist/ReproTypewr.zip

FONTS := $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTTOOL__REGULAR    := --expand-stroke 96
FONTTOOL__SEMI_LIGHT := --expand-stroke 72 # --translate-y -12  --scale-y 1344 --scale-y-from 1320  --scale-x 1008 --scale-x-from 984
FONTTOOL__LIGHT      := --expand-stroke 48 # --translate-y -24  --scale-y 1344 --scale-y-from 1296  --scale-x 1008 --scale-x-from 960

FONTTOOL__ELITE       := --aspect 0.833333 # Elite => 12cpi
FONTTOOL__NARROW     := --aspect 0.606060 # 15cpi => 16.5cpi

default: $(FONTS) $(CHARGRID_HTML) $(CHARLIST_HTML)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
narrow: $(NARROW_FONTS)
elite: $(ELITE_FONTS)
zip: $(ZIP_FILE)

.SUFFIXES: .sfd .ttf

# update source font fron SVG files
update: FORCE
	$(IMPORTSVG) $(FONT_SRC) `find src/chars \! \( -type d -name \*italic\* -prune \) -type f -name '*.svg'`
	$(EXPANDSTROKES) --expand-stroke 96 $(FONT_SRC)
fonttool: FORCE
	echo "use 'make update', dingus." >&2
	false
fontsvg: FORCE
	echo "use 'make update', dingus." >&2
	false

braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(ZIP_FILE): $(FONTS) Makefile
	( cd dist && zip -r ReproTypewr.zip ttf )

# Stage 1: import SVGs and set basic metas
src/build/$(PS_FONT_FAMILY).stage1.sfd: src/$(PS_FONT_FAMILY).sfd Makefile $(IMPORTSVG_PROG) $(SETFONTMETAS_PROG)
	mkdir -p src/build
	$(IMPORTSVG) "$<" -o "$@" src/chars/*.svg
	$(SETFONTMETAS) \
		--family-name '$(FONT_FAMILY)' \
		--full-name '$(FONT_FAMILY)' \
		--ps-name '$(PS_FONT_FAMILY)' \
		--ps-weight 'Medium' \
		--os2-weight 400 \
		--panose 2,0,5,9,3,0,_,_,_,3 \
		"$@"

# Stage 2: unroll references
src/build/$(PS_FONT_FAMILY).stage2.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(FONTUNREF_PROG)
	mkdir -p src/build
	$(FONTUNREF) "$<" -o "$@"

# Stage 3: make Elite and 17Pitch outlines
src/build/$(PS_FONT_FAMILY)Elite.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(FONTASPECT_PROG) $(SETFONTMETAS_PROG)
	mkdir -p src/build
	$(FONTASPECT) --aspect 0.833333333333 "$<" -o "$@"
	$(SETFONTMETAS) \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Elite/' \
		--full-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Elite/' \
		--ps-name 's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)Elite/' \
		"$@"
src/build/$(PS_FONT_FAMILY)17Pitch.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(FONTASPECT_PROG) $(SETFONTMETAS_PROG)
	mkdir -p src/build
	$(FONTASPECT) --aspect 0.606060606060 "$<" -o "$@"
	$(SETFONTMETAS) \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) 17 Pitch/' \
		--full-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) 17 Pitch/' \
		--ps-name 's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)17Pitch/' \
		"$@"

# Stage 4: make weights
dist/ttf/%.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETFONTMETAS_PROG)
	$(EXPANDSTROKES) -x 96 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETFONTMETAS) \
		--ps-weight "Medium" \
		--os2-weight 400 \
		"$@"
	bin/fontfix "$@"
dist/ttf/%-SemiLight.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETFONTMETAS_PROG)
	$(EXPANDSTROKES) -x 72 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETFONTMETAS) \
		--full-name '+ Semi-Light' \
		--ps-name '+-SemiLight' \
		--ps-weight "Semi-Light" \
		--os2-weight 350 \
		--panose _,_,4,_,_,_,_,_,_,_ \
		"$@"
	bin/fontfix "$@"
dist/ttf/%-Light.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETFONTMETAS_PROG)
	$(EXPANDSTROKES) -x 48 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETFONTMETAS) \
		--full-name '+ Light' \
		--ps-name '+-Light' \
		--ps-weight "Light" \
		--os2-weight 300 \
		--panose _,_,3,_,_,_,_,_,_,_ \
		"$@"
	bin/fontfix "$@"

# Stage 5: make code variants
# NOTE: can't use %.ttf because % cannot match zero characters.
dist/ttf/$(PS_FONT_FAMILY)Code%ttf: dist/ttf/$(PS_FONT_FAMILY)%ttf Makefile $(SETFONTMETAS_PROG)
	pyftfeatfreeze -f code "$<" "$@" # -U "" because we do that later
	bin/fontfix "$@"
	$(SETFONTMETAS) \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Code/' \
		--full-name   's/$(FONT_FAMILY)/$(FONT_FAMILY) Code/' \
		--ps-name     's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)Code/' \
		"$@"
	bin/fontfix "$@"

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
	find . -type f \( \
		-name '*.tmp' -o \
		-name '*.tmp.*' -o \
		-name '*.featfreeze.otf' -o \
		-name '*~' -o \
		-name '#*#' \
	\) -exec rm {} + || true
	/bin/rm -fr src/build || true

.PHONY: FORCE

# resetting DisplaySize: ___ doesn't break
# resetting Weight: Regular breaks
