#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, statistics, math

KAPPA = 0.5519150244935105707435627

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
    x_radius = new_glyph_width / 8
    y_radius = font.em / 16
    radius = round(math.sqrt(x_radius * y_radius))

    xc_a = round(new_glyph_width * 1/4)
    xc_b = round(new_glyph_width * 3/4)
    yc_a = round(font.em * 7/8 - font.descent)
    yc_b = round(font.em * 5/8 - font.descent)
    yc_c = round(font.em * 3/8 - font.descent)
    yc_d = round(font.em * 1/8 - font.descent)

    center = {}
    center["1"] = (xc_a, yc_a)
    center["2"] = (xc_a, yc_b)
    center["3"] = (xc_a, yc_c)
    center["4"] = (xc_b, yc_a)
    center["5"] = (xc_b, yc_b)
    center["6"] = (xc_b, yc_c)
    center["7"] = (xc_a, yc_d)
    center["8"] = (xc_b, yc_d)
    
    glyph = font.createChar(0x2800) # BRAILLE PATTERN BLANK
    glyph.width = new_glyph_width
    glyph.foreground = fontforge.layer()

    for code in range(0x2801, 0x2900):
        print(f'{code}')
        glyph = font.createChar(code)
        glyph.width = new_glyph_width
        glyph.foreground = fontforge.layer()
        dots = unicodedata.name(chr(code)).removeprefix("BRAILLE PATTERN DOTS-")
        for dot in dots:
            print(f'    {dot}')
            draw_dot(glyph, center[dot], radius)

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

def draw_dot(glyph, center, r):
    (xc, yc) = center
    pt_1 = (xc - r, yc)
    pt_2 = (xc, yc + r)
    pt_3 = (xc + r, yc)
    pt_4 = (xc, yc - r)
    cp_1 = (xc - r, yc + r * KAPPA)
    cp_2 = (xc - KAPPA * r, yc + r)
    cp_3 = (xc + KAPPA * r, yc + r)
    cp_4 = (xc + r, yc + r * KAPPA)
    cp_5 = (xc + r, yc - r * KAPPA)
    cp_6 = (xc + KAPPA * r, yc - r)
    cp_7 = (xc - KAPPA * r, yc - r)
    cp_8 = (xc - r, yc - r * KAPPA)

    pen = glyph.glyphPen(replace=False)
    pen.moveTo(pt_1)
    pen.curveTo(cp_1, cp_2, pt_2)
    pen.curveTo(cp_3, cp_4, pt_3)
    pen.curveTo(cp_5, cp_6, pt_4)
    pen.curveTo(cp_7, cp_8, pt_1)
    pen.closePath()
    pen = None                  # finalize the pen

main()
