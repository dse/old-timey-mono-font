#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import json
import psMat

sys.path.append("%s/git/dse.d/pyfontutils/lib" % os.getenv("HOME"))
from font_utils import parse_char

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="font filename")
    parser.add_argument('json_filename', help="json references file")
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    references = json.loads(open(args.json_filename).read())
    print("%s" % type(references))

    font = fontforge.open(args.filename)

    for glyph_name, dest_char in references.items():
        dest_codepoint = parse_char(dest_char)[2]
        dest_glyph_name = fontforge.nameFromUnicode(dest_codepoint)

        if dest_char is None:
            if glyph_name in font:
                font.removeGlyph(glyph_name)
            continue

        dest_glyph = font[dest_glyph_name]

        if "." in glyph_name:
            glyph_codepoint = -1
        else:
            glyph_codepoint = fontforge.unicodeFromName(glyph_name)

        if glyph_name in font:
            glyph = font[glyph_name]
            if len(glyph.foreground):
                print("WARNING: %s is a contour glyph; not replacing")
                continue
        else:
            glyph = font.createChar(glyph_codepoint, glyph_name)
        glyph.references = ((dest_glyph_name, psMat.identity()),)
        glyph.width = dest_glyph.width

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
