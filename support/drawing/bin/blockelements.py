#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, statistics

sys.path.append(os.path.dirname(__file__) + "/../../lib")

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    for code in range(0x2580, 0x25a0):
        glyph = font.createChar(code)
        glyph.foreground = fontforge.layer()
        glyph.width = font["space"].width

    draw_rect(font.createChar(0x2580), 0, 0, 1, 1/2) # upper half block
    draw_rect(font.createChar(0x2581), 0, 7/8, 1, 1) # lower 1/8 block
    draw_rect(font.createChar(0x2582), 0, 6/8, 1, 1) # lower 1/4 block
    draw_rect(font.createChar(0x2583), 0, 5/8, 1, 1) # ...
    draw_rect(font.createChar(0x2584), 0, 4/8, 1, 1)
    draw_rect(font.createChar(0x2585), 0, 3/8, 1, 1)
    draw_rect(font.createChar(0x2586), 0, 2/8, 1, 1)
    draw_rect(font.createChar(0x2587), 0, 1/8, 1, 1) # lower 7/8 block
    draw_rect(font.createChar(0x2588), 0, 0/8, 1, 1) # full block
    draw_rect(font.createChar(0x2589), 0, 0, 7/8, 1) # left 7/8 block
    draw_rect(font.createChar(0x258a), 0, 0, 6/8, 1) # left 3/4 block
    draw_rect(font.createChar(0x258b), 0, 0, 5/8, 1) # ...
    draw_rect(font.createChar(0x258c), 0, 0, 4/8, 1)
    draw_rect(font.createChar(0x258d), 0, 0, 3/8, 1)
    draw_rect(font.createChar(0x258e), 0, 0, 2/8, 1)
    draw_rect(font.createChar(0x258f), 0, 0, 1/8, 1) # left 1/8 block
    draw_rect(font.createChar(0x2590), 1/2, 0, 2/2, 1) # right 1/2 block

    draw_light_shade(font.createChar(0x2591))
    draw_medium_shade(font.createChar(0x2592))
    draw_dark_shade(font.createChar(0x2593))

    draw_rect(font.createChar(0x2594), 0, 0, 1, 1/8) # upper 1/8 block
    draw_rect(font.createChar(0x2595), 7/8, 0, 1, 1) # right 1/8 block

    # quadrants
    draw_rect(font.createChar(0x2596), 0, 1/2, 1/2, 1) # lower left
    draw_rect(font.createChar(0x2597), 1/2, 1/2, 1, 1) # lower right
    draw_rect(font.createChar(0x2598), 0, 0, 1/2, 1/2) # upper left
    draw_poly(font.createChar(0x2599), ((0, 0), (1/2, None), 1/2, 1, 1, 0))

    draw_rect(font.createChar(0x259a), 0, 0, 1/2, 1/2) # upper left and...
    draw_rect(font.createChar(0x259a), 1/2, 1/2, 1, 1) # ...lower right

    draw_poly(font.createChar(0x259b), ((0, 0), (1, None), 1/2, 1/2, 1, 0)) # upper left and right and lower left
    draw_poly(font.createChar(0x259c), ((0, 0), (1, None), 1, 1/2, 1/2, 0)) # upper left and right and lower right
    draw_rect(font.createChar(0x259d), 1/2, 0, 1, 1/2) # upper right

    draw_rect(font.createChar(0x259e), 1/2, 0, 1, 1/2) # upper right and...
    draw_rect(font.createChar(0x259e), 0, 1/2, 1/2, 1) # ...lower left

    draw_poly(font.createChar(0x259f), ((1/2, 0), (1, None), 1, 0, 1/2, 1/2)) # upper right and lower left and right

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

def draw_rect(glyph, x1, y1, x2, y2, reverse=False):
    pen = glyph.glyphPen(replace=False)
    if reverse:
        pen.moveTo(coords(glyph, x1, y2))
        pen.lineTo(coords(glyph, x2, y2))
        pen.lineTo(coords(glyph, x2, y1))
        pen.lineTo(coords(glyph, x1, y1))
    else:
        pen.moveTo(coords(glyph, x1, y1))
        pen.lineTo(coords(glyph, x2, y1))
        pen.lineTo(coords(glyph, x2, y2))
        pen.lineTo(coords(glyph, x1, y2))
    pen.closePath()
    pen = None

def draw_light_shade(glyph):
    x_pixel_size = 42
    y_pixel_size = 42
    x_pixel_count = round(glyph.width / x_pixel_size)
    y_pixel_count = round(glyph.font.em / y_pixel_size)
    for row in range(0, y_pixel_count):
        for col in range(2 * (row % 2), x_pixel_count, 4):
            draw_rect(glyph,
                      (col+0.5)/x_pixel_count,
                      (row+0)/y_pixel_count,
                      (col+1.5)/x_pixel_count,
                      (row+1)/y_pixel_count)

def draw_dark_shade(glyph):
    x_pixel_size = 42
    y_pixel_size = 42
    x_pixel_count = round(glyph.width / x_pixel_size)
    y_pixel_count = round(glyph.font.em / y_pixel_size)
    draw_rect(glyph, 0, 0, 1, 1)
    for row in range(0, y_pixel_count):
        for col in range(2 * (row % 2), x_pixel_count, 4):
            draw_rect(glyph,
                      (col+0.5)/x_pixel_count,
                      (row+0)/y_pixel_count,
                      (col+1.5)/x_pixel_count,
                      (row+1)/y_pixel_count,
                      reverse=True)

def draw_medium_shade(glyph):
    x_pixel_size = 84
    y_pixel_size = 84
    x_pixel_count = round(glyph.width / x_pixel_size / 2) * 2 # even number of columns
    y_pixel_count = round(glyph.font.em / y_pixel_size / 2) * 2 # even number of rows
    for row in range(0, y_pixel_count):
        for col in range(row % 2, x_pixel_count, 2):
            draw_rect(glyph,
                      (col)/x_pixel_count,
                      (row)/y_pixel_count,
                      (col+1)/x_pixel_count,
                      (row+1)/y_pixel_count)

def draw_poly(glyph, points, reverse=False):
    pen = glyph.glyphPen(replace=False)
    xx = None
    yy = None
    horizontal = None

    new_points = []
    for i, point in enumerate(points):
        x = None
        y = None
        if i == 0:
            (x, y) = point
            new_points.append((x, y))
        else:
            if type(point) in [list, tuple]:
                (x, y) = point
                if x is None:
                    horizontal = True
                    x = xx
                if y is None:
                    horizontal = False
                    y = yy
            elif type(point) in [int, float]:
                if horizontal:
                    x = point
                    y = yy
                else:
                    x = xx
                    y = point
                horizontal = not horizontal
            new_points.append((x, y))
        (xx, yy) = (x, y)
    points = new_points
    if reverse:
        points.reverse()

    for i, point in enumerate(points):
        (x, y) = point
        if i == 0:
            pen.moveTo(coords(glyph, x, y))
        else:
            pen.lineTo(coords(glyph, x, y))
    pen.closePath()
    pen = None

def coords(glyph, x, y):
    xx = glyph.width * x
    yy = glyph.font.ascent - glyph.font.em * y
    return (xx, yy)

main()
