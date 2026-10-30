#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))
from otm.index import index_svg_filenames, index_glyphs, verify_glyphs

ITEM_CODE = 0
ITEM_VARIANT = 1
ITEM_ORIG_GLYPH_NAME = 2
ITEM_ORIG_BASE_GLYPH_NAME = 3
ITEM_NORM_GLYPH_NAME = 4
ITEM_NORM_BASE_GLYPH_NAME = 5
ITEM_FILENAME = 6
ITEM_GLYPH = 7

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("svg_filenames", nargs="+")
    args = parser.parse_args()

    svg_filenames = walk(args.svg_filenames)
    font = fontforge.open(args.filename)

    svg_list, svg_dict = index_svg_filenames(svg_filenames)
    glyph_list, glyph_dict = index_glyphs(font)

    # for item in svg_list:
    #     print(f"SVG:   {item[ITEM_NORM_GLYPH_NAME]} => {item}")
    # for item in glyph_list:
    #     print(f"GLYPH: {item[ITEM_NORM_GLYPH_NAME]} => {item}")

def walk(filenames):
    retval = []
    for filename in filenames:
        if os.path.isdir(filename):
            for dir_path, dir_names, dir_filenames in os.walk(filename):
                for each_filename in dir_filenames:
                    if each_filename.lower().endswith(".svg"):
                        retval.append(os.path.join(dir_path, each_filename))
        else:
            retval.append(filename)
    return retval

main()
