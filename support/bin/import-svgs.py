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
    args = parser.parse_args()

    if len(args.svg_filenames):
        svg_filenames = walk_svg(args.svg_filenames)
    else:
        svg_filenames = walk_svg(["src/upright"])
    if not len(svg_filenames):
        raise Exception("no SVGs to import")

    font = fontforge.open(args.filename)

    # dicts are indexed by normalized glyph name
    svg_list, svg_dict = index_svg_filenames(svg_filenames)
    glyph_list, glyph_dict = index_glyphs(font)

    (
        success, 
        verified_svg_list,
        verified_svg_dict,
        verified_glyph_list,
        verified_glyph_dict,
        svg_only_list,
        svg_only_dict,
        glyph_only_list,
        glyph_only_dict,
    ) = verify_glyphs(svg_list, svg_dict, glyph_list, glyph_dict)

    widths = [glyph.width for glyph in font.glyphs()]
    widths.sort()
    glyph_width = round(statistics.median(widths))

    for item in svg_list:
        if item.name_is_arbitrary:
            print(item.code)
            glyph = font.createChar(item.code, item.norm_glyph_name)
        else:
            print(item.code)
            glyph = font.createChar(item.code, item.norm_glyph_name)
        if len(glyph.references):
            if len(glyph.foreground):
                raise Exception(f"glyph {glyph.glyphname} contains both contours AND references")
            else:
                glyph.references = ()
        glyph.foreground = fontforge.layer()

        print(f"Importing {glyph.glyphname} from {item.svg_filename}")
        font.strokedfont = True # avoid auto-expanding SVG paths
        glyph.importOutlines(item.svg_filename)
        font.strokedfont = False
        glyph.width = glyph_width
        glyph.comment = "imported from " + item.svg_filename
        
    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
