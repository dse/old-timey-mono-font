MAKEFILE = Makefile
FONTCONVERT = bin/fontconvert
FONT_SRC = src/ReproTypewr.sfd
FONT_TTF = dist/ttf/ReproTypewr.ttf

default: $(FONT_TTF)

dist/ttf/%.ttf: src/%.sfd $(FONTCONVERT) $(MAKEFILE)
	$(FONTCONVERT) "$<" "$@.tmp.ttf"
	mv "$@.tmp.ttf" "$@"
