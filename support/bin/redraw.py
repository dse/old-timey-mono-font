#!/usr/bin/env fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import json
import re

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import reconstitute_references
from my_font_utils import parse_glyph_svg_filename
from my_font_utils import create_smol_glyph
from my_font_utils import check_all_glyph_bounds

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext

sys.path.append(os.getenv("HOME") + "/git/dse.d/pyfontutils/lib")
from font_utils import u

DEFAULT_WIDTH = 1008
STROKE_WIDTH_BASIS = 96
LATIN_SMALL_LETTER_SCHWA = 0x0259

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('svg_filenames', nargs='+', help="svg characters")
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.verbose:
        print("redraw.py: %s: opening" % args.font_filename)
    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    for svg_filename in args.svg_filenames:
        import_svg_glyph(font, svg_filename, args.width)

    if write_font_filename.endswith('.sfd'):
        if args.verbose:
            print("redraw.py: %s: saving" % write_font_filename)
        font.save(write_font_filename)
    else:
        if args.verbose:
            print("redraw.py: %s: generating" % write_font_filename)
        font.generate(write_font_filename)
    font.close()

# FIXME: if allow_json_data is True, allow a ".svg" to override.
def import_svg_glyph(font, svg_filename, width, allow_json_data=False):
    global args

    font_path = os.path.relpath(font.path)
    (codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width) = parse_glyph_svg_filename(svg_filename)
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

    if args.verbose:
        print("redraw.py: %s: %s (%s): creating" % (svg_filename, glyphname, u(glyph.unicode)))
    glyph = font.createChar(codepoint, glyphname)
    glyph.foreground = fontforge.layer()
    if width is None:
        orig_width = glyph.width
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
