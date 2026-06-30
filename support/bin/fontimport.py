#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import os, argparse, fontforge, re, math, json

sys.path.append("%s/git/dse.d/pyfontutils/lib" % os.environ["HOME"])
from font_utils import parse_char_str, u

STROKE_WIDTH = 96

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="font filename")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--width", type=int)
    parser.add_argument("--comment", type=str)
    parser.add_argument("import_filenames", nargs="+", help="vector files, typically SVG")
    parser.add_argument("--italic", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    if args.width is not None:
        glyph_width = args.width
    elif "space" in font:
        glyph_width = font["space"].width
    else:
        glyph_width = round(font.em / 3)

    print(glyph_width)

    for import_filename in args.import_filenames:

        if import_filename.endswith(".svg"):
            (codepoint, glyphname, *_) = parse_glyph_filename(import_filename)
            if args.verbose:
                print("fontimport.py: importing %s into %s at %s" % (import_filename, glyphname, u(codepoint)))

            glyph = font.createChar(codepoint, glyphname)
            glyph.foreground = fontforge.layer() # clear existing glyph
            font.strokedfont = True # avoid expanding strokes automatically
            glyph.importOutlines(import_filename)
            font.strokedfont = False
            glyph.stroke("circular", STROKE_WIDTH)
            glyph.width = glyph_width

            if args.comment is not None:
                glyph.comment = args.comment

        elif import_filename.endswith(".json"):
            if args.verbose:
                print("fontimport.py: reading JSON imports from %s" % import_filename)
            with open(import_filename, "r") as fh:
                data = json.load(fh)
            imports = data["imports"]
            aliases = data["aliases"]
            for idx, (charname, source) in enumerate(imports.items()):
                (codepoint, glyphname, base_codepoint, base_glyphname, variant) = parse_char_str(charname, aliases=aliases)
                if type(source) is dict:
                    import_filename = source.get("filename")
                elif type(source) is str:
                    import_filename = source

                glyph = font.createChar(codepoint, glyphname)
                glyph_width = glyph.width
                glyph.foreground = fontforge.layer() # clear existing glyph
                font.strokedfont = True # avoid expanding strokes automatically
                glyph.importOutlines(import_filename)
                font.strokedfont = False
                glyph.stroke("circular", STROKE_WIDTH)

                if args.italic:
                    if "italicShift" in source:
                        italic_shift = source["italicShift"]
                        (_, y_min, _, y_max) = glyph.boundingBox()
                        y_center = (y_min + y_max) / 2
                        y_pivot = italic_shift.get("y", 0)
                        angle = italic_shift.get("angle", -12)
                        shift_x = (y_pivot - y_center) * math.tan(angle * math.pi / 180)
                        glyph.transform(psMat.translate(shift_x, 0))

                glyph.width = glyph_width

                if args.comment is not None:
                    glyph.comment = args.comment

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def parse_glyph_filename(filename):
    basename = os.path.basename(filename)
    base_glyphname = os.path.splitext(basename)[0]
    variant = None
    if "." in base_glyphname:
        (base_glyphname, variant) = base_glyphname.split(".", 1)
    elif "--" in base_glyphname:
        (base_glyphname, variant) = base_glyphname.split("--", 1)
    base_codepoint = None
    glyphname = None
    if match := re.match(r'(?:0?x|u\+?|uni)?([0-9a-f]{4,})', base_glyphname, flags=re.I):
        base_codepoint = int(match[1], 16)
        glyphname = fontforge.nameFromUnicode(base_codepoint)
    else:
        base_codepoint = fontforge.unicodeFromName(base_glyphname)
        glyphname = base_glyphname
    codepoint = base_codepoint
    if variant is not None:
        glyphname += "." + variant
        codepoint = -1
    return (codepoint, glyphname, base_codepoint, base_glyphname, variant)

main()
