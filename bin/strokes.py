#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import statistics
import time
import re
import unicodedata
import json

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext
import silence

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import u, get_glyph_real_codepoint, get_glyph_char_data

SVG_LINECAP_VALUES = ["butt", "round", "square"]
SVG_LINEJOIN_VALUES = ["arcs", "bevel", "miter", "miter-clip", "miterclip", "round"]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('--expand-stroke', '-x', type=int, help="number of pixels to expand stroke", default=96)
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--log', action='store_true')
    parser.add_argument('--allow-json-data', action='store_true')
    args = parser.parse_args()

    with open("data/glyphs.json") as fh:
        glyph_data_json_text = fh.read()
    glyph_data = json.loads(glyph_data_json_text)
    # allowable linecaps                allowed linejoins
    # svg     fontforge                 svg         fontforge
    # ------  -----------------------   ----------  ----------
    # butt    butt                      arcs        arcs
    # round   round                     bevel       bevel
    # square  butt with extendcap=0.5   miter       miter
    #         bevel                     miter-clip  miterclip
    #                                   round       round

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    # MONOSPACE
    common_glyph_width = statistics.mode([glyph.width for glyph in font.glyphs()])

    fh = open('strokes.log', 'w', encoding='utf-8') if args.log else None

    for glyph in font.glyphs():
        data = None
        try:
            data = json.loads(glyph.comment)
        except json.decoder.JSONDecodeError:
            data = glyph.comment
        stroke_width = None
        if type(data) == dict and "stroke_width" in data:
            stroke_width = data["stroke_width"]

        print("strokes.py %s: Expanding strokes on %s %s" % (args.font_filename, u(glyph.unicode), glyph.glyphname))
        if glyph.unicode == 0x269b: # ATOM SYMBOL
            continue
        if glyph.unicode == 0x2620: # SKULL AND CROSS BONES
            continue
        if glyph.unicode == 0x2622: # RADIOACTIVE SIGN
            continue
        if glyph.unicode == 0x2623: # BIOHAZARD SIGN
            continue
        if glyph.unicode in range(0x2500, 0x25a0):
            continue
        if glyph.unicode in range(0x2800, 0x2900):
            continue
        if len(glyph.foreground) == 0 and len(glyph.references) == 0:
            continue
        if mixedjsontext.fontcomment_says_generated(glyph.comment):
            continue
        if len(glyph.references):
            continue
        orig_width = glyph.width
        real_codepoint = get_glyph_real_codepoint(glyph)
        if args.expand_stroke is not None:
            time_start = time.time()
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            if args.allow_json_data and (char_data := get_glyph_char_data(glyph)) is not None:
                line_join = char_data["linejoin"] if "linejoin" in char_data else None
                line_cap  = char_data["linecap"]  if "linecap"  in char_data else None
                if line_join is not None and not (line_join in SVG_LINEJOIN_VALUES):
                    raise Exception("invalid line join value: %s" % line_join)
                if line_cap is not None and not (line_cap in SVG_LINECAP_VALUES):
                    raise Exception("invalid line cap value: %s" % line_cap)
                params = {}
                if line_join is not None:
                    if line_join == "miter-clip":
                        line_join = "miterclip"
                    params["join"] = line_join
                if line_cap is not None:
                    if line_cap == "square":
                        line_cap = "butt"
                        params["extendcap"] = 0.5
                    params["cap"] = line_cap
                if "fill" in char_data and char_data["fill"]:
                    params["removeinternal"] = True
                having_stroke_width = char_data["having_stroke_width"] if "having_stroke_width" in char_data else 0
                glyph.stroke("circular", args.expand_stroke - having_stroke_width, **params)
            elif stroke_width is not None:
                print("strokes.py %s: marked as already having stroke width of %d; expanding by %d" %
                      (args.font_filename, stroke_width, args.expand_stroke - stroke_width))
                glyph.stroke("circular", args.expand_stroke - stroke_width, removeinternal=True)
            else:
                glyph.stroke("circular", args.expand_stroke)
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            time_end = time.time()
            if fh is not None:
                fh.write("%8.6f  %s\n" % ((time_end - time_start), charname(glyph)))
        if orig_width != 0:
            glyph.width = orig_width
        else:
            glyph.width = common_glyph_width # MONOSPACE

    if write_font_filename.endswith('.sfd'):
        print("strokes.py %s: Saving %s..." % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        print("strokes.py %s: Generating %s..." % (args.font_filename, write_font_filename))
        font.generate(write_font_filename)

    if fh is not None:
        fh.close()

def charname(glyph):
    if glyph.unicode >= 0:
        try:
            unicode_name = unicodedata.name(chr(glyph.unicode))
            return "%s '%s' %s" % (u(glyph.unicode), glyph.glyphname, unicode_name)
        except ValueError:
            return "%s '%s' (%s)" % (u(glyph.unicode), glyph.glyphname, "(no name)")
    idx = glyph.glyphname.find('.')
    if idx < 1:                 # no "." or starts with "."
        return "-1 '%s'" % glyph.glyphname
    real_glyphname = glyph.glyphname[0:idx]
    try:
        real_codepoint = fontforge.unicodeFromName(real_glyphname)
    except ValueError:
        return "-1 '%s'" % glyph.glyphname
    try:
        real_unicode_name = unicodedata.name(chr(real_codepoint))
    except ValueError:
        real_unicode_name = "(no name)"
    return "-1 '%s' %s %s" % (glyph.glyphname, u(real_codepoint), real_unicode_name)

def u(codepoint):
    if codepoint < 0:
        return "%d" % codepoint
    return "U+%04X" % codepoint

main()        
