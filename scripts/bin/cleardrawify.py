#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    for r in [
            range(0x2500, 0x2580),
            range(0x2500, 0x25a0),
            range(0x1fb3c, 0x1fb70),
            range(0x1fb00, 0x1fb3c),
            range(0x2800, 0x2900),
    ]:
        for code in r:
            try:
                font.removeGlyph(code)
            except ValueError as e:
                if str(e) != "This glyph is not in the font":
                    raise

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
def draw_2591(glyph):
    font = glyph.font
    shade_dots_x = round(glyph.width / SHADE_DOT_SIZE / 2) * 2
    shade_dots_y = round(font.em / SHADE_DOT_SIZE / 2) * 2
    for x in range(0, shade_dots_x):
        x1 = x/shade_dots_x
        x2 = (x+1)/shade_dots_x
        if x % 2 == 0:
            for y in range(0, shade_dots_y):
                if (x + y * 2) % 4 == 0:
                    y1 = y/shade_dots_y
                    y2 = (y+1)/shade_dots_y
                    draw_rel_rect(glyph, x1, y1, x2, y2)
def draw_2592(glyph):
    font = glyph.font
    shade_dots_x = round(glyph.width / SHADE_DOT_SIZE / 2) * 2
    shade_dots_y = round(font.em / SHADE_DOT_SIZE / 2) * 2
    for x in range(0, shade_dots_x):
        x1 = x/shade_dots_x
        x2 = (x+1)/shade_dots_x
        for y in range(0, shade_dots_y):
            if (x + y) % 2 == 0:
                y1 = y/shade_dots_y
                y2 = (y+1)/shade_dots_y
                draw_rel_rect(glyph, x1, y1, x2, y2)
def draw_2593(glyph):
    font = glyph.font
    shade_dots_x = round(glyph.width / SHADE_DOT_SIZE / 2) * 2
    shade_dots_y = round(font.em / SHADE_DOT_SIZE / 2) * 2
    draw_rel_rect(glyph, 0, 0, 1, 1)
    for x in range(0, shade_dots_x):
        x1 = x/shade_dots_x
        x2 = (x+1)/shade_dots_x
        if x % 2 == 0:
            for y in range(0, shade_dots_y):
                if (x + y * 2) % 4 == 0:
                    y1 = y/shade_dots_y
                    y2 = (y+1)/shade_dots_y
                    draw_rel_rect(glyph, x1, y1, x2, y2, withershins=True)
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

def draw_upper_left_quadrant(glyph):  draw_rel_rect(glyph, 0, 0.5, 0.5, 1)
def draw_upper_right_quadrant(glyph): draw_rel_rect(glyph, 0.5, 0.5, 1, 1)
def draw_lower_left_quadrant(glyph):  draw_rel_rect(glyph, 0, 0, 0.5, 0.5)
def draw_lower_right_quadrant(glyph): draw_rel_rect(glyph, 0.5, 0, 1, 0.5)
def draw_left_half(glyph):            draw_rel_rect(glyph, 0, 0, 0.5, 1)
def draw_right_half(glyph):           draw_rel_rect(glyph, 0.5, 0, 1, 1)
def draw_upper_half(glyph):           draw_rel_rect(glyph, 0, 0.5, 1, 1)
def draw_lower_half(glyph):           draw_rel_rect(glyph, 0, 0, 1, 0.5)

main()
