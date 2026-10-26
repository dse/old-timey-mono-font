#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, math, os, unicodedata

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("json_filename")
    args = parser.parse_args()

    data = json.load(open(args.json_filename, "r"))

    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        glyph.references = ()
