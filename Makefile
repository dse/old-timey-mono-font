MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONT_FAMILY := Repro Typewr
PS_FONT_FAMILY := ReproTypewr

SVG_PY_PROG		:= bin/svg.py
STROKES_PY_PROG	:= bin/strokes.py
ASPECT_PY_PROG		:= bin/aspect.py
METAS_PY_PROG		:= bin/metas.py
NOTDEF_PY_PROG		:= bin/notdef.py
SMOL_PY_PROG		:= bin/smol.py
BOUNDS_PY_PROG		:= bin/bounds.py
SUPERSUB_PY_PROG	:= bin/supersub.py
UNDERLINE_PY_PROG	:= bin/underline.py

METAS_PY_ARGS :=

OPT_VERBOSE :=

SVG_PY	:= $(SVG_PY_PROG)
STROKES_PY	:= $(STROKES_PY_PROG)
ASPECT_PY	:= $(ASPECT_PY_PROG)
METAS_PY	:= $(METAS_PY_PROG) $(METAS_PY_ARGS)
NOTDEF_PY	:= $(NOTDEF_PY_PROG)
SMOL_PY		:= $(SMOL_PY_PROG)
BOUNDS_PY	:= $(BOUNDS_PY_PROG)
SUPERSUB_PY	:= $(SUPERSUB_PY_PROG)
UNDERLINE_PY	:= $(UNDERLINE_PY_PROG)

DISTDIR := dist

FONT_TTF                        := $(DISTDIR)/ttf/$(PS_FONT_FAMILY).ttf
CODING_FONT_TTF                 := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code.ttf
THIN_FONT_TTF                   := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)-Thin.ttf
THIN_CODING_FONT_TTF            := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code-Thin.ttf
LIGHT_FONT_TTF                  := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)-Light.ttf
LIGHT_CODING_FONT_TTF           := $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code-Light.ttf
FONT_COMP_TTF			:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp.ttf
CODING_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeComp.ttf
THIN_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp-Thin.ttf
THIN_CODING_FONT_COMP_TTF	:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeComp-Thin.ttf
LIGHT_FONT_COMP_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Comp-Light.ttf
LIGHT_CODING_FONT_COMP_TTF	:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeComp-Light.ttf
FONT_COND_TTF			:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond.ttf
CODING_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeCond.ttf
THIN_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond-Thin.ttf
THIN_CODING_FONT_COND_TTF	:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeCond-Thin.ttf
LIGHT_FONT_COND_TTF		:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)Cond-Light.ttf
LIGHT_CODING_FONT_COND_TTF	:= $(DISTDIR)/ttf/$(PS_FONT_FAMILY)CodeCond-Light.ttf

TIMESTAMP := $(shell date +%m%d%H%M%S)

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

ZIP_FILE = dist/ReproTypewr.zip

FONTS := $(ORIGINAL_FONTS) $(CODING_FONTS)

FONTTOOL__REGULAR	:= --expand-stroke 96
FONTTOOL__LIGHT		:= --expand-stroke 72
FONTTOOL__THIN		:= --expand-stroke 48

FONTTOOL__COND		:= --aspect 0.833333 # 12cpi
FONTTOOL__COMP		:= --aspect 0.606060 # 16.5cpi

default: $(FONTS) website
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

testfonts: FORCE
	make fonts FONT_FAMILY="RT$(TIMESTAMP)" \
	           METAS_PY_ARGS="--ffn='ReproTypewr $(TIMESTAMP)' --psfn='ReproTypewr$(TIMESTAMP)'" \
	           PS_FONT_FAMILY="RT$(TIMESTAMP)" \
	           DISTDIR="test-dist/RT$(TIMESTAMP)"
	ln -n -f -s "RT$(TIMESTAMP)" test-dist/latest

# update source font fron SVG files
update: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --log --expand-stroke 96 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	sort -n strokes.log | sponge strokes.log

# update source font fron SVG files, for testing if referenced glyphs
# are too close. (accented letters mostly)
update-168: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --log --expand-stroke 168 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	sort -n strokes.log | sponge strokes.log
update-24: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --log --expand-stroke 24 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	sort -n strokes.log | sponge strokes.log
update-48: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --log --expand-stroke 48 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	sort -n strokes.log | sponge strokes.log
update-72: FORCE
	$(SVG_PY) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(SUPERSUB_PY) $(FONT_SRC)
	$(STROKES_PY) --log --expand-stroke 72 $(FONT_SRC)
	$(NOTDEF_PY) $(FONT_SRC)
	sort -n strokes.log | sponge strokes.log

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

$(ZIP_FILE): $(FONTS) Makefile
	( cd dist && zip -r ReproTypewr.zip ttf )

stage1: src/build/$(PS_FONT_FAMILY).stage1.sfd

# Stage 1: import SVGs
src/build/$(PS_FONT_FAMILY).stage1.sfd: $(FONT_SRC) $(SRC_SVGS) Makefile $(SVG_PY_PROG) $(BOUNDS_PY_PROG) $(SMOL_PY_PROG) $(SUPERSUB_PY_PROG)
	@echo "stage 1"
	mkdir -p src/build
	$(SVG_PY) "$<" -o "$@" $(SRC_SVGS)
	$(BOUNDS_PY) "$@"
	$(SMOL_PY) "$@"
	$(SUPERSUB_PY) "$@"

# Stage 2: does nothing
src/build/$(PS_FONT_FAMILY).stage2.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile
	@echo "stage 2"
	mkdir -p src/build
	cp "$<" "$@"

# Stage 3: make condensed and compressed outlines
src/build/$(PS_FONT_FAMILY)Cond.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 3"
	mkdir -p src/build
	$(ASPECT_PY) --aspect 0.833333333333 "$<" -o "$@"
src/build/$(PS_FONT_FAMILY)Comp.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(ASPECT_PY_PROG)
	@echo "stage 3"
	mkdir -p src/build
	$(ASPECT_PY) --aspect 0.606060606060 "$<" -o "$@"

# Stage 4: make weights
$(DISTDIR)/ttf/%.ttf: src/build/%.stage2.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 4"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 96 "$<" -o "$@"
	bin/fontfix "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 96 "$@"
$(DISTDIR)/ttf/%-Light.ttf: src/build/%.stage2.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 4"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 72 "$<" -o "$@"
	bin/fontfix "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 72 "$@"
$(DISTDIR)/ttf/%-Thin.ttf: src/build/%.stage2.sfd Makefile $(STROKES_PY_PROG) $(METAS_PY_PROG) $(UNDERLINE_PY_PROG)
	@echo "stage 4"
	mkdir -p "$(DISTDIR)/ttf"
	$(STROKES_PY) -x 48 "$<" -o "$@"
	bin/fontfix "$@"
	$(METAS_PY) "$@"
	$(UNDERLINE_PY) -102 48 "$@"

# Stage 5: make code variants
# NOTE: can't use %.ttf because '%' cannot match less than one character.
#                                   vvvv
$(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code%ttf: $(DISTDIR)/ttf/$(PS_FONT_FAMILY)%ttf Makefile $(METAS_PY_PROG) bin/fontfix
	@echo "stage 5"
	pyftfeatfreeze -f code "$<" "$@"
	bin/fontfix "$@"
	$(METAS_PY) "$@"

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
	/bin/rm -fr $(GLYPH_DATA_BY_TYPE) $(GLYPH_DATA_BY_BLOCK) $(GLYPH_DATA_BY_CHAR) \
	            $(GLYPH_HTML_BY_TYPE) $(GLYPH_HTML_BY_BLOCK) $(GLYPH_HTML_BY_CHAR) || true

diffs.txt: FORCE
	fontcmp ./ReproTypewr-0.5.0.sfd src/ReproTypewr.sfd > diffs.txt

todo.txt: FORCE
	fontcoverage --missing --no-ligatures $(FONT_SRC) | tee "$@"

CHARGRID_TPL		:= website/chargrid.mustache
CHARGRID_HTML		:= website/chargrid.html
CHARLIST_TPL		:= website/charlist.mustache
CHARLIST_HTML		:= website/charlist.html
GLYPH_DATA_BY_TYPE	:= data/glyph-data-by-type.json
GLYPH_DATA_BY_BLOCK	:= data/glyph-data-by-block.json
GLYPH_DATA_BY_CHAR	:= data/glyph-data-by-char.json
GLYPH_HTML_BY_TYPE	:= website/glyphs-by-type.html
GLYPH_HTML_BY_BLOCK	:= website/glyphs-by-block.html
GLYPH_HTML_BY_CHAR	:= website/glyphs-by-char.html
TEMPLATE_BY_TYPE	:= website/glyphs-by-type.mustache
TEMPLATE_BY_BLOCK	:= website/glyphs-by-block.mustache
TEMPLATE_BY_CHAR	:= website/glyphs-by-char.mustache
GLYPHSDATA_BIN		:= bin/glyphsdata
GLYPH_DATA		:= $(GLYPH_DATA_BY_TYPE) $(GLYPH_DATA_BY_BLOCK) $(GLYPH_DATA_BY_CHAR)
GLYPH_HTML		:= $(GLYPH_HTML_BY_TYPE) $(GLYPH_HTML_BY_BLOCK) $(GLYPH_HTML_BY_CHAR)

website: copy-fonts $(GLYPH_DATA) $(GLYPH_HTML) $(CHARGRID_HTML) $(CHARLIST_HTML)

html: $(GLYPH_DATA) $(GLYPH_HTML) $(CHARGRID_HTML) $(CHARLIST_HTML)

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

$(GLYPH_DATA_BY_CHAR): $(FONT_SRC) $(GLYPHSDATA_BIN)
	$(GLYPHSDATA_BIN) "$<" >"$@.tmp"
	mv "$@.tmp" "$@"
$(GLYPH_DATA_BY_TYPE): $(FONT_SRC) $(GLYPHSDATA_BIN)
	$(GLYPHSDATA_BIN) --by-type "$<" >"$@.tmp"
	mv "$@.tmp" "$@"
$(GLYPH_DATA_BY_BLOCK): $(FONT_SRC) $(GLYPHSDATA_BIN)
	$(GLYPHSDATA_BIN) --by-block "$<" >"$@.tmp"
	mv "$@.tmp" "$@"
$(GLYPH_HTML_BY_TYPE): $(GLYPH_DATA_BY_TYPE) $(TEMPLATE_BY_TYPE)
	chevron -d $(GLYPH_DATA_BY_TYPE) $(TEMPLATE_BY_TYPE) > "$@.tmp"
	mv "$@.tmp" "$@"
$(GLYPH_HTML_BY_BLOCK): $(GLYPH_DATA_BY_BLOCK) $(TEMPLATE_BY_BLOCK)
	chevron -d $(GLYPH_DATA_BY_BLOCK) $(TEMPLATE_BY_BLOCK) > "$@.tmp"
	mv "$@.tmp" "$@"
$(GLYPH_HTML_BY_CHAR): $(GLYPH_DATA_BY_CHAR) $(TEMPLATE_BY_CHAR)
	chevron -d $(GLYPH_DATA_BY_CHAR) $(TEMPLATE_BY_CHAR) > "$@.tmp"
	mv "$@.tmp" "$@"

copy-fonts: FORCE
	rsync -av dist/ttf website/fonts/

.PHONY: FORCE

# resetting DisplaySize: ___ doesn't break
# resetting Weight: Regular breaks
