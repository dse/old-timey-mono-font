#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
#
# symbols.py - draw certain symbols from the SYMBOLS FOR LEGACY
# COMPUTING block.
#
import fontforge, argparse, os, sys, statistics

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

    # one-eighth blocks
    draw_vertical_one_eighth_block(font, width, 0x1fb70, 1)
    draw_vertical_one_eighth_block(font, width, 0x1fb71, 2)
    draw_vertical_one_eighth_block(font, width, 0x1fb72, 3)
    draw_vertical_one_eighth_block(font, width, 0x1fb73, 4)
    draw_vertical_one_eighth_block(font, width, 0x1fb74, 5)
    draw_vertical_one_eighth_block(font, width, 0x1fb75, 6)
    draw_horizontal_one_eighth_block(font, width, 0x1fb76, 1)
    draw_horizontal_one_eighth_block(font, width, 0x1fb77, 2)
    draw_horizontal_one_eighth_block(font, width, 0x1fb78, 3)
    draw_horizontal_one_eighth_block(font, width, 0x1fb79, 4)
    draw_horizontal_one_eighth_block(font, width, 0x1fb7a, 5)
    draw_horizontal_one_eighth_block(font, width, 0x1fb7b, 6)

    # L-shaped one-eighth blocks
    draw_shape(font, width, 0x1fb7c, 8, 8, [[[0,0],[1,0],[1,7],[8,7],[8,8],[0,8]]])
    draw_shape(font, width, 0x1fb7d, 8, 8, [[[0,0],[8,0],[8,1],[1,1],[1,8],[0,8]]])
    draw_shape(font, width, 0x1fb7e, 8, 8, [[[0,0],[8,0],[8,8],[7,8],[7,1],[0,1]]])
    draw_shape(font, width, 0x1fb7f, 8, 8, [[[7,0],[8,0],[8,8],[0,8],[0,7],[7,7]]])

    # other one-eighth blocks
    draw_shape(font, width, 0x1fb80, 8, 8, [[[0,0],[8,0],[8,1],[0,1]],[[0,7],[8,7],[8,8],[0,8]]])
    draw_shape(font, width, 0x1fb81, 8, 8, [[[0,0],[8,0],[8,1],[0,1]],
                                            [[0,2],[8,2],[8,3],[0,3]],
                                            [[0,4],[8,4],[8,5],[0,5]],
                                            [[0,7],[8,7],[8,8],[0,8]]])

    # additional block elements
    draw_shape(font, width, 0x1fb82, 8, 8, [[[0,0],[8,0],[8,2],[0,2]]])
    draw_shape(font, width, 0x1fb83, 8, 8, [[[0,0],[8,0],[8,3],[0,3]]])
    draw_shape(font, width, 0x1fb84, 8, 8, [[[0,0],[8,0],[8,5],[0,5]]])
    draw_shape(font, width, 0x1fb85, 8, 8, [[[0,0],[8,0],[8,6],[0,6]]])
    draw_shape(font, width, 0x1fb86, 8, 8, [[[0,0],[8,0],[8,7],[0,7]]])
    draw_shape(font, width, 0x1fb87, 8, 8, [[[6,0],[8,0],[8,8],[6,8]]])
    draw_shape(font, width, 0x1fb88, 8, 8, [[[5,0],[8,0],[8,8],[5,8]]])
    draw_shape(font, width, 0x1fb89, 8, 8, [[[3,0],[8,0],[8,8],[3,8]]])
    draw_shape(font, width, 0x1fb8a, 8, 8, [[[2,0],[8,0],[8,8],[2,8]]])
    draw_shape(font, width, 0x1fb8b, 8, 8, [[[1,0],[8,0],[8,8],[1,8]]])

    # shade characters
    draw_shape(font, width, 0x1fb8c, 2, 2, [[1/2,[0,0],[1,0],[1,2],[0,2]]]) # medium shades
    draw_shape(font, width, 0x1fb8d, 2, 2, [[1/2,[1,0],[2,0],[2,2],[1,2]]]) # medium shades
    draw_shape(font, width, 0x1fb8e, 2, 2, [[1/2,[0,0],[2,0],[2,1],[0,1]]]) # medium shades
    draw_shape(font, width, 0x1fb8f, 2, 2, [[1/2,[0,1],[2,1],[2,2],[0,2]]]) # medium shades
    draw_shape(font, width, 0x1fb90, 2, 2, [[1/2,[0,0],[0,2],[2,2],[0.2]]])
    draw_shape(font, width, 0x1fb91, 2, 2, [[1,  [0,0],[2,0],[2,1],[0,1]],
                                            [1/2,[0,1],[2,1],[2,2],[0,2]]])
    draw_shape(font, width, 0x1fb91, 2, 2, [[1/2,[0,0],[2,0],[2,1],[0,1]],
                                            [1,  [0,1],[2,1],[2,2],[0,2]]])
    draw_shape(font, width, 0x1fb94, 2, 2, [[1/2,[0,0],[1,0],[1,2],[0,2]],
                                            [1,  [1,0],[2,0],[2,2],[1,2]]])

    # checkerboard fill
    draw_shape(font, width, 0x1fb95, 4, 4, [[[0,0],[0,1],[1,1],[1,0]],
                                            [[2,0],[2,1],[3,1],[3,0]],
                                            [[0,2],[0,3],[1,3],[1,2]],
                                            [[2,2],[2,3],[3,3],[3,2]],
                                            [[1,1],[2,1],[2,2],[1,2]],
                                            [[3,1],[4,1],[4,2],[3,2]],
                                            [[1,3],[2,4],[2,4],[1,3]],
                                            [[3,3],[4,4],[4,4],[3,3]]])
    draw_shape(font, width, 0x1fb96, 4, 4, [[[1,0],[1,1],[2,1],[2,0]],
                                            [[3,0],[3,1],[4,1],[4,0]],
                                            [[1,2],[1,3],[2,3],[2,2]],
                                            [[3,2],[3,3],[4,3],[4,2]],
                                            [[0,1],[1,1],[1,2],[0,2]],
                                            [[2,1],[3,1],[3,2],[2,2]],
                                            [[0,3],[1,4],[1,4],[0,3]],
                                            [[2,3],[3,4],[3,4],[2,3]]])

    # heavy horizontal fill
    draw_shape(font, width, 0x1fb97, 4, 4, [[[0,1],[2,1],[2,2],[0,2]],
                                            [[0,3],[2,3],[2,4],[0,4]]])

    # smooth mosaic terminal graphic characters
    draw_shape(font, width, 0x1fb9a, 2, 2, [[[0,0],[2,0],[1,1]],
                                            [[1,1],[2,2],[0,2]]])
    draw_shape(font, width, 0x1fb9b, 2, 2, [[[0,0],[1,1],[0,2]],
                                            [[2,0],[2,2],[1,1]]])

    # smooth mosaic
    draw_shape(font, width, 0x1fb9c, 1, 1, [[1/2,[0,0],[1,0],[0,1]]])
    draw_shape(font, width, 0x1fb9d, 1, 1, [[1/2,[0,0],[1,0],[1,1]]])
    draw_shape(font, width, 0x1fb9e, 1, 1, [[1/2,[1,0],[1,1],[0,1]]])
    draw_shape(font, width, 0x1fb9f, 1, 1, [[1/2,[0,0],[1,1],[0,1]]])

    # block elements
    draw_shape(font, width, 0x1fbce, 3, 3, [[[0,0],[2,0],[2,3],[0,3]]])
    draw_shape(font, width, 0x1fbce, 3, 3, [[[0,0],[1,0],[1,3],[0,3]]])

    # one-quarter blocks
    draw_shape(font, width, 0x1fbe4, 4, 4, [[[1,0],[3,0],[3,2],[1,2]]])
    draw_shape(font, width, 0x1fbe5, 4, 4, [[[1,2],[3,2],[3,4],[1,4]]])
    draw_shape(font, width, 0x1fbe6, 4, 4, [[[0,1],[2,1],[2,3],[0,3]]])
    draw_shape(font, width, 0x1fbe7, 4, 4, [[[2,1],[4,1],[4,3],[2,3]]])

def draw_shape(font, width, codept, x_max, y_max, polygons):
    glyphname = fontforge.nameFromUnicode(codept)
    if glyphname in font:
        font.removeGlyph(glyphname)
        glyph = font.createChar(codept)
        glyph.width = width
        pen = glyph.glyphPen()
    for polygon in polygons:
        if type(polygon[0]) in [float, int]:
            black_level = polygon[0]
            points = polygon[1:]
        else:
            black_level = 1
            points = polygon[0:]
            first_point = True
        for point in points:
            [x,y] = point
            x = x * width / x_max
            y = y * (font.ascent - (font.descent + font.ascent)) / y_max
            if first_point:
                pen.moveTo((x, y))
            else:
                pen.lineTo((x, y))
                first_point = False
                pen.closePath()

main()
