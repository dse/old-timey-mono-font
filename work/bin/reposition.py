#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import argparse, fontforge, unicodedata
from pprint import pprint

MARK_NONSPACING         = "Mn"
MARK_SPACING            = "Mc"
MARK_ENCLOSING          = "Me"
MARK_CATEGORIES         = ["Mn", "Mc", "Me"]

UNICODE_RANGE = range(0x0000, 0x110000)

HAS_ASCENDER = {
    "b": True,
    "d": True,
    "f": True,
    "h": True,
    "k": True,
    "l": True,
    "t": True,
    "\u040e": True,  # how does has_ascender otherwise think it's not?
    "\u04ee": True,  # same
    "\u04f2": True,  # same
    "\u0423": True,  # even though we mark THIS glyph as having one?
    "\u0431": True,
    "\u0444": True,
    "\u0452": True,
    "\u045b": True,
    "\u04bb": True,
}

MARK_TYPE_OTHER = -1
MARK_TYPE_ABOVE = 0
MARK_TYPE_TOP_RIGHT = 1
MARK_TYPE_BELOW = 2
MARK_TYPE_ABOVE_RIGHT = 3
MARK_TYPE_ABOVE_SPACING = 4
DEFAULT_MARK_TYPE = MARK_TYPE_ABOVE

MARK_TYPE = {
    "\u031b": MARK_TYPE_TOP_RIGHT,
    "\u0315": MARK_TYPE_ABOVE_RIGHT,
    "\u0326": MARK_TYPE_BELOW,
    "\u0327": MARK_TYPE_BELOW,
    "\u0328": MARK_TYPE_BELOW,
    "\u0345": MARK_TYPE_BELOW,
    "\u037a": MARK_TYPE_BELOW,
    "\u0384": MARK_TYPE_ABOVE,
    "\u0385": MARK_TYPE_ABOVE,  # •/•
    "\u0387": MARK_TYPE_OTHER,
    "\u1fbe": MARK_TYPE_BELOW,
    "\u1fc0": MARK_TYPE_ABOVE_SPACING,
}

SHIFT_MARK = {
    "C":          20,
    "G":          20,
    "J":         240,
    "L":        -200,
    "Æ":         120,
    "a":         -80,
    "f":         120,
    "g":         -60,
    "i":         -60,
    "dotlessi":  -60,
    "j":          40,
    "dotlessj":   40,
    "n":         -40,
    "t":         -80,
    "u":         -30,
};

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='+')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    for filename in args.filename:
        print(filename)
        font = fontforge.open(filename)
        for glyph in font.glyphs():
            if len(glyph.references) < 2: # not a composite glyph
                continue
            unicode = get_origin_unicode(glyph)
            if unicode not in UNICODE_RANGE:
                continue
            (string, glyphs_and_ctxs, name_string, *_) = get_glyph_struct(glyph)
            has = get_glyph_has(glyph)
            if string is None:
                continue
            if "base" not in has:
                continue
            if "mark_above" not in has:
                continue
            if string == "(base,mark_above)":
                (base, base_ctx) = glyphs_and_ctxs[0]
                (mark, mark_ctx) = glyphs_and_ctxs[1]
                (base_ctx_glyph, base_ctx_index) = base_ctx
                (mark_ctx_glyph, mark_ctx_index) = mark_ctx
                refs = [list(r) for r in mark_ctx_glyph.references]
                mark_ref = refs[mark_ctx_index]
                origin_base_unicode = get_origin_unicode(base)
                origin_mark_unicode = get_origin_unicode(mark)
                origin_base_ctx_unicode = get_origin_unicode(base_ctx_glyph)
                origin_mark_ctx_unicode = get_origin_unicode(mark_ctx_glyph)
                if origin_base_unicode not in UNICODE_RANGE:
                    continue
                if origin_mark_unicode not in UNICODE_RANGE:
                    continue
                origin_base_char = chr(origin_base_unicode)

                # horizontal shift
                shift_horiz = 0
                if origin_base_char in SHIFT_MARK:
                    shift_horiz = SHIFT_MARK[origin_base_char]
                elif base.glyphname in SHIFT_MARK:
                    shift_horiz = SHIFT_MARK[base.glyphname]
                xform = psMat.translate(shift_horiz, 0)
                if has_ascender(glyph):
                    mark_name = mark_ref[0].split(".")[0]
                    mark_ref[0] = mark_name
                elif has_ascender(base):
                    mark_name = mark_ref[0].split(".")[0]
                    mark_ref[0] = mark_name
                else:
                    mark_name = mark_ref[0].split(".")[0]
                    mark_name_LCCM = mark_name + ".LCCM"
                    if mark_name_LCCM in font:
                        mark_ref[0] = mark_name_LCCM
                    else:
                        mark_ref[0] = mark_name
                mark_ref[1] = xform
                mark_ctx_glyph.references = []
                for idx, ref in enumerate(refs):
                    if idx == mark_ctx_index:
                        mark_ctx_glyph.addReference(*mark_ref)
                    else:
                        mark_ctx_glyph.addReference(*ref)
                if args.verbose:
                    if shift_horiz > 0:
                        print("%s: positioned %s above, shifting right by %d" % (glyph.glyphname, mark.glyphname, shift_horiz))
                    elif shift_horiz < 0:
                        print("%s: positioned %s above, shifting left by %d" % (glyph.glyphname, mark.glyphname, -shift_horiz))
                    else:
                        print("%s: positioned %s above, with no horizontal shift" % (glyph.glyphname, mark.glyphname))
            else:
                if args.verbose:
                    print("%s: not yet implemented: %s" % (glyph.glyphname, string))
                if args.verbose >= 2:
                    indent = len(": not yet implemented: ") + len(glyph.glyphname)
                    print("%-*s%s" % (indent, "", name_string))
                    print("%-*s%s" % (indent, "", [x[0].glyphname for x in glyphs_and_ctxs]))
                    (expanded_string, expanded_glyphs_and_ctxs, expanded_name_string, *_) = get_glyph_struct(glyph, expand=True)
                    print("%-*s%s" % (indent, "", expanded_string))
                    print("%-*s%s" % (indent, "", expanded_name_string))
                    print("%-*s%s" % (indent, "", [x[0].glyphname for x in expanded_glyphs_and_ctxs]))
            # elif string == "((base,base),mark_above)":
            # elif string == "((base,mark_above),mark_above)":
            # elif string == "(base,(base,(base,mark_above)))":
            # elif string == "(base,(base,mark_above))":
        if filename.endswith(".sfd"):
            print("Saving %s" % filename)
            font.save(filename)
        else:
            print("Generating %s" % filename)
            font.generate(filename)
        font.close()

def get_origin_unicode(glyph):
    glyphname = glyph.glyphname
    unicode = fontforge.unicodeFromName(glyphname)
    if unicode in UNICODE_RANGE:
        return unicode
    unicode = fontforge.unicodeFromName(glyphname.split(".")[0])
    if unicode in UNICODE_RANGE:
        return unicode
    return -1

def find_base_glyphs(glyph):
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            return []
        if is_mark(glyph):
            return []
        return [glyph]
    glyphs = []
    for ref in glyph.references:
        add_glyphs = find_base_glyphs(glyph.font[ref[0]])
        glyphs += add_glyphs
    return glyphs

def has_ascender(glyph):
    if glyph.glyphname in HAS_ASCENDER:
        return HAS_ASCENDER[glyph.glyphname]
    if glyph.unicode in UNICODE_RANGE:
        if glyph.unicode in HAS_ASCENDER:
            return HAS_ASCENDER[glyph.unicode]
        if chr(glyph.unicode) in HAS_ASCENDER:
            return HAS_ASCENDER[chr(glyph.unicode)]

    origin_glyphname = glyph.glyphname.split(".")[0]
    origin_glyph = glyph.font[origin_glyphname]
    origin_unicode = get_origin_unicode(glyph)
    if "." in glyph.glyphname:  # meaning glyph is x.y and we're checking x
        if origin_glyph.glyphname in HAS_ASCENDER:
            return HAS_ASCENDER[origin_glyph.glyphname]
        if origin_glyph.unicode in UNICODE_RANGE:
            if origin_glyph.unicode in HAS_ASCENDER:
                return HAS_ASCENDER[origin_glyph.unicode]
            if chr(origin_glyph.unicode) in HAS_ASCENDER:
                return HAS_ASCENDER[chr(origin_glyph.unicode)]
            
    base_glyphs = find_base_glyphs(glyph)
    for base_glyph in base_glyphs:
        if base_glyph.glyphname == glyph.glyphname:
            continue            # avoid recursion
        if has_ascender(base_glyph):
            return True

    if chr(origin_unicode).islower():
        return False            # assume l/c chars don't have them 
    return True                 # assume u/c chars do

def is_mark_above(glyph):
    origin_unicode = get_origin_unicode(glyph)
    if origin_unicode not in UNICODE_RANGE:
        return False
    if unicodedata.category(chr(origin_unicode)) not in MARK_CATEGORIES:
        return False
    return MARK_TYPE.get(chr(origin_unicode), DEFAULT_MARK_TYPE) == MARK_TYPE_ABOVE

def is_mark(glyph):
    origin_unicode = get_origin_unicode(glyph)
    if origin_unicode not in UNICODE_RANGE:
        return False
    if unicodedata.category(chr(origin_unicode)) not in MARK_CATEGORIES:
        return False
    return True

# attempt to normalize glyph structures
def get_glyph_sort_order(glyph, idx=-1):
    if glyph is None:
        return 99
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            return 98
        if is_mark(glyph):
            if is_mark_above(glyph):
                return 2
            return 3
        return 1
    return min([get_glyph_sort_order(glyph.font[ref[0]]) for ref in enumerate(glyph.references)])

def get_glyph_struct(glyph, all_marks=False, context=None, expand=False):
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            return ("blank", [(glyph, context)], glyph.glyphname, glyph)
        if is_mark(glyph):
            if is_mark_above(glyph):
                return ("mark_above", [(glyph, context)], glyph.glyphname, glyph)
            if all_marks:
                return ("mark_not_above", [(glyph, context)], glyph.glyphname, glyph)
            return None
        return ("base", [(glyph, context)], glyph.glyphname, glyph)
    structs = []
    for idx, ref in enumerate(glyph.references):
        referent_name = ref[0]
        referent_glyph = glyph.font[referent_name]
        struct = get_glyph_struct(referent_glyph, all_marks=all_marks, context=(glyph, idx), expand=expand)
        if struct is None or len(struct) == 0:
            continue
        structs.append(struct)
    if len(structs) == 0:
        return None
    structs.sort(key=lambda struct: get_glyph_sort_order(struct[3]))
    strings = []
    glyphs_and_ctxs = []
    if expand:
        glyphs_and_ctxs.append((glyph, context))
    names = []
    for struct in structs:
        strings.append(struct[0])
        names.append(struct[2])
        for add_glyph_and_ctx in struct[1]:
            glyphs_and_ctxs.append(add_glyph_and_ctx)
    if not expand:
        if len(structs) == 1:
            return (("%s" % ",".join(strings)), glyphs_and_ctxs,
                    ("%s" % ",".join(names)), glyph)
        return (("(%s)" % ",".join(strings)), glyphs_and_ctxs,
                ("(%s)" % ",".join(names)), glyph)
    return (("comp(%s)" % ",".join(strings)), glyphs_and_ctxs,
            ("%s(%s)" % (glyph.glyphname, ",".join(names))), glyph)
    
def get_glyph_has(glyph, has=None):
    if has is None:
        has = {}
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            has["blank"] = has.get("blank", 0) + 1
            return has
        if is_mark(glyph):
            if is_mark_above(glyph):
                has["mark_above"] = has.get("mark_above", 0) + 1
                return has
            has["mark_not_above"] = has.get("mark_not_above", 0) + 1
            return has
        has["base"] = has.get("base", 0) + 1
        return has
    has["comp"] = has.get("comp", 0) + 1
    for idx, ref in enumerate(glyph.references):
        get_glyph_has(glyph.font[ref[0]], has)
    return has

main()
