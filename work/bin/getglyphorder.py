#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    full_data = {}
    data = []
    full_data["glyphOrder"] = data

    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        data.append({
            "glyphname": glyph.glyphname,
            "unicode": glyph.unicode,
            "encoding": glyph.encoding,
            "altuni": glyph.altuni,
        })
    font.close()

    print(json.dumps(full_data, indent=4))

main()
