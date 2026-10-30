#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json, unicodedata

DEFAULT_STROKE_WIDTH = 96
SMOL_STROKE_WIDTH = 72

CODES = [
    *range(32, 127),
    unicodedata.lookup("LATIN_SMALL_LETTER_SCHWA"),
    unicodedata.lookup("GREEK_SMALL_LETTER_BETA"),
    unicodedata.lookup("GREEK_SMALL_LETTER_GAMMA"),
    unicodedata.lookup("GREEK_SMALL_LETTER_RHO"),
    unicodedata.lookup("GREEK_SMALL_LETTER_PHI"),
    unicodedata.lookup("GREEK_SMALL_LETTER_CHI"),
]

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
    "a": "a.ss04",
    "c": "c.ss04",
    "e": "e.ss04",
    "s": "s.ss04",

# code brackets
    "parenleft": "parenleft.WIDE",
    "parenright": "parenright.WIDE",
    "bracketleft": "bracketleft.WIDE",
    "bracketright": "bracketright.WIDE",
    "braceleft": "braceleft.WIDE",
    "braceright": "braceright.WIDE"

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
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    widths = [glyph.width for glyph in font.glyphs()]
    widths.sort()
    glyph_width = statistics.median(widths)

    smol_glyphnames = [glyph.glyphname for glyph in font.glyphs() if glyph.glyphname.endswith(".SMOL")]
    for glyphname in smol_glyphnames:
        font.removeGlyph(glyphname)

    for code in CODES:
        plain_glyphname = fontforge.nameFromUnicode(code)
        source_glyphname = fontforge.nameFromUnicode(code)
        if source_glyphname in SPECIAL_GLYPHS:
            source_glyphname = SPECIAL_GLYPHS[source_glyphname]
        source_glyph = font.createChar(code)

        smol_glyph = font.createChar(-1, plain_glyphname + ".SMOL")
        smol_glyph.foreground = fontforge.layer()
        smol_glyph.references = ()
        pen = smol_glyph.glyphPen()
        source_glyph.draw(pen)
        pen = None

        sm_glyph.transform(psMat.scale(0.5))
        sm_glyph.transform(psMat.translate(source_glyph.width / 4, SMOL_STROKE_WIDTH / 2 - DEFAULT_STROKE_WIDTH / 4))
        sm_glyph.width = glyph_width

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

main()
