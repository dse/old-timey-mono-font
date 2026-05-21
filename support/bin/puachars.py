#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import os, argparse
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
    draw_x_for_hollowed_out_heavy_circle

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

        # this revision
        for glyph in GA(font, "U+FAF00"):
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF01"):
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()

        # merge drawing
        for glyph in GA(font, "U+FAF02"):
            draw_light_vertical(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF03"):
            draw_light_vertical(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF04"):
            draw_light_vertical(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF05"):
            draw_light_vertical(glyph)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF06"):
            draw_light_vertical(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF07"):
            draw_light_vertical(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()

        for glyph in GA(font, "U+FAF08"):
            draw_light_horizontal(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF09"):
            draw_light_horizontal(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF0A"):
            draw_light_horizontal(glyph)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF0B"):
            draw_light_horizontal(glyph)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF0C"):
            draw_light_horizontal(glyph)
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF0D"):
            draw_light_horizontal(glyph)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()

        # this revision
        for glyph in GA(font, "U+FAF0E"):
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF0F"):
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF10"):
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF11"):
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()

        # alternate style arcs
        for glyph in GA(font, "U+FAF12"):
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF13"):
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF14"):
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF15"):
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()

        # double-arcs
        for glyph in GA(font, "U+FAF16"):
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF17"):
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF18"):
            draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF19"):
            draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
            draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
            glyph.removeOverlap()

        # this revision, hollowed out
        for glyph in GA(font, "U+FAF1A"):
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF1B"):
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF1C"):
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF1D"):
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF1E"):
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF1F"):
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()

        # this revision, hollowed out, with X
        for glyph in GA(font, "U+FAF20"):
            draw_light_vertical(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF21"):
            draw_light_horizontal(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF22"):
            draw_light_vertical_top(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF23"):
            draw_light_vertical_bottom(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF24"):
            draw_light_horizontal_left(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF25"):
            draw_light_horizontal_right(glyph)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()

        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)

main()
