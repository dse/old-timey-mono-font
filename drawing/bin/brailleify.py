#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/../scripts/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import draw_dot, get_font_glyph_width, remove_glyphs, initialize_glyphs, finalize_glyphs, save_font
from otm.constants import KAPPA

RANGES = [
    range(0x2800,0x2900)
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
        remove_glyphs(font, RANGES, args)
        save_font(font, args)
        return
                
    new_glyph_width = get_font_glyph_width(font)
    x_radius = new_glyph_width / 8
    y_radius = font.em / 16
    radius = round(math.sqrt(x_radius * y_radius))

    xc_a = round(new_glyph_width * 1/4)
    xc_b = round(new_glyph_width * 3/4)
    yc_a = round(font.em * 7/8 - font.descent)
    yc_b = round(font.em * 5/8 - font.descent)
    yc_c = round(font.em * 3/8 - font.descent)
    yc_d = round(font.em * 1/8 - font.descent)

    center = {}
    center["1"] = (xc_a, yc_a)
    center["2"] = (xc_a, yc_b)
    center["3"] = (xc_a, yc_c)
    center["4"] = (xc_b, yc_a)
    center["5"] = (xc_b, yc_b)
    center["6"] = (xc_b, yc_c)
    center["7"] = (xc_a, yc_d)
    center["8"] = (xc_b, yc_d)
    
    initialize_glyphs(font, RANGES, args, new_glyph_width)

    glyph = font.createChar(0x2800) # BRAILLE PATTERN BLANK
    glyph.width = new_glyph_width
    glyph.foreground = fontforge.layer()

    for code in range(0x2801, 0x2900):
        glyph = font.createChar(code)
        glyph.width = new_glyph_width
        glyph.foreground = fontforge.layer()
        dots = unicodedata.name(chr(code)).removeprefix("BRAILLE PATTERN DOTS-")
        for dot in dots:
            draw_dot(glyph, center[dot], radius)

    finalize_glyphs(font, RANGES, args)
    save_font(font, args)

    font.close()

main()
