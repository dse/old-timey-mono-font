#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, sys, os, statistics, argparse, math

sys.path.append("%s/git/dse.d/my-python/src/my_python_dse" % os.getenv("HOME"))
from font_draw_utils import rect, poly, GA
from font_utils import get_fonts_in

# https://spencermortensen.com/articles/bezier-circle/
C = 0.5519150244935105707435627

X = "X"
Y = "Y"

STROKE_WIDTH = 96
STROKE_WIDTH_HEAVY = 336
STROKE_DIST_DOUBLE = 288

ARC_DRAWING_RADIUS = 2/3

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
    for filename in args.filenames:
        for font in get_fonts_in([filename]):
            boxdraw(font, args)
            if filename.endswith(".sfd"):
                print("Saving %s" % filename)
                font.save(filename)
            else:
                print("Generating %s" % filename)
                font.generate(filename)

def boxdraw(font, args):
    stroke_width       = args.light
    stroke_width_heavy = args.heavy
    stroke_dist_double = args.double
    if args.width is not None:
        width = args.width
    else:
        width = round(statistics.median([glyph.width for glyph in font.glyphs()
                                         if glyph.width]))
    height = font.em

    xc = round(width/2)
    yc = round(font.capHeight/2)

    ascent = font.ascent
    descent = font.descent

    x1_light = round(xc - stroke_width/2)
    x2_light = round(xc + stroke_width/2)
    y1_light = round(yc + stroke_width/2)
    y2_light = round(yc - stroke_width/2)

    x1_heavy = round(xc - stroke_width_heavy/2)
    x2_heavy = round(xc + stroke_width_heavy/2)
    y1_heavy = round(yc + stroke_width_heavy/2)
    y2_heavy = round(yc - stroke_width_heavy/2)

    x1_double = round(xc - stroke_dist_double/2 - stroke_width/2)
    x2_double = round(xc - stroke_dist_double/2 + stroke_width/2)
    x3_double = round(xc + stroke_dist_double/2 - stroke_width/2)
    x4_double = round(xc + stroke_dist_double/2 + stroke_width/2)
    y1_double = round(yc + stroke_dist_double/2 + stroke_width/2)
    y2_double = round(yc + stroke_dist_double/2 - stroke_width/2)
    y3_double = round(yc - stroke_dist_double/2 + stroke_width/2)
    y4_double = round(yc - stroke_dist_double/2 - stroke_width/2)

    arc_radius = ARC_DRAWING_RADIUS * min(width, height) / 2

    x1_arc = xc - arc_radius
    x2_arc = xc + arc_radius
    y1_arc = yc + arc_radius
    y2_arc = yc - arc_radius

    inner_radius = arc_radius - stroke_width / 2
    outer_radius = arc_radius + stroke_width / 2

    # double/triple/quadruple dashes
    dash_horiz = {}
    dash_vert = {}
    # i = 2
    for i in range(2, 5):
        dash_horiz[i] = []
        dash_vert[i]  = []
        # j = 0, 1, 2, 3
        for j in range(0, i*2):
            # k = 1/8, 3/8, 5/8, 7/8
            k = (1 + j*2) / (i*4)
            dash_horiz[i].append(width * k)
            dash_vert[i].append(ascent - height * k)
        print("%d horiz => %s" % (i, repr(dash_horiz[i])))
        print("%d vert  => %s" % (i, repr(dash_vert[i])))

    for glyph in GA(font, "BOX DRAWINGS LIGHT HORIZONTAL"):
        rect(glyph, 0, width, y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS HEAVY HORIZONTAL"):
        rect(glyph, 0, width, y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS LIGHT VERTICAL"):
        rect(glyph, x1_light, x2_light, ascent, -descent)
    for glyph in GA(font, "BOX DRAWINGS HEAVY VERTICAL"):
        rect(glyph, x1_heavy, x2_heavy, ascent, -descent)
    for glyph in GA(font, "BOX DRAWINGS LIGHT TRIPLE DASH HORIZONTAL"):
        for i in range(0, 3):
            rect(glyph, dash_horiz[3][i*2], dash_horiz[3][i*2+1], y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS HEAVY TRIPLE DASH HORIZONTAL"):
        for i in range(0, 3):
            rect(glyph, dash_horiz[3][i*2], dash_horiz[3][i*2+1], y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS LIGHT TRIPLE DASH VERTICAL"):
        for i in range(0, 3):
            rect(glyph, x1_light, x2_light, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS HEAVY TRIPLE DASH VERTICAL"):
        for i in range(0, 3):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS LIGHT QUADRUPLE DASH HORIZONTAL"):
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS HEAVY QUADRUPLE DASH HORIZONTAL"):
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS LIGHT QUADRUPLE DASH VERTICAL"):
        for i in range(0, 4):
            rect(glyph, x1_light, x2_light, dash_vert[4][i*2], dash_vert[4][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS HEAVY QUADRUPLE DASH VERTICAL"):
        for i in range(0, 4):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[4][i*2], dash_vert[4][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOWN AND RIGHT"):
        poly(glyph, ((x1_light, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND RIGHT HEAVY"):
        poly(glyph, ((x1_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND RIGHT LIGHT"):
        poly(glyph, ((x1_heavy, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_heavy, y2_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOWN AND RIGHT"):
        poly(glyph, ((x1_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOWN AND LEFT"):
        poly(glyph, ((0, y1_light),
                     (x2_light, y1_light),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_light),
                     (0, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND LEFT HEAVY"):
        poly(glyph, ((0, y1_heavy),
                     (x2_light, y1_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_heavy),
                     (0, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND LEFT LIGHT"):
        poly(glyph, ((0, y1_light),
                     (x2_heavy, y1_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_light),
                     (0, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOWN AND LEFT"):
        poly(glyph, ((0, y1_heavy),
                     (x2_heavy, y1_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_heavy),
                     (0, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT UP AND RIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x1_light, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND RIGHT HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x1_light, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND RIGHT LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x1_heavy, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY UP AND RIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x1_heavy, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT UP AND LEFT"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y2_light),
                     (0, y2_light),
                     (0, y1_light),
                     (x1_light, y1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND LEFT HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y2_heavy),
                     (0, y2_heavy),
                     (0, y1_heavy),
                     (x1_light, y1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND LEFT LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y2_light),
                     (0, y2_light),
                     (0, y1_light),
                     (x1_heavy, y1_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY UP AND LEFT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y2_heavy),
                     (0, y2_heavy),
                     (0, y1_heavy),
                     (x1_heavy, y1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT VERTICAL AND RIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_light, y2_light),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL LIGHT AND RIGHT HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND RIGHT DOWN LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_light, y2_light),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_light),
                     (x1_heavy, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND RIGHT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL HEAVY AND RIGHT LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND RIGHT UP HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND RIGHT DOWN HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY VERTICAL AND RIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT VERTICAL AND LEFT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL LIGHT AND LEFT HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND LEFT DOWN LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND LEFT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_light),
                     (x2_heavy, y1_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_light),
                     (0, y2_light),
                     (0, y1_light),
                     (x1_light, y1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL HEAVY AND LEFT LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND LEFT UP HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND LEFT DOWN HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY VERTICAL AND LEFT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOWN AND HORIZONTAL"):
        poly(glyph, ((0, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_light, y2_light),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_light),
                     (0, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS LEFT HEAVY AND RIGHT DOWN LIGHT"):
        poly(glyph, ((0, y1_heavy),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT HEAVY AND LEFT DOWN LIGHT"):
        poly(glyph, ((0, y1_light),
                     (X, x1_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND HORIZONTAL HEAVY"):
        poly(glyph, ((0, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_heavy),
                     (0, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND HORIZONTAL LIGHT"):
        poly(glyph, ((0, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_heavy, y2_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_light),
                     (0, y2_light)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT LIGHT AND LEFT DOWN HEAVY"):
        poly(glyph, ((0, y1_heavy),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS LEFT LIGHT AND RIGHT DOWN HEAVY"):
        poly(glyph, ((0, y1_light),
                     (X, x1_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOWN AND HORIZONTAL"):
        poly(glyph, ((0, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_heavy),
                     (0, y2_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT UP AND HORIZONTAL"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS LEFT HEAVY AND RIGHT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
        pass
    for glyph in GA(font, "BOX DRAWINGS RIGHT HEAVY AND LEFT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND HORIZONTAL HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND HORIZONTAL LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT LIGHT AND LEFT UP HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LEFT LIGHT AND RIGHT UP HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY UP AND HORIZONTAL"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS LEFT HEAVY AND RIGHT VERTICAL LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT HEAVY AND LEFT VERTICAL LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL LIGHT AND HORIZONTAL HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP HEAVY AND DOWN HORIZONTAL LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS DOWN HEAVY AND UP HORIZONTAL LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL HEAVY AND HORIZONTAL LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LEFT UP HEAVY AND RIGHT DOWN LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT UP HEAVY AND LEFT DOWN LIGHT"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LEFT DOWN HEAVY AND RIGHT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT DOWN HEAVY AND LEFT UP LIGHT"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS DOWN LIGHT AND UP HORIZONTAL HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS UP LIGHT AND DOWN HORIZONTAL HEAVY"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS RIGHT LIGHT AND LEFT VERTICAL HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LEFT LIGHT AND RIGHT VERTICAL HEAVY"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOUBLE DASH HORIZONTAL"):
        for i in range(0, 2):
            rect(glyph, dash_horiz[2][i*2], dash_horiz[2][i*2+1], y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOUBLE DASH HORIZONTAL"):
        for i in range(0, 2):
            rect(glyph, dash_horiz[2][i*2], dash_horiz[2][i*2+1], y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOUBLE DASH VERTICAL"):
        for i in range(0, 2):
            rect(glyph, x1_light, x2_light, dash_vert[2][i*2], dash_vert[2][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOUBLE DASH VERTICAL"):
        for i in range(0, 2):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[2][i*2], dash_vert[2][i*2+1])
    for glyph in GA(font, "BOX DRAWINGS DOUBLE HORIZONTAL"):
        rect(glyph, 0, width, y1_double, y2_double)
        rect(glyph, 0, width, y3_double, y4_double)
    for glyph in GA(font, "BOX DRAWINGS DOUBLE VERTICAL"):
        rect(glyph, x1_double, x2_double, ascent, -descent)
        rect(glyph, x3_double, x4_double, ascent, -descent)
    for glyph in GA(font, "BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE"):
        poly(glyph, ((x1_light, y1_double),
                     (X, width),
                     (Y, y2_double),
                     (X, x2_light),
                     (Y, y3_double),
                     (X, width),
                     (Y, y4_double),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS DOWN DOUBLE AND RIGHT SINGLE"):
        poly(glyph, ((x1_double, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x4_double),
                     (Y, -descent),
                     (X, x3_double),
                     (Y, y2_light),
                     (X, x2_double),
                     (Y, -descent),
                     (X, x1_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE DOWN AND RIGHT"):
        poly(glyph, ((x1_double, y1_double),
                     (X, width),
                     (Y, y2_double),
                     (X, x2_double),
                     (Y, -descent),
                     (X, x1_double)))
        poly(glyph, ((x3_double, y3_double),
                     (X, width),
                     (Y, y4_double),
                     (X, x4_double),
                     (Y, -descent),
                     (X, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE"):
        poly(glyph, ((0, y1_double),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y4_double),
                     (X, 0),
                     (Y, y3_double),
                     (X, x1_light),
                     (Y, y2_double),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOWN DOUBLE AND LEFT SINGLE"):
        poly(glyph, ((0, y1_light),
                     (X, x4_double),
                     (Y, -descent),
                     (X, x3_double),
                     (Y, y2_light),
                     (X, x2_double),
                     (Y, -descent),
                     (X, x1_double),
                     (Y, y2_light),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE DOWN AND LEFT"):
        poly(glyph, ((0, y1_double),
                     (X, x4_double),
                     (Y, -descent),
                     (X, x3_double),
                     (Y, y2_double),
                     (X, 0)))
        poly(glyph, ((0, y3_double),
                     (X, x2_double),
                     (Y, -descent),
                     (X, x1_double),
                     (Y, y4_double),
                     (X, 0)))
    for glyph in GA(font, "BOX DRAWINGS UP SINGLE AND RIGHT DOUBLE"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_double),
                     (X, width),
                     (Y, y2_double),
                     (X, x2_light),
                     (Y, y3_double),
                     (X, width),
                     (Y, y4_double),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP DOUBLE AND RIGHT SINGLE"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double),
                     (Y, y1_light),
                     (X, x3_double),
                     (Y, ascent),
                     (X, x4_double),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x1_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE UP AND RIGHT"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double),
                     (Y, y3_double),
                     (X, width),
                     (Y, y4_double),
                     (X, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double),
                     (Y, y1_double),
                     (X, width),
                     (Y, y2_double),
                     (X, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS UP SINGLE AND LEFT DOUBLE"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y4_double),
                     (X, 0),
                     (Y, y3_double),
                     (X, x1_light),
                     (Y, y2_double),
                     (X, 0),
                     (Y, y1_double),
                     (X, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP DOUBLE AND LEFT SINGLE"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y2_light, 0, y1_light, x1_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE UP AND LEFT"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y4_double, 0, y3_double, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL SINGLE AND RIGHT DOUBLE"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, x2_light, y3_double, width, y4_double, x2_light, -descent, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL DOUBLE AND RIGHT SINGLE"):
        rect(glyph, x1_double, x2_double, ascent, -descent)
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_light, width, y2_light, x4_double, -descent, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE VERTICAL AND RIGHT"):
        rect(glyph, x1_double, x2_double, ascent, -descent)
        poly(glyph, ((x3_double, ascent), (X, x4_double, y1_double, width, y2_double, x3_double)))
        poly(glyph, ((x3_double, y3_double), (X, width, y4_double, x4_double, -descent, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL SINGLE AND LEFT DOUBLE"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, -descent, x1_light, y4_double, 0, y3_double, x1_light, y2_double, 0, y1_double, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL DOUBLE AND LEFT SINGLE"):
        rect(glyph, x3_double, x4_double, ascent, -descent)
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, -descent, x1_double, y2_light, 0, y1_light, x1_double)))

    for glyph in GA(font, "BOX DRAWINGS DOUBLE VERTICAL AND LEFT"):
        rect(glyph, x3_double, x4_double, ascent, -descent)
        poly(glyph, ((x1_double, ascent), (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOWN SINGLE AND HORIZONTAL DOUBLE"):
        rect(glyph, 0, width, y1_double, y2_double)
        poly(glyph, ((0, y3_double),
                     (X, width, y4_double, x2_light, -descent, x1_light, y4_double, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOWN DOUBLE AND HORIZONTAL SINGLE"):
        poly(glyph, ((0, y1_light),
                     (X, width, y2_light, x4_double, -descent, x3_double, y2_light, x2_double, -descent, x1_double, y2_light, 0)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL"):
        rect(glyph, 0, width, y1_double, y2_double)
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
        poly(glyph, ((x3_double, y3_double),
                     (X, width, y4_double, x4_double, -descent, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS UP SINGLE AND HORIZONTAL DOUBLE"):
        rect(glyph, 0, width, y3_double, y4_double)
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, 0, y1_double, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS UP DOUBLE AND HORIZONTAL SINGLE"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y1_light, width, y2_light, 0, y1_light, x1_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE UP AND HORIZONTAL"):
        rect(glyph, 0, width, y3_double, y4_double)
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_double, width, y2_double, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL SINGLE AND HORIZONTAL DOUBLE"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, x2_light, y3_double, width,
                      y4_double, x2_light, -descent, x1_light, y4_double, 0, y3_double, x1_light, y2_double, 0, y1_double, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS VERTICAL DOUBLE AND HORIZONTAL SINGLE"):
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y1_light, width, y2_light, x4_double, -descent, x3_double, y2_light, x2_double,
                      -descent, x1_double, y2_light, 0, y1_light, x1_double)))
    for glyph in GA(font, "BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL"):
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
        poly(glyph, ((x3_double, y3_double),
                     (X, width, y4_double, x4_double, -descent, x3_double)))
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_double, width, y2_double, x3_double)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT ARC DOWN AND RIGHT"):
        pen = glyph.glyphPen(replace=False)
        pen.moveTo((x2_arc, y1_light))
        pen.lineTo((width, y1_light))
        pen.lineTo((width, y2_light))
        pen.lineTo((x2_arc, y2_light))
        pen.curveTo(
            # assuming quadratic font
            (x2_arc - inner_radius * C, y2_light),
            (x2_light, y2_arc + inner_radius * C),
            (x2_light, y2_arc)
        )
        pen.lineTo((x2_light, -descent))
        pen.lineTo((x1_light, -descent))
        pen.lineTo((x1_light, y2_arc))
        pen.curveTo(
            # again, assuming quadratic font
            (x1_light, y2_arc + outer_radius * C),
            (x2_arc - outer_radius * C, y1_light),
            (x2_arc, y1_light)
        )
        pen.closePath()
        pen = None
    for glyph in GA(font, "BOX DRAWINGS LIGHT ARC DOWN AND LEFT"):
        pen = glyph.glyphPen(replace=False)
        pen.moveTo((0, y1_light))
        pen.lineTo((x1_arc, y1_light))
        pen.curveTo((x1_arc + outer_radius * C, y1_light),
                    (x2_light, y2_arc + outer_radius * C),
                    (x2_light, y2_arc))
        pen.lineTo((x2_light, -descent))
        pen.lineTo((x1_light, -descent))
        pen.lineTo((x1_light, y2_arc))
        pen.curveTo((x1_light, y2_arc + inner_radius * C),
                    (x1_arc + inner_radius * C, y2_light),
                    (x1_arc, y2_light))
        pen.lineTo((0, y2_light))
        pen.closePath()
        pen = None
    for glyph in GA(font, "BOX DRAWINGS LIGHT ARC UP AND LEFT"):
        pen = glyph.glyphPen(replace=False)
        pen.moveTo((x1_light, ascent))
        pen.lineTo((x2_light, ascent))
        pen.lineTo((x2_light, y1_arc))
        pen.curveTo((x2_light, y1_arc - outer_radius * C),
                    (x1_arc + outer_radius * C, y2_light),
                    (x1_arc, y2_light))
        pen.lineTo((0, y2_light))
        pen.lineTo((0, y1_light))
        pen.lineTo((x1_arc, y1_light))
        pen.curveTo((x1_arc + inner_radius * C, y1_light),
                    (x1_light, y1_arc - inner_radius * C),
                    (x1_light, y1_arc))
        pen.closePath()
        pen = None
    for glyph in GA(font, "BOX DRAWINGS LIGHT ARC UP AND RIGHT"):
        pen = glyph.glyphPen(replace=False)
        pen.moveTo((x1_light, ascent))
        pen.lineTo((x2_light, ascent))
        pen.lineTo((x2_light, y1_arc))
        pen.curveTo((x2_light, y1_arc - inner_radius * C),
                    (x2_arc - inner_radius * C, y1_light),
                    (x2_arc, y1_light))
        pen.lineTo((width, y1_light))
        pen.lineTo((width, y2_light))
        pen.lineTo((x2_arc, y2_light))
        pen.curveTo((x2_arc - outer_radius * C, y2_light),
                    (x1_light, y1_arc - outer_radius * C),
                    (x1_light, y1_arc))
        pen.closePath()
        pen = None

    theta = math.atan(width / height)
    x1_diag = 0 - stroke_width / 2 * math.cos(theta)
    x2_diag = 0 + stroke_width / 2 * math.cos(theta)
    x3_diag = width - stroke_width / 2 * math.cos(theta)
    x4_diag = width + stroke_width / 2 * math.cos(theta)
    y1_diag = ascent + stroke_width / 2 * math.sin(theta)
    y2_diag = ascent - stroke_width / 2 * math.sin(theta)
    y3_diag = -descent + stroke_width / 2 * math.sin(theta)
    y4_diag = -descent - stroke_width / 2 * math.sin(theta)

    for glyph in GA(font, "BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT"):
        poly(glyph, ((x3_diag, y1_diag),
                     (x4_diag, y2_diag),
                     (x2_diag, y4_diag),
                     (x1_diag, y3_diag)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT"):
        poly(glyph, ((x1_diag, y2_diag),
                     (x2_diag, y1_diag),
                     (x4_diag, y3_diag),
                     (x3_diag, y4_diag)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT DIAGONAL CROSS"):
        poly(glyph, ((x3_diag, y1_diag),
                     (x4_diag, y2_diag),
                     (x2_diag, y4_diag),
                     (x1_diag, y3_diag)))
        poly(glyph, ((x1_diag, y2_diag),
                     (x2_diag, y1_diag),
                     (x4_diag, y3_diag),
                     (x3_diag, y4_diag)))
        glyph.removeOverlap()
    for glyph in GA(font, "BOX DRAWINGS LIGHT LEFT"):
        rect(glyph, 0, x2_light, y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS LIGHT UP"):
        rect(glyph, x1_light, x2_light, ascent, y2_light)
    for glyph in GA(font, "BOX DRAWINGS LIGHT RIGHT"):
        rect(glyph, x1_light, width, y1_light, y2_light)
    for glyph in GA(font, "BOX DRAWINGS LIGHT DOWN"):
        rect(glyph, x1_light, x2_light, y1_light, -descent)
    for glyph in GA(font, "BOX DRAWINGS HEAVY LEFT"):
        rect(glyph, 0, x2_heavy, y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS HEAVY UP"):
        rect(glyph, x1_heavy, x2_heavy, ascent, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS HEAVY RIGHT"):
        rect(glyph, x1_heavy, width, y1_heavy, y2_heavy)
    for glyph in GA(font, "BOX DRAWINGS HEAVY DOWN"):
        rect(glyph, x1_heavy, x2_heavy, y1_heavy, -descent)
    for glyph in GA(font, "BOX DRAWINGS LIGHT LEFT AND HEAVY RIGHT"):
        poly(glyph, ((0, y1_light),
                     (X, x1_heavy, y1_heavy, width, y2_heavy, x1_heavy, y2_light, 0)))
    for glyph in GA(font, "BOX DRAWINGS LIGHT UP AND HEAVY DOWN"):
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_heavy, x2_heavy, -descent, x1_heavy, y1_heavy, x1_light)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY LEFT AND LIGHT RIGHT"):
        poly(glyph, ((0, y1_heavy),
                     (X, x2_heavy, y1_light, width, y2_light, x2_heavy, y2_heavy, 0)))
    for glyph in GA(font, "BOX DRAWINGS HEAVY UP AND LIGHT DOWN"):
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy, y2_heavy, x2_light, -descent, x1_light, y2_heavy, x1_heavy)))

    for codepoint in range(0x2500, 0x2580):
        glyph = font.createChar(codepoint)
        glyph.width = width

main()
