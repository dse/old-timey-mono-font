#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import draw_rect, draw_rel_rect, get_font_glyph_width

RANGES = [
    range(0x1fb00, 0x1fb3c),
]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-c", "--clear", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    if args.clear:
        for r in RANGES:
            for code in r:
                try:
                    font.removeGlyph(code)
                except ValueError as e:
                    if str(e) != "This glyph is not in the font":
                        raise
        return
                
    new_glyph_width = get_font_glyph_width(font)

    for r in RANGES:
        for code in r:
            glyph = font.createChar(code)
            glyph.foreground = fontforge.layer()
            glyph.width = new_glyph_width

    draw_block_sextant(font.createChar(0x1FB00))
    draw_block_sextant(font.createChar(0x1FB01))
    draw_block_sextant(font.createChar(0x1FB02))
    draw_block_sextant(font.createChar(0x1FB03))
    draw_block_sextant(font.createChar(0x1FB04))
    draw_block_sextant(font.createChar(0x1FB05))
    draw_block_sextant(font.createChar(0x1FB06))
    draw_block_sextant(font.createChar(0x1FB07))
    draw_block_sextant(font.createChar(0x1FB08))
    draw_block_sextant(font.createChar(0x1FB09))
    draw_block_sextant(font.createChar(0x1FB0A))
    draw_block_sextant(font.createChar(0x1FB0B))
    draw_block_sextant(font.createChar(0x1FB0C))
    draw_block_sextant(font.createChar(0x1FB0D))
    draw_block_sextant(font.createChar(0x1FB0E))
    draw_block_sextant(font.createChar(0x1FB0F))
    draw_block_sextant(font.createChar(0x1FB10))
    draw_block_sextant(font.createChar(0x1FB11))
    draw_block_sextant(font.createChar(0x1FB12))
    draw_block_sextant(font.createChar(0x1FB13))
    draw_block_sextant(font.createChar(0x1FB14))
    draw_block_sextant(font.createChar(0x1FB15))
    draw_block_sextant(font.createChar(0x1FB16))
    draw_block_sextant(font.createChar(0x1FB17))
    draw_block_sextant(font.createChar(0x1FB18))
    draw_block_sextant(font.createChar(0x1FB19))
    draw_block_sextant(font.createChar(0x1FB1A))
    draw_block_sextant(font.createChar(0x1FB1B))
    draw_block_sextant(font.createChar(0x1FB1C))
    draw_block_sextant(font.createChar(0x1FB1D))
    draw_block_sextant(font.createChar(0x1FB1E))
    draw_block_sextant(font.createChar(0x1FB1F))
    draw_block_sextant(font.createChar(0x1FB20))
    draw_block_sextant(font.createChar(0x1FB21))
    draw_block_sextant(font.createChar(0x1FB22))
    draw_block_sextant(font.createChar(0x1FB23))
    draw_block_sextant(font.createChar(0x1FB24))
    draw_block_sextant(font.createChar(0x1FB25))
    draw_block_sextant(font.createChar(0x1FB26))
    draw_block_sextant(font.createChar(0x1FB27))
    draw_block_sextant(font.createChar(0x1FB28))
    draw_block_sextant(font.createChar(0x1FB29))
    draw_block_sextant(font.createChar(0x1FB2A))
    draw_block_sextant(font.createChar(0x1FB2B))
    draw_block_sextant(font.createChar(0x1FB2C))
    draw_block_sextant(font.createChar(0x1FB2D))
    draw_block_sextant(font.createChar(0x1FB2E))
    draw_block_sextant(font.createChar(0x1FB2F))
    draw_block_sextant(font.createChar(0x1FB30))
    draw_block_sextant(font.createChar(0x1FB31))
    draw_block_sextant(font.createChar(0x1FB32))
    draw_block_sextant(font.createChar(0x1FB33))
    draw_block_sextant(font.createChar(0x1FB34))
    draw_block_sextant(font.createChar(0x1FB35))
    draw_block_sextant(font.createChar(0x1FB36))
    draw_block_sextant(font.createChar(0x1FB37))
    draw_block_sextant(font.createChar(0x1FB38))
    draw_block_sextant(font.createChar(0x1FB39))
    draw_block_sextant(font.createChar(0x1FB3A))
    draw_block_sextant(font.createChar(0x1FB3B))

    for r in RANGES:
        for code in r:
            glyph = font.createChar(code)
            glyph.removeOverlap()
            glyph.simplify()

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

def draw_block_sextant(glyph):
    code = glyph.unicode
    if code < 0:
        glyph = fontforge.unicodeFromName(glyph.glyphname.split(".", 1)[0])
    if code < 0:
        return
    parts = unicodedata.name(chr(code)).removeprefix("BLOCK SEXTANT-")
    for part in parts:
        if   part == "1": draw_rel_rect(glyph, 0, 2/3, 1/2, 1)
        elif part == "2": draw_rel_rect(glyph, 1/2, 2/3, 1, 1)
        elif part == "3": draw_rel_rect(glyph, 0, 1/3, 1/2, 2/3)
        elif part == "4": draw_rel_rect(glyph, 1/2, 1/3, 1, 2/3)
        elif part == "5": draw_rel_rect(glyph, 0, 0, 1/2, 1/3)
        elif part == "6": draw_rel_rect(glyph, 1/2, 0, 1, 1/3)

def draw_upper_left_sextant(glyph):   draw_rel_rect(glyph, 0, 2/3, 0.5, 1)
def draw_upper_right_sextant(glyph):  draw_rel_rect(glyph, 0.5, 2/3, 1, 1)
def draw_middle_left_sextant(glyph):  draw_rel_rect(glyph, 0, 1/3, 0.5, 2/3)
def draw_middle_right_sextant(glyph): draw_rel_rect(glyph, 0.5, 1/3, 1, 2/3)
def draw_lower_left_sextant(glyph):   draw_rel_rect(glyph, 0, 0, 0.5, 1/3)
def draw_lower_right_sextant(glyph):  draw_rel_rect(glyph, 0.5, 0, 1, 1/3)
def draw_upper_third(glyph):          draw_rel_rect(glyph, 0, 2/3, 1, 1)
def draw_middle_third(glyph):         draw_rel_rect(glyph, 0, 1/3, 1, 2/3)
def draw_lower_third(glyph):          draw_rel_rect(glyph, 0, 0, 1, 1/3)

main()

