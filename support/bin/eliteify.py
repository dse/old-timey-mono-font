#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, psMat

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

SHIFT_ACCENT_UP = 264

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    incr = round((round(font.em * 1.2) - round(font.em)) / 2)
    font.ascent += incr
    font.descent += incr

    for glyph in font.glyphs():
        fix_refs(glyph)

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

    font.close()

def fix_refs(glyph, init=True, fixed={}):
    font = glyph.font

    if fixed.get(glyph.glyphname, False):
        return
    if glyph.glyphname.endswith(".LCCM"):
        return
    fixed[glyph.glyphname] = True

    refs = []
    for ref in glyph.references:
        ref_glyphname, ref_transform, ref_selected = ref

        new_ref_glyphname = ref_glyphname + ".LCCM"
        if new_ref_glyphname not in font:
            pass
        elif new_ref_glyphname == "uni0345.LCCM":
            pass
        else:
            if ref_glyphname in font:
                fix_refs(font[ref_glyphname], init=False, fixed=fixed)
            if new_ref_glyphname in font:
                fix_refs(font[new_ref_glyphname], init=False, fixed=fixed)
            if init:
                if (glyph.glyphname, ref_glyphname) == ("uni022C", "uni0304"):
                    ref_glyphname += ".LCCM"
                    ref_transform = psMat.compose(ref_transform, psMat.translate(0, 400))
                elif (glyph.glyphname, ref_glyphname) == ("Aringacute", "acutecomb"):
                    ref_glyphname += ".LCCM"
                    ref_transform = psMat.compose(ref_transform, psMat.translate(0, 400))
                elif (glyph.glyphname, ref_glyphname) == ("uni1FCF", "uni1FC0"):
                    ref_transform = psMat.compose(ref_transform, psMat.translate(0, 250))
                elif (glyph.glyphname, ref_glyphname) == ("uni1FC1", "uni1FC0"):
                    ref_transform = psMat.compose(ref_transform, psMat.translate(0, 300))
                else:
                    ref_glyphname = new_ref_glyphname
                    if ref_glyphname == "uni0305.LCCM":
                        ref_transform = psMat.compose(ref_transform, psMat.translate(0, 30))
                    else:
                        ref_transform = psMat.compose(ref_transform, psMat.translate(0, SHIFT_ACCENT_UP))

        refs.append((ref_glyphname, ref_transform, ref_selected))

    glyph.references = tuple(refs)

def get_flattened_refs(glyph, transform=None, top=True):
    font = glyph.font
    if transform is None:
        transform = psMat.identity()
    if len(glyph.references) == 0:
        if top:
            return []
        else:
            return [(glyph.glyphname, transform, False)]
    refs = []
    for ref in glyph.references:
        ref_glyphname, ref_xform, ref_selected = ref
        ref_xform = psMat.compose(ref_xform, transform)
        refs += get_flattened_refs(font[ref_glyphname], ref_xform, False)
    return tuple(refs)

main()
