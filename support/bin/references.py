#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import json
import psMat

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="font filename")
    parser.add_argument('json_filename', help="json references file")
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    args = parser.parse_args()
    references = json.loads(open(args.json_filename).read())
    print("%s" % type(references))

    font = fontforge.open(args.filename)

    for glyph_name, dest_char in references.items():

        if type(dest_char) == str:
            if len(dest_char) == 1:
                dest_codepoint = ord(dest_char)
                dest_glyph_name = fontforge.nameFromUnicode(dest_codepoint)
            else:
                dest_codepoint = fontforge.unicodeFromName(dest_char)
                dest_glyph_name = dest_char
        else:
            raise Exception("unsupported reference value: %s" % repr(dest_char))

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
