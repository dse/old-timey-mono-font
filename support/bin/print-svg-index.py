#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, sys, re, json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.index import index_svg_filenames
from otm.util import walk_svg

DEFAULT_WIDTH = 1008
DEFAULT_STROKE_WIDTH = 96

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('svg_filenames', nargs='*')
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    if len(args.svg_filenames):
        svg_filenames = walk_svg(args.svg_filenames)
    else:
        svg_filenames = walk_svg(["src/upright"])
    if not len(svg_filenames):
        raise Exception("no SVGs to import")

    index_svg_filenames(svg_filenames, verbose=True)

main()
