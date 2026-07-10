#!/usr/bin/env -S fontforge -quiet -lang=py -script
import fontforge, argparse, math, unicodedata, psMat, os, sys, numpy

sys.path.append(os.getenv("HOME") + "/git/dse.d/pyfontutils/lib")
from font_utils import parse_char_str, u

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    for glyph in font.glyphs():
        glyph.temporary = {}
        parsed = parse_char_str(glyph.glyphname, (-1,))
        norm_cp = parsed[2]
        glyph.temporary["norm_codepoint"] = norm_cp
        glyph.temporary["char"] = chr(norm_cp) if norm_cp >= 0 else None
        glyph.temporary["cat"] = unicodedata.category(chr(norm_cp)) if norm_cp >= 0 else None

    for glyph in font.glyphs():
        italic_shift_type = compute_italic_shift_type(glyph)
        if italic_shift_type is not None:
            if args.verbose:
                print("%s: %s (%s): italic shift for %s case letters" % (args.filename,
                                                                         glyph.glyphname,
                                                                         u(glyph.unicode),
                                                                         italic_shift_type))
            do_italic_shift(glyph, italic_shift_type)

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
            
    font.close()

def compute_italic_shift_type(glyph):
    global args
    if is_italicized(glyph):
        if glyph.temporary["cat"] in ["Ll"]:
            return "lower"
        elif glyph.temporary["cat"] in ["Lu"]:
            return "upper"
        else:
            return None
    if not len(glyph.references): # non-italicized without references
        return None
    ref_glyphs = [glyph.font[ref[0]] for ref in glyph.references]
    ref_base_glyphs = [glyph for glyph in ref_glyphs if is_italicizable_base(glyph)]
    italic_shift_types = set([compute_italic_shift_type(glyph) for glyph in ref_base_glyphs])
    if italic_shift_types == set("Ll"):
        return "lower"
    elif None in italic_shift_types:
        return None
    else:                       # either uppercase only or mixed upper/lowercase
        return "upper"

def is_italicized(glyph):
    return glyph.comment == "italicized" or any([
        is_italicized(glyph.font[ref[0]]) for ref in glyph.references
    ])

def do_italic_shift(glyph, italic_shift_type):
    global args
    if italic_shift_type == "lower":
        base_y_center = glyph.font.xHeight / 2
    else:
        base_y_center = glyph.font.capHeight / 2
    if not len(glyph.references):
        return
    new_refs = []

    glyphs = get_glyph_ref_struct(glyph)
    italicizable_base_glyph_names = [g.glyphname for g in glyphs if is_italicizable_base(g)]
    italicizable_marks = [
        glyph.font[ref[0]]
        for ref in glyph.references
        if is_italicizable_mark(glyph.font[ref[0]])
    ]

    ref_glyphs = [glyph.font[ref[0]] for ref in glyph.references]
    ref_base_glyphs = [glyph for glyph in ref_glyphs if is_italicizable_base(glyph)]
    ref_base_glyph_names = [glyph.glyphname for glyph in ref_base_glyphs]

    correction = 0
    if italicizable_base_glyph_names == ["a"]:
        correction = 80
    elif italicizable_base_glyph_names == ["y"]:
        correction = 20

    for ref in glyph.references:
        ref_glyph = glyph.font[ref[0]]
        if is_italicizable_mark(ref_glyph):
            (_, y_min, _, y_max) = ref_glyph.boundingBox()
            (x_min, y_min, x_max, y_max) = ref_glyph.boundingBox()

            # work with transformed accent references
            center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
            center = transform_point(center, ref[1])
            mark_y_center = center[1]

            if args.verbose:
                print("    %s (%s) is %d milliems above the appropriate height" % (ref_glyph.glyphname,
                                                                                   u(ref_glyph.unicode),
                                                                                   abs(mark_y_center - base_y_center)))
            shift_x = (mark_y_center - base_y_center) * math.tan(-glyph.font.italicangle * math.pi / 180) + correction
            if args.verbose:
                print("    shifting %s (%s) %d milliems to the right" % (ref_glyph.glyphname,
                                                                         u(ref_glyph.unicode),
                                                                         shift_x))
            transform = psMat.compose(ref[1], psMat.translate(shift_x, 0))
            ref = list(ref)
            ref[1] = transform
            new_refs.append(tuple(ref))
        else:
            new_refs.append(ref)
    glyph.references = tuple(new_refs)

def is_italicizable_mark(glyph):
    return glyph.temporary["norm_codepoint"] in range(0x0300, 0x0370) or \
        glyph.glyphname == "x_mediumhorizline"

def is_italicizable_base(glyph):
    return glyph.temporary["cat"] in ["Ll", "Lu"]

def transform_point(point, transform):
    point = (*point, 1)
    (a, b, c, d, e, f) = transform
    t = numpy.array([[a, c, e], [b, d, f], [0, 0, 1]])
    point = t @ point
    return point[0:2]

def get_glyph_ref_struct(glyph):
    a = [glyph] if len(glyph.foreground) else []
    for ref in glyph.references:
        a += get_glyph_ref_struct(glyph.font[ref[0]])
    return a

def flatten_deep(iterable):
    for item in iterable:
        # Check if the item is a list or tuple, but exclude strings
        if isinstance(item, (list, tuple)):
            yield from flatten_deep(item)
        else:
            yield item

main()
