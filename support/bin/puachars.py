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

        for glyph in GA(font, "U+FAF26"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=True)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF27"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=True)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF28"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=False)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF29"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=False)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF2A"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=True)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF2B"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=True)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF2C"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=False)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF2D"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=False)
            glyph.removeOverlap()

        for glyph in GA(font, "U+FAF2E"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF2F"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF30"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF31"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF32"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF33"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF34"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF35"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()

        for glyph in GA(font, "U+FAF36"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF37"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF38"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF39"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF3A"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF3B"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF3C"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF3D"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()

        for glyph in GA(font, "U+FAF3E"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF3F"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF40"):
            draw_vertical_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF41"):
            draw_vertical_diagonal_arc(glyph, left=False, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF42"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF43"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=True)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF44"):
            draw_horizontal_diagonal_arc(glyph, left=True, upper=False)
            draw_heavy_circle(glyph)
            glyph.removeOverlap()
            hollow_out_heavy_circle(glyph)
            glyph.removeOverlap()
            draw_x_for_hollowed_out_heavy_circle(glyph)
            glyph.removeOverlap()
        for glyph in GA(font, "U+FAF45"):
            draw_horizontal_diagonal_arc(glyph, left=False, upper=False)
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

main()
