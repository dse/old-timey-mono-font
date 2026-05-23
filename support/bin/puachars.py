#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import os, argparse, math
sys.path.append("%s/git/dse.d/my-python/src/my_python_dse" % os.getenv("HOME"))
from font_draw_utils import rect, poly, GA
from font_utils import get_fonts_from

from box_draw_utils import \
    ARC_TYPE_A, \
    ARC_TYPE_B, \
    draw_light_vertical, \
    draw_light_horizontal, \
    draw_light_horizontal_left, \
    draw_light_horizontal_right, \
    draw_light_vertical_top, \
    draw_light_vertical_bottom, \
    draw_light_upper_left_arc, \
    draw_light_upper_right_arc, \
    draw_light_lower_left_arc, \
    draw_light_lower_right_arc, \
    draw_heavy_circle, \
    hollow_out_heavy_circle, \
    draw_x_for_hollowed_out_heavy_circle, \
    draw_dot


# https://spencermortensen.com/articles/bezier-circle/
C = 0.5519150244935105707435627

X = "X"
Y = "Y"

STROKE_WIDTH = 96
STROKE_WIDTH_HEAVY = 336
STROKE_DIST_DOUBLE = 288

def main():
    global STROKE_WIDTH
    global STROKE_WIDTH_HEAVY
    global STROKE_DIST_DOUBLE
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("--light", type=int, default=STROKE_WIDTH)
    parser.add_argument("--heavy", type=int, default=STROKE_WIDTH_HEAVY)
    parser.add_argument("--double", type=int, default=STROKE_DIST_DOUBLE)
    parser.add_argument("--width", type=int)
    args = parser.parse_args()

    # Symbols for Revision Control Graphs

    for [font, filename, font_in_file] in get_fonts_from(args.filenames, with_filenames=True, ttc=False):

        codepoint = 0xfaf00

        # revision mark, heavy circle
        for glyph in GA(font, codepoint):
            # heavy circle revision mark
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light horizontal
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light vertical
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light vertical upper
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light vertical lower
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light horizontal left
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # heavy circle revision mark light horizontal right
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark, light circle
        for glyph in GA(font, codepoint):
            # light circle revision mark
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light horizontal
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light vertical
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light vertical upper
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light vertical lower
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light horizontal left
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle revision mark light horizontal right
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark, light circle with x
        for glyph in GA(font, codepoint):
            # light circle with x revision mark
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light horizontal
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light vertical
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light vertical upper
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light vertical lower
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light horizontal left
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with x revision mark light horizontal right
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark, light circle with dot
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light horizontal
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light vertical
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light vertical upper
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light vertical lower
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light horizontal left
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light circle with dot revision mark light horizontal right
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # merge drawing
        for glyph in GA(font, codepoint):
            # vertical merge upper from left
            draw_light_vertical(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # vertical merge upper from right
            draw_light_vertical(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # vertical merge lower from left
            draw_light_vertical(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # vertical merge lower from right
            draw_light_vertical(glyph)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # vertical merge upper from left and right
            draw_light_vertical(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # vertical merge lower from left and right
            draw_light_vertical(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1

        for glyph in GA(font, codepoint):
            # horizontal merge left from upper
            draw_light_horizontal(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # horizontal merge right from upper
            draw_light_horizontal(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # horizontal merge left from lower
            draw_light_horizontal(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # horizontal merge right from lower
            draw_light_horizontal(glyph)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # horizontal merge left from upper and lower
            draw_light_horizontal(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # horizontal merge right from upper and lower
            draw_light_horizontal(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1

        # alternate style arcs
        for glyph in GA(font, codepoint):
            # revision log drawing upper left arc
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing upper right arc
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing lower left arc
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing lower right arc
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1

        # double-arcs
        for glyph in GA(font, codepoint):
            # revision log drawing upper left and right arcs
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing lower left and right arcs
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing lower and upper left arcs
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision log drawing lower and upper right arcs
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
            codepoint += 1

        # diagonal to horizontal/vertical
        for glyph in GA(font, codepoint):
            # light diagonal upper left to down
            draw_vertical_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal upper right to down
            draw_vertical_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal lower left to up
            draw_vertical_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal lower right to up
            draw_vertical_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light dialgonal upper left to right
            draw_horizontal_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal upper right to left
            draw_horizontal_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal lower left to right
            draw_horizontal_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # light diagonal lower right to left
            draw_horizontal_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark heavy circle with diagonal to horizontal/vertical
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal upper left to down
            draw_vertical_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal upper right to down
            draw_vertical_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower left to up
            draw_vertical_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower right to up
            draw_vertical_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light dialgonal upper left to right
            draw_horizontal_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal upper right to left
            draw_horizontal_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower left to right
            draw_horizontal_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower right to left
            draw_horizontal_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower left
            draw_diagonal_piece(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal lower right
            draw_diagonal_piece(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal upper left
            draw_diagonal_piece(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark heavy circle with light diagonal upper right
            draw_diagonal_piece(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark light circle with diagonal to horizontal/vertical
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal upper left to down
            draw_vertical_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal upper right to down
            draw_vertical_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower left to up
            draw_vertical_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower right to up
            draw_vertical_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light dialgonal upper left to right
            draw_horizontal_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal upper right to left
            draw_horizontal_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower left to right
            draw_horizontal_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower right to left
            draw_horizontal_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower left
            draw_diagonal_piece(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal lower right
            draw_diagonal_piece(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal upper left
            draw_diagonal_piece(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with light diagonal upper right
            draw_diagonal_piece(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark light circle with x with diagonal to horizontal/vertical
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal upper left to down
            draw_vertical_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal upper right to down
            draw_vertical_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower left to up
            draw_vertical_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower right to up
            draw_vertical_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light dialgonal upper left to right
            draw_horizontal_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal upper right to left
            draw_horizontal_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower left to right
            draw_horizontal_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower right to left
            draw_horizontal_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower left
            draw_diagonal_piece(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal lower right
            draw_diagonal_piece(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal upper left
            draw_diagonal_piece(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with x with light diagonal upper right
            draw_diagonal_piece(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
            codepoint += 1

        # revision mark light circle with dot with diagonal to horizontal/vertical
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal upper left to down
            draw_vertical_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal upper right to down
            draw_vertical_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower left to up
            draw_vertical_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower right to up
            draw_vertical_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light dialgonal upper left to right
            draw_horizontal_diagonal(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal upper right to left
            draw_horizontal_diagonal(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower left to right
            draw_horizontal_diagonal(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower right to left
            draw_horizontal_diagonal(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower left
            draw_diagonal_piece(glyph, left=True, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal lower right
            draw_diagonal_piece(glyph, left=False, upper=False)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal upper left
            draw_diagonal_piece(glyph, left=True, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1
        for glyph in GA(font, codepoint):
            # revision mark light circle with dot with light diagonal upper right
            draw_diagonal_piece(glyph, left=False, upper=True)
            glyph.removeOverlap()
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_dot(glyph)
            glyph.removeOverlap()
            codepoint += 1

        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)

def draw_horizontal_diagonal_arc(glyph, clockwise=True, left=True, upper=True):
    draw_vertical_diagonal_arc(glyph, clockwise=clockwise, left=left, upper=upper,
                               horizontal=True)

def draw_vertical_diagonal_arc(glyph, clockwise=True, left=True, upper=True, horizontal=False):
    global STROKE_WIDTH

    font = glyph.font

    this_way = clockwise
    if not left:
        this_way = not this_way
    if not upper:
        this_way = not this_way

    w = glyph.width
    h = font.ascent + font.descent

    # lower left corner
    x0 = 0
    y0 = -font.descent
    x0a = x0 - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y0a = y0 + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    x0b = x0 + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y0b = y0 - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    # start of curve
    x1 = 0
    y1 = -font.descent
    if horizontal:
        x1 = glyph.width / 4
        y1 = -font.descent + (font.ascent + font.descent) / 4
    x1a = x1 - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1a = y1 + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    x1b = x1 + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1b = y1 - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    # upper center
    x2 = glyph.width / 2
    y2 = font.ascent
    x2a = x2 - STROKE_WIDTH / 2
    y2a = y2
    x2b = x2 + STROKE_WIDTH / 2
    y2b = y2

    if horizontal:
        x2 = glyph.width
        y2 = (font.ascent - font.descent) / 2
        x2a = x2
        x2b = x2
        y2a = y2 + STROKE_WIDTH / 2
        y2b = y2 - STROKE_WIDTH / 2

    # centers used for computing control points
    xc = glyph.width / 2
    yc = (font.ascent - font.descent) / 2
    xca = xc - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    xcb = xc + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    yca = yc + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    ycb = yc - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    # control points
    x3a = x1a + (xca - x1a) * C
    y3a = y1a + (yca - y1a) * C
    x3b = x1b + (xcb - x1b) * C
    y3b = y1b + (ycb - y1b) * C
    x4a = x2a
    x4b = x2b
    y4a = y2a + (yca - y2a) * C
    y4b = y2b + (ycb - y2b) * C
    if horizontal:
        x4a = glyph.width + (xca - glyph.width) * C
        x4b = glyph.width + (xcb - glyph.width) * C
        y4a = y2a
        y4b = y2b

    if not left:
        (x0a, x0b, x1a, x3a, x4a, x2a, x2b, x4b, x3b, x1b) = [
            glyph.width - x
            for x in (x0a, x0b, x1a, x3a, x4a, x2a, x2b, x4b, x3b, x1b)
        ]
    if not upper:
        (y0a, y0b, y1a, y3a, y4a, y2a, y2b, y4b, y3b, y1b) = [
            font.ascent - font.descent - y
            for y in (y0a, y0b, y1a, y3a, y4a, y2a, y2b, y4b, y3b, y1b)
        ]

    pen = glyph.glyphPen(replace=False)
    if this_way:
        if horizontal:
            pen.moveTo((x0a, y0a))
            pen.lineTo((x1a, y1a))
            pen.curveTo((x3a, y3a), (x4a, y4a), (x2a, y2a))
            pen.lineTo((x2b, y2b))
            pen.curveTo((x4b, y4b), (x3b, y3b), (x1b, y1b))
            pen.lineTo((x0b, y0b))
            pen.lineTo((x0a, y0a))
        else:
            pen.moveTo((x1a, y1a))
            pen.curveTo((x3a, y3a), (x4a, y4a), (x2a, y2a))
            pen.lineTo((x2b, y2b))
            pen.curveTo((x4b, y4b), (x3b, y3b), (x1b, y1b))
            pen.lineTo((x1a, y1a))
    else:
        if horizontal:
            pen.moveTo((x0a, y0a))
            pen.lineTo((x0b, y0b))
            pen.lineTo((x1b, y1b))
            pen.curveTo((x3b, y3b), (x4b, y4b), (x2b, y2b))
            pen.lineTo((x2a, y2a))
            pen.curveTo((x4a, y4a), (x3a, y3a), (x1a, y1a))
            pen.lineTo((x0a, y0a))
        else:
            pen.moveTo((x1a, y1a))
            pen.lineTo((x1b, y1b))
            pen.curveTo((x3b, y3b), (x4b, y4b), (x2b, y2b))
            pen.lineTo((x2a, y2a))
            pen.curveTo((x4a, y4a), (x3a, y3a), (x1a, y1a))
    pen.closePath()
    pen = None

def draw_vertical_diagonal(glyph, clockwise=True, left=True, upper=False):
    draw_horizontal_diagonal(glyph, clockwise=clockwise, left=left, upper=upper, horizontal=False)

def draw_horizontal_diagonal(glyph, clockwise=True, left=True, upper=False, horizontal=True):
    global STROKE_WIDTH
    font = glyph.font

    this_way = clockwise
    if not left:
        this_way = not this_way
    if upper:
        this_way = not this_way

    w = glyph.width
    h = font.ascent + font.descent

    x1 = 0
    y1 = -font.descent
    x1a = x1 - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1a = y1 + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    x1b = x1 + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1b = y1 - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    if horizontal:
        x3a = glyph.width
        x3b = glyph.width
        y3a = (font.ascent - font.descent) / 2 + STROKE_WIDTH/2
        y3b = (font.ascent - font.descent) / 2 - STROKE_WIDTH/2
        y2a = y3a
        y2b = y3b
        x2a = x1a + w/h * (y2a - y1a)
        x2b = x1b + w/h * (y2b - y1b)
    else:
        x3a = glyph.width/2 - STROKE_WIDTH/2
        x3b = glyph.width/2 + STROKE_WIDTH/2
        y3a = font.ascent
        y3b = font.ascent
        x2a = x3a
        x2b = x3b
        y2a = y1a + h/w * (x2a - x1a)
        y2b = y1b + h/w * (x2b - x1b)

    if not left:
        (x1, x1a, x1b, x2a, x2b, x3a, x3b) = [
            glyph.width - x for x in
            (x1, x1a, x1b, x2a, x2b, x3a, x3b)
        ]
    if upper:
        (y1, y1a, y1b, y2a, y2b, y3a, y3b) = [
            font.ascent - font.descent - y for y in
            (y1, y1a, y1b, y2a, y2b, y3a, y3b)
        ]

    pen = glyph.glyphPen(replace=False)
    if this_way:
        pen.moveTo((x1a, y1a))
        pen.lineTo((x2a, y2a))
        pen.lineTo((x3a, y3a))
        pen.lineTo((x3b, y3b))
        pen.lineTo((x2b, y2b))
        pen.lineTo((x1b, y1b))
    else:
        pen.moveTo((x1a, y1a))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x2b, y2b))
        pen.lineTo((x3b, y3b))
        pen.lineTo((x3a, y3a))
        pen.lineTo((x2a, y2a))
    pen.closePath()
    pen = None

def draw_diagonal_piece(glyph, clockwise=True, left=True, upper=False):
    global STROKE_WIDTH

    font = glyph.font

    this_way = clockwise
    if not left:
        this_way = not this_way
    if upper:
        this_way = not this_way

    w = glyph.width
    h = font.ascent + font.descent

    x0 = 0
    y0 = -font.descent
    x0a = x0 - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y0a = y0 + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    x0b = x0 + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y0b = y0 - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    x1 = glyph.width / 2
    y1 = (font.ascent - font.descent) / 2
    x1a = x1 - STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1a = y1 + STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)
    x1b = x1 + STROKE_WIDTH/2 * h / math.sqrt(w*w + h*h)
    y1b = y1 - STROKE_WIDTH/2 * w / math.sqrt(w*w + h*h)

    if not left:
        (x0, x0a, x0b, x1, x1a, x1b) = [
            glyph.width - x for x in
            (x0, x0a, x0b, x1, x1a, x1b)
        ]
    if upper:
        (y0, y0a, y0b, y1, y1a, y1b) = [
            font.ascent - font.descent - y for y in
            (y0, y0a, y0b, y1, y1a, y1b)
        ]

    pen = glyph.glyphPen(replace=False)
    if this_way:
        pen.moveTo((x0a, y0a))
        pen.lineTo((x1a, y1a))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x0b, y0b))
    else:
        pen.moveTo((x0a, y0a))
        pen.lineTo((x0b, y0b))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x1a, y1a))
    pen.closePath()
    pen = None

main()
