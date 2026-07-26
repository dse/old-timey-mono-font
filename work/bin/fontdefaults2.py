#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os, pickle

# external pkgs
# import dill

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from fontforge_attr_names import FONTFORGE_FONT_ATTR_NAMES

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", type=str)
    args = parser.parse_args()

    data = {}
    defaults = {}
    errors = {}
    data["defaults"] = defaults
    data["errors"] = errors

    font = None
    if args.filename is not None:
        font = fontforge.open(args.filename)
    else:
        font = fontforge.font()
    for attr_name in FONTFORGE_FONT_ATTR_NAMES:
        error_type = None
        try:
            attr_val = getattr(font, attr_name)
            try:
                json.dumps(attr_val)
                defaults[attr_name] = attr_val
            except Exception as error:
                error_type = str(type(error)).split("'")[1]
                attr_val = [error_type, str(error)]
        except Exception as error:
            error_type = str(type(error)).split("'")[1]
            attr_val = [error_type, str(error)]
        if error_type is not None:
            errors[attr_name] = attr_val
        else:
            defaults[attr_name] = attr_val

    font.close()

    print(json.dumps(data, indent=4))

main()
