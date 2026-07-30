#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, statistics

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import draw_grid_shape

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    font = fontforge.open(args.filename)

    glyphs = list(font.glyphs())
    widths = [glyph.width for glyph in glyphs]
    widths.sort()
    median_width = statistics.median(widths)

    glyphs_having_median_width = [glyph for glyph in glyphs if abs(glyph.width - median_width) < median_width / 1000]
    if len(glyphs_having_median_width) / len(glyphs) < 0.95:
        raise Exception("not enough glyphs same width")

    width = round(median_width)

    draw_grid_shape(width, 2, 2, [[[0,0],[2,0],[2,2],[0,2],[1,1]]], codept=0x1fb68, font=font)
    draw_grid_shape(width, 2, 2, [[[0,0],[1,1],[2,0],[2,2],[0,2]]], codept=0x1fb69, font=font)
    draw_grid_shape(width, 2, 2, [[[0,0],[2,0],[1,1],[2,2],[0,2]]], codept=0x1fb6a, font=font)
    draw_grid_shape(width, 2, 2, [[[0,0],[2,0],[2,2],[1,1],[0,2]]], codept=0x1fb6b, font=font)
    draw_grid_shape(width, 2, 2, [[[0,0],[1,1],[0,2]]], codept=0x1fb6c, font=font)
    draw_grid_shape(width, 2, 2, [[[0,0],[2,0],[1,1]]], codept=0x1fb6d, font=font)
    draw_grid_shape(width, 2, 2, [[[2,0],[2,2],[1,1]]], codept=0x1fb6e, font=font)
    draw_grid_shape(width, 2, 2, [[[1,1],[2,2],[0,2]]], codept=0x1fb6f, font=font)

    if args.filename.endswith(".sfd"):
        font.save()
    else:
        font.generate()

main()
