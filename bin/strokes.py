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
# allowable linecaps                allowed linejoins
# svg     fontforge                 svg         fontforge
# ------  -----------------------   ----------  ----------
# butt    butt                      arcs        arcs
# round   round                     bevel       bevel
# square  butt with extendcap=0.5   miter       miter
#         bevel                     miter-clip  miterclip
#                                   round       round

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
        glyphs_data_json_text = fh.read()
    glyphs_data = json.loads(glyphs_data_json_text)

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    # MONOSPACE
    common_glyph_width = statistics.mode([glyph.width for glyph in font.glyphs()])

    fh = open('strokes.log', 'w', encoding='utf-8') if args.log else None

    if args.expand_stroke is None:
        if "DEBUG" in os.environ:
            print("strokes.py %s: --expand-stroke not specified; not expanding strokes" % args.font_filename)
    else:
        for glyph in font.glyphs():
            time_start = time.time()
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            glyph_data = get_glyph_char_data(glyph) # always a dict
            real_codepoint = get_glyph_real_codepoint(glyph)
            fill_flag = glyph_data.get("fill", False)
            expand_flag = glyph_data.get("expandStrokes", True)
            if not expand_flag:
                if "DEBUG" in os.environ:
                    print("strokes.py %s: %s %s is flagged 'expandStrokes: false'; not expanding strokes" % (args.font_filename, glyph.glyphname, u(real_codepoint)))
                continue
            if len(glyph.foreground) == 0 and len(glyph.references) == 0:
                if "DEBUG" in os.environ:
                    print("strokes.py %s: %s %s is blank; not expanding strokes" % (args.font_filename, glyph.glyphname, u(real_codepoint)))
                continue
            if len(glyph.references):
                if "DEBUG" in os.environ:
                    print("strokes.py %s: %s %s has references; not expanding any strokes" % (args.font_filename, glyph.glyphname, u(real_codepoint)))
                continue
            orig_width = glyph.width
            if "DEBUG" in os.environ:
                print("strokes.py %s: %s %s: expanding strokes" % (args.font_filename, glyph.glyphname, u(real_codepoint)))
            expand_params = {}
            line_join = glyph_data.get("linejoin")
            line_cap = glyph_data.get("linecap")
            if line_join is not None and not (line_join in SVG_LINEJOIN_VALUES):
                raise Exception("invalid line join value: %s" % line_join)
            if line_cap is not None and not (line_cap in SVG_LINECAP_VALUES):
                raise Exception("invalid line cap value: %s" % line_cap)
            if line_join is not None:
                if line_join == "miter-clip":
                    line_join = "miterclip"
                expand_params["join"] = line_join
            if line_cap is not None:
                if line_cap == "square":
                    line_cap = "butt"
                    expand_params["extendcap"] = 0.5
                expand_params["cap"] = line_cap
            if fill_flag:
                expand_params["removeinternal"] = True
            if not "DEBUG" in os.environ:
                silence.on()
            glyph.stroke("circular", args.expand_stroke, **expand_params)
            if not "DEBUG" in os.environ:
                silence.off()
            if orig_width != 0:
                glyph.width = orig_width
            else:
                glyph.width = common_glyph_width # MONOSPACE
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            time_end = time.time()
            if fh is not None:
                fh.write("%8.6f  %s\n" % ((time_end - time_start), charname(glyph)))

            # #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #     having_stroke_width = char_data["having_stroke_width"] if "having_stroke_width" in char_data else 0
            #     glyph.stroke("circular", args.expand_stroke - having_stroke_width, **params)
            # elif stroke_width is not None:
            #     print("strokes.py %s: marked as already having stroke width of %d; expanding by %d" %
            #           (args.font_filename, stroke_width, args.expand_stroke - stroke_width))
            #     glyph.stroke("circular", args.expand_stroke - stroke_width, removeinternal=True)
            # else:
            #     glyph.stroke("circular", args.expand_stroke)
            # #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    if write_font_filename.endswith('.sfd'):
        if "DEBUG" in os.environ:
            print("strokes.py %s: Saving %s..." % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        if "DEBUG" in os.environ:
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
