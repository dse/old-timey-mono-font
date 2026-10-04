#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import draw_rect, draw_rel_rect, get_font_glyph_width

SHADE_DOT_SIZE_PX = 84

RANGES = [
    range(0x2580, 0x25a0),
    range(0x1fb70, 0x1fb97),
    range(0x1fbce, 0x1fbd0),
    range(0x1fbe4, 0x1fbe8),
]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-c", "--clear", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    if args.clear:
        for r in RANGES:
            for code in r:
                try:
                    font.removeGlyph(code)
                except ValueError as e:
                    if str(e) != "This glyph is not in the font":
                        raise
        return
                
    new_glyph_width = get_font_glyph_width(font)

    for r in RANGES:
        for code in r:
            if code == 0x1fb93:     # reserved
                continue
            glyph = font.createChar(code)
            glyph.foreground = fontforge.layer()
            glyph.width = new_glyph_width

    draw_2580(font.createChar(0x2580))
    draw_2581(font.createChar(0x2581))
    draw_2582(font.createChar(0x2582))
    draw_2583(font.createChar(0x2583))
    draw_2584(font.createChar(0x2584))
    draw_2585(font.createChar(0x2585))
    draw_2586(font.createChar(0x2586))
    draw_2587(font.createChar(0x2587))
    draw_2588(font.createChar(0x2588))
    draw_2589(font.createChar(0x2589))
    draw_258A(font.createChar(0x258a))
    draw_258B(font.createChar(0x258b))
    draw_258C(font.createChar(0x258c))
    draw_258D(font.createChar(0x258d))
    draw_258E(font.createChar(0x258e))
    draw_258F(font.createChar(0x258f))
    draw_2590(font.createChar(0x2590))
    draw_2591(font.createChar(0x2591))
    draw_2592(font.createChar(0x2592))
    draw_2593(font.createChar(0x2593))
    draw_2594(font.createChar(0x2594))
    draw_2595(font.createChar(0x2595))
    draw_2596(font.createChar(0x2596))
    draw_2597(font.createChar(0x2597))
    draw_2598(font.createChar(0x2598))
    draw_2599(font.createChar(0x2599))
    draw_259A(font.createChar(0x259a))
    draw_259B(font.createChar(0x259b))
    draw_259C(font.createChar(0x259c))
    draw_259D(font.createChar(0x259d))
    draw_259E(font.createChar(0x259e))
    draw_259F(font.createChar(0x259f))

    draw_1FB70(font.createChar(0x1FB70))
    draw_1FB71(font.createChar(0x1FB71))
    draw_1FB72(font.createChar(0x1FB72))
    draw_1FB73(font.createChar(0x1FB73))
    draw_1FB74(font.createChar(0x1FB74))
    draw_1FB75(font.createChar(0x1FB75))
    draw_1FB76(font.createChar(0x1FB76))
    draw_1FB77(font.createChar(0x1FB77))
    draw_1FB78(font.createChar(0x1FB78))
    draw_1FB79(font.createChar(0x1FB79))
    draw_1FB7A(font.createChar(0x1FB7A))
    draw_1FB7B(font.createChar(0x1FB7B))
    draw_1FB7C(font.createChar(0x1FB7C))
    draw_1FB7D(font.createChar(0x1FB7D))
    draw_1FB7E(font.createChar(0x1FB7E))
    draw_1FB7F(font.createChar(0x1FB7F))
    draw_1FB80(font.createChar(0x1FB80))
    draw_1FB81(font.createChar(0x1FB81))
    draw_1FB82(font.createChar(0x1FB82))
    draw_1FB83(font.createChar(0x1FB83))
    draw_1FB84(font.createChar(0x1FB84))
    draw_1FB85(font.createChar(0x1FB85))
    draw_1FB86(font.createChar(0x1FB86))
    draw_1FB87(font.createChar(0x1FB87))
    draw_1FB88(font.createChar(0x1FB88))
    draw_1FB89(font.createChar(0x1FB89))
    draw_1FB8A(font.createChar(0x1FB8A))
    draw_1FB8B(font.createChar(0x1FB8B))

    draw_1FB8C(font.createChar(0x1FB8C))
    draw_1FB8D(font.createChar(0x1FB8D))
    draw_1FB8E(font.createChar(0x1FB8E))
    draw_1FB8F(font.createChar(0x1FB8F))
    draw_1FB90(font.createChar(0x1FB90))
    draw_1FB91(font.createChar(0x1FB91))
    draw_1FB92(font.createChar(0x1FB92))
    draw_1FB94(font.createChar(0x1FB94))
    draw_1FB95(font.createChar(0x1FB95))
    draw_1FB96(font.createChar(0x1FB96))

    draw_1FBCE(font.createChar(0x1FBCE))
    draw_1FBCF(font.createChar(0x1FBCF))

    draw_1FBE4(font.createChar(0x1FBE4))
    draw_1FBE5(font.createChar(0x1FBE5))
    draw_1FBE6(font.createChar(0x1FBE6))
    draw_1FBE7(font.createChar(0x1FBE7))

    for r in RANGES:
        for code in r:
            if code == 0x1fb93: # reserved
                continue
            glyph = font.createChar(code)
            glyph.removeOverlap()
            glyph.simplify()

    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')

    font.close()

def draw_2580(glyph): draw_rel_rect(glyph, 0, 0.5, 1, 1)
def draw_2581(glyph): draw_rel_rect(glyph, 0, 0, 1, 1/8)
def draw_2582(glyph): draw_rel_rect(glyph, 0, 0, 1, 2/8)
def draw_2583(glyph): draw_rel_rect(glyph, 0, 0, 1, 3/8)
def draw_2584(glyph): draw_rel_rect(glyph, 0, 0, 1, 4/8)
def draw_2585(glyph): draw_rel_rect(glyph, 0, 0, 1, 5/8)
def draw_2586(glyph): draw_rel_rect(glyph, 0, 0, 1, 6/8)
def draw_2587(glyph): draw_rel_rect(glyph, 0, 0, 1, 7/8)
def draw_2588(glyph): draw_rel_rect(glyph, 0, 0, 1, 1)
def draw_2589(glyph): draw_rel_rect(glyph, 0, 0, 7/8, 1)
def draw_258A(glyph): draw_rel_rect(glyph, 0, 0, 6/8, 1)
def draw_258B(glyph): draw_rel_rect(glyph, 0, 0, 5/8, 1)
def draw_258C(glyph): draw_rel_rect(glyph, 0, 0, 4/8, 1)
def draw_258D(glyph): draw_rel_rect(glyph, 0, 0, 3/8, 1)
def draw_258E(glyph): draw_rel_rect(glyph, 0, 0, 2/8, 1)
def draw_258F(glyph): draw_rel_rect(glyph, 0, 0, 1/8, 1)
def draw_2590(glyph): draw_rel_rect(glyph, 0.5, 0, 1, 1)

def draw_2591(glyph): draw_light_shade(glyph, 0, 0, 1, 1)
def draw_2592(glyph): draw_medium_shade(glyph, 0, 0, 1, 1)
def draw_2593(glyph): draw_dark_shade(glyph, 0, 0, 1, 1)

def draw_light_shade(glyph, x1=0, y1=0, x2=1, y2=1, inverse=False):
    font = glyph.font
    dot_count_x = round(glyph.width / SHADE_DOT_SIZE_PX / 2) * 2
    dot_count_y = round(font.em / SHADE_DOT_SIZE_PX / 2) * 2
    for x in range(round(dot_count_x * x1), round(dot_count_x * x2)):
        x1d = x/dot_count_x
        x2d = (x+1)/dot_count_x
        if x % 2 == (0 if inverse else 1):
            for y in range(round(dot_count_y * y1), round(dot_count_y * y2)):
                if (x + y * 2) % 4 == 0:
                    y1d = y/dot_count_y
                    y2d = (y+1)/dot_count_y
                    draw_rel_rect(glyph, x1d, y1d, x2d, y2d)

def draw_medium_shade(glyph, x1=0, y1=0, x2=1, y2=1, inverse=False, dot_count_x=None, dot_count_y=None):
    font = glyph.font
    if dot_count_x is None:
        dot_count_x = round(glyph.width / SHADE_DOT_SIZE_PX / 2) * 2
    if dot_count_y is None:
        dot_count_y = round(font.em / SHADE_DOT_SIZE_PX / 2) * 2
    for x in range(round(dot_count_x * x1), round(dot_count_x * x2)):
        x1d = x/dot_count_x
        x2d = (x+1)/dot_count_x
        for y in range(round(dot_count_y * y1), round(dot_count_y * y2)):
            if (x + y) % 2 == (1 if inverse else 0):
                y1d = y/dot_count_y
                y2d = (y+1)/dot_count_y
                draw_rel_rect(glyph, x1d, y1d, x2d, y2d)

def draw_dark_shade(glyph, x1=0, y1=0, x2=1, y2=1, inverse=False):
    font = glyph.font
    dot_count_x = round(glyph.width / SHADE_DOT_SIZE_PX / 2) * 2
    dot_count_y = round(font.em / SHADE_DOT_SIZE_PX / 2) * 2
    draw_rel_rect(glyph, 0, 0, 1, 1)
    for x in range(round(dot_count_x * x1), round(dot_count_x * x2)):
        x1d = x/dot_count_x
        x2d = (x+1)/dot_count_x
        if x % 2 == (0 if inverse else 1):
            for y in range(round(dot_count_y * y1), round(dot_count_y * y2)):
                if (x + y * 2) % 4 == 0:
                    y1d = y/dot_count_y
                    y2d = (y+1)/dot_count_y
                    draw_rel_rect(glyph, x1d, y1d, x2d, y2d, withershins=True)

def draw_2594(glyph): draw_rel_rect(glyph, 0, 7/8, 1, 1)
def draw_2595(glyph): draw_rel_rect(glyph, 7/8, 0, 1, 1)
def draw_2596(glyph): 
    draw_lower_left_quadrant(glyph)
def draw_2597(glyph):
    draw_lower_right_quadrant(glyph)
def draw_2598(glyph):
    draw_upper_left_quadrant(glyph)
def draw_2599(glyph):
    draw_upper_left_quadrant(glyph)
    draw_lower_half(glyph)
def draw_259A(glyph):
    draw_upper_left_quadrant(glyph)
    draw_lower_right_quadrant(glyph)
def draw_259B(glyph):
    draw_upper_half(glyph)
    draw_lower_left_quadrant(glyph)
def draw_259C(glyph):
    draw_upper_half(glyph)
    draw_lower_right_quadrant(glyph)
def draw_259D(glyph):
    draw_upper_right_quadrant(glyph)
def draw_259E(glyph):
    draw_upper_right_quadrant(glyph)
    draw_lower_left_quadrant(glyph)
def draw_259F(glyph):
    draw_upper_right_quadrant(glyph)
    draw_lower_half(glyph)

def draw_1FB70(glyph): draw_rel_rect(glyph, 1/8, 0, 2/8, 1)
def draw_1FB71(glyph): draw_rel_rect(glyph, 2/8, 0, 3/8, 1)
def draw_1FB72(glyph): draw_rel_rect(glyph, 3/8, 0, 4/8, 1)
def draw_1FB73(glyph): draw_rel_rect(glyph, 4/8, 0, 5/8, 1)
def draw_1FB74(glyph): draw_rel_rect(glyph, 5/8, 0, 6/8, 1)
def draw_1FB75(glyph): draw_rel_rect(glyph, 6/8, 0, 7/8, 1)
def draw_1FB76(glyph): draw_rel_rect(glyph, 0, 6/8, 1, 7/8)
def draw_1FB77(glyph): draw_rel_rect(glyph, 0, 5/8, 1, 6/8)
def draw_1FB78(glyph): draw_rel_rect(glyph, 0, 4/8, 1, 5/8)
def draw_1FB79(glyph): draw_rel_rect(glyph, 0, 3/8, 1, 4/8)
def draw_1FB7A(glyph): draw_rel_rect(glyph, 0, 2/8, 1, 3/8)
def draw_1FB7B(glyph): draw_rel_rect(glyph, 0, 1/8, 1, 2/8)
def draw_1FB7C(glyph):
    draw_rel_rect(glyph, 0, 0, 1/8, 1)
    draw_rel_rect(glyph, 0, 0, 1, 1/8)
def draw_1FB7D(glyph):
    draw_rel_rect(glyph, 0, 0, 1/8, 1)
    draw_rel_rect(glyph, 0, 7/8, 1, 1)
def draw_1FB7E(glyph):
    draw_rel_rect(glyph, 7/8, 0, 8/8, 1)
    draw_rel_rect(glyph, 0, 7/8, 1, 1)
def draw_1FB7F(glyph):
    draw_rel_rect(glyph, 7/8, 0, 8/8, 1)
    draw_rel_rect(glyph, 0/8, 0, 1, 1/8)
def draw_1FB80(glyph):
    draw_rel_rect(glyph, 0/8, 0, 1, 1/8)
    draw_rel_rect(glyph, 7/8, 0, 1, 1)
def draw_1FB81(glyph):
    draw_rel_rect(glyph, 0, 0/8, 1, 1/8)
    draw_rel_rect(glyph, 0, 3/8, 1, 4/8)
    draw_rel_rect(glyph, 0, 5/8, 1, 6/8)
    draw_rel_rect(glyph, 0, 7/8, 1, 8/8)
def draw_1FB82(glyph): draw_rel_rect(glyph, 0, 6/8, 1, 1)
def draw_1FB83(glyph): draw_rel_rect(glyph, 0, 5/8, 1, 1)
def draw_1FB84(glyph): draw_rel_rect(glyph, 0, 3/8, 1, 1)
def draw_1FB85(glyph): draw_rel_rect(glyph, 0, 2/8, 1, 1)
def draw_1FB86(glyph): draw_rel_rect(glyph, 0, 1/8, 1, 1)
def draw_1FB87(glyph): draw_rel_rect(glyph, 6/8, 0, 1, 1)
def draw_1FB88(glyph): draw_rel_rect(glyph, 5/8, 0, 1, 1)
def draw_1FB89(glyph): draw_rel_rect(glyph, 3/8, 0, 1, 1)
def draw_1FB8A(glyph): draw_rel_rect(glyph, 2/8, 0, 1, 1)
def draw_1FB8B(glyph): draw_rel_rect(glyph, 1/8, 0, 1, 1)

def draw_1FB8C(glyph): draw_medium_shade(glyph, 0, 0, 1/2, 1)
def draw_1FB8D(glyph): draw_medium_shade(glyph, 1/2, 0, 1, 1)
def draw_1FB8E(glyph): draw_medium_shade(glyph, 0, 1/2, 1, 1)
def draw_1FB8F(glyph): draw_medium_shade(glyph, 0, 0, 1, 1/2)
def draw_1FB90(glyph): draw_medium_shade(glyph, 0, 0, 1, 1, inverse=True)
def draw_1FB91(glyph):
    draw_light_shade(glyph, 0, 0, 1, 1/2, inverse=True)
    draw_rel_rect(glyph, 0, 1/2, 1, 1)
def draw_1FB92(glyph):
    draw_light_shade(glyph, 0, 1/2, 1, 1, inverse=True)
    draw_rel_rect(glyph, 0, 1, 1, 1/2)
def draw_1FB94(glyph):
    draw_medium_shade(glyph, 0, 0, 1/2, 1, inverse=True)
    draw_rel_rect(glyph, 1/2, 0, 1, 1)

def draw_1FB95(glyph): draw_medium_shade(glyph, 0, 0, 1, 1, inverse=False, dot_count_x=4, dot_count_y=4)
def draw_1FB96(glyph): draw_medium_shade(glyph, 0, 0, 1, 1, inverse=True, dot_count_x=4, dot_count_y=4)
def draw_1FB97(glyph):
    draw_rel_rect(glyph, 0, 0, 1, 1/4)
    draw_rel_rect(glyph, 0, 1/2, 1, 3/4)

def draw_1FBCE(glyph): draw_rel_rect(glyph, 0, 0, 2/3, 1)
def draw_1FBCF(glyph): draw_rel_rect(glyph, 0, 0, 1/3, 1)

def draw_1FBE4(glyph): draw_rel_rect(glyph, 1/4, 1/2, 3/4, 1)
def draw_1FBE5(glyph): draw_rel_rect(glyph, 1/4, 0, 3/4, 1/2)
def draw_1FBE6(glyph): draw_rel_rect(glyph, 0, 1/4, 1/2, 3/4)
def draw_1FBE7(glyph): draw_rel_rect(glyph, 1/2, 1/4, 1, 3/4)

def draw_upper_left_quadrant(glyph):  draw_rel_rect(glyph, 0, 0.5, 0.5, 1)
def draw_upper_right_quadrant(glyph): draw_rel_rect(glyph, 0.5, 0.5, 1, 1)
def draw_lower_left_quadrant(glyph):  draw_rel_rect(glyph, 0, 0, 0.5, 0.5)
def draw_lower_right_quadrant(glyph): draw_rel_rect(glyph, 0.5, 0, 1, 0.5)
def draw_left_half(glyph):            draw_rel_rect(glyph, 0, 0, 0.5, 1)
def draw_right_half(glyph):           draw_rel_rect(glyph, 0.5, 0, 1, 1)
def draw_upper_half(glyph):           draw_rel_rect(glyph, 0, 0.5, 1, 1)
def draw_lower_half(glyph):           draw_rel_rect(glyph, 0, 0, 1, 0.5)

main()
