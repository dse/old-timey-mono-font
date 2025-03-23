#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge
import argparse
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    print("notready.py: Opening %s" % args.filename)
    font = fontforge.open(args.filename)
    for codepoint in [
            *range(0x0250, 0x02b0), # IPA, not finished yet
            0x046c,                 # one of those "hm" lookin glyphs in Cyrillic
            0x046d,                 # the other one
    ]:
        if codepoint in font:
            print("notready.py: Removing %s" % fontforge.nameFromUnicode(codepoint))
            font.removeGlyph(codepoint)
    if args.filename.endswith('.sfd'):
        print("notready.py: Saving %s" % args.filename)
        font.save(args.filename)
    else:
        print("notready.py: Generating %s" % args.filename)
        font.generate(args.filename)
    font.close()
main()
