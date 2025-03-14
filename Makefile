MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONT_FAMILY := Repro Typewr
PS_FONT_FAMILY := ReproTypewr

IMPORTSVG_PROG		:= bin/importsvg
EXPANDSTROKES_PROG	:= bin/expandstrokes
FONTASPECT_PROG		:= bin/fontaspect
SETRTMETAS_PROG		:= bin/setrtmetas
FONTNOTDEF_PROG		:= bin/fontnotdef
SMOL_PY_PROG		:= bin/smol.py
BOUNDS_PY_PROG		:= bin/bounds.py
FRACSUPERSUB_PROG	:= bin/fracsupersub

SETRTMETAS_ARGS :=

OPT_VERBOSE :=

IMPORTSVG	:= $(IMPORTSVG_PROG)
EXPANDSTROKES	:= $(EXPANDSTROKES_PROG)
FONTASPECT	:= $(FONTASPECT_PROG)
SETRTMETAS	:= $(SETRTMETAS_PROG) $(SETRTMETAS_ARGS)
FONTNOTDEF	:= $(FONTNOTDEF_PROG)
SMOL_PY		:= $(SMOL_PY_PROG)
BOUNDS_PY	:= $(BOUNDS_PY_PROG)
FRACSUPERSUB	:= $(FRACSUPERSUB_PROG)

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

SRC_SVGS := `find src/chars -type f -name '*.svg'`

.SUFFIXES: .sfd .ttf

testfonts: FORCE
	make fonts FONT_FAMILY="RT$(TIMESTAMP)" \
	           SETRTMETAS_ARGS="--ffn='ReproTypewr $(TIMESTAMP)' --psfn='ReproTypewr$(TIMESTAMP)'" \
	           PS_FONT_FAMILY="RT$(TIMESTAMP)" \
	           DISTDIR="test-dist/RT$(TIMESTAMP)"
	ln -n -f -s "RT$(TIMESTAMP)" test-dist/latest

# update source font fron SVG files
update: FORCE
	$(IMPORTSVG) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(FRACSUPERSUB) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(EXPANDSTROKES) --expand-stroke 96 $(FONT_SRC)
	$(FONTNOTDEF) $(FONT_SRC)

# update source font fron SVG files, for testing if referenced glyphs
# are too close. (accented letters mostly)
update2: FORCE
	$(IMPORTSVG) $(FONT_SRC) $(SRC_SVGS)
	$(BOUNDS_PY) $(FONT_SRC)
	$(FRACSUPERSUB) $(FONT_SRC)
	$(SMOL_PY) $(FONT_SRC)
	$(EXPANDSTROKES) --expand-stroke 168 $(FONT_SRC)
	$(FONTNOTDEF) $(FONT_SRC)

fonttool: FORCE
	echo "use 'make update', dingus." >&2
	false
fontsvg: FORCE
	echo "use 'make update', dingus." >&2
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
src/build/$(PS_FONT_FAMILY).stage1.sfd: $(FONT_SRC) Makefile $(IMPORTSVG_PROG)
	mkdir -p src/build
	$(IMPORTSVG) "$<" -o "$@" $(SRC_SVGS)

# Stage 2: unroll references
src/build/$(PS_FONT_FAMILY).stage2.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile
	mkdir -p src/build
	cp "$<" "$@"

# Stage 3: make condensed and compressed outlines
src/build/$(PS_FONT_FAMILY)Cond.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(FONTASPECT_PROG)
	mkdir -p src/build
	$(FONTASPECT) --aspect 0.833333333333 "$<" -o "$@"
src/build/$(PS_FONT_FAMILY)Comp.stage2.sfd: src/build/$(PS_FONT_FAMILY).stage2.sfd Makefile $(FONTASPECT_PROG)
	mkdir -p src/build
	$(FONTASPECT) --aspect 0.606060606060 "$<" -o "$@"

# Stage 4: make weights
$(DISTDIR)/ttf/%.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETRTMETAS_PROG)
	mkdir -p "$(DISTDIR)/ttf"
	$(EXPANDSTROKES) -x 96 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETRTMETAS) "$@"
$(DISTDIR)/ttf/%-Light.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETRTMETAS_PROG)
	mkdir -p "$(DISTDIR)/ttf"
	$(EXPANDSTROKES) -x 72 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETRTMETAS) "$@"
$(DISTDIR)/ttf/%-Thin.ttf: src/build/%.stage2.sfd Makefile $(EXPANDSTROKES_PROG) $(SETRTMETAS_PROG)
	mkdir -p "$(DISTDIR)/ttf"
	$(EXPANDSTROKES) -x 48 "$<" -o "$@"
	bin/fontfix "$@"
	$(SETRTMETAS) "$@"

# Stage 5: make code variants
# NOTE: can't use %.ttf because '%' cannot match less than one character.
#                                   vvvv
$(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code%ttf: $(DISTDIR)/ttf/$(PS_FONT_FAMILY)%ttf Makefile $(SETRTMETAS_PROG)
	pyftfeatfreeze -f code "$<" "$@"
	bin/fontfix "$@"
	$(SETRTMETAS) "$@"


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
	( wgl4.py --missing $(FONT_SRC) ; aglfn.py --missing $(FONT_SRC) ) | grep -F 'U+' | sort | uniq >"$@"

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
