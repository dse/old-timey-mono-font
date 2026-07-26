#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os, pickle

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from fontforge_attr_names import get_valid_font_attr_names

def main():
    global args
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    data = {
        "fontData": {}
    }
    font_data = data["fontData"]

    font = fontforge.font()
    for attr_name in get_valid_font_attr_names(exclude_json=True):
        font_data[attr_name] = getattr(font, attr_name)
    font.close()

    print(json.dumps(data, indent=4))

main()
