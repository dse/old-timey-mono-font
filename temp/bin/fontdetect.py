#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import argparse
import fontforge

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('fudge', action='store_true')
    args = parser.parse_args()
    for filename in filenames:
        font = fontforge.open(filename)
        fontdetect(font, filename)
        font.close()

def fontdetect(font, filename):
    global args

    # find characters that go above the top and/or
    # below the bottom.
    top = font.ascent
    bottom = -font.descent
    if args.fudge:
        top += font.em / 4
        bottom -= font.em / 4
    for glyph in font.glyphs():
        (xmin, ymin, xmax, ymax) = glyph.boundingBox();
        if ymin < bottom:
            print("fontdetect: %s: bounding box bottom too low: %d < %d" % (filename, bottom, -font.descent))
        if ymax > top:
            print("fontdetect: %s: bounding box top too high: %d > %d" % (filename, top, font.ascent))

main()
