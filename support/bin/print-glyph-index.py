#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge, argparse, glob, os, sys, re, json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))
from otm.index import index_glyphs
from otm.util import walk_svg

DEFAULT_WIDTH = 1008
DEFAULT_STROKE_WIDTH = 96

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    index_glyphs(font, verbose=True)

main()
