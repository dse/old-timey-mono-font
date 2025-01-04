MAKEFILE := Makefile
FONT_SRC := src/ReproTypewr.sfd

FONT_FAMILY := Repro Typewr
PS_FONT_FAMILY := ReproTypewr

IMPORTSVG_PROG     := bin/importsvg
FONTUNREF_PROG     := bin/fontunref
EXPANDSTROKES_PROG := bin/expandstrokes
FONTASPECT_PROG    := bin/fontaspect
SETFONTMETAS_PROG  := bin/setfontmetas
SETRTMETAS_PROG    := bin/setrtmetas

OPT_VERBOSE :=

IMPORTSVG     := $(IMPORTSVG_PROG)
FONTUNREF     := $(FONTUNREF_PROG)
EXPANDSTROKES := $(EXPANDSTROKES_PROG)
FONTASPECT    := $(FONTASPECT_PROG)
SETFONTMETAS  := $(SETFONTMETAS_PROG)
SETRTMETAS    := $(SETRTMETAS_PROG)

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

CHARGRID_TPL	:= website/chargrid.mustache
CHARGRID_HTML	:= website/chargrid.html
CHARLIST_TPL	:= website/charlist.mustache
CHARLIST_HTML	:= website/charlist.html

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
FONTTOOL__LIGHT		:= --expand-stroke 72 # --translate-y -12  --scale-y 1344 --scale-y-from 1320  --scale-x 1008 --scale-x-from 984
FONTTOOL__THIN		:= --expand-stroke 48 # --translate-y -24  --scale-y 1344 --scale-y-from 1296  --scale-x 1008 --scale-x-from 960

FONTTOOL__COND		:= --aspect 0.833333 # 12cpi
FONTTOOL__COMP		:= --aspect 0.606060 # 16.5cpi

default: $(FONTS) $(CHARGRID_HTML) $(CHARLIST_HTML)
fonts: $(FONTS)
original: $(ORIGINAL_FONTS)
coding: $(CODING_FONTS)
compressed: $(COMP_FONTS)
condensed: $(COND_FONTS)
zip: $(ZIP_FILE)

.SUFFIXES: .sfd .ttf

# update source font fron SVG files
testfonts: FORCE
	make fonts FONT_FAMILY="RT$(TIMESTAMP)" \
	           PS_FONT_FAMILY="RT$(TIMESTAMP)" \
	           DISTDIR="test-dist/RT$(TIMESTAMP)"
	ln -n -f -s "RT$(TIMESTAMP)" test-dist/latest
update: FORCE
	$(IMPORTSVG) $(FONT_SRC) `find src/chars \! \( -type d -name \*italic\* -prune \) \! \( -type d -name greek-lc -prune \) -type f -name '*.svg'`
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
src/build/$(PS_FONT_FAMILY).stage1.sfd: $(FONT_SRC) Makefile $(IMPORTSVG_PROG) $(SETRTMETAS_PROG)
	mkdir -p src/build
	$(IMPORTSVG) "$<" -o "$@" src/chars/*.svg

# Stage 2: unroll references
src/build/$(PS_FONT_FAMILY).stage2.sfd: src/build/$(PS_FONT_FAMILY).stage1.sfd Makefile $(FONTUNREF_PROG)
	mkdir -p src/build
	$(FONTUNREF) "$<" -o "$@"

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
# NOTE: can't use %.ttf because % cannot match zero characters.
$(DISTDIR)/ttf/$(PS_FONT_FAMILY)Code%ttf: $(DISTDIR)/ttf/$(PS_FONT_FAMILY)%ttf Makefile $(SETRTMETAS_PROG)
	pyftfeatfreeze -f code "$<" "$@" # -U "" because we do that later
	bin/fontfix "$@"
	$(SETRTMETAS) "$@"

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
