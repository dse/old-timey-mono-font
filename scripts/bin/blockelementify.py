#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, statistics, math

SHADE_DOT_SIZE = 84

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    glyphs = []
    for glyph in font.glyphs():
        if glyph.glyphname == ".notdef":
            continue
        if glyph.glyphname == ".null":
            continue
        if glyph.glyphname == "nonmarkingreturn":
            continue
        if glyph.width == 0:
            continue
        glyphs.append(glyph)

    new_glyph_width = round(statistics.median([glyph.width for glyph in glyphs]))

    for code in range(0x2580, 0x25a0):
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

    for code in range(0x2500, 0x2580):
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

def draw_rel_rect(glyph, x1, y1, x2, y2, withershins=False):
    font = glyph.font
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    if x1 <= 0 and x2 <= 0:
        return
    if x1 >= 1 and x2 >= 1:
        return
    if y1 <= 0 and y2 <= 0:
        return
    if y1 >= 1 and y2 >= 1:
        return
    if x1 < 0:
        x1 = 0
    if x1 > 1:
        x1 = 1
    if x2 < 0:
        x2 = 0
    if x2 > 1:
        x2 = 1
    if y1 < 0:
        y1 = 0
    if y1 > 1:
        y1 = 1
    if y2 < 0:
        y2 = 0
    if y2 > 1:
        y2 = 1
    x1 = round(glyph.width * x1)
    x2 = round(glyph.width * x2)
    y1 = round(-font.descent + font.em * y1)
    y2 = round(-font.descent + font.em * y2)
    draw_rect(glyph, x1, y1, x2, y2, withershins=withershins)

def draw_rect(glyph, x1, y1, x2, y2, withershins=False):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    (x1, y1, x2, y2) = [round(w) for w in (x1, y1, x2, y2)]
    pen = glyph.glyphPen(replace=False)
    if withershins:
        pen.moveTo((x1, y1))
        pen.lineTo((x2, y1))
        pen.lineTo((x2, y2))
        pen.lineTo((x1, y2))
    else:
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y2))
        pen.lineTo((x2, y2))
        pen.lineTo((x2, y1))
    pen.closePath()
    pen = None

main()
