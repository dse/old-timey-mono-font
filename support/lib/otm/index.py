import fontforge, os, re
from otm.generated import GENERATED_GLYPH_CODES
from types import SimpleNamespace
from .char_data import SVGCharData, GlyphCharData, GlyphNameCharData

SPACES = [
    *list(range(0x0000, 0x0020)), # C0 controls
    *list(range(0x0080, 0x00a0)), # C1 controls
    0x0020,                       # SPACE
    0x007f,                       # <control> (DELETE)
    0x00a0,                       # NO-BREAK SPACE
    0x2000,                       # EN QUAD
    0x2001,                       # EM QUAD
    0x2002,                       # EN SPACE
    0x2003,                       # EM SPACE
    0x2004,                       # THREE-PER-EM SPACE
    0x2005,                       # FOUR-PER-EM SPACE
    0x2006,                       # SIX-PER-EM SPACE
    0x2007,                       # FIGURE SPACE
    0x2008,                       # PUNCTUATION SPACE
    0x2009,                       # THIN SPACE
    0x200a,                       # HAIR SPACE
    0x200b,                       # ZERO WIDTH SPACE
    0x200c,                       # ZERO WIDTH NON-JOINER
    0x200d,                       # ZERO WIDTH JOINER
    0x200e,                       # LEFT-TO-RIGHT MARK
    0x200f,                       # RIGHT-TO-LEFT MARK
    0x2028,                       # LINE SEPARATOR
    0x2029,                       # PARAGRAPH SEPARATOR
    0x202f,                       # NARROW NO-BREAK SPACE
    0x205f,                       # MEDIUM MATHEMATICAL SPACE
    0x3000,                       # IDEOGRAPHIC SPACE
    0x1680,                       # OGHAM SPACE MARK
    0xfeff,              # ZERO WIDTH NO-BREAK SPACE (BYTE ORDER MARK)
]

def index_svg_filenames(filenames, verbose=False):
    svg_list = [parse_svg_filename(filename, verbose=verbose) for filename in filenames]
    svg_list = [
        item for item in svg_list
        if item.orig_glyph_name not in [".notdef", "nonmarkingreturn", ".null"]
    ]
    svg_dict = {}
    for item in svg_list:
        if verbose:
            print("index_svg_filenames: " + str(item))
        if item.key in svg_dict:
            raise KeyError(f"{repr(item.key)} already in svg_dict:\n{item}")
        else:
            svg_dict[item.key] = item
    return svg_list, svg_dict

def parse_svg_filename(svg_filename, verbose=False):
    data = SVGCharData(svg_filename)
    # if verbose:
    #     print("parse_svg_filename: " + str(data))
    return data

def index_glyphs(font, verbose=False):
    glyph_list = [parse_glyph_name(glyph, verbose=verbose) for glyph in font.glyphs()]
    glyph_list = [
        item for item in glyph_list
        if item.orig_glyph_name not in [".notdef", "nonmarkingreturn", ".null"]
    ]
    glyph_dict = {}
    for item in glyph_list:
        if verbose:
            print("index_glyphs: " + str(item))
        if item.key in glyph_dict:
            raise KeyError(f"{repr(item.key)} already in glyph_dict:\n{item}")
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
            raise KeyError(f"{repr(item.key)} already in named_glyph_dict:\n{item}")
        else:
            named_glyph_dict[item.key] = item
    return named_glyph_list, named_glyph_dict

def parse_glyph_name(glyph, verbose=False):
    data = GlyphCharData(glyph)
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
                raise KeyError(f"{repr(item.key)} already in svg_only_dict:\n{item}")
                pass
            else:
                svg_only_dict[item.key] = item
        else:
            verified_svg_list.append(item)
            if item.key in verified_glyph_dict:
                raise KeyError(f"{repr(item.key)} already in verified_svg_dict:\n{item}")
                pass
            else:
                verified_svg_dict[item.key] = item

    matches = []

    for item in glyph_list:
        if noindex(item):
            continue

        glyph = item.glyph
        if len(glyph.references):
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
                raise KeyError(f"{repr(item.key)} already in glyph_only_dict:\n{item}")
                pass
            else:
                glyph_only_dict[item.key] = item
        else:
            verified_glyph_list.append(item)
            if item.key in verified_glyph_dict:
                raise KeyError(f"{repr(item.key)} already in verified_glyph_dict:\n{item}")
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
        code in SPACES or
        code in GENERATED_GLYPH_CODES
    )

