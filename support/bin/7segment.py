#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, statistics, math

sys.path.append("%s/git/dse.d/pyfontutils/lib" % os.getenv("HOME"))
from font_utils import get_fonts_from

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    for [font, filename, _] in get_fonts_from(args.filenames, with_filenames=True):
        draw_seven_segment_digits(font)
        if filename.endswith(".sfd"):
            print("Saving %s" % filename)
            font.save(filename)
        else:
            print("Generating %s" % filename)
            font.generate(filename)

def draw_seven_segment_digits(font):
    glyphs = list(font.glyphs())
    widths = [glyph.width for glyph in glyphs]
    widths.sort()
    median_width = statistics.median(widths)

    glyphs_having_median_width = [glyph for glyph in glyphs if abs(glyph.width - median_width) < median_width / 1000]
    if len(glyphs_having_median_width) / len(glyphs) < 0.95:
        raise Exception("not enough glyphs same width")

    width = round(median_width)

    draw_7_segments(font, width, 0x1fbf0, 0b1110111)
    draw_7_segments(font, width, 0x1fbf1, 0b0010010)
    draw_7_segments(font, width, 0x1fbf2, 0b1011101)
    draw_7_segments(font, width, 0x1fbf3, 0b1011011)
    draw_7_segments(font, width, 0x1fbf4, 0b0111010)
    draw_7_segments(font, width, 0x1fbf5, 0b1101011)
    draw_7_segments(font, width, 0x1fbf6, 0b1101111)
    draw_7_segments(font, width, 0x1fbf7, 0b1010010)
    draw_7_segments(font, width, 0x1fbf8, 0b1111111)
    draw_7_segments(font, width, 0x1fbf9, 0b1111011)

def draw_7_segments(font, width, codept, bits):
    glyphname = fontforge.nameFromUnicode(codept)
    if glyphname in font:
        font.deleteGlyph(glyphname)
    glyph = font.createChar(codept)
    glyph.width = width

    pi = 3.14159265358979323846
    italic_angle = 8
    thickness = 120
    gap = 24
    margin = 96
    shift = math.tan(italic_angle * pi / 180) * font.capHeight

    polygons = []

    # vertical segments on left
    x0 = margin
    x1 = margin + thickness

    # horizontal segments
    x2 = margin + thickness + gap
    x3 = glyph.width - margin - thickness - gap - shift

    # vertical segments on right
    x4 = glyph.width - margin - thickness - shift
    x5 = glyph.width - margin - shift

    # top horizontal segments
    y0 = font.capHeight
    y1 = font.capHeight - thickness

    # middle horizontal segments
    y2 = font.capHeight/2 + thickness/2
    y3 = font.capHeight/2 - thickness/2

    # bottom horizontal segments
    y4 = thickness
    y5 = 0

    # top vertical segments
    y6 = font.capHeight - thickness/2
    y7 = font.capHeight/2 + gap/2

    # bottom vertical segments
    y8 = font.capHeight/2 - gap/2
    y9 = thickness/2

    if bits & (1 << 6):
        polygons.append([[x2,y0],[x3,y0],[x3,y1],[x2,y1]])
    if bits & (1 << 5):
        polygons.append([[x0,y6],[x1,y6],[x1,y7],[x0,y7]])
    if bits & (1 << 4):
        polygons.append([[x4,y6],[x5,y6],[x5,y7],[x4,y7]])
    if bits & (1 << 3):
        polygons.append([[x2,y2],[x3,y2],[x3,y3],[x2,y3]])
    if bits & (1 << 2):
        polygons.append([[x0,y8],[x1,y8],[x1,y9],[x0,y9]])
    if bits & (1 << 1):
        polygons.append([[x4,y8],[x5,y8],[x5,y9],[x4,y9]])
    if bits & (1 << 0):
        polygons.append([[x2,y4],[x3,y4],[x3,y5],[x2,y5]])
    for polygon in polygons:
        for coords in polygon:
            coords[0] += shift * coords[1] / font.capHeight

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
            if first_point:
                pen.moveTo((x, y))
                first_point = False
            else:
                pen.lineTo((x, y))
        pen.closePath()

    glyph.width = width

main()
