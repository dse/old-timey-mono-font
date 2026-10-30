#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys

import os, sys
dir = os.path.dirname(__file__) + "/../lib"
if dir not in sys.path:
    sys.path.append(dir)

import otm
from otm.util import draw_rect, draw_rel_rect, get_font_glyph_width, draw_circle, remove_glyphs, initialize_glyphs, finalize_glyphs
from otm.quarter_arc import elliptic_quarter_arc_contour

LSW = 96
RANGES = [
    range(0xfaf00, 0xfaf1c),
]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    new_glyph_width = get_font_glyph_width(font)
    initialize_glyphs(font, RANGES, args, new_glyph_width)

    # DRAW THINGS HERE
    draw_FAF00(font.createChar(0xfaf00))
    draw_FAF01(font.createChar(0xfaf01))
    draw_FAF02(font.createChar(0xfaf02))
    draw_FAF03(font.createChar(0xfaf03))
    draw_FAF04(font.createChar(0xfaf04))
    draw_FAF05(font.createChar(0xfaf05))
    draw_FAF06(font.createChar(0xfaf06))
    draw_FAF07(font.createChar(0xfaf07))
    draw_FAF08(font.createChar(0xfaf08))
    draw_FAF09(font.createChar(0xfaf09))
    draw_FAF0A(font.createChar(0xfaf0a))
    draw_FAF0B(font.createChar(0xfaf0b))
    draw_FAF0C(font.createChar(0xfaf0c))
    draw_FAF0D(font.createChar(0xfaf0d))
    draw_FAF0E(font.createChar(0xfaf0e))
    draw_FAF0F(font.createChar(0xfaf0f))
    draw_FAF10(font.createChar(0xfaf10))
    draw_FAF11(font.createChar(0xfaf11))
    draw_FAF12(font.createChar(0xfaf12))
    draw_FAF13(font.createChar(0xfaf13))
    draw_FAF14(font.createChar(0xfaf14))
    draw_FAF15(font.createChar(0xfaf15))
    draw_FAF16(font.createChar(0xfaf16))
    draw_FAF17(font.createChar(0xfaf17))
    draw_FAF18(font.createChar(0xfaf18))
    draw_FAF19(font.createChar(0xfaf19))
    draw_FAF1A(font.createChar(0xfaf1a))
    draw_FAF1B(font.createChar(0xfaf1b))

    finalize_glyphs(font, RANGES, args)

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

    font.close()

###############################################################################

# BOX DRAWINGS LIGHT ARC UP AND LEFT FOR REVISION LOGS
def draw_FAF00(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)

# BOX DRAWINGS LIGHT ARC UP AND RIGHT FOR REVISION LOGS
def draw_FAF01(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT ARC DOWN AND LEFT FOR REVISION LOGS
def draw_FAF02(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)

# BOX DRAWINGS LIGHT ARC DOWN AND RIGHT FOR REVISION LOGS
def draw_FAF03(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)

# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARC UP AND LEFT
def draw_FAF04(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)

# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARC UP AND RIGHT
def draw_FAF05(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARC DOWN AND LEFT
def draw_FAF06(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)

# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARC DOWN AND RIGHT
def draw_FAF07(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)

# BOX DRAWINGS LIGHT HORIZONTAL AND LIGHT ARC UP AND LEFT
def draw_FAF08(glyph):
    draw_light_horizontal(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)

# BOX DRAWINGS LIGHT HORIZONTAL AND LIGHT ARC UP AND RIGHT
def draw_FAF09(glyph):
    draw_light_horizontal(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT HORIZONTAL AND LIGHT ARC DOWN AND LEFT
def draw_FAF0A(glyph):
    draw_light_horizontal(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)

# BOX DRAWINGS LIGHT HORIZONTAL AND LIGHT ARC DOWN AND RIGHT
def draw_FAF0B(glyph):
    draw_light_horizontal(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)

# BOX DRAWINGS LIGHT HORIZONTAL AND VERTICAL AND LIGHT ARC UP AND LEFT
def draw_FAF0C(glyph):
    draw_light_horizontal(glyph)
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)

# BOX DRAWINGS LIGHT HORIZONTAL AND VERTICAL AND LIGHT ARC UP AND RIGHT
def draw_FAF0D(glyph):
    draw_light_horizontal(glyph)
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT HORIZONTAL AND VERTICAL AND LIGHT ARC DOWN AND LEFT
def draw_FAF0E(glyph):
    draw_light_horizontal(glyph)
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)

# BOX DRAWINGS LIGHT HORIZONTAL AND VERTICAL AND LIGHT ARC DOWN AND RIGHT
def draw_FAF0F(glyph):
    draw_light_horizontal(glyph)
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)



# BOX DRAWINGS LIGHT VERTICAL WITH BULLET
def draw_FAF13(glyph, up=True, down=True):
    font = glyph.font
    xc = glyph.width/2
    yc = (font.ascent-font.descent)/2
    r_out = glyph.width/3
    r_in = r_out - LSW
    r = (r_out + r_in) / 2
    if down:
        draw_rect(glyph, glyph.width/2 - LSW/2, yc - r, glyph.width/2 + LSW/2, -font.descent)
    if up:
        draw_rect(glyph, glyph.width/2 - LSW/2, yc + r, glyph.width/2 + LSW/2, font.ascent)
    draw_circle(glyph, (xc, yc), glyph.width/3)

# BOX DRAWINGS LIGHT UP VERTICAL WITH BULLET
def draw_FAF11(glyph):
    draw_FAF13(glyph, down=False)

# BOX DRAWINGS LIGHT DOWN VERTICAL WITH BULLET
def draw_FAF12(glyph):
    draw_FAF13(glyph, up=False)

# BULLET FOR REVISION LOGS
def draw_FAF10(glyph):
    draw_FAF13(glyph, up=False, down=False)



# BOX DRAWINGS LIGHT VERTICAL WITH CIRCLE
def draw_FAF17(glyph, up=True, down=True):
    font = glyph.font
    r_out = glyph.width/3
    r_in = r_out - LSW
    r = (r_out + r_in) / 2
    xc = glyph.width/2
    yc = (font.ascent-font.descent)/2
    if down:
        draw_rect(glyph, glyph.width/2 - LSW/2, yc - r, glyph.width/2 + LSW/2, -font.descent)
    if up:
        draw_rect(glyph, glyph.width/2 - LSW/2, yc + r, glyph.width/2 + LSW/2, font.ascent)
    draw_circle(glyph, (xc, yc), r_out)
    draw_circle(glyph, (xc, yc), r_in, withershins=True)

# BOX DRAWINGS LIGHT UP VERTICAL WITH CIRCLE
def draw_FAF15(glyph):
    draw_FAF17(glyph, down=False)

# BOX DRAWINGS LIGHT DOWN VERTICAL WITH CIRCLE
def draw_FAF16(glyph):
    draw_FAF17(glyph, up=False)

# CIRCLE FOR REVISION LOGS
def draw_FAF14(glyph):
    draw_FAF17(glyph, up=False, down=False)


# BOX DRAWINGS LIGHT ARCS UP AND LEFT AND RIGHT
def draw_FAF18(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT ARCS DOWN AND LEFT AND RIGHT
def draw_FAF19(glyph):
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)


# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARCS UP AND LEFT AND RIGHT
def draw_FAF1A(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_LEFT)
    draw_box_drawing_arc(glyph, otm.quarter_arc.UP_AND_RIGHT)

# BOX DRAWINGS LIGHT VERTICAL AND LIGHT ARCS DOWN AND LEFT AND RIGHT
def draw_FAF1B(glyph):
    draw_light_vertical(glyph)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_LEFT)
    draw_box_drawing_arc(glyph, otm.quarter_arc.DOWN_AND_RIGHT)


###############################################################################

def draw_light_vertical(glyph):
    font = glyph.font
    draw_rect(glyph, glyph.width/2 - LSW/2, -font.descent, glyph.width/2 + LSW/2, font.ascent)

def draw_light_horizontal(glyph):
    font = glyph.font
    y = (font.ascent - font.descent) / 2
    draw_rect(glyph, 0, y - LSW/2, glyph.width, y + LSW/2)

def draw_box_drawing_arc(glyph, direction):
    contour = box_drawing_arc_contour(glyph, direction)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def box_drawing_arc_contour(glyph, direction):
    font = glyph.font
    r_in_x = glyph.width/2 - LSW/2
    r_out_x = glyph.width/2 + LSW/2
    r_in_y = font.em/2 - LSW/2
    r_out_y = font.em/2 + LSW/2
    direction = otm.quarter_arc.normalize_direction(direction)
    if direction in [otm.quarter_arc.UP_AND_LEFT, otm.quarter_arc.UP_AND_RIGHT]:
        cy = font.ascent
    else:
        cy = -font.descent
    if direction in [otm.quarter_arc.UP_AND_LEFT, otm.quarter_arc.DOWN_AND_LEFT]:
        cx = 0
    else:
        cx = glyph.width
    return elliptic_quarter_arc_contour(glyph, (cx, cy), r_in_x, r_out_x, r_in_y, r_out_y, direction,
                                        kappa_x=.8, kappa_y=.8)

###############################################################################
main()
