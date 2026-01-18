#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import argparse, fontforge, unicodedata
from pprint import pprint

RD_REFERENT_GLYPHNAME   = 0
RD_REF_IDX              = 1
RD_REF_TUPLE            = 2
RD_REF_GLYPHNAME        = 3
RD_REF_TRANSFORM        = 4
RD_REF_SELECTED         = 5
RD_REF_BASE_GLYPHNAME   = 6
RD_REF_BASE_UNICODE     = 7
RD_ORDER                = 8

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
print(chr(0x04ee) in HAS_ASCENDER)

MARK_TYPE_ABOVE = 0
MARK_TYPE_TOP_RIGHT = 1
MARK_TYPE_BELOW = 2
MARK_TYPE_ABOVE_RIGHT = 3
MARK_TYPE_ABOVE_SPACING = 4

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
    "\u0387": -1,
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
    args = parser.parse_args()
    for filename in args.filename:
        print(filename)
        font = fontforge.open(filename)
        for glyph in font.glyphs():
            if len(glyph.references) < 2:
                print("%s: not a composite glyph" % glyph.glyphname)
                continue
            unicode = glyph.unicode
            if unicode not in UNICODE_RANGE:
                if "." not in glyph.glyphname:
                    print("%s: out of range" % glyph.glyphname)
                    continue
                unicode = fontforge.unicodeFromName(glyph.glyphname.split(".")[0])
            if unicode not in UNICODE_RANGE:
                print("%s: out of range" % glyph.glyphname)
                continue
            charname = unicodedata.name(chr(unicode))

            (string, glyphs_and_ctxs, names) = get_glyph_struct(glyph, no_marks_not_above=True)
            has = get_glyph_has(glyph)
            if string is None:
                print("%s: no string representation of structure" % glyph.glyphname)
                continue
            if "base" not in has:
                print("%s: no base glyph" % glyph.glyphname)
                continue
            if "mark_above" not in has:
                print("%s: no mark_above glyph" % glyph.glyphname)
                continue
            if string == "(base,mark_above)":
                print("%s: %s" % (glyph.glyphname, string))
                (unrolled_string, _, _) = get_glyph_struct(glyph, no_marks_not_above=True, unroll=True)
                print("%*s  uncompactified %s" % (len(glyph.glyphname), "", unrolled_string))

                (base, base_ctx) = glyphs_and_ctxs[0]
                print("    base glyph is %s" % base.glyphname)
                (mark, mark_ctx) = glyphs_and_ctxs[1]
                print("    mark glyph is %s" % mark.glyphname)

                (base_ctx_glyph, base_ctx_index) = base_ctx
                (mark_ctx_glyph, mark_ctx_index) = mark_ctx

                print("    base context is %s.references[%s]" % (base_ctx_glyph.glyphname, base_ctx_index))
                print("    mark context is %s.references[%s]" % (mark_ctx_glyph.glyphname, base_ctx_index))

                refs = [list(r) for r in mark_ctx_glyph.references]
                mark_ref = refs[mark_ctx_index]

                print("    %s's references:" % mark_ctx_glyph.glyphname)
                for ref in mark_ctx_glyph.references:
                    print("        %s" % repr(ref))

                print("    %s's mark reference: %s" % (mark_ctx_glyph.glyphname, repr(mark_ref)))

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
                print("    trying shifts: %s or %s" % (origin_base_char, base.glyphname))
                shift_horiz = 0
                if origin_base_char in SHIFT_MARK:
                    shift_horiz = SHIFT_MARK[origin_base_char]
                elif base.glyphname in SHIFT_MARK:
                    shift_horiz = SHIFT_MARK[base.glyphname]
                print("    horizontal shift is %d" % shift_horiz)
                xform = psMat.translate(shift_horiz, 0)
                if has_ascender(glyph):
                    print("    original glyph %s HAS an ascender" % glyph.glyphname)
                    mark_name = mark_ref[0].split(".")[0]
                    mark_ref[0] = mark_name
                elif has_ascender(base):
                    print("    base glyph %s HAS an ascender" % base.glyphname)
                    mark_name = mark_ref[0].split(".")[0]
                    mark_ref[0] = mark_name
                else:
                    print("    NEITHER original glyph %s nor base glyph %s has an ascender" % (glyph.glyphname, base.glyphname))
                    mark_name = mark_ref[0].split(".")[0]
                    mark_name_LCCM = mark_name + ".LCCM"
                    if mark_name_LCCM in font:
                        mark_ref[0] = mark_name_LCCM
                    else:
                        mark_ref[0] = mark_name
                mark_ref[1] = xform
                print("    updating %s's mark reference to: %s" % (mark_ctx_glyph.glyphname, repr(mark_ref)))
                print("    we have to re-create its list of references as follows:")
                mark_ctx_glyph.references = []
                for idx, ref in enumerate(refs):
                    if idx == mark_ctx_index:
                        print("        [%d] adding modified reference %s" % (idx, repr(mark_ref)))
                        mark_ctx_glyph.addReference(*mark_ref)
                    else:
                        print("        [%d] adding original reference %s" % (idx, repr(ref)))
                        mark_ctx_glyph.addReference(*ref)
                pprint(glyph.references)
            elif string == "((base,base),mark_above)":
                print("%s: %s not yet implemented" % (glyph.glyphname, string))
            elif string == "((base,mark_above),mark_above)":
                print("%s: %s not yet implemented" % (glyph.glyphname, string))
            elif string == "(base,(base,(base,mark_above)))":
                print("%s: %s not yet implemented" % (glyph.glyphname, string))
            elif string == "(base,(base,mark_above))":
                print("%s: %s not yet implemented" % (glyph.glyphname, string))
            else:
                print("%s: %s not supported" % (glyph.glyphname, string))
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
    print("has_ascender(%s %d):" % (glyph.glyphname, glyph.unicode))
    if glyph.glyphname in HAS_ASCENDER:
        has = HAS_ASCENDER[glyph.glyphname]
        print("    glyph %s is in HAS_ASCENDER by key %s as %s" % (glyph.glyphname,
                                                                   glyph.glyphname, has))
        return has
    if glyph.unicode in UNICODE_RANGE:
        if glyph.unicode in HAS_ASCENDER:
            has = HAS_ASCENDER[glyph.unicode]
            print("    glyph %s is in HAS_ASCENDER by codepoint U+%04X as %s" % (glyph.glyphname,
                                                                                 glyph.unicode,
                                                                                 has))
            return has
        if chr(glyph.unicode) in HAS_ASCENDER:
            has = HAS_ASCENDER[chr(glyph.unicode)]
            print(repr(HAS_ASCENDER))
            print("    glyph %s is in HAS_ASCENDER by character %s (U+%04X) as %s" %
                  (glyph.glyphname, repr(chr(glyph.unicode)), glyph.unicode, has))
            return has

    origin_glyphname = glyph.glyphname.split(".")[0]
    origin_glyph = glyph.font[origin_glyphname]
    origin_unicode = get_origin_unicode(glyph)

    if "." in glyph.glyphname:  # meaning glyph is x.y and we're checking x
        if origin_glyph.glyphname in HAS_ASCENDER:
            has = HAS_ASCENDER[origin_glyph.glyphname]
            print("    origin_glyph %s is in HAS_ASCENDER by key %s as %s" % (origin_glyph.glyphname,
                                                                              origin_glyph.glyphname, has))
            return has
        if origin_glyph.unicode in UNICODE_RANGE:
            if origin_glyph.unicode in HAS_ASCENDER:
                has = HAS_ASCENDER[origin_glyph.unicode]
                print("    origin_glyph %s is in HAS_ASCENDER by codepoint U+%04X as %s" % (origin_glyph.glyphname,
                                                                                            origin_glyph.unicode,
                                                                                            has))
                return has
            if chr(origin_glyph.unicode) in HAS_ASCENDER:
                has = HAS_ASCENDER[chr(origin_glyph.unicode)]
                print("    origin_glyph %s is in HAS_ASCENDER by character %s (U+%04X) as %s" %
                      (origin_glyph.glyphname, repr(chr(origin_glyph.unicode)), origin_glyph.unicode, has))
                return has

            
    base_glyphs = find_base_glyphs(glyph)
    for base_glyph in base_glyphs:
        if base_glyph.glyphname == glyph.glyphname:
            # avoid recursion
            continue
        if has_ascender(base_glyph):
            return True

    # We'd rather put a short accent way above a glyph not having an
    # ascender, than put a tall ascent on top of a glyph with an
    # ascender.  Assume worst case is the former.
    origin_char = chr(origin_unicode)
    if origin_char.islower():
        print("    origin character %s is lower case" % repr(origin_char))
        return False
    print("    origin character %s is NOT lower case" % repr(origin_char))
    return True

def is_mark_above(glyph):
    origin_unicode = get_origin_unicode(glyph)
    if origin_unicode < 0:
        return False
    origin_char = chr(origin_unicode)
    if unicodedata.category(origin_char) not in MARK_CATEGORIES:
        return False
    return MARK_TYPE.get(origin_char, MARK_TYPE_ABOVE) == MARK_TYPE_ABOVE

def is_mark(glyph):
    unicode = fontforge.unicodeFromName(glyph.glyphname.split(".")[0])
    if unicode < 0:
        return False
    if unicodedata.category(chr(unicode)) in MARK_CATEGORIES:
        return True
    return False

def get_glyph_type_order(glyph_type):
    if glyph_type is None:
        return -1
    name = glyph_type[0]
    if name is None:
        return -1
    if name == "blank":
        return 0
    if name == "base":
        return 1
    if name.startswith("("):
        return 2
    if name == "mark":
        return 3
    return 99

def get_glyph_struct(glyph, no_marks_not_above=False, context=None, unroll=False):
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            return ("blank", [(glyph, context)], [(glyph.glyphname, context)])
        if is_mark(glyph):
            if is_mark_above(glyph):
                return ("mark_above", [(glyph, context)], [(glyph.glyphname, context)])
            if no_marks_not_above:
                return None
            return ("mark_not_above", [(glyph, context)], [(glyph.glyphname, context)])
        return ("base", [(glyph, context)], [(glyph.glyphname, context)])

    structs = []
    for idx, ref in enumerate(glyph.references):
        referent_name = ref[0]
        referent_glyph = glyph.font[referent_name]
        struct = get_glyph_struct(referent_glyph, no_marks_not_above=no_marks_not_above, context=(glyph, idx), unroll=unroll)
        if struct is None or len(struct) == 0:
            continue
        structs.append(struct)

    if len(structs) == 0:
        return None
    if len(structs) == 1:
        if unroll:
            return (
                "(" + structs[0][0] + ")", # string
                [structs[0][1]],           # building flat list of glyphs
                [structs[0][2]],           # building flat list of names
            )
        return structs[0]
    
    structs.sort(key=get_glyph_type_order)

    # NOTE: a ctx is a tuple of the origin glyph and the index into
    # its references that points to this glyph.
    strings = []
    glyphs_and_ctxs = []
    names = []
    for struct in structs:
        strings.append(struct[0])
        for add_glyph_and_ctx in struct[1]:
            glyphs_and_ctxs.append(add_glyph_and_ctx)
        for add_name in struct[2]:
            names.append(add_name)
            
    return (("(%s)" % ",".join(strings)), glyphs_and_ctxs, names)

def get_glyph_has(glyph, has=None):
    if has is None:
        has = {}
    if len(glyph.references) == 0:
        if len(glyph.foreground) == 0:
            has["blank"] = True
            return has
        if is_mark(glyph):
            if is_mark_above(glyph):
                has["mark_above"] = True
                return has
            has["mark_not_above"] = True
            return has
        has["base"] = True
        return has
    for idx, ref in enumerate(glyph.references):
        get_glyph_has(glyph.font[ref[0]], has)
    return has

main()
