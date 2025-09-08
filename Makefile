MAKEFILE			= Makefile
SRC_BASEFONT			= src/basefont
SUPPORT_BIN			= exec/bin
DIST_TTF			= dist/ttf
DIST_ZIP			= dist/zip
SRC_DATA			= src/data

BASEFONT_SFD			= $(SRC_BASEFONT)/$(PS_FONT_FAMILY).sfd

#                                 XXX.YZZ, typically
SFNT_REVISION			= 000.902
VERSION				= 0.9.2

FONT_FAMILY			= Old Timey Mono
PS_FONT_FAMILY			= OldTimeyMono
CODE_FONT_FAMILY		= Old Timey Code
PS_CODE_FONT_FAMILY		= OldTimeyCode

SVG_PY_PROG			= $(SUPPORT_BIN)/svg.py
STROKES_PY_PROG			= $(SUPPORT_BIN)/strokes.py
ASPECT_PY_PROG			= $(SUPPORT_BIN)/aspect.py
METAS_PY_PROG			= $(SUPPORT_BIN)/metas.py
NOTDEF_PY_PROG			= $(SUPPORT_BIN)/notdef.py
SMOL_PY_PROG			= $(SUPPORT_BIN)/smol.py
BOUNDS_PY_PROG			= $(SUPPORT_BIN)/bounds.py
SUPERSUB_PY_PROG		= $(SUPPORT_BIN)/supersub.py
UNDERLINE_PY_PROG		= $(SUPPORT_BIN)/underline.py
NOTREADY_PY_PROG		= $(SUPPORT_BIN)/notready.py
SETSUBSTITUTIONS_PY_PROG	= $(SUPPORT_BIN)/setsubstitutions.py
FONTAUTOHINT_PY_PROG		= $(SUPPORT_BIN)/fontautohint.py
FONTUNHINT_PY_PROG		= $(SUPPORT_BIN)/fontunhint.py
BUILDNR_PY_PROG			= $(SUPPORT_BIN)/buildnr.py
VERSION_PY_PROG			= $(SUPPORT_BIN)/version.py
FONTFIX_PY_PROG			= $(SUPPORT_BIN)/fontfix.py

METAS_PY_ARGS			= --ffn='$(FONT_FAMILY)' --psfn='$(PS_FONT_FAMILY)'
METAS_PY_CODE_ARGS		= --ffn='$(CODE_FONT_FAMILY)' --psfn='$(PS_CODE_FONT_FAMILY)'

SVG_PY				= $(SVG_PY_PROG)
STROKES_PY			= $(STROKES_PY_PROG)
ASPECT_PY			= $(ASPECT_PY_PROG)
METAS_PY			= $(METAS_PY_PROG) $(METAS_PY_ARGS)
METAS_PY_CODE			= $(METAS_PY_PROG) $(METAS_PY_CODE_ARGS)
NOTDEF_PY			= $(NOTDEF_PY_PROG)
SMOL_PY				= $(SMOL_PY_PROG)
BOUNDS_PY			= $(BOUNDS_PY_PROG)
SUPERSUB_PY			= $(SUPERSUB_PY_PROG)
UNDERLINE_PY			= $(UNDERLINE_PY_PROG)
NOTREADY_PY			= $(NOTREADY_PY_PROG)
SETSUBSTITUTIONS_PY		= $(SETSUBSTITUTIONS_PY_PROG)
FONTAUTOHINT_PY			= $(FONTAUTOHINT_PY_PROG)
FONTUNHINT_PY			= $(FONTUNHINT_PY_PROG)
BUILDNR_PY			= $(BUILDNR_PY_PROG)
VERSION_PY			= $(VERSION_PY_PROG)
FONTFIX_PY			= $(FONTFIX_PY_PROG)

SUBSTITUTIONS_JSON		= $(SRC_DATA)/substitutions.json

FONT_TTF			= $(DIST_TTF)/$(PS_FONT_FAMILY).ttf
CODING_FONT_TTF			= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY).ttf
THIN_FONT_TTF			= $(DIST_TTF)/$(PS_FONT_FAMILY)-Thin.ttf
THIN_CODING_FONT_TTF		= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)-Thin.ttf
LIGHT_FONT_TTF			= $(DIST_TTF)/$(PS_FONT_FAMILY)-Light.ttf
LIGHT_CODING_FONT_TTF		= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)-Light.ttf
FONT_COMP_TTF			= $(DIST_TTF)/$(PS_FONT_FAMILY)Comp.ttf
CODING_FONT_COMP_TTF		= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Comp.ttf
THIN_FONT_COMP_TTF		= $(DIST_TTF)/$(PS_FONT_FAMILY)Comp-Thin.ttf
THIN_CODING_FONT_COMP_TTF	= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Comp-Thin.ttf
LIGHT_FONT_COMP_TTF		= $(DIST_TTF)/$(PS_FONT_FAMILY)Comp-Light.ttf
LIGHT_CODING_FONT_COMP_TTF	= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Comp-Light.ttf
FONT_COND_TTF			= $(DIST_TTF)/$(PS_FONT_FAMILY)Cond.ttf
CODING_FONT_COND_TTF		= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Cond.ttf
THIN_FONT_COND_TTF		= $(DIST_TTF)/$(PS_FONT_FAMILY)Cond-Thin.ttf
THIN_CODING_FONT_COND_TTF	= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Cond-Thin.ttf
LIGHT_FONT_COND_TTF		= $(DIST_TTF)/$(PS_FONT_FAMILY)Cond-Light.ttf
LIGHT_CODING_FONT_COND_TTF	= $(DIST_TTF)/$(PS_CODE_FONT_FAMILY)Cond-Light.ttf

ORIGINAL_FONTS = \
	$(FONT_TTF) \
	$(THIN_FONT_TTF) \
	$(LIGHT_FONT_TTF) \
	$(FONT_COMP_TTF) \
	$(THIN_FONT_COMP_TTF) \
	$(LIGHT_FONT_COMP_TTF) \
	$(FONT_COND_TTF) \
	$(THIN_FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) 

CODING_FONTS = \
	$(CODING_FONT_TTF) \
	$(THIN_CODING_FONT_TTF) \
	$(LIGHT_CODING_FONT_TTF) \
	$(CODING_FONT_COMP_TTF) \
	$(THIN_CODING_FONT_COMP_TTF) \
	$(LIGHT_CODING_FONT_COMP_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(THIN_CODING_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF)

COMP_FONTS = \
	$(FONT_COMP_TTF) \
	$(CODING_FONT_COMP_TTF) \
	$(THIN_FONT_COMP_TTF) \
	$(THIN_CODING_FONT_COMP_TTF) \
	$(LIGHT_FONT_COMP_TTF) \
	$(LIGHT_CODING_FONT_COMP_TTF)

COND_FONTS = \
	$(FONT_COND_TTF) \
	$(CODING_FONT_COND_TTF) \
	$(THIN_FONT_COND_TTF) \
	$(THIN_CODING_FONT_COND_TTF) \
	$(LIGHT_FONT_COND_TTF) \
	$(LIGHT_CODING_FONT_COND_TTF)

ZIP_FILE			= $(DIST_ZIP)/$(PS_FONT_FAMILY).zip

FONTS				= $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTTOOL__REGULAR		= --expand-stroke 96
FONTTOOL__LIGHT			= --expand-stroke 72
FONTTOOL__THIN			= --expand-stroke 48

FONTTOOL__COND			= --aspect 0.833333 # 12cpi
FONTTOOL__COMP			= --aspect 0.606060 # 16.5cpi

default: $(FONTS)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
compressed: $(COMP_FONTS)
condensed: $(COND_FONTS)
zip: $(ZIP_FILE)

SRC_SVGS			= $(shell find src/vector -type f -name '*.svg')

.SUFFIXES: .sfd .ttf

testfontsweb: FORCE
	rm -fr website/fonts/ttf/*
	make fonts DISTDIR="website/fonts"

TESTFONTS_DIR			= tmp/testfonts

testfonts: FORCE
	$(eval BUILD_NR = $(shell $(BUILDNR_PY)))
	$(eval DISTDIR_NAME = $(PS_FONT_FAMILY)$(BUILD_NR))
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
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 96 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log

update-test: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 96 --allow-json-data $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log

# update source font fron SVG files, for testing if referenced glyphs
# are too close. (accented letters mostly)
update-168: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 168 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log
update-24: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 24 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log
update-48: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 48 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log
update-72: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 72 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	make fix-strokes-log
update-128: FORCE
	$(SVG_PY) $(BASEFONT_SFD) $(SRC_SVGS)
	$(BOUNDS_PY) $(BASEFONT_SFD)
	$(SMOL_PY) $(BASEFONT_SFD)
	$(SUPERSUB_PY) $(BASEFONT_SFD)
	$(STROKES_PY) --expand-stroke 128 $(BASEFONT_SFD)
	$(NOTDEF_PY) $(BASEFONT_SFD)
	$(FONTAUTOHINT_PY) $(BASEFONT_SFD)
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
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
	fontbraille -W 200 -f $(BASEFONT_SFD)

# generate box drawing characters
boxdraw: FORCE
	fontboxdraw -f $(BASEFONT_SFD)

$(ZIP_FILE): $(FONTS) Makefile _zip

_zip: FORCE
	cd $(DIST_ZIP) && \
		bsdtar -c -f "$(PS_FONT_FAMILY)-$(VERSION).zip" \
		--format zip \
		-s '#^\.\./ttf#$(PS_FONT_FAMILY)-$(VERSION)#' \
		../ttf

unversionedzip: FORCE
	cp "$(DIST_ZIP)/$(PS_FONT_FAMILY)-$(VERSION).zip" "$(DIST_ZIP)/$(PS_FONT_FAMILY).zip"

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

stage1: tmp/_build/$(PS_FONT_FAMILY).stage1.sfd

# Stage 1: import SVGs
tmp/_build/$(PS_FONT_FAMILY).stage1.sfd: $(BASEFONT_SFD) $(SRC_SVGS) Makefile $(SVG_PY_PROG) $(BOUNDS_PY_PROG) $(SMOL_PY_PROG) $(SUPERSUB_PY_PROG) $(NOTREADY_PY_PROG) $(SETSUBSTITUTIONS_PY_PROG) $(SUBSTITUTIONS_JSON)
	@echo "stage 1"
	mkdir -p tmp/_build
	$(SVG_PY) "$<" -o "$@" $(SRC_SVGS)
	$(BOUNDS_PY) "$@"
	$(SMOL_PY) "$@"
	$(SUPERSUB_PY) "$@"
	$(SETSUBSTITUTIONS_PY) $(SUBSTITUTIONS_JSON) $(BASEFONT_SFD)
	$(NOTREADY_PY) "$@"

# Stage 2: make condensed and compressed outlines
tmp/_build/$(PS_FONT_FAMILY)Cond.stage1.sfd: tmp/_build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 2 condensed"
	mkdir -p tmp/_build
	$(ASPECT_PY) --aspect 0.833333333333 "$<" -o "$@"
tmp/_build/$(PS_FONT_FAMILY)Comp.stage1.sfd: tmp/_build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 2 compressed"
	mkdir -p tmp/_build
	$(ASPECT_PY) --aspect 0.606060606060 "$<" -o "$@"

# Stage 3: make weights
$(DIST_TTF)/%.ttf: tmp/_build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 normal (weight)"
	mkdir -p "$(DIST_TTF)"
	$(STROKES_PY) -x 96 "$<" -o "$@"
	$(FONTFIX_PY) "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 96 "$@"
$(DIST_TTF)/%-Light.ttf: tmp/_build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 light"
	mkdir -p "$(DIST_TTF)"
	$(STROKES_PY) -x 72 "$<" -o "$@"
	$(FONTFIX_PY) "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 72 "$@"
$(DIST_TTF)/%-Thin.ttf: tmp/_build/%.stage1.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 3 thin"
	mkdir -p "$(DIST_TTF)"
	$(STROKES_PY) -x 48 "$<" -o "$@"
	$(FONTFIX_PY) "$@"
	$(FONTAUTOHINT_PY) "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 48 "$@"

# Stage 4: make code variants
# NOTE: can't use %.ttf because '%' cannot match less than one character.
#                                   vvvv
$(DIST_TTF)/$(PS_CODE_FONT_FAMILY)%ttf: $(DIST_TTF)/$(PS_FONT_FAMILY)%ttf Makefile $(METAS_PY_PROG) $(FONTFIX_PY_PROG)
	@echo "stage 4 code variant"
	pyftfeatfreeze -f ss01 "$<" "$@"
	$(FONTFIX_PY) "$@"
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
	/bin/rm -fr tmp/_build || true

version: FORCE
	$(VERSION_PY) $(BASEFONT_SFD) \
		--sfnt-revision "$(SFNT_REVISION)" \
		--ps-version "$(VERSION)"

publish:
	ssh dse@webonastick.com 'cd git/dse.d/fonts.d/old-timey-mono-font && git pull && cd specimen && yarn build'

.PHONY: FORCE
