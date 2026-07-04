#!/usr/bin/env fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, unicodedata

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        if glyph.glyphname == ".notdef":
            continue
        if len(glyph.foreground) >= 1:
            continue
        if len(glyph.references) == 0:
            continue
        if glyph.unicode < 0x00a0 or glyph.unicode >= 0x2000:
            continue
        combining_mark_count = get_combining_mark_count(glyph)
        if combining_mark_count == 0:
            continue
        print("%s" % glyph.glyphname)
        print("    %s" % repr(glyph.references))
        glyph.build()
        print("    %s" % repr(glyph.references))
        base_glyph_name = glyph.glyphname.split(".")[0]
        base_codepoint = fontforge.unicodeFromName(base_glyph_name)
        uplus = "U+%04X" % base_codepoint if base_codepoint >= 0 else str(base_codepoint)
        # print("%2d  %-8s  %s" % (combining_mark_count, uplus, glyph.glyphname))
        # print("%2s  %-8s  %s" % ("", "", get_constituent_glyph_list(glyph)))
    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def get_combining_mark_count(glyph):
    if len(glyph.foreground) >= 1 and glyph.unicode in range(0x0300, 0x0370):
        return 1
    if len(glyph.references) == 0:
        return 0
    refnames = [ref[0] for ref in glyph.references]
    glyphs   = [glyph.font[name] for name in refnames]
    return sum([get_combining_mark_count(glyph) for glyph in glyphs])

def get_constituent_glyph_list(glyph):
    if len(glyph.references) == 0:
        return [glyph]
    glyph_list = []
    refnames = [ref[0] for ref in glyph.references]
    glyphs   = [glyph.font[name] for name in refnames]
    for sub_glyph in glyphs:
        glyph_list += get_constituent_glyph_list(sub_glyph)
    return glyph_list


main()
