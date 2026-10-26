#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--stroke-width", "--width", type=int, default=96)
    args = parser.parse_args()

    glyphs_data = json.loads(open("src/data/glyphs.json").read())
    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        code = glyph.unicode
        if code < 0:
            code = fontforge.unicodeFromName(glyph.glyphname.split(".", 1)[0])
        if "." in glyph.glyphname:
            variant_suffix = "." + glyph.glyphname.split(".", 1)[1]
        else:
            variant_suffix = ""
        if code < 0:
            entry = glyphs_data.get(glyph.glyphname)
        else:
            entry = glyphs_data.get(chr(code) + variant_suffix)
            if entry is None:
                entry = glyphs_data.get(f'U+{code:04X}' + variant_suffix)
            if entry is None:
                entry = glyphs_data.get(chr(code))
            if entry is None:
                entry = glyphs_data.get(f'U+{code:04X}')
        if entry is None:
            for entry in glyphs_data["__RANGES__"]:
                range_from = ranges_key_conv(entry["from"])
                range_to   = ranges_key_conv(entry["to"]) + 1
                if code in range(range_from, range_to):
                    entry = entry["data"]
                    break
        if entry is not None:
            fill = entry.get("fill", False)
            expand_strokes = entry.get("expandStrokes", True)

            # default to args.stroke_width.  if strokeWidth is specified, no more than that.
            stroke_width = min([entry.get("strokeWidth", float("inf")), args.stroke_width])
        if not expand_strokes:
            if args.verbose:
                print(f'{args.filename}: not expanding strokes on glyph {glyph.glyphname}: expandStrokes is set to false')
            continue
        if variant_suffix == ".SMOL":
            if args.verbose:
                print(f'{args.filename}: not expanding strokes on glyph {glyph.glyphname}: is a .SMOL glyph')
            continue

        if args.verbose:
            print(f'{args.filename}: expanding strokes on glyph {glyph.glyphname}')
        glyph.stroke("circular", stroke_width, removeinternal=fill)

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

    font.close()

def ranges_key_conv(key):
    if type(key) == float:
        return round(key)
    if type(key) == int:
        return key
    if len(key) == 1:
        return ord(key)
    if match := re.fullmatch(r'U\+([0-9a-f]{4,})', key, flags=re.I):
        return int(match[1], 16)
    raise Exception(f'invalid key in ranges: {key}')

main()
