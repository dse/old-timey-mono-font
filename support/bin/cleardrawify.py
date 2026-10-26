#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse

BOX_DRAWING                            = range(0x2500, 0x2580)
BLOCK_ELEMENTS                         = range(0x2580, 0x25a0)
SYMBOLS_FOR_LEGACY_COMPUTING_PORTION_1 = range(0x1fb00, 0x1fb70)
BRAILLE                                = range(0x2800, 0x2900)
SEGMENTED_DIGITS                       = range(0x1fbf0, 0x1fbfa)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for r in [BOX_DRAWING,
              BLOCK_ELEMENTS,
              SYMBOLS_FOR_LEGACY_COMPUTING_PORTION_1,
              SEGMENTED_DIGITS,
              BRAILLE]:
        for code in r:
            try:
                font.removeGlyph(code)
            except ValueError as e:
                if str(e) != "This glyph is not in the font":
                    raise
    if args.filename.endswith(".sfd"):
        font.save(filename)
    else:
        font.generate(filename)
    font.close()

main()
