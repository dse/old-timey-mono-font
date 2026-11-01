#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, sys, re, json, unicodedata, statistics, psMat

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.index import index_svg_filenames, index_glyphs, verify_glyphs
from otm.util import walk_svg
from otm.parse import parse_glyph_name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    references_dict = json.loads(open("src/data/new-references.json", "r").read())["references"]

    font = fontforge.open(args.filename)

    glyph_width = statistics.median([glyph.width for glyph in font.glyphs()])

    iter_count = 0
    while len(references_dict.keys()):
        iter_count += 1
        new_references_dict = {}
        glyph_created_count = 0
        for glyphname, refdata1 in references_dict.items():

            parse_result = parse_glyph_name(glyphname)
            code = parse_result.code
            name = parse_result.norm_glyph_name

            if name in font and len(font[name].foreground):
                raise Exception(f"glyph {glyphname} already contains contours; skipping")
            glyph_references = []
            skip_this_glyph = False
            if type(refdata1) is str:
                if refdata1 in font:
                    glyph_references.append((refdata1,))
                else:
                    skip_this_glyph = True
            elif type(refdata1) is list:
                for refdata2 in refdata1:
                    if type(refdata2) is str:
                        if refdata2 in font:
                            glyph_references.append((refdata2,))
                        else:
                            skip_this_glyph = True
                            break
                    elif type(refdata2) is list:
                        [refdata3, refxforms] = refdata2
                        if refdata3 in font:
                            xform = psMat.identity()
                            for xformitem in refxforms:
                                if xformitem["op"] == "translate":
                                    dx = xformitem.get("dx", 0)
                                    dy = xformitem.get("dy", 0)
                                    if dx or dy:
                                        xform = psMat.compose(xform, psMat.translate(dx, dy))
                                elif xformitem["op"] == "scale":
                                    cx = xformitem.get("cx", 0)
                                    cy = xformitem.get("cy", 0)
                                    sx = xformitem.get("x", 0)
                                    sy = xformitem.get("y", 0)
                                    if cx or cy:
                                        xform = psMat.compose(xform, psMat.translate(-cx, -cy))
                                    xform = psMat.compose(xform, psMat.scale(sx, sy))
                                    if cx or cy:
                                        xform = psMat.compose(xform, psMat.translate(cx, cy))
                                else:
                                    raise Exception(f"unknown translate operation: {repr(xformitem["op"])}")
                            glyph_references.append((refdata3, xform))
                        else:
                            skip_this_glyph = True
                            break
                    else:
                        raise Exception(f"unknown refdata2 type: {repr(type(refdata2))}")
            else:
                raise Exception(f"unknown refdata1 type: {repr(type(refdata2))}")
            if skip_this_glyph:
                new_references_dict[name] = refdata1
                continue
            if not len(glyph_references):
                continue

            glyph_created_count += 1
            glyph = font.createChar(code, name)
            glyph.width = round(glyph_width)
            for ref in glyph_references:
                glyph.addReference(*ref)

        if not glyph_created_count:
            break
        if len(new_references_dict.keys()):
            references_dict = new_references_dict
            continue
        else:
            break

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
