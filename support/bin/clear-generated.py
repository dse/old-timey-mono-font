#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse

U2500_BOX_DRAWING             = range(0x2500, 0x2580)
U2580_BLOCK_ELEMENTS          = range(0x2580, 0x25a0)
U2800_BRAILLE                 = range(0x2800, 0x2900)
U1FBF0_BLOCK_SEXTANTS         = range(0x1fb00, 0x1fb3c)
U1FB3C_MOSAICS                = range(0x1fb3c, 0x1fb70)
U1FB9A_TRIANGULAR_HALF_BLOCKS = range(0x1fb9a, 0x1fb9c)
U1FBF0_SEGMENTED_DIGITS       = range(0x1fbf0, 0x1fbfa)

ALL = (
    U2500_BOX_DRAWING +
    U2580_BLOCK_ELEMENTS +
    U2800_BRAILLE +
    U1FBF0_BLOCK_SEXTANTS +
    U1FB3C_MOSAICS +
    U1FB9A_TRIANGULAR_HALF_BLOCKS +
    U1FBF0_SEGMENTED_DIGITS +
    []
)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for code in ALL:
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
