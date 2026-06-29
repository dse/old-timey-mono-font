#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import check_all_glyph_bounds

DEFAULT_WIDTH = 1008

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.verbose:
        print("bounds.py: %s: Opening and reading..." % args.font_filename)
    font = fontforge.open(args.font_filename)

    if args.verbose:
        print("bounds.py: %s: Checking glyph bounds..." % args.font_filename)
    check_all_glyph_bounds(font, args.width)

    font.close()

main()
