#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import check_all_glyph_bounds

DEFAULT_WIDTH = 1008
LATIN_SMALL_LETTER_SCHWA = 0x0259

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('-o', '--save-as', '--output', type=str)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    print("bounds.py %s: Opening and reading..." % args.font_filename)
    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    print("bounds.py %s: Checking glyph bounds..." % args.font_filename)
    check_all_glyph_bounds(font, args.width)

    if write_font_filename.endswith('.sfd'):
        print("bounds.py %s: Saving %s..." % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        print("bounds.py %s: Generating %s..." % (args.font_filename, write_font_filename))
        font.generate(write_font_filename)
    font.close()

main()
