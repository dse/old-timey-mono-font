#!/usr/bin/env fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, unicodedata

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    notused = {}

    glyphs = list(font.glyphs())
    glyphs.sort(key = lambda glyph: glyph.unicode)

    for glyph in glyphs:
        if glyph.unicode in range(0x0300, 0x0370):
            notused[glyph.glyphname] = True
    for glyph in glyphs:
        if glyph.unicode in range(0x0300, 0x0370):
            continue
        for glyphname in get_constituent_glyph_names(glyph):
            notused[glyphname] = False
    for glyph in glyphs:
        if glyph.unicode in range(0x0300, 0x0370):
            if notused[glyph.glyphname]:
                print("Removing %s (%s %s)" % (glyph.glyphname,
                                               "U+%04X" % glyph.unicode if glyph.unicode >= 0 else str(glyph.unicode),
                                               unicodedata.name(chr(glyph.unicode))))
                font.removeGlyph(glyph)
    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def get_constituent_glyph_names(glyph):
    if len(glyph.references) == 0:
        return [glyph.glyphname]
    glyph_list = []
    refnames = [ref[0] for ref in glyph.references]
    glyphs   = [glyph.font[name] for name in refnames]
    for sub_glyph in glyphs:
        glyph_list += get_constituent_glyph_names(sub_glyph)
    return glyph_list

main()
