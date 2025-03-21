#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import reconstitute_references
from my_font_utils import import_svg_glyph
from my_font_utils import create_smol_glyph
from my_font_utils import check_all_glyph_bounds

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext

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

    print("svg.py %s: Opening and reading..." % args.font_filename)
    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    print("svg.py %s: Importing glyphs...")
    for svg_filename in args.svg_filenames:
        import_svg_glyph(font, svg_filename, args.width)

    if write_font_filename.endswith('.sfd'):
        print("svg.py %s: Saving... %s" % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        print("svg.py %s: Generating... %s" % (args.font_filename, write_font_filename))
        font.generate(write_font_filename)
    font.close()

main()
