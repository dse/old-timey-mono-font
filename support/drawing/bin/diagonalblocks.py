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

    # [0,0] is upper left; [x,0] is upper right; [0,y] is lower left; [x,y] is lower right
    draw_grid_shape(width, 2, 3, [[[0,2],[1,3],[0,3]]],             font=font, codept=0x1fb3c)
    draw_grid_shape(width, 2, 3, [[[0,2],[2,3],[0,3]]],             font=font, codept=0x1fb3d)
    draw_grid_shape(width, 2, 3, [[[0,1],[1,3],[0,3]]],             font=font, codept=0x1fb3e)
    draw_grid_shape(width, 2, 3, [[[0,1],[2,3],[0,3]]],             font=font, codept=0x1fb3f)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,3],[0,3]]],             font=font, codept=0x1fb40)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,3],[0,3],[0,1]]], font=font, codept=0x1fb41)
    draw_grid_shape(width, 2, 3, [[[2,0],[2,3],[0,3],[0,1]]],       font=font, codept=0x1fb42)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,3],[0,3],[0,2]]], font=font, codept=0x1fb43)
    draw_grid_shape(width, 2, 3, [[[2,0],[2,3],[0,3],[0,2]]],       font=font, codept=0x1fb44)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,3],[0,3]]],       font=font, codept=0x1fb45)
    draw_grid_shape(width, 2, 3, [[[2,1],[2,3],[0,3],[0,2]]],       font=font, codept=0x1fb46)
    draw_grid_shape(width, 2, 3, [[[2,2],[2,3],[1,3]]],             font=font, codept=0x1fb47)
    draw_grid_shape(width, 2, 3, [[[2,2],[2,3],[0,3]]],             font=font, codept=0x1fb48)
    draw_grid_shape(width, 2, 3, [[[2,1],[2,3],[1,3]]],             font=font, codept=0x1fb49)
    draw_grid_shape(width, 2, 3, [[[2,1],[2,3],[0,3]]],             font=font, codept=0x1fb4a)
    draw_grid_shape(width, 2, 3, [[[2,0],[2,3],[1,3]]],             font=font, codept=0x1fb4b)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[2,1],[2,3],[0,3]]], font=font, codept=0x1fb4c)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,1],[2,3],[0,3]]],       font=font, codept=0x1fb4d)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[2,2],[2,3],[0,3]]], font=font, codept=0x1fb4e)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,2],[2,3],[0,3]]],       font=font, codept=0x1fb4f)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[2,3],[0,3]]],       font=font, codept=0x1fb50)
    draw_grid_shape(width, 2, 3, [[[0,1],[2,2],[2,3],[0,3]]],       font=font, codept=0x1fb51)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,3],[1,3],[0,2]]], font=font, codept=0x1fb52)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,3],[0,2]]],       font=font, codept=0x1fb53)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,3],[1,3],[0,1]]], font=font, codept=0x1fb54)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,3],[0,1]]],       font=font, codept=0x1fb55)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,3],[1,3]]],       font=font, codept=0x1fb56)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[0,1]]],             font=font, codept=0x1fb57)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[0,1]]],             font=font, codept=0x1fb58)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[0,2]]],             font=font, codept=0x1fb59)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[0,2]]],             font=font, codept=0x1fb5a)
    draw_grid_shape(width, 2, 3, [[[0,0],[1,0],[0,3]]],             font=font, codept=0x1fb5b)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,1],[0,2]]],       font=font, codept=0x1fb5c)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,2],[1,3],[0,3]]], font=font, codept=0x1fb5d)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,2],[0,3]]],       font=font, codept=0x1fb5e)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,1],[1,3],[0,3]]], font=font, codept=0x1fb5f)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,1],[0,3]]],       font=font, codept=0x1fb60)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[1,3],[0,3]]],       font=font, codept=0x1fb61)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,1]]],             font=font, codept=0x1fb62)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,1]]],             font=font, codept=0x1fb63)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,2]]],             font=font, codept=0x1fb64)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,2]]],             font=font, codept=0x1fb65)
    draw_grid_shape(width, 2, 3, [[[1,0],[2,0],[2,3]]],             font=font, codept=0x1fb66)
    draw_grid_shape(width, 2, 3, [[[0,0],[2,0],[2,2],[0,1]]],       font=font, codept=0x1fb67)

    if args.filename.endswith(".sfd"):
        font.save()
    else:
        font.generate()

main()
