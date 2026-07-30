#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os, re
from psMat import identity, translate, scale, compose

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from fontforge_attr_names import get_valid_font_attr_names

def main():

    # Command-line options.
    #--------------------------------------------------------------------------

    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("svg_filename", nargs="+", type=str)
    parser.add_argument("--font-data-json", type=str)
    parser.add_argument("--glyph-order-json", type=str)
    parser.add_argument("--references-json", type=str)
    parser.add_argument("--substitutions-json", type=str)
    parser.add_argument("--font-name", type=str)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()

    # Turn off a bunch of output while expanding strokes.
    #--------------------------------------------------------------------------

    silent = False
    stderr_fd = None
    if args.verbose < 2:
        stderr_fd = os.dup(2)

    def silence():
        nonlocal silent
        nonlocal stderr_fd
        if args.verbose < 2:
            if silent:
                return
            silent = True
            os.close(2)

    def no_silence():
        nonlocal silent
        nonlocal stderr_fd
        if args.verbose < 2:
            if not silent:
                return
            silent = False
            os.dup2(stderr_fd, 2)

    # Create new font; get data.
    #--------------------------------------------------------------------------

    font = fontforge.font()

    font_data_json = json.load(open(args.font_data_json, "r"))
    font_data = font_data_json["fontData"]
    fontforge_data = font_data_json["fontforgeData"]

    glyphs_data = json.load(open("src/data/glyphs.json", "r"))

    default_stroke_width = font_data.get("strokeWidth", 96)
    smol_stroke_width = font_data.get("smolStrokeWidth", default_stroke_width)
    glyph_width = font_data["glyphWidth"]

    set_font_attrs(font, fontforge_data, args.font_name)

    # Will draw contoured glyphs first, then references.
    #--------------------------------------------------------------------------

    # Contoured glyphs.  Checking for duplicates here.
    svg_glyph_list = get_svg_glyph_list(args.svg_filename)
    print("    %d glyphs before duplicate checking" % len(svg_glyph_list))
    svg_glyph_dict = {}
    new_svg_glyph_list = []
    for item in svg_glyph_list:
        glyphname = item.glyphname
        if glyphname in svg_glyph_dict:
            print("WARNING WARNING WARNING: duplicate glyph found: %s" % glyphname)
            for item in [i for i in svg_glyph_list if i.glyphname == glyphname]:
                print("    %s %s" % (repr(item), repr(item.filename)))
        else:
            new_svg_glyph_list.append(item)
            svg_glyph_dict[glyphname] = item
    svg_glyph_list = new_svg_glyph_list
    print("    %d glyphs after duplicate checking" % len(svg_glyph_list))

    if args.verbose:
        print("%d SVG files found" % len(svg_glyph_list))

    # Reference glyphs.
    reference_glyph_list = []
    if args.references_json is not None:
        references_json = json.load(open(args.references_json, "r"))
        references_data = references_json["references"]
        reference_glyph_list = get_reference_glyph_list(references_data)
        if args.verbose:
            print("%s reference glyphs found" % len(reference_glyph_list))

    # Combine them.
    glyph_list = svg_glyph_list + reference_glyph_list

    if args.verbose:
        print("%d glyphs either SVG or reference" % len(glyph_list))

    # Sort them if a glyph sort order is provided.
    #
    # TODO: This is primary for DEVELOPMENT.  This allows us to "diff"
    # fonts.
    # --------------------------------------------------------------------------

    glyph_order_data = None
    if args.glyph_order_json:
        glyph_order_data = json.load(open(args.glyph_order_json, "r"))["glyphOrder"]
        if args.verbose:
            print("%d glyphs listed in glyph order sequence" % len(glyph_order_data))
        glyph_list = get_ordered_glyph_list(glyph_list, glyph_order_data)

    # Create the glyphs, possibly in glyph order.
    #--------------------------------------------------------------------------

    if args.verbose:
        print("Creating %d fresh glyphs to establish order" % len(glyph_list))

    i = 0
    for item in glyph_list:
        i += 1
        glyphname = item.glyphname
        codepoint = item.codepoint
        if args.verbose:
            print("    [%d/%d] createChar %d %s [%s]" % (i, len(glyph_list), codepoint, glyphname, item.kind))
        glyph = font.createChar(codepoint, glyphname)
        glyph.width = glyph_width

    # Import outlines on SVG glyphs.
    #--------------------------------------------------------------------------

    svg_glyph_list = [g for g in glyph_list if g.kind == "svg"]

    if args.verbose:
        print("about to import outlines on %d SVG glyphs" % len(svg_glyph_list))
    for item in svg_glyph_list:
        glyphname = item.glyphname
        codepoint = item.codepoint
        data = item.data
        this_glyph_data = get_glyph_data(glyphname, glyphs_data)
        if args.verbose:
            print("    inporting outlines for %s from %s (%s)" % (glyphname, data, repr(this_glyph_data)))

        glyph = font[glyphname]
        glyph.foreground = fontforge.layer()

        font.strokedfont = True # avoid expanding strokes automatically
        glyph.importOutlines(data)
        font.strokedfont = False

        glyph.width = glyph_width

    # Populate outlines for the .SMOL glyphs.
    #--------------------------------------------------------------------------

    smol_glyphs = []
    smol_codepoint_list = [
        *range(33, 127),
        ord("\N{LATIN SMALL LETTER SCHWA}"),
        ord("\N{GREEK SMALL LETTER BETA}"),
        ord("\N{GREEK SMALL LETTER GAMMA}"),
        ord("\N{GREEK SMALL LETTER RHO}"),
        ord("\N{GREEK SMALL LETTER PHI}"),
        ord("\N{GREEK SMALL LETTER CHI}"),
    ]

    if args.verbose:
        print("about to copy outlines into %d SMOL glyphs" % len(smol_codepoint_list))

    for codepoint in smol_codepoint_list:
        glyphname = fontforge.nameFromUnicode(codepoint)
        if glyphname == 'equal':
            codepoint = -1
            glyphname = 'equal.cv11'
        elif glyphname == 'comma':
            codepoint = -1
            glyphname = 'comma.ss05'
        elif glyphname == 'period':
            codepoint = -1
            glyphname = 'period.ss05'
        elif glyphname == 'colon':
            codepoint = -1
            glyphname = 'colon.ss05'
        elif glyphname == 'semicolon':
            codepoint = -1
            glyphname = 'semicolon.ss05'

        big_glyph = font[glyphname]
        big_glyph_width = glyph.width
        smol_glyphname = big_glyph.glyphname.split(".", 1)[0] + ".SMOL"

        if args.verbose:
            print("    drawing %s from %s" % (smol_glyphname, glyphname))

        smol_glyph = font.createChar(-1, smol_glyphname)
        smol_glyph.foreground = fontforge.layer()
        smol_glyphs.append(smol_glyph)

        pen = smol_glyph.glyphPen()
        big_glyph.draw(pen)
        pen = None

        smol_glyph.transform(psMat.scale(0.5, 0.5))
        smol_glyph.transform(psMat.translate(big_glyph_width / 4, default_stroke_width / 4))
        smol_glyph.width = big_glyph_width

    # Expand strokes on SVG glyphs.
    #--------------------------------------------------------------------------

    if args.verbose:
        print("about to expand strokes on %d SVG glyphs" % len(svg_glyph_list))
    for item in svg_glyph_list:
        glyphname = item.glyphname
        codepoint = item.codepoint
        data = item.data
        this_glyph_data = get_glyph_data(glyphname, glyphs_data)

        glyph = font[glyphname]
        stroke_width = this_glyph_data.get("strokeWidth", default_stroke_width)

        if args.verbose:
            print("    expanding strokes for %s (stroke width = %d) (%s)" % (glyphname, stroke_width, repr(this_glyph_data)))

        fill_flag = this_glyph_data.get("fill", False)
        expand_strokes_flag = this_glyph_data.get("expandStrokes", True)
        if expand_strokes_flag:
            silence()
            glyph.stroke("circular", stroke_width, removeinternal=fill_flag)
            no_silence()
            glyph.correctDirection()

        glyph.width = glyph_width

    # Expand strokes on .SMOL glyphs
    #--------------------------------------------------------------------------

    if args.verbose:
        print("About to expand strokes on %d .SMOL glyphs" % len(smol_glyphs))
    for glyph in smol_glyphs:
        silence()
        glyph.stroke("circular", smol_stroke_width) # no fill_flag
        no_silence()
        glyph.correctDirection()

    # Compose reference glyphs.
    #--------------------------------------------------------------------------

    reference_glyph_list = [g for g in glyph_list if g.kind == "refs"]

    if args.verbose:
        print("about to fill out %d reference glyphs" % len(reference_glyph_list))

    for item in reference_glyph_list:
        glyphname = item.glyphname
        if args.verbose:
            print("    creating %s from references" % glyphname)
        glyph = font[glyphname]
        if args.verbose:
            print("    %s.references = %s" % (repr(glyph), repr(item.data)))
        glyph.references = item.data

    # Substitutions
    #--------------------------------------------------------------------------
    if args.substitutions_json is not None:
        substns_data = json.load(open(args.substitutions_json, "r"))["substitutions"]
        features_data = substns_data["features"]
        lookups_data = substns_data["lookups"]
        script_lang_tuples_data = substns_data["scriptLangTuples"]
        for lookup_name in font.gsub_lookups:
            font.removeLookup(lookup_name)
        for (lookup_name, lookup) in lookups_data.items():
            font.addLookup(lookup_name, "gsub_single", None)
            for (subtable_name, subtable) in lookup.items():
                for (glyph_name, replacement_glyph_name) in subtable.items():
                    font[glyph_name].addPosSub(subtable_name, replacement_glyph_name)

    # Save the font.
    #--------------------------------------------------------------------------

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

###############################################################################

"""
"Insanity as a Pathway to Fame and Fortune: The Life and Times of Gary Busey" by Killitorous
"""

def parse_file_name(filename):
    (dirname, basename) = os.path.split(filename)
    (glyphname, ext) = os.path.splitext(basename)
    result = parse_glyph_name(glyphname)
    result.filename = filename
    return result

def parse_glyph_name(glyphname):
    raw_glyphname = glyphname
    base_glyphname = glyphname
    variant = None
    if "." in glyphname and not glyphname.startswith(".") and not glyphname.endswith("."):
        (base_glyphname, variant) = glyphname.split(".", 1)
        variant = variant.split("-")[0]
    base_glyphname = base_glyphname.split("-")[0]
    base_codepoint = -1
    if match := re.fullmatch(r'(?:u\+|0?x)?([0-9a-f]{4,})', base_glyphname, flags=re.I):
        base_codepoint = int(match[1], 16)
        base_glyphname = fontforge.nameFromUnicode(base_codepoint)
        codepoint = base_codepoint if variant is None else -1
        glyphname = base_glyphname + ("" if variant is None else "." + variant)
    elif (base_codepoint := fontforge.unicodeFromName(base_glyphname)) >= 0:
        base_glyphname = fontforge.nameFromUnicode(base_codepoint)
        codepoint = base_codepoint if variant is None else -1
        glyphname = base_glyphname + ("" if variant is None else "." + variant)
    else:
        codepoint = -1
        glyphname = base_glyphname
    return GlyphItem(codepoint=codepoint, glyphname=glyphname, base_codepoint=base_codepoint, base_glyphname=base_glyphname, raw_glyphname=glyphname, variant=variant)

def parse_char_name(char_name):
    base_char_name = char_name
    variant = None
    if "." in char_name and not char_name.startswith(".") and not char_name.endswith("."):
        (base_char_name, variant) = char_name.split(".", 1)
        variant = variant.split("-")[0]

    if len(char_name) == 2 and (high_surr := ord(char_name[0])) in range(0xd800, 0xdc00) and \
                               (low_surr := ord(char_name[1])) in range(0xdc00, 0xe000):
        base_codepoint = 0x10000 + (high_surr - 0xd800) * 1024 + (low_surr - 0xdc00)
    elif len(char_name) == 1:
        base_codepoint = ord(char_name)
    elif match := re.fullmatch(r'(?:u\+|0?x)?([0-9a-f]{4,})', char_name, flags=re.I):
        base_codepoint = int(match[1], 16)
    elif base_codepoint := fontforge.unicodeFromName(char_name):
        pass
    else:
        base_codepoint = -1
        base_glyphname = char_name

    base_glyphname = fontforge.nameFromUnicode(base_codepoint) if base_codepoint >= 0 else char_name
    codepoint = base_codepoint if variant is None else -1
    glyphname = base_glyphname + ("" if variant is None else ("." + variant))
    return GlyphItem(codepoint=codepoint, glyphname=glyphname, base_codepoint=base_codepoint, base_glyphname=base_glyphname, variant=variant, raw_char_name=char_name)

def set_font_attrs(font, fontforge_data, font_name=None):
    defaults = fontforge_data["defaults"]
    font_overrides = fontforge_data["fonts"]
    for attr_name, attr_value in defaults.items():
        if font_name is not None:
            fonts_hash = font_overrides
            if font_name in fonts_hash:
                overrides = fonts_hash[font_name]
                if attr_name in overrides:
                    attr_value = overrides[attr_name]
        if attr_name == "os2_panose":
            attr_value = tuple(attr_value)
        elif attr_name == "gasp":
            attr_value = tuple([tuple([v2 for v2 in v1]) for v1 in attr_value])
        if attr_name == "encoding":
            if type(attr_value) is list:
                for each_value in attr_value:
                    setattr(font, attr_name, each_value)
            else:
                setattr(font, attr_name, attr_value)
        else:
            setattr(font, attr_name, attr_value)

def get_svg_glyph_list(filenames):
    global args

    svg_glyph_list = []
    for filename in filenames:
        if os.path.isdir(filename):
            for dir_path, dir_names, dir_filenames in os.walk(filename):
                for each_filename in dir_filenames:
                    pathname = os.path.join(dir_path, each_filename)
                    parsed = parse_file_name(each_filename)
                    parsed.kind = "svg"
                    parsed.data = each_filename
                    parsed.filename = each_filename
                    svg_glyph_list.append(parsed)
                    print("    added %s to SVG glyph list" % parsed.glyphname)
        else:
            # not tested yet
            parsed = parse_file_name(filename)
            parsed.kind = "svg"
            parsed.data = filename
            parsed.filename = filename
            svg_glyph_list.append(parsed)
            print("    added %s to SVG glyph list" % parsed.glyphname)
    return svg_glyph_list

def get_reference_glyph_list(references_data):
    reference_glyph_list = []
    data = deep_tuple(references_data)
    for glyphname, refs in data.items():
        parsed = parse_glyph_name(glyphname)
        if type(refs) is str:
            parsed.kind="refs"
            parsed.data=((refs, (1.0000001, 0, 0, 1.0000001, 0, 0)),)
            reference_glyph_list.append(parsed)
        else:
            rrefs = []
            for ref in refs:
                if type(ref) is str:
                    rrefs.append((ref, (1, 0, 0, 1, 0, 0)))
                else:
                    xform = identity()
                    (ref_glyphname, opers) = ref
                    for oper in opers:
                        op = oper.get("op", None)
                        if op is None:
                            continue
                        if op == "scale":
                            sx = oper.get("x", 1)
                            sy = oper.get("y", 1)
                            cx = oper.get("cx", 0)
                            cy = oper.get("cy", 0)
                            if cx or cy:
                                xform = compose(xform, translate(-cx, -cy))
                            xform = compose(xform, scale(sx, sy))
                            if cx or cy:
                                xform = compose(xform, translate(cx, cy))
                        elif op == "translate":
                            dx = oper.get("dx", 0)
                            dy = oper.get("dy", 0)
                            if dx or dy:
                                xform = compose(xform, translate(dx, dy))
                        else:
                            raise Exception("unsupported op: %s" % repr(oper))
                    rrefs.append((ref_glyphname, xform))
            parsed.kind = "refs"
            parsed.data = tuple(rrefs)
            reference_glyph_list.append(parsed)
    return reference_glyph_list

def get_ordered_glyph_list(glyph_list, glyph_order_data):
    global args

    if args.verbose:
        print("get_ordered_glyph_list: glyph_list has %d items" % len(glyph_list))
        print("get_ordered_glyph_list:     first item is %s" % repr(glyph_list[0].glyphname))
        print("get_ordered_glyph_list: glyph_order_data has %d items" % len(glyph_order_data))
        print("get_ordered_glyph_list:     first item is %s" % glyph_order_data[0]["glyphname"])

    ordered_glyph_names = [d["glyphname"] for d in glyph_order_data]

    new_glyph_list = []
    missing_glyph_count = 0
    for item in glyph_order_data:
        glyphname = item["glyphname"]
        codepoint = item["unicode"]
        this_glyph_list = [g for g in glyph_list if g.glyphname == glyphname]
        if len(this_glyph_list) < 1:
            missing_glyph_count += 1
            if args.verbose:
                print("WARNING: glyph %s, listed in order data not found" % glyphname)
            parsed = parse_glyph_name(glyphname)
            parsed.kind = "blank"
            parsed.data = None
            if codepoint >= 0:  # "glyph2202" e.g.
                parsed.codepoint = codepoint
            new_glyph_list.append(parsed)
        elif len(this_glyph_list) > 1:
            if args.verbose:
                print("WARNING: glyph %s, listed in order data, found %d times " % (glyphname, len(this_glyph_list)))
        new_glyph_list += this_glyph_list

    if args.verbose:
        if missing_glyph_count:
            print("WARNING: %d glyphs missing" % missing_glyph_count)

    if args.verbose:
        print("get_ordered_glyph_list: new_glyph_list has %d items" % len(new_glyph_list))

    unordered_glyph_list = [g for g in glyph_list if g.glyphname not in ordered_glyph_names]

    if args.verbose:
        print("get_ordered_glyph_list: unordered_glyph_list has %d items" % len(unordered_glyph_list))

    new_glyph_list += unordered_glyph_list

    if args.verbose:
        print("get_ordered_glyph_list: new_glyph_list now has %d items" % len(new_glyph_list))

    return new_glyph_list

def deep_tuple(value):
    if type(value) in [list, tuple]:
        return tuple([deep_tuple(v) for v in value])
    return value

def get_glyph_data(glyphname, glyphs_data):
    global args

    if args.verbose >= 2:
        print("get_glyph_data(%s, ...)" % repr(glyphname))
    parsed = parse_glyph_name(glyphname)
    codepoint = parsed.codepoint
    glyph_data = {}

    for each_char_name, each_data in glyphs_data.items():
        parsed = parse_char_name(each_char_name)
        each_codepoint = parsed.codepoint
        each_glyphname = parsed.glyphname
        if each_glyphname == glyphname:
            glyph_data |= each_data
            if args.verbose >= 2:
                print("    from each_glyphname == glyphname == %s: %s" % (repr(glyphname), repr(each_data)))
        if each_codepoint in range(0, 0x110000) and each_codepoint == codepoint:
            glyph_data |= each_data
            if args.verbose >= 2:
                print("    each_codepoint == codepoint == %d: %s" % (codepoint, repr(each_data)))

    for glyph_range in glyphs_data["__RANGES__"]:
        from_parsed = parse_char_name(glyph_range["from"])
        to_parsed = parse_char_name(glyph_range["to"])
        from_cp = from_parsed.base_codepoint
        to_cp = to_parsed.base_codepoint
        if codepoint in range(from_cp, to_cp + 1):
            if args.verbose >= 2:
                print("    codepoint %d in range(%s, %s): %s [%s]" % (codepoint, from_cp, to_cp, repr(glyph_range["data"]), repr(glyph_range)))
            glyph_data |= glyph_range["data"]

    return glyph_data

class GlyphItem:
    def __init__(self, codepoint=None, glyphname=None, base_codepoint=None, base_glyphname=None, variant=None, kind=None, filename=None, raw_glyphname=None, raw_char_name=None):
        self.codepoint      = codepoint
        self.glyphname      = glyphname
        self.base_codepoint = base_codepoint
        self.base_glyphname = base_glyphname
        self.variant        = variant
        self.kind           = kind
        self.filename       = filename
        self.raw_glyphname  = raw_glyphname
        self.raw_char_name  = raw_char_name

main()
