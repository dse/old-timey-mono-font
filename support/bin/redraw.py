#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import json
import re
from os.path import basename

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import parse_glyph_svg_filename

sys.path.append(os.getenv("HOME") + "/git/dse.d/pyfontutils/lib")
from font_utils import u

sys.path.append(os.path.dirname(__file__) + "/../lib")
from otm.index import index_svg_files, index_glyphs

DEFAULT_WIDTH = 1008
STROKE_WIDTH_BASIS = 96

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="font filename")
    parser.add_argument('svg_filenames', nargs='*', help="svg characters")
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.svg_filenames is None or not len(args.svg_filenames):
        svg_filenames = glob("src/upright/**/*.svg")
    else:
        svg_filenames = args.svg_filenames

    font = fontforge.open(args.filename)

    svg_list, svg_dict = index_svg_files(svg_filenames)
    glyph_list, glyph_dict = index_glyphs(font)

    for svg_filename in args.svg_filenames:
        import_svg_glyph(font, svg_filename, args.width)

    if args.filename.endswith('.sfd'):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

# FIXME: if allow_json_data is True, allow a ".svg" to override.
def import_svg_glyph(font, svg_filename, width, allow_json_data=False):
    global args

    svg_base_filename = basename(svg_filename)

    font_path = os.path.relpath(font.path)
    parse_result = parse_glyph_svg_filename(svg_filename)
    (codepoint, glyphname, _, _, stroke_width) = parse_result
    if args.verbose:
        print("parse_glyph_svg_filename(%s) => %s" % (
            repr(svg_filename), repr(parse_result)
        ))
    if codepoint is None and glyphname is None:
        if args.verbose:
            print("redraw.py: %s: not importing" % svg_filename)
        return
    glyph = None
    if glyphname in font:
        glyph = font[glyphname]
        if len(glyph.references):
            if args.verbose:
                print("redraw.py: %s: %s (%s): has references; not redrawing" % (svg_filename, glyphname, u(glyph.unicode)))
            return

    glyph = font.createChar(codepoint, glyphname)
    if args.verbose:
        print("redraw.py: %s: %s (%s): clearing" % (svg_filename, glyphname, u(glyph.unicode)))
    glyph.foreground = fontforge.layer()
    if width is None:
        orig_width = glyph.width
    if args.verbose:
        print("redraw.py: %s: %s (%s): importing outline" % (svg_filename, glyphname, u(glyph.unicode)))
    if stroke_width is not None:
        font.strokedfont = True
        glyph.importOutlines(svg_filename, correctdir=True)
        font.strokedfont = False
    else:
        font.strokedfont = True
        glyph.importOutlines(svg_filename)
        font.strokedfont = False
    if width is None:
        glyph.width = orig_width
    else:
        glyph.width = width

main()
