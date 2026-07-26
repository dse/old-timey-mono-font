#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os, pickle

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from fontforge_attr_names import get_valid_glyph_attr_names

def main():
    global args
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    data = {
        "glyphData": {}
    }
    glyph_data = data["glyphData"]

    font = fontforge.font()
    glyph = font.createChar(65)
    for attr_name in get_valid_glyph_attr_names(exclude_json=True):
        glyph_data[attr_name] = getattr(glyph, attr_name)
    font.close()

    print(json.dumps(data, indent=4))

main()
