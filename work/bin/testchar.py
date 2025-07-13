#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import parse_codepoint_argument

def main():
    codepoints = []
    filenames = []
    for arg in sys.argv[1:]:
        if (codepoint := parse_codepoint_argument(arg)) is not None:
            codepoints.append(codepoint)
            print(codepoint)
        else:
            filenames.append(arg)
    if not len(codepoints):
        raise Exception("No codepoints specified")
    if len(filenames) < 2:
        raise Exception("No filenames or fewer than two specified")
    out_filename = filenames[0]
    in_filenames = filenames[1:]

    counter = 0

    out_font = fontforge.font()
    out_font.is_quadratic = True
    out_font.ascent = 1344
    out_font.descent = 336
    for filename in in_filenames:
        in_font = fontforge.open(filename)

        for codepoint in codepoints:
            glyphname = fontforge.nameFromUnicode(codepoint)
            if not glyphname in in_font:
                continue
            in_glyph = in_font[glyphname]

            counter += 1
            out_glyph = out_font.createChar(-1, "%s.%d" % (glyphname, counter))

            pen = out_glyph.glyphPen()
            in_glyph.draw(pen)
            pen = None
            out_glyph.width = in_glyph.width

        in_font.close()

    if out_filename.endswith(".sfd"):
        out_font.save(out_filename)
    else:
        font.generate(out_filename)

main()
