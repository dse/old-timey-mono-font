#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_chars import UNICODE
from my_font_utils import create_smol_glyph

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
    for codepoint in [*range(33, 127),
                      UNICODE["LATIN_SMALL_LETTER_SCHWA"],
                      UNICODE["GREEK_SMALL_LETTER_BETA"],
                      UNICODE["GREEK_SMALL_LETTER_GAMMA"],
                      UNICODE["GREEK_SMALL_LETTER_RHO"],
                      UNICODE["GREEK_SMALL_LETTER_PHI"],
                      UNICODE["GREEK_SMALL_LETTER_CHI"]]:
        create_smol_glyph(font, codepoint)

    print("Writing %s" % write_font_filename)
    if write_font_filename.endswith('.sfd'):
        font.save(write_font_filename)
    else:
        font.generate(write_font_filename)
    font.close()

main()
