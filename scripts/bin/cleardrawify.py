#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    for r in [
            range(0x2500, 0x2580),
            range(0x2500, 0x25a0),
            range(0x1fb3c, 0x1fb70),
            range(0x1fb00, 0x1fb3c),
            range(0x2800, 0x2900),
    ]:
        for code in r:
            try:
                font.removeGlyph(code)
            except ValueError as e:
                if str(e) != "This glyph is not in the font":
                    raise

    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')

    font.close()

main()
