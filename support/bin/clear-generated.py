#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse

sys.path.append(os.path.dirname(__file__) + "/../lib")
from otm.generated import ALL

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for code in ALL:
        try:
            font.removeGlyph(code)
        except ValueError as e:
            if str(e) != "This glyph is not in the font":
                raise
    if args.filename.endswith(".sfd"):
        font.save(filename)
    else:
        font.generate(filename)
    font.close()

main()
