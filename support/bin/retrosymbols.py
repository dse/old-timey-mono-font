#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
#
# symbols.py - draw certain symbols from the SYMBOLS FOR LEGACY
# COMPUTING block.
#
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

    # one-eighth blocks
    draw_vertical_one_eighth_block(width, 1, font=font, codept=0x1fb70)
    draw_vertical_one_eighth_block(width, 2, font=font, codept=0x1fb71)
    draw_vertical_one_eighth_block(width, 3, font=font, codept=0x1fb72)
    draw_vertical_one_eighth_block(width, 4, font=font, codept=0x1fb73)
    draw_vertical_one_eighth_block(width, 5, font=font, codept=0x1fb74)
    draw_vertical_one_eighth_block(width, 6, font=font, codept=0x1fb75)
    draw_horizontal_one_eighth_block(width, 1, font=font, codept=0x1fb76)
    draw_horizontal_one_eighth_block(width, 2, font=font, codept=0x1fb77)
    draw_horizontal_one_eighth_block(width, 3, font=font, codept=0x1fb78)
    draw_horizontal_one_eighth_block(width, 4, font=font, codept=0x1fb79)
    draw_horizontal_one_eighth_block(width, 5, font=font, codept=0x1fb7a)
    draw_horizontal_one_eighth_block(width, 6, font=font, codept=0x1fb7b)

    # L-shaped one-eighth blocks
    draw_grid_shape(width, 8, 8, [[[0,0],[1,0],[1,7],[8,7],[8,8],[0,8]]], font=font, codept=0x1fb7c)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,1],[1,1],[1,8],[0,8]]], font=font, codept=0x1fb7d)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,8],[7,8],[7,1],[0,1]]], font=font, codept=0x1fb7e)
    draw_grid_shape(width, 8, 8, [[[7,0],[8,0],[8,8],[0,8],[0,7],[7,7]]], font=font, codept=0x1fb7f)

    # other one-eighth blocks
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,1],[0,1]],[[0,7],[8,7],[8,8],[0,8]]], font=font, codept=0x1fb80)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,1],[0,1]],[[0,2],[8,2],[8,3],[0,3]],[[0,4],[8,4],[8,5],[0,5]],[[0,7],[8,7],[8,8],[0,8]]], font=font, codept=0x1fb81)

    # additional block elements
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,2],[0,2]]], font=font, codept=0x1fb82)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,3],[0,3]]], font=font, codept=0x1fb83)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,5],[0,5]]], font=font, codept=0x1fb84)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,6],[0,6]]], font=font, codept=0x1fb85)
    draw_grid_shape(width, 8, 8, [[[0,0],[8,0],[8,7],[0,7]]], font=font, codept=0x1fb86)
    draw_grid_shape(width, 8, 8, [[[6,0],[8,0],[8,8],[6,8]]], font=font, codept=0x1fb87)
    draw_grid_shape(width, 8, 8, [[[5,0],[8,0],[8,8],[5,8]]], font=font, codept=0x1fb88)
    draw_grid_shape(width, 8, 8, [[[3,0],[8,0],[8,8],[3,8]]], font=font, codept=0x1fb89)
    draw_grid_shape(width, 8, 8, [[[2,0],[8,0],[8,8],[2,8]]], font=font, codept=0x1fb8a)
    draw_grid_shape(width, 8, 8, [[[1,0],[8,0],[8,8],[1,8]]], font=font, codept=0x1fb8b)

    # shade characters
    # draw_grid_shape(width, 2, 2, [[1/2,[0,0],[1,0],[1,2],[0,2]]], font=font, codept=0x1fb8c)
    # draw_grid_shape(width, 2, 2, [[1/2,[1,0],[2,0],[2,2],[1,2]]], font=font, codept=0x1fb8d)
    # draw_grid_shape(width, 2, 2, [[1/2,[0,0],[2,0],[2,1],[0,1]]], font=font, codept=0x1fb8e)
    # draw_grid_shape(width, 2, 2, [[1/2,[0,1],[2,1],[2,2],[0,2]]], font=font, codept=0x1fb8f)
    # draw_grid_shape(width, 2, 2, [[1/2,[0,0],[0,2],[2,2],[0.2]]], font=font, codept=0x1fb90)
    # draw_grid_shape(width, 2, 2, [[1,  [0,0],[2,0],[2,1],[0,1]],[1/2,[0,1],[2,1],[2,2],[0,2]]], font=font, codept=0x1fb91)
    # draw_grid_shape(width, 2, 2, [[1/2,[0,0],[2,0],[2,1],[0,1]],[1,  [0,1],[2,1],[2,2],[0,2]]], font=font, codept=0x1fb91)
    # draw_grid_shape(width, 2, 2, [[1/2,[0,0],[1,0],[1,2],[0,2]],[1,  [1,0],[2,0],[2,2],[1,2]]], font=font, codept=0x1fb94)

    # checkerboard fill
    draw_grid_shape(width, 4, 4, [[[0,0],[0,1],[1,1],[1,0]],[[2,0],[2,1],[3,1],[3,0]],
                                         [[0,2],[0,3],[1,3],[1,2]],[[2,2],[2,3],[3,3],[3,2]],
                                         [[1,1],[2,1],[2,2],[1,2]],[[3,1],[4,1],[4,2],[3,2]],
                                         [[1,3],[2,3],[2,4],[1,4]],[[3,3],[4,3],[4,4],[3,4]]], font=font, codept=0x1fb95)
    draw_grid_shape(width, 4, 4, [[[1,0],[1,1],[2,1],[2,0]],[[3,0],[3,1],[4,1],[4,0]],
                                         [[1,2],[1,3],[2,3],[2,2]],[[3,2],[3,3],[4,3],[4,2]],
                                         [[0,1],[1,1],[1,2],[0,2]],[[2,1],[3,1],[3,2],[2,2]],
                                         [[0,3],[1,3],[1,4],[0,4]],[[2,3],[3,3],[3,4],[2,4]]], font=font, codept=0x1fb96)

    # heavy horizontal fill
    draw_grid_shape(width, 4, 4, [[[0,1],[4,1],[4,2],[0,2]],[[0,3],[4,3],[4,4],[0,4]]], font=font, codept=0x1fb97)

    # smooth mosaic terminal graphic characters
    draw_grid_shape(width, 2, 2, [[[0,0],[2,0],[1,1]],[[1,1],[2,2],[0,2]]], font=font, codept=0x1fb9a)
    draw_grid_shape(width, 2, 2, [[[0,0],[1,1],[0,2]],[[2,0],[2,2],[1,1]]], font=font, codept=0x1fb9b)

    # smooth mosaic
    draw_grid_shape(width, 1, 1, [[1/2,[0,0],[1,0],[0,1]]], font=font, codept=0x1fb9c)
    draw_grid_shape(width, 1, 1, [[1/2,[0,0],[1,0],[1,1]]], font=font, codept=0x1fb9d)
    draw_grid_shape(width, 1, 1, [[1/2,[1,0],[1,1],[0,1]]], font=font, codept=0x1fb9e)
    draw_grid_shape(width, 1, 1, [[1/2,[0,0],[1,1],[0,1]]], font=font, codept=0x1fb9f)

    # block elements
    draw_grid_shape(width, 3, 3, [[[0,0],[2,0],[2,3],[0,3]]], font=font, codept=0x1fbce)
    draw_grid_shape(width, 3, 3, [[[0,0],[1,0],[1,3],[0,3]]], font=font, codept=0x1fbcf)

    # one-quarter blocks
    draw_grid_shape(width, 4, 4, [[[1,0],[3,0],[3,2],[1,2]]], font=font, codept=0x1fbe4)
    draw_grid_shape(width, 4, 4, [[[1,2],[3,2],[3,4],[1,4]]], font=font, codept=0x1fbe5)
    draw_grid_shape(width, 4, 4, [[[0,1],[2,1],[2,3],[0,3]]], font=font, codept=0x1fbe6)
    draw_grid_shape(width, 4, 4, [[[2,1],[4,1],[4,3],[2,3]]], font=font, codept=0x1fbe7)

    if args.filename.endswith(".sfd"):
        font.save()
    else:
        font.generate()

def draw_vertical_one_eighth_block(width, eighth, codept=None, font=None):
    draw_grid_shape(width, 8, 1, [[[eighth,0],[eighth+1,0],[eighth+1,1],[eighth,1]]], font=font, codept=codept)

def draw_horizontal_one_eighth_block(width, eighth, codept=None, font=None):
    draw_grid_shape(width, 1, 8, [[[0,eighth],[1,eighth],[1,eighth+1],[0,eighth+1]]], font=font, codept=codept)

main()
