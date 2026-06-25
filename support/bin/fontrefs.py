#!/usr/bin/env -S fontforge -quiet -script
# -*- mode: python; coding: utf-8 -*-
import os, argparse, fontforge, re, psMat, math, json
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="font filename")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("json_filename", help="JSON data file")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    with open(args.json_filename) as fp:
        data = json.load(fp)

    for i, (base_char, base_char_data) in enumerate(data.items()):
        base_codepoint = ord(base_char[0])
        base_charname = fontforge.nameFromUnicode(base_codepoint)
        base_glyph = font.createChar(base_codepoint, base_charname)
        base_glyph.foreground = fontforge.layer() # erase anything existing
        base_glyph.references = ()
        old_width = base_glyph.width
        for j, (ref_char, ref_char_data) in enumerate(base_char_data.items()):
            ref_codepoint = ord(ref_char[0])
            ref_charname  = fontforge.nameFromUnicode(ref_codepoint)
            ref_glyph     = font[ref_charname]
            if ref_charname not in font:
                print("%s: %s: %s: referent glyph %s not found" % (
                    args.filename, args.json_filename, base_charname, ref_charname
                ))
            if "center" in ref_char_data:
                if "x" in ref_char_data["center"]:
                    x = ref_char_data["center"]["x"]
                else:
                    x = 0
                if "y" in ref_char_data["center"]:
                    y = ref_char_data["center"]["y"]
                else:
                    y = 0
            if "rotate" in ref_char_data:
                rotate = ref_char_data["rotate"]
            else:
                rotate = 0
            xform = psMat.identity()
            if y or x:
                xform = psMat.compose(xform, psMat.translate(-x, -y))
            if rotate:
                xform = psMat.compose(xform, psMat.rotate(rotate / 180 * math.pi))
            if y or x:
                xform = psMat.compose(xform, psMat.translate(x, y))
            xform = tuple([round_if_approx(n) for n in xform])

            if args.verbose:
                print("%s: %s: adding reference to %s" % (args.filename, base_charname, ref_charname))
            base_glyph.addReference(ref_charname, xform)
        if old_width:
            base_glyph.width = old_width
        else:
            base_glyph.width = ref_glyph.width

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def round_if_approx(num):
    if abs(round(num) - num) < 0.000001:
        return round(num)
    return nump

main()
