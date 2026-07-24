#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
# -nosplash -quiet

import fontforge
import argparse
import os
import sys
import statistics
import time
import re
import unicodedata
import json

# sys.path.append("%s/git/dse.d/pyfontutils/lib" % os.getenv("HOME"))

mod_path = os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib"
if not mod_path in sys.path:
    sys.path.append(mod_path)

mod_path = os.getenv("HOME") + "/git/dse.d/fonts.d/old-timey-mono-font/support/lib"
if not mod_path in sys.path:
    sys.path.append(mod_path)

mod_path = os.getenv("HOME") + "/git/dse.d/pyfontutils/lib"
if not mod_path in sys.path:
    sys.path.append(mod_path)

import mixedjsontext

from my_font_utils import get_glyph_char_data, DEFAULT_GLYPHS_DATA_JSON_FILENAME
from font_utils import get_base_codepoint, u

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
    parser.add_argument('json_filename', nargs='?', type=str, default=DEFAULT_GLYPHS_DATA_JSON_FILENAME)
    args = parser.parse_args()

    with open(args.json_filename) as fh:
        glyphs_data_json_text = fh.read()
    glyphs_data = json.loads(glyphs_data_json_text)

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    # MONOSPACE
    common_glyph_width = statistics.mode([glyph.width for glyph in font.glyphs()])

    for glyph in font.glyphs():
        if glyph.glyphname == ".notdef":
            continue

        glyph_data = get_glyph_char_data(glyph, json_filename=args.json_filename) # always a dict
        real_codepoint = get_base_codepoint(glyph)

        fill_flag = glyph_data.get("fill", False)
        expand_flag = glyph_data.get("expandStrokes", True)
        if not expand_flag:
            if args.verbose >= 2:
                print("A")
                print("strokes.py: %s: %s (%s): flagged 'expandStrokes: false'; not expanding strokes" %
                      (args.font_filename, glyph.glyphname, u(glyph.unicode)))
            continue
        has_contours   = len(glyph.foreground) != 0
        has_references = len(glyph.references) != 0

        if args.verbose:
            if not has_contours:
                print("B")
                print("strokes.py: %s: %s (%s): INFO: has no contours" % 
                      (args.font_filename, glyph.glyphname, u(glyph.unicode)))
            elif has_references:
                print("C")
                print("strokes.py: %s: %s (%s): INFO: contains both references AND contours" %
                      (args.font_filename, glyph.glyphname, u(glyph.unicode)))

        if args.verbose:
            print("D")
            print("strokes.py: %s: %s (%s): will expand strokes" % 
                  (args.font_filename, glyph.glyphname, u(glyph.unicode)))
        orig_width = glyph.width
        expand_params = {}
        if fill_flag:
            expand_params["removeinternal"] = True
        if args.verbose:
            print("E")
            print("strokes.py: %s: %s (%s): expanding strokes by %d, with parameters %s" % 
                  (args.font_filename, glyph.glyphname, u(glyph.unicode), args.expand_stroke, json.dumps(expand_params)))
        glyph.stroke("circular", args.expand_stroke, **expand_params)
        if args.verbose:
            print("F")
            print("strokes.py: %s: %s (%s): finished expanding strokes" % 
                  (args.font_filename, glyph.glyphname, u(glyph.unicode)))
        if orig_width != 0:
            glyph.width = orig_width
        else:
            glyph.width = common_glyph_width # MONOSPACE

    if write_font_filename.endswith('.sfd'):
        if args.verbose >= 2:
            print("G")
            print("strokes.py %s: Saving %s..." % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        if args.verbose >= 2:
            print("H")
            print("strokes.py %s: Generating %s..." % (args.font_filename, write_font_filename))
        font.generate(write_font_filename)

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
