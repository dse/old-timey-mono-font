import fontforge, os, re, sys
from otm.generated import GENERATED_GLYPH_CODES, GENERATED_SPACE_CODES, NON_GRAPHIC_CODES
from types import SimpleNamespace
from .char_data import SVGCharData, GlyphCharData, GlyphNameCharData

def index_svg_filenames(filenames, verbose=False):
    svg_list = [parse_svg_filename(filename, verbose=verbose) for filename in filenames]
    svg_dict = {}
    for item in svg_list:
        if verbose:
            print("index_svg_filenames: " + str(item))
        if item.key in svg_dict:
            sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {svg_dict[item.key]}\n")
            raise KeyError(f"{repr(item.key)} already in svg_dict:\n")
        else:
            svg_dict[item.key] = item
    return svg_list, svg_dict

def parse_svg_filename(svg_filename, verbose=False):
    data = SVGCharData(svg_filename)
    # if verbose:
    #     print("parse_svg_filename: " + str(data))
    return data

def index_glyphs(font, verbose=False):
    glyph_list = [parse_glyph_name(glyph.glyphname, verbose=verbose) for glyph in font.glyphs()]
    glyph_dict = {}
    for item in glyph_list:
        if verbose:
            print("index_glyphs: " + str(item))
        if item.key in glyph_dict:
            sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {glyph_dict[item.key]}\n")
            raise KeyError(f"{repr(item.key)} already in glyph_dict:")
            pass
        else:
            glyph_dict[item.key] = item
    return glyph_list, glyph_dict

def index_glyph_names(glyph_names):
    named_glyph_list = []
    named_glyph_dict = {}
    for glyph_name in glyph_names:
        item = GlyphNameCharData(glyph_name)
        named_glyph_list.append(item)
        if item.key in named_glyph_dict:
            sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {named_glyph_dict[item.key]}\n")
            raise KeyError(f"{repr(item.key)} already in named_glyph_dict:")
        else:
            named_glyph_dict[item.key] = item
    return named_glyph_list, named_glyph_dict

def parse_glyph_name(glyphname, verbose=False):
    data = GlyphNameCharData(glyphname)
    # if verbose:
    #     print("parse_glyph_name: " + str(data))
    return data

def verify_glyphs(svg_list, svg_dict, glyph_list, glyph_dict, verbose=False):
    verified_svg_list = []
    verified_svg_dict = {}
    verified_glyph_list = []
    verified_glyph_dict = {}

    svg_only_list = []
    svg_only_dict = {}
    glyph_only_list = []
    glyph_only_dict = {}

    success = True

    for item in svg_list:
        if noindex(item):
            continue

        if item.key not in glyph_dict:
            if verbose:
                print("verify_glyphs: " + str(item) + " -- not in glyphs")
            success = False
            svg_only_list.append(item)
            if item.key in svg_only_dict:
                sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {svg_only_dict[item.key]}\n")
                raise KeyError(f"{repr(item.key)} already in svg_only_dict:")
                pass
            else:
                svg_only_dict[item.key] = item
        else:
            verified_svg_list.append(item)
            if item.key in verified_glyph_dict:
                sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {verified_glyph_dict[item.key]}\n")
                raise KeyError(f"{repr(item.key)} already in verified_svg_dict:")
                pass
            else:
                verified_svg_dict[item.key] = item

    matches = []

    for item in glyph_list:
        if noindex(item):
            continue

        glyph = item.glyph
        if glyph is None:
            pass
        elif len(glyph.references):
            if len(glyph.foreground):
                if verbose:
                    print("verify_glyphs: " + str(item) + " -- contains both references AND contours")
            continue
        if item.key not in svg_dict:
            if verbose:
                print("verify_glyphs: " + str(item) + " -- not found in SVG files")
            success = False
            glyph_only_list.append(item)
            if item.key in glyph_only_dict:
                sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {glyph_only_dict[item.key]}\n")
                raise KeyError(f"{repr(item.key)} already in glyph_only_dict:")
                pass
            else:
                glyph_only_dict[item.key] = item
        else:
            verified_glyph_list.append(item)
            if item.key in verified_glyph_dict:
                sys.stderr.write(f"NEW ITEM: {item}\nOLD ITEM: {verified_glyph_dict[item.key]}\n")
                raise KeyError(f"{repr(item.key)} already in verified_glyph_dict:")
                pass
            else:
                verified_glyph_dict[item.key] = item
            matches.append((svg_dict[item.key], item))

    if verbose:
        for match in matches:
            print("verify_glyphs: MATCH:  %s" % match[0])
            print("                       %s" % match[1])

    return (success, 
            verified_svg_list, verified_svg_dict, verified_glyph_list, verified_glyph_dict,
            svg_only_list,     svg_only_dict,     glyph_only_list,     glyph_only_dict,
            matches)

def noindex(item):
    glyphname = item.norm_glyph_name
    code = item.code
    return (
        glyphname.endswith(".SMOL") or
        code in GENERATED_SPACE_CODES or
        code in NON_GRAPHIC_CODES or
        code in GENERATED_GLYPH_CODES
    )
