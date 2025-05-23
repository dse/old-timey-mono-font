MAKEFILE := Makefile
FONT_SRC := src/OldTimeyMono.sfd

#                XXX.YZZ, typically
SFNT_REVISION := 000.902
VERSION       := 0.9.2

FONT_FAMILY		= Old Timey Mono
PS_FONT_FAMILY		= OldTimeyMono
CODE_FONT_FAMILY	= Old Timey Code
PS_CODE_FONT_FAMILY	= OldTimeyCode

SVG_PY_PROG			:= bin/svg.py
STROKES_PY_PROG			:= bin/strokes.py
ASPECT_PY_PROG			:= bin/aspect.py
METAS_PY_PROG			:= bin/metas.py
NOTDEF_PY_PROG			:= bin/notdef.py
SMOL_PY_PROG			:= bin/smol.py
BOUNDS_PY_PROG			:= bin/bounds.py
SUPERSUB_PY_PROG		:= bin/supersub.py
UNDERLINE_PY_PROG		:= bin/underline.py
NOTREADY_PY_PROG		:= bin/notready.py
SETSUBSTITUTIONS_PY_PROG	:= bin/setsubstitutions.py
FONTAUTOHINT_PY_PROG		:= bin/fontautohint.py
FONTUNHINT_PY_PROG		:= bin/fontunhint.py

METAS_PY_ARGS      := --ffn='$(FONT_FAMILY)' --psfn='$(PS_FONT_FAMILY)'
METAS_PY_CODE_ARGS := --ffn='$(CODE_FONT_FAMILY)' --psfn='$(PS_CODE_FONT_FAMILY)'

OPT_VERBOSE :=

SVG_PY			:= $(SVG_PY_PROG)
STROKES_PY		:= $(STROKES_PY_PROG)
ASPECT_PY		:= $(ASPECT_PY_PROG)
METAS_PY		:= $(METAS_PY_PROG) $(METAS_PY_ARGS)
METAS_PY_CODE		:= $(METAS_PY_PROG) $(METAS_PY_CODE_ARGS)
NOTDEF_PY		:= $(NOTDEF_PY_PROG)
SMOL_PY			:= $(SMOL_PY_PROG)
BOUNDS_PY		:= $(BOUNDS_PY_PROG)
SUPERSUB_PY		:= $(SUPERSUB_PY_PROG)
UNDERLINE_PY		:= $(UNDERLINE_PY_PROG)
NOTREADY_PY		:= $(NOTREADY_PY_PROG)
SETSUBSTITUTIONS_PY	:= $(SETSUBSTITUTIONS_PY_PROG)
FONTAUTOHINT_PY		:= $(FONTAUTOHINT_PY_PROG)
FONTUNHINT_PY		:= $(FONTUNHINT_PY_PROG)

SUBSTITUTIONS_JSON	:= data/substitutions.json

DISTDIR := dist

FONT_TTF                        := $(DISTDIR)/ttf/$(PS_FONT_FAMILY).ttf
CODING_FONT_TTF                 := $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY).ttf
THIN_FONT_TTF                   := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)-Thin.ttf
THIN_CODING_FONT_TTF            := $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)-Thin.ttf
LIGHT_FONT_TTF                  := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)-Light.ttf
LIGHT_CODING_FONT_TTF           := $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)-Light.ttf
FONT_COMP_TTF			:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp.ttf
CODING_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Comp.ttf
THIN_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp-Thin.ttf
THIN_CODING_FONT_COMP_TTF	:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Comp-Thin.ttf
LIGHT_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp-Light.ttf
LIGHT_CODING_FONT_COMP_TTF	:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Comp-Light.ttf
FONT_COND_TTF			:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond.ttf
CODING_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Cond.ttf
THIN_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond-Thin.ttf
THIN_CODING_FONT_COND_TTF	:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Cond-Thin.ttf
LIGHT_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond-Light.ttf
LIGHT_CODING_FONT_COND_TTF	:= $(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)Cond-Light.ttf

ORIGINAL_FONTS := \
	$(FONT_TTF) \
	$(THIN_FONT_TTF) \
	$(LIGHT_FONT_TTF) \
	$(FONT_COMP_TTF) \
	$(THIN_FONT_COMP_TTF) \
	$(LIGHT_FONT_COMP_TTF) \
	$(FONT_COND_TTF) \
	$(THIN_FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) 

CODING_FONTS := \
	$(CODING_FONT_TTF) \
	$(THIN_CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(CODING_FONT_COMP_TTF) \
	$(THIN_CODING_FONT_COMP_TTF) \
	$(LIGHT_CODING_FONT_COMP_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(THIN_CODING_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF)

COMP_FONTS := \
	$(FONT_COMP_TTF) \
	$(CODING_FONT_COMP_TTF) \
	$(THIN_FONT_COMP_TTF) \
	$(THIN_CODING_FONT_COMP_TTF) \
	$(LIGHT_FONT_COMP_TTF) \
	$(LIGHT_CODING_FONT_COMP_TTF)

COND_FONTS := \
	$(FONT_COND_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(THIN_FONT_COND_TTF) \
	$(THIN_CODING_FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF)

ZIP_FILE = dist/OldTimeyMono.zip

FONTS := $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTTOOL__REGULAR	:= --expand-stroke 96
FONTTOOL__LIGHT		:= --expand-stroke 72
FONTTOOL__THIN		:= --expand-stroke 48

FONTTOOL__COND		:= --aspect 0.833333 # 12cpi
FONTTOOL__COMP		:= --aspect 0.606060 # 16.5cpi

default: $(FONTS)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
compressed: $(COMP_FONTS)
condensed: $(COND_FONTS)
zip: $(ZIP_FILE)

SRC_SVGS := $(shell find src/chars -type f -name '*.svg')

.SUFFIXES: .sfd .ttf

testfontsweb: FORCE
	rm -fr website/fonts/ttf/*
	make fonts DISTDIR="website/fonts"

TESTFONTS_DIR := testfonts

testfonts: FORCE
	$(eval BUILD_NR := $(shell bin/buildnr.py))
	$(eval DISTDIR_NAME := $(PS_FONT_FAMILY)$(BUILD_NR))
	mkdir -p $(TESTFONTS_DIR)
	make fonts \
		FONT_FAMILY="$(FONT_FAMILY) $(BUILD_NR)" \
		PS_FONT_FAMILY="$(PS_FONT_FAMILY)$(BUILD_NR)" \
		CODE_FONT_FAMILY="$(CODE_FONT_FAMILY) $(BUILD_NR)" \
		PS_CODE_FONT_FAMILY="$(PS_CODE_FONT_FAMILY)$(BUILD_NR)" \
		DISTDIR="$(TESTFONTS_DIR)/$(DISTDIR_NAME).tmp"
	mv "$(TESTFONTS_DIR)/$(DISTDIR_NAME).tmp" "$(TESTFONTS_DIR)/$(DISTDIR_NAME)"
	ln -n -f -s "$(DISTDIR_NAME)/ttf" $(TESTFONTS_DIR)/latest

# update source font fron SVG files
update: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 96 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log

update-test: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 96 --allow-json-data $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log

# update source font fron SVG files, for testing if referenced glyphs
# are too close. (accented letters mostly)
update-168: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 168 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log
update-24: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 24 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log
update-48: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 48 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log
update-72: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 72 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log
update-128: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --expand-stroke 128 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	$(FONTAUTOHINT_PY) $(FONT_SRC)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	make fix-strokes-log

fix-strokes-log:
	if test -e strokes.log ; then sort -n strokes.log | sponge strokes.log ; else true ; fi

fonttool: FORCE
	@echo "use 'make update', dingus." >&2
	false
fontsvg: FORCE
	@echo "use 'make update', dingus." >&2
	false

# generate braille characters
braille: FORCE
	fontbraille -W 200 -f $(FONT_SRC)

# generate box drawing characters
boxdraw: FORCE
	fontboxdraw -f $(FONT_SRC)

$(ZIP_FILE): $(FONTS) Makefile _zip

_zip: FORCE
	cd dist && \
		bsdtar -c -f "OldTimeyMono-$(VERSION).zip" \
		--format zip \
		-s '/^ttf/OldTimeyMono-$(VERSION)/' \
		ttf

unversionedzip: FORCE
	cp "dist/OldTimeyMono-$(VERSION).zip" "dist/OldTimeyMono.zip"

specimen: $(FONTS) Makefile _specimen

_specimen: FORCE
	rm -fr specimen/src/fonts/*.woff2 || true
	mkdir -p specimen/src/fonts
	for i in dist/ttf/*.ttf ; do woff2_compress "$$i" && mv "$${i%.ttf}.woff2" specimen/src/fonts ; done
	@echo "==============================================================================="
	@echo "You'll need to do the following manually:"
	@echo ""
	@echo "cd specimen && yarn build"
	@echo "==============================================================================="

stage1: src/build/$(PS_FONT_FAMILY).stage1.sfd

# Stage 1: import SVGs
src/build/$(PS_FONT_FAMILY).stage1.sfd: $(FONT_SRC) $(SRC_SVGS) Makefile $(SVG_PY_PROG) $(BOUNDS_PY_PROG) $(SMOL_PY_PROG) $(SUPERSUB_PY_PROG) $(NOTREADY_PY_PROG) $(SETSUBSTITUTIONS_PY_PROG) $(SUBSTITUTIONS_JSON)
	@echo "stage 1"
	mkdir -p src/build
	$(SVG_PY) "$<" -o "$@" $(SRC_SVGS)
	$(BOUNDS_PY) "$@"
	$(SMOL_PY) "$@"
	$(SUPERSUB_PY) "$@"
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(FONT_SRC)
	$(NOTREADY_PY) "$@"

# Stage 2: make condensed and compressed outlines
src/build/$(PS_FONT_FAMILY)Cond.stage1.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 2 condensed"
	mkdir -p src/build
	$(ASPECT_PY) --aspect 0.833333333333 "$<" -o "$@"
src/build/$(PS_FONT_FAMILY)Comp.stage1.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 2 compressed"
	mkdir -p src/build
	$(ASPECT_PY) --aspect 0.606060606060 "$<" -o "$@"

# Stage 3: make weights
$(DISTDIR)/ttf/%.ttf: src/build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 normal (weight)"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 96 "$<" -o "$@"
	bin/fontfix "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 96 "$@"
$(DISTDIR)/ttf/%-Light.ttf: src/build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 light"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 72 "$<" -o "$@"
	bin/fontfix "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 72 "$@"
$(DISTDIR)/ttf/%-Thin.ttf: src/build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 thin"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 48 "$<" -o "$@"
	bin/fontfix "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 48 "$@"

# Stage 4: make code variants
# NOTE: can't use %.ttf because '%' cannot match less than one character.
#                                   vvvv
$(DISTDIR)/ttf/$(PS_CODE_FONT_FAMILY)%ttf: $(DISTDIR)/ttf/$(PS_FONT_FAMILY)%ttf Makefile $(METAS_PY_PROG) bin/fontfix
	@echo "stage 4 code variant"
	pyftfeatfreeze -f ss01 "$<" "$@"
	bin/fontfix "$@"
	$(METAS_PY_CODE) "$@"

clean: FORCE
	/bin/rm $(FONTS) $(ZIP_FILE) || true
	/bin/rm specimen/src/fonts/*.woff2 || true
	find . -type f \( \
		-name '*.tmp' -o \
		-name '*.tmp.*' -o \
		-name '*.featfreeze.otf' -o \
		-name '*~' -o \
		-name '#*#' \
	\) -exec rm {} + || true
	/bin/rm -fr src/build || true

version: FORCE
	bin/version.py src/OldTimeyMono.sfd \
		--sfnt-revision "$(SFNT_REVISION)" \
		--ps-version "$(VERSION)"

publish:
	ssh dse@webonastick.com 'cd git/dse.d/fonts.d/old-timey-mono-font && git pull && cd specimen && yarn build'

.PHONY: FORCE
