#!/usr/bin/env -S fontforge -quiet
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

    # bits are: upper left, upper right, middle left, middle right, lower left, lower right
    draw_block_sextant(font, median_width, 0x1fb00, 0b100000)
    draw_block_sextant(font, median_width, 0x1fb01, 0b010000)
    draw_block_sextant(font, median_width, 0x1fb02, 0b110000)
    draw_block_sextant(font, median_width, 0x1fb03, 0b001000)
    draw_block_sextant(font, median_width, 0x1fb04, 0b101000)
    draw_block_sextant(font, median_width, 0x1fb05, 0b011000)
    draw_block_sextant(font, median_width, 0x1fb06, 0b111000)
    draw_block_sextant(font, median_width, 0x1fb07, 0b000100)
    draw_block_sextant(font, median_width, 0x1fb08, 0b100100)
    draw_block_sextant(font, median_width, 0x1fb09, 0b010100)
    draw_block_sextant(font, median_width, 0x1fb0a, 0b110100)
    draw_block_sextant(font, median_width, 0x1fb0b, 0b001100)
    draw_block_sextant(font, median_width, 0x1fb0c, 0b101100)
    draw_block_sextant(font, median_width, 0x1fb0d, 0b011100)
    draw_block_sextant(font, median_width, 0x1fb0e, 0b111100)
    draw_block_sextant(font, median_width, 0x1fb0f, 0b000010)
    draw_block_sextant(font, median_width, 0x1fb10, 0b100010)
    draw_block_sextant(font, median_width, 0x1fb11, 0b010010)
    draw_block_sextant(font, median_width, 0x1fb12, 0b110010)
    draw_block_sextant(font, median_width, 0x1fb13, 0b001010)
    draw_block_sextant(font, median_width, 0x1fb14, 0b011010)
    draw_block_sextant(font, median_width, 0x1fb15, 0b111010)
    draw_block_sextant(font, median_width, 0x1fb16, 0b000110)
    draw_block_sextant(font, median_width, 0x1fb17, 0b100110)
    draw_block_sextant(font, median_width, 0x1fb18, 0b010110)
    draw_block_sextant(font, median_width, 0x1fb19, 0b110110)
    draw_block_sextant(font, median_width, 0x1fb1a, 0b001110)
    draw_block_sextant(font, median_width, 0x1fb1b, 0b101110)
    draw_block_sextant(font, median_width, 0x1fb1c, 0b011110)
    draw_block_sextant(font, median_width, 0x1fb1d, 0b111110)
    draw_block_sextant(font, median_width, 0x1fb1e, 0b000001)
    draw_block_sextant(font, median_width, 0x1fb1f, 0b100001)
    draw_block_sextant(font, median_width, 0x1fb20, 0b010001)
    draw_block_sextant(font, median_width, 0x1fb21, 0b110001)
    draw_block_sextant(font, median_width, 0x1fb22, 0b001001)
    draw_block_sextant(font, median_width, 0x1fb23, 0b101001)
    draw_block_sextant(font, median_width, 0x1fb24, 0b011001)
    draw_block_sextant(font, median_width, 0x1fb25, 0b111001)
    draw_block_sextant(font, median_width, 0x1fb26, 0b000101)
    draw_block_sextant(font, median_width, 0x1fb27, 0b100101)
    draw_block_sextant(font, median_width, 0x1fb28, 0b110101)
    draw_block_sextant(font, median_width, 0x1fb29, 0b001101)
    draw_block_sextant(font, median_width, 0x1fb2a, 0b101101)
    draw_block_sextant(font, median_width, 0x1fb2b, 0b011101)
    draw_block_sextant(font, median_width, 0x1fb2c, 0b111101)
    draw_block_sextant(font, median_width, 0x1fb2d, 0b000011)
    draw_block_sextant(font, median_width, 0x1fb2e, 0b100011)
    draw_block_sextant(font, median_width, 0x1fb2f, 0b010011)
    draw_block_sextant(font, median_width, 0x1fb30, 0b110011)
    draw_block_sextant(font, median_width, 0x1fb31, 0b001011)
    draw_block_sextant(font, median_width, 0x1fb32, 0b101011)
    draw_block_sextant(font, median_width, 0x1fb33, 0b011011)
    draw_block_sextant(font, median_width, 0x1fb34, 0b111011)
    draw_block_sextant(font, median_width, 0x1fb35, 0b000111)
    draw_block_sextant(font, median_width, 0x1fb36, 0b100111)
    draw_block_sextant(font, median_width, 0x1fb37, 0b010111)
    draw_block_sextant(font, median_width, 0x1fb38, 0b110111)
    draw_block_sextant(font, median_width, 0x1fb39, 0b001111)
    draw_block_sextant(font, median_width, 0x1fb3a, 0b101111)
    draw_block_sextant(font, median_width, 0x1fb3b, 0b011111)

    if args.filename.endswith(".sfd"):
        font.save()
    else:
        font.generate()

def draw_block_sextant(font, width, codept, bits):
    print("draw_block_sextant")
    glyphname = fontforge.nameFromUnicode(codept)
    if glyphname in font:
        font.removeGlyph(glyphname)
    glyph = font.createChar(codept)
    glyph.width = round(width)
    pen = glyph.glyphPen()

    if bits & (1 << 5):
        draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[1,1],[0,1]]], glyph=glyph, pen=pen)
    if bits & (1 << 4):
        draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,1],[1,1]]], glyph=glyph, pen=pen)
    if bits & (1 << 3):
        draw_grid_shape(width, 2, 3, [[[0,1],[1,1],[1,2],[0,2]]], glyph=glyph, pen=pen)
    if bits & (1 << 2):
        draw_grid_shape(width, 2, 3, [[[1,1],[2,1],[2,2],[1,2]]], glyph=glyph, pen=pen)
    if bits & (1 << 1):
        draw_grid_shape(width, 2, 3, [[[0,2],[1,2],[1,3],[0,3]]], glyph=glyph, pen=pen)
    if bits & (1 << 0):
        draw_grid_shape(width, 2, 3, [[[1,2],[2,2],[2,3],[1,3]]], glyph=glyph, pen=pen)

    glyph.width = round(width)

main()
