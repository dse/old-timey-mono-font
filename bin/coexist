#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
#
# coexist - warn about any glyphs containing references AND contours -
# something that's not supported very well.

import fontforge
import argparse
import os
sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import parse_glyph_svg_filename
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename')
    parser.add_argument('svg_filenames', nargs='+')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    font = fontforge.open(args.font_filename)
    for svg_filename in args.svg_filenames:
        (codepoint, glyphname, real_codepoint, plain_glyphname) = parse_glyph_svg_filename(svg_filename)
        if codepoint is None and glyphname is None:
            print("INFO: coexist %s: %s: will not use" % (args.font_filename, svg_filename))
            continue
        if glyphname not in font:
            print("INFO: coexist %s: %s: will be new glyph" % (args.font_filename, svg_filename))
            continue
        glyph = font[glyphname]
        ref_count = len(glyph.references)
        contour_count = len(glyph.foreground)
        if ref_count and contour_count:
            print("WARN: coexist %s: %s: existing glyph has %d refs and %d contours" %
                  (args.font_filename, svg_filename, ref_count, contour_count))

main()
