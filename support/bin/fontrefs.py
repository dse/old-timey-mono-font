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

    for (char_name, referent_char) in data.items():
        if char_name[0] == "$":
            continue
        (codepoint, glyphname, *_) = font_utils.parse_char_str(char_name)
        glyph = font.createChar(codepoint, glyphname)
        glyph.foreground = fontforge.layer() # erase anything existing
        glyph.references = ()
        add_refs(glyph, referent_char)

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def add_refs(glyph, dest, data=None):
    if type(dest) is str:
        if dest[0] == "$":
            return
        (codepoint, glyphname, *_) = font_utils.parse_char_str(dest)
        if glyphname not in glyph.font:
            print("%s: %s (%s): referent glyph %s not found" % (glyph.font.path, glyph.glyphname, u(glyph.unicode), glyphname))
            return
        width = glyph.width
        transform = psMat.identity()
        if type(data) == dict:
            x = 0
            y = 0
            rotate = 0
            if "center" in data:
                (x, y) = data["center"]
            if "rotate" in data:
                rotate = data["rotate"]
            if x or y:
                transform = psMat.compose(transform, psMat.translate(-x, -y))
            if rotate:
                transform = psMat.compose(transform, psMat.rotate(rotate / 180 * math.pi))
            if x or y:
                transform = psMat.compose(transform, psMat.translate(x, y))
            if "translate" in data:
                [translate_x, translate_y] = data["translate"]
                transform = psMat.compose(transform, psMat.translate(translate_x, translate_y))
            transform = tuple([0 if abs(a) < 1e-6 else a for a in transform])
        glyph.addReference(glyphname, transform)
        if width:
            glyph.width = width
        else:
            glyph.width = glyph.font["H"].width
    elif type(dest) is list:
        for dest_item in dest:
            add_refs(glyph, dest_item)
    elif type(dest) is dict:
        for dest_char_name, dest_char_data in dest.items():
            add_refs(glyph, dest_char_name, dest_char_data)

def round_if_approx(num):
    if abs(round(num) - num) < 0.000001:
        return round(num)
    return num

main()
