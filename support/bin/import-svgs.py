#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, sys, re, json, unicodedata, statistics

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.index import index_svg_filenames, index_glyphs, verify_glyphs
from otm.util import walk_svg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("svg_filenames", nargs="*")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    if len(args.svg_filenames):
        svg_filenames = walk_svg(args.svg_filenames)
    else:
        svg_filenames = walk_svg(["src/upright"])
    if not len(svg_filenames):
        raise Exception("no SVGs to import")

    font = fontforge.open(args.filename)

    # dicts are indexed by normalized glyph name
    svg_list, _ = index_svg_filenames(svg_filenames)

    widths = [glyph.width for glyph in font.glyphs()]
    widths.sort()
    glyph_width = round(statistics.median(widths))

    for item in svg_list:
        glyph = font.createChar(item.code, item.name)
        if len(glyph.references):
            if len(glyph.foreground):
                raise Exception(f"glyph {glyph.glyphname} contains both contours AND references")
            else:
                glyph.references = ()
        glyph.foreground = fontforge.layer()

        font.strokedfont = True # avoid auto-expanding SVG paths
        glyph.importOutlines(item.svg_filename)
        font.strokedfont = False
        glyph.width = glyph_width
        glyph.comment = "imported from " + item.svg_filename

    for glyph in font.glyphs():
        if glyph.glyphname.startswith("periodcentered"):
            glyphs1 = [g for g in font.glyphs() if g.encoding == glyph.encoding]
            glyphs2 = [g for g in font.glyphs() if g.originalgid == glyph.originalgid]
        
    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
