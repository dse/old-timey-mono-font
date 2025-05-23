#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import math
import psMat

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext

STROKE_WIDTH_BASIS = 96

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--aspect', '--aspect-ratio', type=float)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    for glyph in font.glyphs():
        if mixedjsontext.fontcomment_says_generated(glyph.comment):
            if use_aspect_method_2(glyph.unicode):
                apply_aspect_method_2(glyph)
            else:
                final_width = math.floor(glyph.width * args.aspect)
                glyph.transform(psMat.scale(args.aspect, 1), ("partialRefs",))
                glyph.width = final_width
            continue
        if len(glyph.references):
            glyph.transform(psMat.scale(args.aspect, 1), ("partialRefs",))
            continue
        if not args.aspect: # how does this even occur?
            continue
        if args.aspect > 1:
            final_width = math.floor(glyph.width * args.aspect)
            glyph.transform(psMat.scale(args.aspect, 1), ("partialRefs",))
            glyph.width = final_width
            continue
        apply_aspect_method_1(glyph)

    if write_font_filename.endswith('.sfd'):
        font.save(write_font_filename)
    else:
        font.generate(write_font_filename)

def apply_aspect_method_1(glyph): # normal characters
    orig_width = glyph.width
    # we need to store and set the final width because transform
    # may produce an incorrect glyph width.
    final_width = math.floor(glyph.width * args.aspect)
    xform = psMat.identity()
    xform = psMat.compose(xform, psMat.translate(-orig_width / 2, 0))
    orig_width_2 = orig_width - STROKE_WIDTH_BASIS
    final_width_2 = final_width - STROKE_WIDTH_BASIS
    xform = psMat.compose(xform, psMat.scale(final_width_2 / orig_width_2, 1))
    xform = psMat.compose(xform, psMat.translate(final_width / 2, 0))
    glyph.transform(xform, ("partialRefs",))
    glyph.width = final_width

def apply_aspect_method_2(glyph): # box drawing characters and such
    global args
    new_contours = []
    ow = glyph.width
    fw = math.floor(glyph.width * args.aspect)
    ow1 = round(ow * 1/4)
    ow2 = round(ow * 1/2)
    ow3 = round(ow * 3/4)
    fw1 = round(fw * 1/2) - ow2 + ow1
    fw2 = round(fw * 1/2)
    fw3 = round(fw * 1/2) - ow2 + ow3
    new_foreground = fontforge.layer()
    for contour in glyph.foreground:
        new_contour = fontforge.contour(is_quadratic=contour.is_quadratic)
        for point in contour:
            x = point.x
            if x <= 0:
                pass
            elif x >= ow:
                x = x - ow + fw
            elif x <= ow1:
                x = round(x / ow1 * fw1)
            elif x <= ow3:
                x = fw1 + (x - ow1) / (ow3 - ow1) * (fw3 - fw1)
            elif x <= ow:
                x = fw3 + (x - ow3) / (ow - ow3) * (fw - fw3)
            point.x = x
            new_contour += point
        new_foreground += new_contour

    glyph.foreground = new_foreground
    glyph.width = fw

def use_aspect_method_2(codepoint):
    return (
        codepoint in range(0x2500, 0x2504) or
        codepoint in range(0x2506, 0x2508) or
        codepoint in range(0x250a, 0x254c) or
        codepoint in range(0x254e, 0x2571) or
        codepoint in range(0x2574, 0x2580)
    )

main()
