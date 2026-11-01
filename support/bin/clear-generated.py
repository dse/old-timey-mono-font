#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.generated import GENERATED_GLYPH_CODES

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for code in GENERATED_GLYPH_CODES:
        try:
            font.removeGlyph(code)
        except ValueError as e:
            if str(e) != "This glyph is not in the font":
                raise
    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
