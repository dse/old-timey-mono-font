#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json, psMat

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import get_font_glyph_width

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output-filename", type=str, nargs="?", default=None)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--aspect", "--width", type=float, default=5/6)
    args = parser.parse_args()
    font = fontforge.open(args.filename)

    new_glyph_width = get_font_glyph_width(font)

    for glyph in font.glyphs():
        glyph.transform(psMat.scale(args.aspect, 1), ("partialRefs",))
        glyph.width = new_glyph_width # transform sometimes narrows the advance width twice

        # if len(glyph.references):
        #     refs = list(glyph.references)
        #     for ref in glyph.references:
        #         ref = list(ref)
        #         ref[1] = psMat.compose(ref[1], psMat.scale(args.aspect, 1))
        #         ref = tuple(ref)
        #     glyph.references = tuple(refs)
        #     glyph.width = round(glyph.width * args.aspect)
        # else:
        #     glyph.transform(psMat.scale(args.aspect, 1))

    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')

    font.close()

def ranges_key_conv(key):
    if type(key) == float:
        return round(key)
    if type(key) == int:
        return key
    if len(key) == 1:
        return ord(key)
    if match := re.fullmatch(r'U\+([0-9a-f]{4,})', key, flags=re.I):
        return int(match[1], 16)
    raise Exception(f'invalid key in ranges: {key}')

main()
