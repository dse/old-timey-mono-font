#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse
parser = argparse.ArgumentParser()
parser.add_argument('filenames', nargs='+')
args = parser.parse_args()
for filename in args.filenames:
    font = fontforge.open(filename)
    for glyph in font.glyphs():
        glyph.autoHint()
    if filename.endswith(".sfd"):
        font.save(filename)
    else:
        font.generate(filename)
    font.close()
