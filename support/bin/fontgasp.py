#!/usr/bin/env fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import os
import fontforge
import argparse
def main():
    global args
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    for filename in args.filenames:
        font = fontforge.open(filename)
        for glyph in font.glyphs():
            glyph.dhints = tuple()
            glyph.hhints = tuple()
            glyph.vhints = tuple()
            glyph.manualHints = True
        font.gasp_version = 1
        font.gasp = (
            (65535, ('antialias',          'symmetric-smoothing',                    ),),
        )
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)
        font.close()
main()
