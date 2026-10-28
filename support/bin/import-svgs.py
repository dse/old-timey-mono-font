#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import get_font_glyph_width
from otm.index import index_svg_files, index_glyphs, verify

args = None

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--width", "--glyph-width", type=int, default=1008)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    svg_filenames = glob.glob("src/upright/**/*.svg", recursive=True)

    svg_list, svg_dict = index_svg_files()
    glyph_list, glyph_dict = index_glyphs(font)

    if args.verify:
        success = verify(svg_list, svg_dict, glyph_list, glyph_dict)
        if not success:
            raise Exception("verify found an issue")

    if len(glyph_list) == 0:
        new_glyph_width = args.width
    else:
        new_glyph_width = get_font_glyph_width(font)

    glyphs_data = json.loads(open("src/data/glyphs.json").read())
    references_data = json.loads(open("src/data/references.json").read())

    for svg_filename, glyphname, _, code, variant in svg_list:
        if code < 0:
            glyph_entry = glyph_dict.get(glyphname)
            svg_entry = svg_dict.get(glyphname)
        else:
            glyph_entry = glyph_dict.get((code,variant))
            svg_entry = svg_dict.get((code,variant))
        (svg_filename, *_) = svg_entry
        if glyph_entry is None:
            glyph = font.createChar(code, glyphname)
        else:
            (*_, glyph) = glyph_entry

        import_glyphs = [glyph]
        if code == 0xfffd:      # U+FFFD REPLACEMENT CHARACTER
            import_glyphs.append(font.createChar(-1, ".notdef"))

        for glyph in import_glyphs:
            if args.verbose:
                print(f'{svg_filename}: importing into glyph {glyph.glyphname}')
            glyph.references = tuple()   # in case replacing reference glyph with contour glyph
            glyph.foreground = fontforge.layer()
            font.strokedfont = True # avoid expanding strokes to stroke-widths in SVG
            glyph.importOutlines(svg_filename)
            font.strokedfont = False
            glyph.width = new_glyph_width
            if args.verbose >= 2:
                print(f'{svg_filename}: finished importing into glyph {glyph.glyphname}')

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
