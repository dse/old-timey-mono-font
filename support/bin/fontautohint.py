#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse
parser = argparse.ArgumentParser()
parser.add_argument('filenames', nargs='+')
parser.add_argument('--verbose', '-v', action='count', default=0)
args = parser.parse_args()
for filename in args.filenames:
    font = fontforge.open(filename)
    for glyph in font.glyphs():
        glyph.autoHint()
        font.gasp_version = 1
        font.gasp = (
            (10, ('antialias','symmetric-smoothing',),),
            (65535, ('antialias','symmetric-smoothing','gridfit','gridfit+smoothing',),),
        )
    if filename.endswith(".sfd"):
        font.save(filename)
    else:
        font.generate(filename)
    font.close()
