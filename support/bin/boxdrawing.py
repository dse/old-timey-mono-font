#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, sys, os, statistics, argparse, math

sys.path.append("%s/git/dse.d/font-utils/lib" % os.getenv("HOME"))
from font_utils import fonts_in

# https://spencermortensen.com/articles/bezier-circle/
C = 0.5519150244935105707435627

X = "X"
Y = "Y"

LIGHT_HORIZONTAL                         = 0x2500
HEAVY_HORIZONTAL                         = 0x2501
LIGHT_VERTICAL                           = 0x2502
HEAVY_VERTICAL                           = 0x2503
LIGHT_TRIPLE_DASH_HORIZONTAL             = 0x2504
HEAVY_TRIPLE_DASH_HORIZONTAL             = 0x2505
LIGHT_TRIPLE_DASH_VERTICAL               = 0x2506
HEAVY_TRIPLE_DASH_VERTICAL               = 0x2507
LIGHT_QUADRUPLE_DASH_HORIZONTAL          = 0x2508
HEAVY_QUADRUPLE_DASH_HORIZONTAL          = 0x2509
LIGHT_QUADRUPLE_DASH_VERTICAL            = 0x250A
HEAVY_QUADRUPLE_DASH_VERTICAL            = 0x250B
LIGHT_DOWN_AND_RIGHT                     = 0x250C
DOWN_LIGHT_AND_RIGHT_HEAVY               = 0x250D
DOWN_HEAVY_AND_RIGHT_LIGHT               = 0x250E
HEAVY_DOWN_AND_RIGHT                     = 0x250F
LIGHT_DOWN_AND_LEFT                      = 0x2510
DOWN_LIGHT_AND_LEFT_HEAVY                = 0x2511
DOWN_HEAVY_AND_LEFT_LIGHT                = 0x2512
HEAVY_DOWN_AND_LEFT                      = 0x2513
LIGHT_UP_AND_RIGHT                       = 0x2514
UP_LIGHT_AND_RIGHT_HEAVY                 = 0x2515
UP_HEAVY_AND_RIGHT_LIGHT                 = 0x2516
HEAVY_UP_AND_RIGHT                       = 0x2517
LIGHT_UP_AND_LEFT                        = 0x2518
UP_LIGHT_AND_LEFT_HEAVY                  = 0x2519
UP_HEAVY_AND_LEFT_LIGHT                  = 0x251A
HEAVY_UP_AND_LEFT                        = 0x251B
LIGHT_VERTICAL_AND_RIGHT                 = 0x251C
VERTICAL_LIGHT_AND_RIGHT_HEAVY           = 0x251D
UP_HEAVY_AND_RIGHT_DOWN_LIGHT            = 0x251E
DOWN_HEAVY_AND_RIGHT_UP_LIGHT            = 0x251F
VERTICAL_HEAVY_AND_RIGHT_LIGHT           = 0x2520
DOWN_LIGHT_AND_RIGHT_UP_HEAVY            = 0x2521
UP_LIGHT_AND_RIGHT_DOWN_HEAVY            = 0x2522
HEAVY_VERTICAL_AND_RIGHT                 = 0x2523
LIGHT_VERTICAL_AND_LEFT                  = 0x2524
VERTICAL_LIGHT_AND_LEFT_HEAVY            = 0x2525
UP_HEAVY_AND_LEFT_DOWN_LIGHT             = 0x2526
DOWN_HEAVY_AND_LEFT_UP_LIGHT             = 0x2527
VERTICAL_HEAVY_AND_LEFT_LIGHT            = 0x2528
DOWN_LIGHT_AND_LEFT_UP_HEAVY             = 0x2529
UP_LIGHT_AND_LEFT_DOWN_HEAVY             = 0x252A
HEAVY_VERTICAL_AND_LEFT                  = 0x252B
LIGHT_DOWN_AND_HORIZONTAL                = 0x252C
LEFT_HEAVY_AND_RIGHT_DOWN_LIGHT          = 0x252D
RIGHT_HEAVY_AND_LEFT_DOWN_LIGHT          = 0x252E
DOWN_LIGHT_AND_HORIZONTAL_HEAVY          = 0x252F
DOWN_HEAVY_AND_HORIZONTAL_LIGHT          = 0x2530
RIGHT_LIGHT_AND_LEFT_DOWN_HEAVY          = 0x2531
LEFT_LIGHT_AND_RIGHT_DOWN_HEAVY          = 0x2532
HEAVY_DOWN_AND_HORIZONTAL                = 0x2533
LIGHT_UP_AND_HORIZONTAL                  = 0x2534
LEFT_HEAVY_AND_RIGHT_UP_LIGHT            = 0x2535
RIGHT_HEAVY_AND_LEFT_UP_LIGHT            = 0x2536
UP_LIGHT_AND_HORIZONTAL_HEAVY            = 0x2537
UP_HEAVY_AND_HORIZONTAL_LIGHT            = 0x2538
RIGHT_LIGHT_AND_LEFT_UP_HEAVY            = 0x2539
LEFT_LIGHT_AND_RIGHT_UP_HEAVY            = 0x253A
HEAVY_UP_AND_HORIZONTAL                  = 0x253B
LIGHT_VERTICAL_AND_HORIZONTAL            = 0x253C
LEFT_HEAVY_AND_RIGHT_VERTICAL_LIGHT      = 0x253D
RIGHT_HEAVY_AND_LEFT_VERTICAL_LIGHT      = 0x253E
VERTICAL_LIGHT_AND_HORIZONTAL_HEAVY      = 0x253F
UP_HEAVY_AND_DOWN_HORIZONTAL_LIGHT       = 0x2540
DOWN_HEAVY_AND_UP_HORIZONTAL_LIGHT       = 0x2541
VERTICAL_HEAVY_AND_HORIZONTAL_LIGHT      = 0x2542
LEFT_UP_HEAVY_AND_RIGHT_DOWN_LIGHT       = 0x2543
RIGHT_UP_HEAVY_AND_LEFT_DOWN_LIGHT       = 0x2544
LEFT_DOWN_HEAVY_AND_RIGHT_UP_LIGHT       = 0x2545
RIGHT_DOWN_HEAVY_AND_LEFT_UP_LIGHT       = 0x2546
DOWN_LIGHT_AND_UP_HORIZONTAL_HEAVY       = 0x2547
UP_LIGHT_AND_DOWN_HORIZONTAL_HEAVY       = 0x2548
RIGHT_LIGHT_AND_LEFT_VERTICAL_HEAVY      = 0x2549
LEFT_LIGHT_AND_RIGHT_VERTICAL_HEAVY      = 0x254A
HEAVY_VERTICAL_AND_HORIZONTAL            = 0x254B
LIGHT_DOUBLE_DASH_HORIZONTAL             = 0x254C
HEAVY_DOUBLE_DASH_HORIZONTAL             = 0x254D
LIGHT_DOUBLE_DASH_VERTICAL               = 0x254E
HEAVY_DOUBLE_DASH_VERTICAL               = 0x254F
DOUBLE_HORIZONTAL                        = 0x2550
DOUBLE_VERTICAL                          = 0x2551
DOWN_SINGLE_AND_RIGHT_DOUBLE             = 0x2552
DOWN_DOUBLE_AND_RIGHT_SINGLE             = 0x2553
DOUBLE_DOWN_AND_RIGHT                    = 0x2554
DOWN_SINGLE_AND_LEFT_DOUBLE              = 0x2555
DOWN_DOUBLE_AND_LEFT_SINGLE              = 0x2556
DOUBLE_DOWN_AND_LEFT                     = 0x2557
UP_SINGLE_AND_RIGHT_DOUBLE               = 0x2558
UP_DOUBLE_AND_RIGHT_SINGLE               = 0x2559
DOUBLE_UP_AND_RIGHT                      = 0x255A
UP_SINGLE_AND_LEFT_DOUBLE                = 0x255B
UP_DOUBLE_AND_LEFT_SINGLE                = 0x255C
DOUBLE_UP_AND_LEFT                       = 0x255D
VERTICAL_SINGLE_AND_RIGHT_DOUBLE         = 0x255E
VERTICAL_DOUBLE_AND_RIGHT_SINGLE         = 0x255F
DOUBLE_VERTICAL_AND_RIGHT                = 0x2560
VERTICAL_SINGLE_AND_LEFT_DOUBLE          = 0x2561
VERTICAL_DOUBLE_AND_LEFT_SINGLE          = 0x2562
DOUBLE_VERTICAL_AND_LEFT                 = 0x2563
DOWN_SINGLE_AND_HORIZONTAL_DOUBLE        = 0x2564
DOWN_DOUBLE_AND_HORIZONTAL_SINGLE        = 0x2565
DOUBLE_DOWN_AND_HORIZONTAL               = 0x2566
UP_SINGLE_AND_HORIZONTAL_DOUBLE          = 0x2567
UP_DOUBLE_AND_HORIZONTAL_SINGLE          = 0x2568
DOUBLE_UP_AND_HORIZONTAL                 = 0x2569
VERTICAL_SINGLE_AND_HORIZONTAL_DOUBLE    = 0x256A
VERTICAL_DOUBLE_AND_HORIZONTAL_SINGLE    = 0x256B
DOUBLE_VERTICAL_AND_HORIZONTAL           = 0x256C
LIGHT_ARC_DOWN_AND_RIGHT                 = 0x256D
LIGHT_ARC_DOWN_AND_LEFT                  = 0x256E
LIGHT_ARC_UP_AND_LEFT                    = 0x256F
LIGHT_ARC_UP_AND_RIGHT                   = 0x2570
LIGHT_DIAGONAL_UPPER_RIGHT_TO_LOWER_LEFT = 0x2571
LIGHT_DIAGONAL_UPPER_LEFT_TO_LOWER_RIGHT = 0x2572
LIGHT_DIAGONAL_CROSS                     = 0x2573
LIGHT_LEFT                               = 0x2574
LIGHT_UP                                 = 0x2575
LIGHT_RIGHT                              = 0x2576
LIGHT_DOWN                               = 0x2577
HEAVY_LEFT                               = 0x2578
HEAVY_UP                                 = 0x2579
HEAVY_RIGHT                              = 0x257A
HEAVY_DOWN                               = 0x257B
LIGHT_LEFT_AND_HEAVY_RIGHT               = 0x257C
LIGHT_UP_AND_HEAVY_DOWN                  = 0x257D
HEAVY_LEFT_AND_LIGHT_RIGHT               = 0x257E
HEAVY_UP_AND_LIGHT_DOWN                  = 0x257F

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
        for font in fonts_in([filename], names=False):
            boxdraw(font)
            if filename.endswith(".sfd"):
                print("Saving %s" % filename)
                font.save(filename)
            else:
                print("Generating %s" % filename)
                font.generate(filename)

def boxdraw(font):
    global STROKE_WIDTH
    global STROKE_WIDTH_HEAVY
    global STROKE_DIST_DOUBLE
    global args

    if args.width is not None:
        width = args.width
    else:
        width = round(statistics.median([glyph.width for glyph in font.glyphs()]))
    print("width => %d" % width)
    height = font.em
    print("height => %d" % height)

    xc = round(width/2)
    yc = round(font.capHeight/2)

    ascent = font.ascent
    descent = font.descent

    x1_light = round(xc - STROKE_WIDTH/2)
    x2_light = round(xc + STROKE_WIDTH/2)
    y1_light = round(yc + STROKE_WIDTH/2)
    y2_light = round(yc - STROKE_WIDTH/2)

    x1_heavy = round(xc - STROKE_WIDTH_HEAVY/2)
    x2_heavy = round(xc + STROKE_WIDTH_HEAVY/2)
    y1_heavy = round(yc + STROKE_WIDTH_HEAVY/2)
    y2_heavy = round(yc - STROKE_WIDTH_HEAVY/2)

    x1_double = round(xc - STROKE_DIST_DOUBLE/2 - STROKE_WIDTH/2)
    x2_double = round(xc - STROKE_DIST_DOUBLE/2 + STROKE_WIDTH/2)
    x3_double = round(xc + STROKE_DIST_DOUBLE/2 - STROKE_WIDTH/2)
    x4_double = round(xc + STROKE_DIST_DOUBLE/2 + STROKE_WIDTH/2)
    y1_double = round(yc + STROKE_DIST_DOUBLE/2 + STROKE_WIDTH/2)
    y2_double = round(yc + STROKE_DIST_DOUBLE/2 - STROKE_WIDTH/2)
    y3_double = round(yc - STROKE_DIST_DOUBLE/2 + STROKE_WIDTH/2)
    y4_double = round(yc - STROKE_DIST_DOUBLE/2 - STROKE_WIDTH/2)

    arc_radius = ARC_DRAWING_RADIUS * min(width, height) / 2

    x1_arc = xc - arc_radius
    x2_arc = xc + arc_radius
    y1_arc = yc + arc_radius
    y2_arc = yc - arc_radius

    inner_radius = arc_radius - STROKE_WIDTH / 2
    outer_radius = arc_radius + STROKE_WIDTH / 2

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

    for codepoint in range(0x2500, 0x2580):
        glyph = font.createChar(codepoint)
        glyph.clear()

    for glyph in [font.createChar(LIGHT_HORIZONTAL)]:               # ─ 0x2500
        rect(glyph, 0, width, y1_light, y2_light)
    for glyph in [font.createChar(HEAVY_HORIZONTAL)]:               # ━ 0x2501
        rect(glyph, 0, width, y1_heavy, y2_heavy)
    for glyph in [font.createChar(LIGHT_VERTICAL)]:                 # │ 0x2502
        rect(glyph, x1_light, x2_light, ascent, -descent)
    for glyph in [font.createChar(HEAVY_VERTICAL)]:                 # ┃ 0x2503
        rect(glyph, x1_heavy, x2_heavy, ascent, -descent)
    for glyph in [font.createChar(LIGHT_TRIPLE_DASH_HORIZONTAL)]:   # ┄ 0x2504
        for i in range(0, 3):
            rect(glyph, dash_horiz[3][i*2], dash_horiz[3][i*2+1], y1_light, y2_light)
    for glyph in [font.createChar(HEAVY_TRIPLE_DASH_HORIZONTAL)]:   # ┅ 0x2505
        for i in range(0, 3):
            rect(glyph, dash_horiz[3][i*2], dash_horiz[3][i*2+1], y1_heavy, y2_heavy)
    for glyph in [font.createChar(LIGHT_TRIPLE_DASH_VERTICAL)]:     # ┆ 0x2506
        for i in range(0, 3):
            rect(glyph, x1_light, x2_light, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in [font.createChar(HEAVY_TRIPLE_DASH_VERTICAL)]:     # ┇ 0x2507
        for i in range(0, 3):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in [font.createChar(LIGHT_QUADRUPLE_DASH_HORIZONTAL)]:# ┈ 0x2508
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_light, y2_light)
    for glyph in [font.createChar(HEAVY_QUADRUPLE_DASH_HORIZONTAL)]:# ┉ 0x2509
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_heavy, y2_heavy)
    for glyph in [font.createChar(LIGHT_QUADRUPLE_DASH_VERTICAL)]:  # ┊ 0x250A
        for i in range(0, 4):
            rect(glyph, x1_light, x2_light, dash_vert[4][i*2], dash_vert[4][i*2+1])
    for glyph in [font.createChar(HEAVY_QUADRUPLE_DASH_VERTICAL)]:  # ┋ 0x250B
        for i in range(0, 4):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[4][i*2], dash_vert[4][i*2+1])
    for glyph in [font.createChar(LIGHT_DOWN_AND_RIGHT)]:                    # ┌ 0x250C
        poly(glyph, ((x1_light, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light)))
    for glyph in [font.createChar(DOWN_LIGHT_AND_RIGHT_HEAVY)]:              # ┍ 0x250D
        poly(glyph, ((x1_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in [font.createChar(DOWN_HEAVY_AND_RIGHT_LIGHT)]:              # ┎ 0x250E
        poly(glyph, ((x1_heavy, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_heavy, y2_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in [font.createChar(HEAVY_DOWN_AND_RIGHT)]:                    # ┏ 0x250F
        poly(glyph, ((x1_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in [font.createChar(LIGHT_DOWN_AND_LEFT)]:                     # ┐ 0x2510
        poly(glyph, ((0, y1_light),
                     (x2_light, y1_light),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_light),
                     (0, y2_light)))
    for glyph in [font.createChar(DOWN_LIGHT_AND_LEFT_HEAVY)]:               # ┑ 0x2511
        poly(glyph, ((0, y1_heavy),
                     (x2_light, y1_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_heavy),
                     (0, y2_heavy)))
    for glyph in [font.createChar(DOWN_HEAVY_AND_LEFT_LIGHT)]:               # ┒ 0x2512
        poly(glyph, ((0, y1_light),
                     (x2_heavy, y1_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_light),
                     (0, y2_light)))
    for glyph in [font.createChar(HEAVY_DOWN_AND_LEFT)]:                     # ┓ 0x2513
        poly(glyph, ((0, y1_heavy),
                     (x2_heavy, y1_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_heavy),
                     (0, y2_heavy)))
    for glyph in [font.createChar(LIGHT_UP_AND_RIGHT)]:                      # └ 0x2514
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x1_light, y2_light)))
    for glyph in [font.createChar(UP_LIGHT_AND_RIGHT_HEAVY)]:                # ┕ 0x2515
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x1_light, y2_heavy)))
    for glyph in [font.createChar(UP_HEAVY_AND_RIGHT_LIGHT)]:                # ┖ 0x2516
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x1_heavy, y2_light)))
    for glyph in [font.createChar(HEAVY_UP_AND_RIGHT)]:                      # ┗ 0x2517
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x1_heavy, y2_heavy)))
    for glyph in [font.createChar(LIGHT_UP_AND_LEFT)]:                       # ┘ 0x2518
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y2_light),
                     (0, y2_light),
                     (0, y1_light),
                     (x1_light, y1_light)))
    for glyph in [font.createChar(UP_LIGHT_AND_LEFT_HEAVY)]:                 # ┙ 0x2519
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y2_heavy),
                     (0, y2_heavy),
                     (0, y1_heavy),
                     (x1_light, y1_heavy)))
    for glyph in [font.createChar(UP_HEAVY_AND_LEFT_LIGHT)]:                 # ┚ 0x251A
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y2_light),
                     (0, y2_light),
                     (0, y1_light),
                     (x1_heavy, y1_light)))
    for glyph in [font.createChar(HEAVY_UP_AND_LEFT)]:                       # ┛ 0x251B
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y2_heavy),
                     (0, y2_heavy),
                     (0, y1_heavy),
                     (x1_heavy, y1_heavy)))
    for glyph in [font.createChar(LIGHT_VERTICAL_AND_RIGHT)]:                # ├ 0x251C
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_light, y2_light),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in [font.createChar(VERTICAL_LIGHT_AND_RIGHT_HEAVY)]:          # ┝ 0x251D
        poly(glyph, ((x1_light, ascent),
                     (x2_light, ascent),
                     (x2_light, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent)))
    for glyph in [font.createChar(UP_HEAVY_AND_RIGHT_DOWN_LIGHT)]:           # ┞ 0x251E
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
    for glyph in [font.createChar(DOWN_HEAVY_AND_RIGHT_UP_LIGHT)]:           # ┟ 0x251F
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
    for glyph in [font.createChar(VERTICAL_HEAVY_AND_RIGHT_LIGHT)]:          # ┠ 0x2520
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy)))
    for glyph in [font.createChar(DOWN_LIGHT_AND_RIGHT_UP_HEAVY)]:           # ┡ 0x2521
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
    for glyph in [font.createChar(UP_LIGHT_AND_RIGHT_DOWN_HEAVY)]:           # ┢ 0x2522
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
    for glyph in [font.createChar(HEAVY_VERTICAL_AND_RIGHT)]:                # ┣ 0x2523
        poly(glyph, ((x1_heavy, ascent),
                     (x2_heavy, ascent),
                     (x2_heavy, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent)))
    for glyph in [font.createChar(LIGHT_VERTICAL_AND_LEFT)]:                 # ┤ 0x2524
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in [font.createChar(VERTICAL_LIGHT_AND_LEFT_HEAVY)]:           # ┥ 0x2525
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, -descent),
                     (X, x1_light),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in [font.createChar(UP_HEAVY_AND_LEFT_DOWN_LIGHT)]:            # ┦ 0x2526
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
    for glyph in [font.createChar(DOWN_HEAVY_AND_LEFT_UP_LIGHT)]:            # ┧ 0x2527
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
    for glyph in [font.createChar(VERTICAL_HEAVY_AND_LEFT_LIGHT)]:           # ┨ 0x2528
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in [font.createChar(DOWN_LIGHT_AND_LEFT_UP_HEAVY)]:            # ┩ 0x2529
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
    for glyph in [font.createChar(UP_LIGHT_AND_LEFT_DOWN_HEAVY)]:            # ┪ 0x252A
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
    for glyph in [font.createChar(HEAVY_VERTICAL_AND_LEFT)]:                 # ┫ 0x252B
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, -descent),
                     (X, x1_heavy),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in [font.createChar(LIGHT_DOWN_AND_HORIZONTAL)]:               # ┬ 0x252C
        poly(glyph, ((0, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_light, y2_light),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_light),
                     (0, y2_light)))
    for glyph in [font.createChar(LEFT_HEAVY_AND_RIGHT_DOWN_LIGHT)]:         # ┭ 0x252D
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
    for glyph in [font.createChar(RIGHT_HEAVY_AND_LEFT_DOWN_LIGHT)]:         # ┮ 0x252E
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
    for glyph in [font.createChar(DOWN_LIGHT_AND_HORIZONTAL_HEAVY)]:         # ┯ 0x252F
        poly(glyph, ((0, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_light, y2_heavy),
                     (x2_light, -descent),
                     (x1_light, -descent),
                     (x1_light, y2_heavy),
                     (0, y2_heavy)))
    for glyph in [font.createChar(DOWN_HEAVY_AND_HORIZONTAL_LIGHT)]:         # ┰ 0x2530
        poly(glyph, ((0, y1_light),
                     (width, y1_light),
                     (width, y2_light),
                     (x2_heavy, y2_light),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_light),
                     (0, y2_light)))
    for glyph in [font.createChar(RIGHT_LIGHT_AND_LEFT_DOWN_HEAVY)]:         # ┱ 0x2531
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
    for glyph in [font.createChar(LEFT_LIGHT_AND_RIGHT_DOWN_HEAVY)]:         # ┲ 0x2532
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
    for glyph in [font.createChar(HEAVY_DOWN_AND_HORIZONTAL)]:               # ┳ 0x2533
        poly(glyph, ((0, y1_heavy),
                     (width, y1_heavy),
                     (width, y2_heavy),
                     (x2_heavy, y2_heavy),
                     (x2_heavy, -descent),
                     (x1_heavy, -descent),
                     (x1_heavy, y2_heavy),
                     (0, y2_heavy)))
    for glyph in [font.createChar(LIGHT_UP_AND_HORIZONTAL)]:                 # ┴ 0x2534
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_light)))
    for glyph in [font.createChar(LEFT_HEAVY_AND_RIGHT_UP_LIGHT)]:           # ┵ 0x2535
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
    for glyph in [font.createChar(RIGHT_HEAVY_AND_LEFT_UP_LIGHT)]:           # ┶ 0x2536
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
    for glyph in [font.createChar(UP_LIGHT_AND_HORIZONTAL_HEAVY)]:           # ┷ 0x2537
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_light)))
    for glyph in [font.createChar(UP_HEAVY_AND_HORIZONTAL_LIGHT)]:           # ┸ 0x2538
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_light),
                     (X, width),
                     (Y, y2_light),
                     (X, 0),
                     (Y, y1_light),
                     (X, x1_heavy)))
    for glyph in [font.createChar(RIGHT_LIGHT_AND_LEFT_UP_HEAVY)]:           # ┹ 0x2539
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
    for glyph in [font.createChar(LEFT_LIGHT_AND_RIGHT_UP_HEAVY)]:           # ┺ 0x253A
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
    for glyph in [font.createChar(HEAVY_UP_AND_HORIZONTAL)]:                 # ┻ 0x253B
        poly(glyph, ((x1_heavy, ascent),
                     (X, x2_heavy),
                     (Y, y1_heavy),
                     (X, width),
                     (Y, y2_heavy),
                     (X, 0),
                     (Y, y1_heavy),
                     (X, x1_heavy)))
    for glyph in [font.createChar(LIGHT_VERTICAL_AND_HORIZONTAL)]:           # ┼ 0x253C
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
    for glyph in [font.createChar(LEFT_HEAVY_AND_RIGHT_VERTICAL_LIGHT)]:     # ┽ 0x253D
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
    for glyph in [font.createChar(RIGHT_HEAVY_AND_LEFT_VERTICAL_LIGHT)]:     # ┾ 0x253E
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
    for glyph in [font.createChar(VERTICAL_LIGHT_AND_HORIZONTAL_HEAVY)]:     # ┿ 0x253F
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
    for glyph in [font.createChar(UP_HEAVY_AND_DOWN_HORIZONTAL_LIGHT)]:      # ╀ 0x2540
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
    for glyph in [font.createChar(DOWN_HEAVY_AND_UP_HORIZONTAL_LIGHT)]:      # ╁ 0x2541
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
    for glyph in [font.createChar(VERTICAL_HEAVY_AND_HORIZONTAL_LIGHT)]:     # ╂ 0x2542
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
    for glyph in [font.createChar(LEFT_UP_HEAVY_AND_RIGHT_DOWN_LIGHT)]:      # ╃ 0x2543
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
    for glyph in [font.createChar(RIGHT_UP_HEAVY_AND_LEFT_DOWN_LIGHT)]:      # ╄ 0x2544
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
    for glyph in [font.createChar(LEFT_DOWN_HEAVY_AND_RIGHT_UP_LIGHT)]:      # ╅ 0x2545
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
    for glyph in [font.createChar(RIGHT_DOWN_HEAVY_AND_LEFT_UP_LIGHT)]:      # ╆ 0x2546
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
    for glyph in [font.createChar(DOWN_LIGHT_AND_UP_HORIZONTAL_HEAVY)]:      # ╇ 0x2547
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
    for glyph in [font.createChar(UP_LIGHT_AND_DOWN_HORIZONTAL_HEAVY)]:      # ╈ 0x2548
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
    for glyph in [font.createChar(RIGHT_LIGHT_AND_LEFT_VERTICAL_HEAVY)]:     # ╉ 0x2549
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
    for glyph in [font.createChar(LEFT_LIGHT_AND_RIGHT_VERTICAL_HEAVY)]:     # ╊ 0x254A
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
    for glyph in [font.createChar(HEAVY_VERTICAL_AND_HORIZONTAL)]:           # ╋ 0x254B
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
    for glyph in [font.createChar(LIGHT_DOUBLE_DASH_HORIZONTAL)]:            # ╌ 0x254C
        for i in range(0, 2):
            rect(glyph, dash_horiz[2][i*2], dash_horiz[2][i*2+1], y1_light, y2_light)
    for glyph in [font.createChar(HEAVY_DOUBLE_DASH_HORIZONTAL)]:            # ╍ 0x254D
        for i in range(0, 2):
            rect(glyph, dash_horiz[2][i*2], dash_horiz[2][i*2+1], y1_heavy, y2_heavy)
    for glyph in [font.createChar(LIGHT_DOUBLE_DASH_VERTICAL)]:              # ╎ 0x254E
        for i in range(0, 2):
            rect(glyph, x1_light, x2_light, dash_vert[2][i*2], dash_vert[2][i*2+1])
    for glyph in [font.createChar(HEAVY_DOUBLE_DASH_VERTICAL)]:              # ╏ 0x254F
        for i in range(0, 2):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[2][i*2], dash_vert[2][i*2+1])
    for glyph in [font.createChar(DOUBLE_HORIZONTAL)]:                       # ═ 0x2550
        rect(glyph, 0, width, y1_double, y2_double)
        rect(glyph, 0, width, y3_double, y4_double)
    for glyph in [font.createChar(DOUBLE_VERTICAL)]:                         # ║ 0x2551
        rect(glyph, x1_double, x2_double, ascent, -descent)
        rect(glyph, x3_double, x4_double, ascent, -descent)
    for glyph in [font.createChar(DOWN_SINGLE_AND_RIGHT_DOUBLE)]:            # ╒ 0x2552
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
    for glyph in [font.createChar(DOWN_DOUBLE_AND_RIGHT_SINGLE)]:            # ╓ 0x2553
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
    for glyph in [font.createChar(DOUBLE_DOWN_AND_RIGHT)]:                   # ╔ 0x2554
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
    for glyph in [font.createChar(DOWN_SINGLE_AND_LEFT_DOUBLE)]:             # ╕ 0x2555
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
    for glyph in [font.createChar(DOWN_DOUBLE_AND_LEFT_SINGLE)]:             # ╖ 0x2556
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
    for glyph in [font.createChar(DOUBLE_DOWN_AND_LEFT)]:                    # ╗ 0x2557
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
    for glyph in [font.createChar(UP_SINGLE_AND_RIGHT_DOUBLE)]:              # ╘ 0x2558
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
    for glyph in [font.createChar(UP_DOUBLE_AND_RIGHT_SINGLE)]:              # ╙ 0x2559
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
    for glyph in [font.createChar(DOUBLE_UP_AND_RIGHT)]:                     # ╚ 0x255A
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
    for glyph in [font.createChar(UP_SINGLE_AND_LEFT_DOUBLE)]:               # ╛ 0x255B
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
    for glyph in [font.createChar(UP_DOUBLE_AND_LEFT_SINGLE)]:               # ╜ 0x255C
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y2_light, 0, y1_light, x1_double)))
    for glyph in [font.createChar(DOUBLE_UP_AND_LEFT)]:                      # ╝ 0x255D
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y4_double, 0, y3_double, x3_double)))
    for glyph in [font.createChar(VERTICAL_SINGLE_AND_RIGHT_DOUBLE)]:        # ╞ 0x255E
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, x2_light, y3_double, width, y4_double, x2_light, -descent, x1_light)))
    for glyph in [font.createChar(VERTICAL_DOUBLE_AND_RIGHT_SINGLE)]:        # ╟ 0x255F
        rect(glyph, x1_double, x2_double, ascent, -descent)
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_light, width, y2_light, x4_double, -descent, x3_double)))
    for glyph in [font.createChar(DOUBLE_VERTICAL_AND_RIGHT)]:               # ╠ 0x2560
        rect(glyph, x1_double, x2_double, ascent, -descent)
        poly(glyph, ((x3_double, ascent), (X, x4_double, y1_double, width, y2_double, x3_double)))
        poly(glyph, ((x3_double, y3_double), (X, width, y4_double, x4_double, -descent, x3_double)))
    for glyph in [font.createChar(VERTICAL_SINGLE_AND_LEFT_DOUBLE)]:         # ╡ 0x2561
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, -descent, x1_light, y4_double, 0, y3_double, x1_light, y2_double, 0, y1_double, x1_light)))
    for glyph in [font.createChar(VERTICAL_DOUBLE_AND_LEFT_SINGLE)]:         # ╢ 0x2562
        rect(glyph, x3_double, x4_double, ascent, -descent)
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, -descent, x1_double, y2_light, 0, y1_light, x1_double)))

    for glyph in [font.createChar(DOUBLE_VERTICAL_AND_LEFT)]:                # ╣ 0x2563
        rect(glyph, x3_double, x4_double, ascent, -descent)
        poly(glyph, ((x1_double, ascent), (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
    for glyph in [font.createChar(DOWN_SINGLE_AND_HORIZONTAL_DOUBLE)]:       # ╤ 0x2564
        rect(glyph, 0, width, y1_double, y2_double)
        poly(glyph, ((0, y3_double),
                     (X, width, y4_double, x2_light, -descent, x1_light, y4_double, 0)))
    for glyph in [font.createChar(DOWN_DOUBLE_AND_HORIZONTAL_SINGLE)]:       # ╥ 0x2565
        poly(glyph, ((0, y1_light),
                     (X, width, y2_light, x4_double, -descent, x3_double, y2_light, x2_double, -descent, x1_double, y2_light, 0)))
    for glyph in [font.createChar(DOUBLE_DOWN_AND_HORIZONTAL)]:              # ╦ 0x2566
        rect(glyph, 0, width, y1_double, y2_double)
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
        poly(glyph, ((x3_double, y3_double),
                     (X, width, y4_double, x4_double, -descent, x3_double)))
    for glyph in [font.createChar(UP_SINGLE_AND_HORIZONTAL_DOUBLE)]:         # ╧ 0x2567
        rect(glyph, 0, width, y3_double, y4_double)
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, 0, y1_double, x1_light)))
    for glyph in [font.createChar(UP_DOUBLE_AND_HORIZONTAL_SINGLE)]:         # ╨ 0x2568
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y1_light, width, y2_light, 0, y1_light, x1_double)))
    for glyph in [font.createChar(DOUBLE_UP_AND_HORIZONTAL)]:                # ╩ 0x2569
        rect(glyph, 0, width, y3_double, y4_double)
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_double, width, y2_double, x3_double)))
    for glyph in [font.createChar(VERTICAL_SINGLE_AND_HORIZONTAL_DOUBLE)]:   # ╪ 0x256A
        poly(glyph, ((x1_light, ascent),
                     (X, x2_light, y1_double, width, y2_double, x2_light, y3_double, width,
                      y4_double, x2_light, -descent, x1_light, y4_double, 0, y3_double, x1_light, y2_double, 0, y1_double, x1_light)))
    for glyph in [font.createChar(VERTICAL_DOUBLE_AND_HORIZONTAL_SINGLE)]:   # ╫ 0x256B
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y1_light, x3_double, ascent, x4_double, y1_light, width, y2_light, x4_double, -descent, x3_double, y2_light, x2_double,
                      -descent, x1_double, y2_light, 0, y1_light, x1_double)))
    for glyph in [font.createChar(DOUBLE_VERTICAL_AND_HORIZONTAL)]:          # ╬ 0x256C
        poly(glyph, ((0, y3_double), (X, x2_double, -descent, x1_double, y4_double, 0)))
        poly(glyph, ((x3_double, y3_double),
                     (X, width, y4_double, x4_double, -descent, x3_double)))
        poly(glyph, ((x1_double, ascent),
                     (X, x2_double, y2_double, 0, y1_double, x1_double)))
        poly(glyph, ((x3_double, ascent),
                     (X, x4_double, y1_double, width, y2_double, x3_double)))
    for glyph in [font.createChar(LIGHT_ARC_DOWN_AND_RIGHT)]:                # ╭ 0x256D
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
    for glyph in [font.createChar(LIGHT_ARC_DOWN_AND_LEFT)]:                 # ╮ 0x256E
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
    for glyph in [font.createChar(LIGHT_ARC_UP_AND_LEFT)]:                   # ╯ 0x256F
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
    for glyph in [font.createChar(LIGHT_ARC_UP_AND_RIGHT)]:                  # ╰ 0x2570
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
    x1_diag = 0 - STROKE_WIDTH / 2 * math.cos(theta)
    x2_diag = 0 + STROKE_WIDTH / 2 * math.cos(theta)
    x3_diag = width - STROKE_WIDTH / 2 * math.cos(theta)
    x4_diag = width + STROKE_WIDTH / 2 * math.cos(theta)
    y1_diag = ascent + STROKE_WIDTH / 2 * math.sin(theta)
    y2_diag = ascent - STROKE_WIDTH / 2 * math.sin(theta)
    y3_diag = -descent + STROKE_WIDTH / 2 * math.sin(theta)
    y4_diag = -descent - STROKE_WIDTH / 2 * math.sin(theta)

    for glyph in [font.createChar(LIGHT_DIAGONAL_UPPER_RIGHT_TO_LOWER_LEFT)]:# ╱ 0x2571
        poly(glyph, ((x3_diag, y1_diag),
                     (x4_diag, y2_diag),
                     (x2_diag, y4_diag),
                     (x1_diag, y3_diag)))
    for glyph in [font.createChar(LIGHT_DIAGONAL_UPPER_LEFT_TO_LOWER_RIGHT)]:# ╲ 0x2572
        poly(glyph, ((x1_diag, y2_diag),
                     (x2_diag, y1_diag),
                     (x4_diag, y3_diag),
                     (x3_diag, y4_diag)))
    for glyph in [font.createChar(LIGHT_DIAGONAL_CROSS)]:                    # ╳ 0x2573
        poly(glyph, ((x3_diag, y1_diag),
                     (x4_diag, y2_diag),
                     (x2_diag, y4_diag),
                     (x1_diag, y3_diag)))
        poly(glyph, ((x1_diag, y2_diag),
                     (x2_diag, y1_diag),
                     (x4_diag, y3_diag),
                     (x3_diag, y4_diag)))
        glyph.removeOverlap()
    for glyph in [font.createChar(LIGHT_LEFT)]:                              # ╴ 0x2574
        pass
    for glyph in [font.createChar(LIGHT_UP)]:                                # ╵ 0x2575
        pass
    for glyph in [font.createChar(LIGHT_RIGHT)]:                             # ╶ 0x2576
        pass
    for glyph in [font.createChar(LIGHT_DOWN)]:                              # ╷ 0x2577
        pass
    for glyph in [font.createChar(HEAVY_LEFT)]:                              # ╸ 0x2578
        pass
    for glyph in [font.createChar(HEAVY_UP)]:                                # ╹ 0x2579
        pass
    for glyph in [font.createChar(HEAVY_RIGHT)]:                             # ╺ 0x257A
        pass
    for glyph in [font.createChar(HEAVY_DOWN)]:                              # ╻ 0x257B
        pass
    for glyph in [font.createChar(LIGHT_LEFT_AND_HEAVY_RIGHT)]:              # ╼ 0x257C
        pass
    for glyph in [font.createChar(LIGHT_UP_AND_HEAVY_DOWN)]:                 # ╽ 0x257D
        pass
    for glyph in [font.createChar(HEAVY_LEFT_AND_LIGHT_RIGHT)]:              # ╾ 0x257E
        pass
    for glyph in [font.createChar(HEAVY_UP_AND_LIGHT_DOWN)]:                 # ╿ 0x257F
        pass

    for codepoint in range(0x2500, 0x2580):
        glyph = font.createChar(codepoint)
        old_width = glyph.width
        glyph.width = width
        new_width = glyph.width
        print("%s: %d => %d" % (glyph.glyphname, old_width, new_width))

def rect(glyph, x1, x2, y1, y2):
    print("rect(%s, %d, %d, %d, %d)" % (glyph, x1, x2, y1, y2))
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()
    pen = None

def poly(glyph, pairs):
    pen = glyph.glyphPen(replace=False)
    x = pairs[0][0]
    y = pairs[0][1]
    pen.moveTo((x, y))
    for pair in pairs[1:]:
        if len(pair) > 2:
            if pair[0] == X:
                horizontal = True
            elif pair[0] == Y:
                horizontal = False
            else:
                raise Exception("pair of coordinates of more than 2 must start with X or Y")
            for i in range(1, len(pair)):
                if horizontal:
                    x = pair[i]
                else:
                    y = pair[i]
                pen.lineTo((x, y))
                horizontal = not horizontal
        elif pair[0] == X:
            x = pair[1]
            pen.lineTo((x, y))
        elif pair[0] == Y:
            y = pair[1]
            pen.lineTo((x, y))
        else:
            (x, y) = pair
            pen.lineTo((x, y))
    pen.closePath()
    pen = None

def clip(glyph, x1, y1, x2, y2):
    contour = fontforge.contour()
    contour.moveTo((x1, y1))
    contour.lineTo((x2, y1))
    contour.lineTo((x2, y2))
    contour.lineTo((x1, y2))
    contour.closed = True
    contour = None
    glyph.layers["Fore"] += clipContour
    glyph.intersect()

main()
