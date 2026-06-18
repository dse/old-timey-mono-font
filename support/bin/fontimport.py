#!/usr/bin/env -S fontforge -quiet -script
# -*- mode: python; coding: utf-8 -*-
import os, argparse, fontforge, re
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="font filename")
    parser.add_argument("import_filenames", nargs="+", help="vector files, typically SVG")
    parser.add_argument("--width", type=int, help="width for imported glyphs")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for import_filename in args.import_filenames:
        (codepoint, glyphname, *_) = parse_glyph_filename(import_filename)
        glyph = font.createChar(codepoint, glyphname)
        glyph.foreground = fontforge.layer() # clear existing glyph
        space_glyphname = fontforge.nameFromUnicode(32)
        if args.width is not None:
            glyph.width = args.width
        elif space_glyphname in font:
            glyph.width = font[space_glyphname].width
        else:
            glyph.width = round(font.em/3)
        font.strokedfont = True # avoid expanding strokes automatically
        glyph.importOutlines(import_filename)
        font.strokedfont = False
        glyph.stroke("circular", 96)

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
