#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, sys, re, json, unicodedata, statistics

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.generated import SMOL_GLYPH_CODES

DEFAULT_STROKE_WIDTH = 96
SMOL_STROKE_WIDTH = 72

SPECIAL_GLYPHS = {
    "periodcentered": "periodcentered.ss05",
    # "onedotenleader": "onedotenleader.ss05",
    # "twodotenleader": "twodotenleader.ss05",
    # "ellipsis": "ellipsis.ss05",
    "quotesinglbase": "quotesinglbase.ss05",
    "quotereversed": "quotereversed.ss05",
    "quotedblbase": "quotedblbase.ss05",
    "uni201F": "uni201F.ss05",  # U+201F DOUBLE HIGH-REVERSED-9 QUOTATION MARK -- DOUBLE REVERSED COMMA QUOTATION MARK
    "uni2027": "uni2027.ss05",  # U+2027 HYPHENATION POINT
    "uni204F": "uni204F.ss05",  # U+204F REVERSED SEMICOLON
    "comma": "comma.ss05",
    "period": "period.ss05",
    "colon": "colon.ss05",
    "semicolon": "semicolon.ss05",
    "quoteleft": "quoteleft.ss05",
    "quoteright": "quoteright.ss05",
    "quotedblleft": "quotedblleft.ss05",
    "quotedblright": "quotedblright.ss05",
    "asciitilde": "asciitilde.cv14",

# spaced further apart
    "equal": "equal.cv11",
    "grave": "grave.cv09",

# aperture
    "a": "a.ss07",
    "c": "c.ss04",
    "e": "e.ss04",
    "s": "s.ss04",

# code brackets
    "parenleft": "parenleft.WIDE",
    "parenright": "parenright.WIDE",
    "bracketleft": "bracketleft.WIDE",
    "bracketright": "bracketright.WIDE",
    "braceleft": "braceleft.WIDE",
    "braceright": "braceright.WIDE",

# simplified forms
    "zero": "zero.ss07",
    "one": "one.ss07",
    "two": "two.ss07",
    "three": "three.ss07",
    "five": "five.ss07",
    "dollar": "dollar.ss07",
    "numbersign": "numbersign.ss07",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    widths = [glyph.width for glyph in font.glyphs()]
    widths.sort()
    glyph_width = statistics.median(widths)

    for code in SMOL_GLYPH_CODES:
        plain_glyphname = fontforge.nameFromUnicode(code)
        source_glyphname = plain_glyphname
        if source_glyphname in SPECIAL_GLYPHS:
            source_glyphname = SPECIAL_GLYPHS[source_glyphname]
        elif source_glyphname + ".ss07" in font:
            source_glyphname += ".ss07"
        smol_glyphname = plain_glyphname + ".SMOL"

        # print("generating %s from %s" % (smol_glyphname, source_glyphname))

        source_glyph = font[source_glyphname]

        smol_glyph = font.createChar(-1, smol_glyphname)
        smol_glyph.foreground = fontforge.layer()
        smol_glyph.references = ()
        pen = smol_glyph.glyphPen()
        source_glyph.draw(pen)
        pen = None

        # if len(smol_glyph.references):
        #     reconstitute_references(smol_glyph)
        #     smol_glyph.unlinkRef()

        smol_glyph.transform(psMat.scale(0.5))
        smol_glyph.transform(psMat.translate(source_glyph.width / 4, SMOL_STROKE_WIDTH / 2 - DEFAULT_STROKE_WIDTH / 4))
        smol_glyph.width = round(glyph_width)

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
