#!/usr/bin/env fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, unicodedata

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    glyphs_with_references = []
    glyphs_with_contours   = []
    for glyph in font.glyphs():
        if glyph.glyphname == ".notdef":
            continue
        reference_count = len(glyph.references)
        contour_count   = len(glyph.foreground)
        if reference_count >= 1 and contour_count >= 1:
            print("WARNING: %s (%s) has both contours and references; skipping"
                  % (glyph.glyphname, "U+%04X" % glyph.unicode if glyph.unicode >= 0 else str(glyph.unicode)))
            continue
        if reference_count >= 1:
            glyphs_with_references.append(glyph)
        if contour_count >= 1:
            glyphs_with_contours.append(glyph)
    for glyph in glyphs_with_references:
        refs = glyph.references
        glyphs = get_constituent_glyphs(glyph)
        if len(glyphs) < 2:
            continue
        for glyph in glyphs:
            base_codepoint = glyph.unicode if glyph.unicode >= 0 else fontforge.unicodeFromName(glyph.glyphname.split(".")[0])
            print("U+%04X" % base_codepoint if base_codepoint >= 0 else "-1")

def get_constituent_glyphs(glyph):
    if len(glyph.foreground) > 0:
        return [glyph]
    if len(glyph.references) == 0:
        return []
    names = []
    for ref in glyph.references:
        ref_glyph_name = ref[0]
        ref_glyph = glyph.font[ref_glyph_name]
        names += get_constituent_glyphs(ref_glyph)
    return names

main()
