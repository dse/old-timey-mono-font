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

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext
import silence

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import u

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('--expand-stroke', '-x', type=int, help="number of pixels to expand stroke", default=96)
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    # MONOSPACE
    common_glyph_width = statistics.mode([glyph.width for glyph in font.glyphs()])

    fh = open('strokes.log', 'w', encoding='utf-8')

    for glyph in font.glyphs():
        print("strokes.py %s: Expanding strokes on %s %s" % (args.font_filename, u(glyph.unicode), glyph.glyphname))
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
        if args.expand_stroke is not None:
            time_start = time.time()
            glyph.stroke("circular", args.expand_stroke)
            time_end = time.time()
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
