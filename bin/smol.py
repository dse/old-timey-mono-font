#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import create_smol_glyph

LATIN_SMALL_LETTER_SCHWA = 0x0259

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('-o', '--save-as', '--output', type=str)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    print("Creating small glyphs...")
    for codepoint in [*range(33, 127), LATIN_SMALL_LETTER_SCHWA]:
        create_smol_glyph(font, codepoint)

    print("Writing %s" % write_font_filename)
    if write_font_filename.endswith('.sfd'):
        font.save(write_font_filename)
    else:
        font.generate(write_font_filename)
    font.close()

main()
