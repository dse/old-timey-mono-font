#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os
def main():
    global args
    parser = argparse.ArgumentParser(description="remove hints from specified font(s)")
    parser.add_argument('filename', nargs='+')
    args = parser.parse_args()
    for filename in args.filename:
        font = fontforge.open(args.source_filename)
        for glyph in font.glyphs():
            # glyph.dhints = tuple()
            glyph.hhints = tuple()
            glyph.vhints = tuple()
            glyph.manualHints = True
            font.gasp_version = 1
            font.gasp = ((1, ('antialias',),),)
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename, flags=['no-hints','no-flex'])
        font.close()
