#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, sys, re, json, psMat

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.index import index_svg_filenames, index_glyphs, match_glyphs, index_glyph_names
from otm.util import walk_svg
from my_font_utils import DEFAULT_GLYPHS_DATA_JSON_FILENAME
from otm.generated import GENERATED_GLYPH_CODES

DEFAULT_WIDTH = 1008
DEFAULT_STROKE_WIDTH = 96

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('svg_filenames', nargs='*')
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    if len(args.svg_filenames):
        svg_filenames = walk_svg(args.svg_filenames)
    else:
        svg_filenames = walk_svg(["src/upright"])
    if not len(svg_filenames):
        raise Exception("no SVGs to import")

    font = fontforge.open(args.filename)

    svg_list, svg_dict = index_svg_filenames(svg_filenames)
    glyph_list, glyph_dict = index_glyphs(font)

    matched_svg_list = match_glyphs(svg_list, svg_dict, glyph_list, glyph_dict)[1]

    smol_glyph_names = [glyph.glyphname for glyph in font.glyphs() if glyph.glyphname.endswith(".SMOL")]
    smol_glyph_list, smol_glyph_dict = index_glyph_names(smol_glyph_names)

    for item in [*matched_svg_list, *smol_glyph_list]:
        glyph = font.createChar(item.code, item.name)
        if item.code in GENERATED_GLYPH_CODES:
            # print("%s: is a generated char; skipping..." % glyph.glyphname)
            continue
        if len(glyph.references) and len(glyph.foreground):
            raise Exception(f"glyph {glyph.glyphname} contains both contours AND references")
        if len(glyph.references):
            # print("%s: has %d references; trying to unroll..." % (glyph.glyphname, len(glyph.references)))
            unroll(glyph)

    for item in [*matched_svg_list, *smol_glyph_list]:
        glyph = font.createChar(item.code, item.name)
        if item.code in GENERATED_GLYPH_CODES:
            # print("%s: is a generated char; skipping..." % glyph.glyphname)
            continue
        if not len(glyph.foreground):
            # print("%s: no contours; skipping..." % (glyph.glyphname))
            continue
        stroke_width = None
        if item.code in STROKE_WIDTHS:
            stroke_width = STROKE_WIDTHS[item.code]
        elif glyph.glyphname in STROKE_WIDTHS:
            stroke_width = STROKE_WIDTHS[glyph.glyphname]
        elif item.variant in STROKE_WIDTHS:
            stroke_width = STROKE_WIDTHS[item.variant]
        if stroke_width is None:
            ranges = [r for r in STROKE_WIDTHS if isinstance(r, range)]
            for r in ranges:
                if item.code in r:
                    stroke_width = STROKE_WIDTHS[r]
                    break
        if stroke_width is None:
            lists = [r for r in STROKE_WIDTHS if type(r) is list]
            for l in lists:
                if item.code in l:
                    stroke_width = STROKE_WIDTHS[l]
                    break
        if stroke_width is None:
            stroke_width = DEFAULT_STROKE_WIDTH
        if not stroke_width:
            continue
        fill = item.code in FILL_GLYPHS or glyph.glyphname in FILL_GLYPHS
        # print("%s: stroking ..." % glyph.glyphname)
        glyph.stroke("circular", stroke_width, removeinternal=fill)

    if args.filename.endswith('.sfd'):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

STROKE_WIDTHS = {
    ".SMOL": 72,
    "x_nutfractionbar": 72,
    "x_ordinalindicatorbar": 72,
    "x_copyrightcircle": 72,
    0x269b: 0,  # ATOM SYMBOL
    0x2620: 0,  # SKULL AND CROSSBONES
    0x2622: 0,  # RADIOACTIVE SIGN
    0x2623: 0,  # BIOHAZARD SIGN
    0x2139: 0,  # INFORMATION SOURCE
    0x237c: 48, # RIGHT ANGLE WITH DOWNWARDS ZIGZAG ARROW (ANGZARR)
    0x2388: 48, # HELM SYMBOL
    0x2190: 72, # LEFTWARDS ARROW (LEFT ARROW)
    0x2191: 72, # UPWARDS ARROW (UP ARROW)
    0x2192: 72, # RIGHTWARDS ARROW (RIGHT ARROW)
    0x2193: 72, # DOWNWARDS ARROW (DOWN ARROW)
    0x2194: 72, # LEFT RIGHT ARROW
    0x2195: 72, # UP DOWN ARROW
    0x2196: 72, # NORTH WEST ARROW (UPPER LEFT ARROW)
    0x2197: 72, # NORTH EAST ARROW (UPPER RIGHT ARROW)
    0x2198: 72, # SOUTH EAST ARROW (LOWER RIGHT ARROW)
    0x2199: 72, # SOUTH WEST ARROW (LOWER LEFT ARROW)
    0x219a: 72, # LEFTWARDS ARROW WITH STROKE (LEFT ARROW WITH STROKE)
    0x219b: 72, # RIGHTWARDS ARROW WITH STROKE (RIGHT ARROW WITH STROKE)
    0x219e: 72, # LEFTWARDS TWO HEADED ARROW (LEFT TWO HEADED ARROW)
    0x219f: 72, # UPWARDS TWO HEADED ARROW (UP TWO HEADED ARROW)
    0x21a0: 72, # RIGHTWARDS TWO HEADED ARROW (RIGHT TWO HEADED ARROW)
    0x21a1: 72, # DOWNWARDS TWO HEADED ARROW (DOWN TWO HEADED ARROW)
    0x21a8: 72, # UP DOWN ARROW WITH BASE
    0x21ae: 72, # LEFT RIGHT ARROW WITH STROKE
}

FILL_GLYPHS = [
    0x00a8, # DIAERESIS (SPACING DIAERESIS)
    0x00ba, # MASCULINE ORDINAL INDICATOR
    0x0308, # COMBINING DIAERESIS (NON-SPACING DIAERESIS)
    0x0307, # COMBINING DOT ABOVE (NON-SPACING DOT ABOVE)
    0x0358, # COMBINING DOT ABOVE RIGHT
    0x0310, # COMBINING CANDRABINDU (NON-SPACING CANDRABINDU)
    0x0323, # COMBINING DOT BELOW (NON-SPACING DOT BELOW)
    0x0324, # COMBINING DIAERESIS BELOW (NON-SPACING DOUBLE DOT BELOW)
    0x0352, # COMBINING FERMATA
    0x2022, # BULLET
    0x2034, # TRIPLE PRIME
    0x2037, # REVERSED TRIPLE PRIME
    0x204c, # BLACK LEFTWARDS BULLET
    0x204d, # BLACK RIGHTWARDS BULLET
    0x2055, # FLOWER PUNCTUATION MARK
    0x2234, # THEREFORE
    0x25a0, # BLACK SQUARE
    0x25cf, # BLACK CIRCLE
    0x25d8, # INVERSE BULLET
    0x25d9, # INVERSE WHITE CIRCLE
    0x2605, # BLACK STAR
    0x263b, # BLACK SMILING FACE
    0x2660, # BLACK SPADE SUIT
    0x2663, # BLACK CLUB SUIT
    0x2665, # BLACK HEART SUIT
    0x2666, # BLACK DIAMOND SUIT
    ord('"'),
    ord("."),
    ord("'"),
    ord("!"),
    "uni0308.LCCM",             # diaeresis
    "uni0307.LCCM",             # dot above
]

def unroll(glyph, sub_glyph=None, transform=(1,0,0,1,0,0), indent=""):
    # print(indent + "unroll(%s, %s, transform=%s)" % (glyph.glyphname, sub_glyph.glyphname if sub_glyph else "None", transform))
    if not sub_glyph and not glyph.references:
        return
    if not sub_glyph:
        sub_glyph = glyph
    for ref in sub_glyph.references:
        # print(indent + "  %s has reference %s" % (sub_glyph.glyphname, repr(ref)))
        ref_glyphname, ref_transform, *_ = ref
        ref_glyph = glyph.font[ref_glyphname]
        new_transform = psMat.compose(transform, ref_transform)
        unroll(glyph, ref_glyph, transform=new_transform, indent=indent+"    ")
    if sub_glyph is not glyph:
        for contour in sub_glyph.foreground:
            # print(indent + "  %s has contour of length %d; drawing into %s" % (sub_glyph.glyphname, len(contour), glyph.glyphname))
            contour = contour.dup()
            contour.transform(transform)
            pen = glyph.glyphPen(replace=False)
            contour.draw(pen)
            pen = None
    sub_glyph.references = ()

main()
