#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import os, sys, argparse, fontforge, re, psMat, math, json, unicodedata

sys.path.append("%s/git/dse.d/pyfontutils/lib" % os.environ["HOME"])
import font_utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="font filename")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("json_filename", help="JSON data file")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    with open(args.json_filename) as fp:
        data = json.load(fp)
        data = data["references"]

    for i, (char_name, char_data) in enumerate(data.items()):
        build_char_data = char_data["build"]
        (codepoint, glyphname, base_codepoint, base_glyphname, variant) = font_utils.parse_char_str(char_name)

        base_glyph = font.createChar(codepoint, glyphname)
        base_glyph.foreground = fontforge.layer() # erase anything existing
        base_glyph.references = ()

        old_width = base_glyph.width

        for j, (ref_char_name, build_ref_char_data) in enumerate(build_char_data.items()):
            if build_ref_char_data is None:
                continue

            (ref_codepoint, ref_glyphname, ref_base_codepoint, ref_base_glyphname, ref_variant) = \
                font_utils.parse_char_str(ref_char_name)
            if ref_glyphname not in font:
                print("%s: %s: %s: referent glyph %s not found" % (
                    args.filename, args.json_filename, base_glyphname, ref_glyphname
                ))

            x = 0
            y = 0
            rotate = 0
            if "center" in build_ref_char_data:
                if "x" in build_ref_char_data["center"]:
                    x = build_ref_char_data["center"]["x"]
                if "y" in build_ref_char_data["center"]:
                    y = build_ref_char_data["center"]["y"]
            if "rotate" in build_ref_char_data:
                rotate = build_ref_char_data["rotate"]

            xform = psMat.identity()
            if y or x:
                xform = psMat.compose(xform, psMat.translate(-x, -y))
            if rotate:
                xform = psMat.compose(xform, psMat.rotate(rotate / 180 * math.pi))
            if y or x:
                xform = psMat.compose(xform, psMat.translate(x, y))
            if "translate" in build_ref_char_data:
                [x, y] = build_ref_char_data["translate"]
                xform = psMat.compose(xform, psMat.translate(x, y))
            xform = tuple([round_if_approx(n) for n in xform])

            if args.verbose:
                print("%s: %s: adding reference to %s" % (args.filename, base_glyphname, ref_glyphname))
            base_glyph.addReference(ref_glyphname, xform)

        if old_width:
            base_glyph.width = old_width
        else:
            base_glyph.width = font["H"].width

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def round_if_approx(num):
    if abs(round(num) - num) < 0.000001:
        return round(num)
    return num

main()
