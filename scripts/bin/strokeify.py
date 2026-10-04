#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output-filename", type=str, nargs="?", default=None)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--stroke-width", "--width", type=int, default=96)
    args = parser.parse_args()
    font = fontforge.open(args.filename)

    glyphs_data = json.loads(open("src/data/glyphs.json").read())

    stderr_copy = os.dup(2)
    silent = False
    def silence():
        nonlocal silent
        if silent:
            return
        os.close(2)
        silent = True
    def unsilence():
        nonlocal silent, stderr_copy
        if not silent:
            return
        os.dup2(stderr_copy, 2)
        silent = False

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
        try:
            silence()
            glyph.stroke("circular", stroke_width, removeinternal=fill)
            unsilence()
        except:
            unsilence()
            print(f'FATAL: {args.filename}: error stroking {glyph.glyphname}:', file=sys.stderr)
            raise
        finally:
            unsilence()
        if args.verbose >= 2:
            print(f'{args.filename}: finished expanding strokes on glyph {glyph.glyphname}')

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
