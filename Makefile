MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONT_FAMILY := Repro Typewr
PS_FONT_FAMILY := ReproTypewr

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
FONT_PICA_TTF                           := dist/ttf/$(PS_FONT_FAMILY)Pica.ttf
CODING_FONT_PICA_TTF                    := dist/ttf/$(PS_FONT_FAMILY)CodePica.ttf
LIGHT_FONT_PICA_TTF                     := dist/ttf/$(PS_FONT_FAMILY)Pica-Light.ttf
LIGHT_CODING_FONT_PICA_TTF              := dist/ttf/$(PS_FONT_FAMILY)CodePica-Light.ttf
SEMI_LIGHT_FONT_PICA_TTF                := dist/ttf/$(PS_FONT_FAMILY)Pica-SemiLight.ttf
SEMI_LIGHT_CODING_FONT_PICA_TTF         := dist/ttf/$(PS_FONT_FAMILY)CodePica-SemiLight.ttf

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
update: FORCE
	bin/importsvg $(FONT_SRC) `find src/chars -type f -name '*.svg'`
	bin/expandstrokes --expand-stroke 96 $(FONT_SRC)
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

# Stage 1: import SVGs and set basic metas
src/build/$(PS_FONT_FAMILY).stage1.sfd: src/$(PS_FONT_FAMILY).sfd Makefile bin/importsvg bin/setfontmetas
	mkdir -p src/build
	bin/importsvg "$<" -o "$@" src/chars/*.svg
	bin/setfontmetas -v \
		--family-name '$(FONT_FAMILY)' \
		--full-name '$(FONT_FAMILY)' \
		--ps-name '$(PS_FONT_FAMILY)' \
		--ps-weight 'Medium' \
		--os2-weight 400 \
		--panose 2,0,5,9,3,0,_,_,_,3 \
		"$@"

# Stage 2: unroll references
src/build/$(PS_FONT_FAMILY).stage2.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile bin/fontunref
	mkdir -p src/build
	bin/fontunref "$<" -o "$@"

# Stage 3: make Pica and 17Pitch outlines
src/build/$(PS_FONT_FAMILY)Pica.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile bin/fontaspect bin/setfontmetas
	mkdir -p src/build
	bin/fontaspect --aspect 0.833333333333 "$<" -o "$@"
	bin/setfontmetas -v \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Pica/' \
		--full-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Pica/' \
		--ps-name 's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)Pica/' \
		"$@"
src/build/$(PS_FONT_FAMILY)17Pitch.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile bin/fontaspect bin/setfontmetas
	mkdir -p src/build
	bin/fontaspect --aspect 0.606060606060 "$<" -o "$@"
	bin/setfontmetas -v \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) 17 Pitch/' \
		--full-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) 17 Pitch/' \
		--ps-name 's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)17Pitch/' \
		"$@"

# Stage 4: make weights
dist/ttf/%.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes bin/setfontmetas
	bin/expandstrokes -x 96 "$<" -o "$@"
	bin/setfontmetas -v \
		--ps-weight "Medium" \
		--os2-weight 400 \
		"$@"
dist/ttf/%-SemiLight.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes bin/setfontmetas
	bin/expandstrokes -x 72 "$<" -o "$@"
	bin/setfontmetas -v \
		--full-name '+ Semi-Light' \
		--ps-name '+-SemiLight' \
		--ps-weight "Semi-Light" \
		--os2-weight 350 \
		--panose _,_,4,_,_,_,_,_,_,_ \
		"$@"
dist/ttf/%-Light.ttf: src/build/%.stage2.sfd Makefile bin/expandstrokes bin/setfontmetas
	bin/expandstrokes -x 48 "$<" -o "$@"
	bin/setfontmetas -v \
		--full-name '+ Light' \
		--ps-name '+-Light' \
		--ps-weight "Light" \
		--os2-weight 300 \
		--panose _,_,3,_,_,_,_,_,_,_ \
		"$@"

# Stage 5: make code variants
# NOTE: can't use %.ttf because % cannot match zero characters.
dist/ttf/$(PS_FONT_FAMILY)Code%ttf: dist/ttf/$(PS_FONT_FAMILY)%ttf Makefile bin/setfontmetas
	pyftfeatfreeze -f code "$<" "$@" # -U "" because we do that later
	bin/setfontmetas -v \
		--family-name 's/$(FONT_FAMILY)/$(FONT_FAMILY) Code/' \
		--full-name   's/$(FONT_FAMILY)/$(FONT_FAMILY) Code/' \
		--ps-name     's/$(PS_FONT_FAMILY)/$(PS_FONT_FAMILY)Code/' \
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
