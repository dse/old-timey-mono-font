#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge, argparse, unicodedata, numpy, math

GC = {
    "Lu": "Uppercase_Letter",
    "Ll": "Lowercase_Letter",
    "Lt": "Titlecase_Letter",
    "LC": "Cased_Letter",
    "Lm": "Modifier_Letter",
    "Lo": "Other_Letter",
    "L": "Letter",
    "Mn": "Nonspacing_Mark",
    "Mc": "Spacing_Mark",
    "Me": "Enclosing_Mark",
    "M": "Mark",
    "Nd": "Decimal_Number",
    "Nl": "Letter_Number",
    "No": "Other_Number",
    "N": "Number",
    "Pc": "Connector_Punctuation",
    "Pd": "Dash_Punctuation",
    "Ps": "Open_Punctuation",
    "Pe": "Close_Punctuation",
    "Pi": "Initial_Punctuation",
    "Pf": "Final_Punctuation",
    "Po": "Other_Punctuation",
    "P": "Punctuation",
    "Sm": "Math_Symbol",
    "Sc": "Currency_Symbol",
    "Sk": "Modifier_Symbol",
    "So": "Other_Symbol",
    "S": "Symbol",
    "Zs": "Space_Separator",
    "Zl": "Line_Separator",
    "Zp": "Paragraph_Separator",
    "Z": "Separator",
    "Cc": "Control",
    "Cf": "Format",
    "Cs": "Surrogate",
    "Co": "Private_Use",
    "Cn": "Unassigned",
    "C": "Other",
}

UPPER_CASE_CATEGORIES = [
    "Uppercase_Letter",
    "Titlecase_Letter",
    "Decimal_Number",
    "Letter_Number",
    "Currency_Symbol",
]

LOWER_CASE_CATEGORIES = [
    "Lowercase_Letter",
    "Math_Symbol",
]

COMBINING_CATEGORIES = [
    "Nonspacing_Mark",
    "Spacing_Mark",
    "Enclosing_Mark",
]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    font = fontforge.open(args.filename)
    font.temporary = { "italicized": {} }
    if not font.italicangle:
        font.italicangle = -12.0
    for glyph in font.glyphs():
        italicize_refs(glyph)
    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def italicize_refs(glyph, pivot_y):
    pivot_y = get_pivot_y(glyph)
    new_refs = []
    for ref in glyph.references():
        ref_glyphname = ref[0]
        ref_glyph = glyph.font[ref_glyphname]
        ref_transform = ref[1]
        (xmin, ymin, xmax, ymax) = glyph.boundingBox()
        center = ((xmin + xmax) / 2, (ymin + ymax) / 2)
        center = transform_point(center, ref_transform)
        shift_x = (y - pivot_y) * math.tan(-glyph.font.italicangle * math.pi / 180)
        transform = psMat.compose(ref_transform, psMat.translate(shift_x, 0))
        new_refs.append((ref_glyphname, transform))
    glyph.references = tuple(new_refs)

def _get_pivot_y(glyph):
    """backend for get_pivot_y that does not compute average y-coordinates"""
    unicode = get_base_unicode(glyph)
    if unicode in range(0, 0x110000):
        glyphname_split = glyph.glyphname.split(".", 1)[1]
        variant = glyphname_split[1] if len(glyphname_split) > 1 else None
        gc = GC.get(unicodedata.category(chr(unicode)))
        if gc in UPPER_CASE_CATEGORIES:
            if variant == "c2pc": # petite caps
                return glyph.font.xHeight / 2
            elif variant == "c2sc": # small caps
                return (glyph.font.xHeight + glyph.font.capHeight) / 4
            else:
                return glyph.font.capHeight / 2
        elif gc in LOWER_CASE_CATEGORIES:
            return glyph.font.xHeight / 2
    for ref in glyph.references:
        ref_glyphname = ref[0]
        ref_glyph = glyph.font[ref_glyphname]
        pivot_y = get_pivot_y[ref_glyph]
        if pivot_y is not None:
            return pivot_y
    return None

def get_pivot_y(glyph):
    pivot_y = _get_pivot_y[ref_glyph]
    if pivot_y is not None:
        return pivot_y
    (_, ymin, _, ymax) = glyph.boundingBox()
    return (ymin + ymax) / 2

def get_base_unicode(glyph):
    if glyph.unicode < 0:
        glyphname = glyph.glyphname.split(".")[0]
        return fontforge.unicodeFromName(glyphname)
    return glyph.unicode

def transform_y(y, transform):
    point = (0, y, 1)
    (a, b, c, d, e, f) = transform
    t = numpy.array([[a, c, e], [b, d, f], [0, 0, 1]])
    point = t @ point
    return point[1]

def transform_point(point, transform):
    point = (*point, 1)
    (a, b, c, d, e, f) = transform
    t = numpy.array([[a, c, e], [b, d, f], [0, 0, 1]])
    point = t @ point
    return point[0:2]

main()
