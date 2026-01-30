#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse
import os
import sys
import json

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_utils import reconstitute_references
from my_font_utils import parse_glyph_svg_filename
from my_font_utils import create_smol_glyph
from my_font_utils import check_all_glyph_bounds

sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import mixedjsontext

DEFAULT_WIDTH = 1008
STROKE_WIDTH_BASIS = 96
LATIN_SMALL_LETTER_SCHWA = 0x0259

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('font_filename', help="font filename")
    parser.add_argument('svg_filenames', nargs='+', help="svg characters")
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('-o', '--save-as', '--output', type=str,
                        help="after editing, save as new file, converts if file extension is different")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.verbose >= 2:
        print("redraw.py %s: Opening and reading..." % args.font_filename)
    font = fontforge.open(args.font_filename)
    write_font_filename = args.save_as if args.save_as is not None else args.font_filename

    if args.verbose >= 2:
        print("redraw.py %s: Importing glyphs...")
    for svg_filename in args.svg_filenames:
        if args.verbose >= 2:
            print("redraw.py %s: Importing %s ..." % (args.font_filename, svg_filename))
        import_svg_glyph(font, svg_filename, args.width)
        if args.verbose >= 2:
            print("redraw.py %s: %s is imported" % (args.font_filename, svg_filename))

    if write_font_filename.endswith('.sfd'):
        if args.verbose >= 2:
            print("redraw.py %s: Saving... %s" % (args.font_filename, write_font_filename))
        font.save(write_font_filename)
    else:
        if args.verbose >= 2:
            print("redraw.py %s: Generating... %s" % (args.font_filename, write_font_filename))
        font.generate(write_font_filename)
    font.close()

# FIXME: if allow_json_data is True, allow a ".svg" to override.
def import_svg_glyph(font, svg_filename, width, allow_json_data=False):
    font_path = os.path.relpath(font.path)
    (codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width) = parse_glyph_svg_filename(svg_filename)
    if codepoint is None and glyphname is None:
        return
    glyph = None
    if glyphname in font:
        glyph = font[glyphname]
        if len(glyph.references):
            print("redraw.py %s: not redrawing onto %s which has references" % (svg_filename, glyphname))
            return
    glyph = font.createChar(codepoint, glyphname)
    glyph.foreground = fontforge.layer()
    if width is None:
        orig_width = glyph.width
    if stroke_width is not None:
        font.strokedfont = True
        glyph.importOutlines(svg_filename, correctdir=True)
        font.strokedfont = False
    else:
        font.strokedfont = True
        glyph.importOutlines(svg_filename)
        font.strokedfont = False
    if width is None:
        glyph.width = orig_width
    else:
        glyph.width = width

    data = None
    try:
        data = json.loads(glyph.comment)
    except json.decoder.JSONDecodeError:
        data = glyph.comment
    if type(data) == str and not re.search(r'\S', data):
        data = { }
    elif data is not None and type(data) != dict:
        data = { "data": data }
    if stroke_width is None:
        if "stroke_width" in data:
            del data["stroke_width"]
    else:
        data["stroke_width"] = stroke_width
    glyph.comment = json.dumps(data, indent=4)

main()
