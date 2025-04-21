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

    for glyph in font.glyphs():
        codepoint = glyph.unicode
        idx = glyph.glyphname.find(".")
        if codepoint < 0 and idx >= 0:
            base_glyphname = glyph.glyphname[0:idx]
            codepoint = fontforge.unicodeFromName(base_glyphname)
            if codepoint in [*range(0x0250, 0x0258), *range(0x0259, 0x02b0), 0x046c, 0x046d]:
                font.removeGlyph(glyph)
    if args.filename.endswith('.sfd'):
        print("notready.py: Saving %s" % args.filename)
        font.save(args.filename)
    else:
        print("notready.py: Generating %s" % args.filename)
        font.generate(args.filename)
    font.close()
main()
