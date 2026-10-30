import fontforge, os, re
from otm.generated import ALL
from types import SimpleNamespace

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

def index_svg_filenames(filenames):
    svg_list = [parse_svg_filename(filename) for filename in filenames]
    svg_list = [
        item for item in svg_list
        if item.orig_glyph_name not in [".notdef", "nonmarkingreturn", ".null"]
    ]
    svg_dict = {}
    for item in svg_list:
        svg_dict[item.norm_glyph_name] = item
    return svg_list, svg_dict

def parse_svg_filename(filename):
    _, basename = os.path.split(filename)
    stem, _ = os.path.splitext(basename)

    name_is_arbitrary = False
    if match := re.fullmatch(r'([0-9A-Fa-f]{4,})(\.[^\.]+)', stem):
        code = int(match[1], 16)
        variant = match[2]
        orig_glyph_name      = fontforge.nameFromUnicode(code) + variant
        orig_base_glyph_name = fontforge.nameFromUnicode(code)
        norm_glyph_name      = fontforge.nameFromUnicode(code) + variant
        norm_base_glyph_name = fontforge.nameFromUnicode(code)
    elif match := re.fullmatch(r'[0-9A-Fa-f]{4,}', stem):
        code = int(stem, 16)
        variant = ""
        orig_glyph_name      = fontforge.nameFromUnicode(code)
        orig_base_glyph_name = fontforge.nameFromUnicode(code)
        norm_glyph_name      = fontforge.nameFromUnicode(code)
        norm_base_glyph_name = fontforge.nameFromUnicode(code)
    elif match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', stem):
        variant = match[2]
        orig_glyph_name      = match[1] + variant
        orig_base_glyph_name = match[1]
        code = fontforge.unicodeFromName(match[1])
        if code < 0:
            norm_glyph_name      = match[1] + variant
            norm_base_glyph_name = match[1]
            name_is_arbitrary    = True
        else:
            norm_glyph_name      = fontforge.nameFromUnicode(code) + variant
            norm_base_glyph_name = fontforge.nameFromUnicode(code)
    elif match := re.fullmatch(r'([^\.]+)', stem):
        variant = ""
        orig_glyph_name      = match[1] + variant
        orig_base_glyph_name = match[1]
        code = fontforge.unicodeFromName(match[1])
        if code < 0:
            norm_glyph_name      = match[1] + variant
            norm_base_glyph_name = match[1]
            name_is_arbitrary    = True
        else:
            norm_glyph_name      = fontforge.nameFromUnicode(code) + variant
            norm_base_glyph_name = fontforge.nameFromUnicode(code)
    else:
        raise Exception(f'{repr(filename)} cannot be parsed')
    as_tuple = (
        code,
        variant,
        orig_glyph_name,
        orig_base_glyph_name,
        norm_glyph_name,
        norm_base_glyph_name,
        filename,
        None,
        name_is_arbitrary,
    )
    return SimpleNamespace(
        code                =code,
        variant             =variant,
        orig_glyph_name     =orig_glyph_name,
        orig_base_glyph_name=orig_base_glyph_name,
        norm_glyph_name     =norm_glyph_name,
        norm_base_glyph_name=norm_base_glyph_name,
        filename            =filename,
        glyph               =None,
        name_is_arbitrary   =name_is_arbitrary,
        as_tuple            =as_tuple,
    )

def index_glyphs(font):
    glyph_list = [parse_glyph_name(glyph) for glyph in font.glyphs()]
    glyph_list = [
        item for item in glyph_list
        if item.orig_glyph_name not in [".notdef", "nonmarkingreturn", ".null"]
    ]
    glyph_dict = {}
    for item in glyph_list:
        glyph_dict[item.norm_glyph_name] = item
    return glyph_list, glyph_dict

def parse_glyph_name(glyph):
    orig_glyph_name = glyph.glyphname
    if match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', glyph.glyphname):
        orig_base_glyph_name = match[1]
        variant = match[2]
    else:
        orig_base_glyph_name = glyph.glyphname
        variant = ""
    code = fontforge.unicodeFromName(orig_base_glyph_name)
    name_is_arbitrary = False
    if code < 0:
        code = glyph.unicode
        if code in range(0, 0x110000):
            name_is_arbitrary = True
    if code < 0:
        norm_base_glyph_name = orig_base_glyph_name
        norm_glyph_name      = orig_base_glyph_name + variant
    else:
        norm_base_glyph_name = fontforge.nameFromUnicode(code)
        norm_glyph_name      = fontforge.nameFromUnicode(code) + variant
    as_tuple = (
        code,
        variant,
        orig_glyph_name,
        orig_base_glyph_name,
        norm_glyph_name,
        norm_base_glyph_name,
        filename,
        glyph,
        name_is_arbitrary,
    )
    return [
        code                =code,
        variant             =variant,
        orig_glyph_name     =orig_glyph_name,
        orig_base_glyph_name=orig_base_glyph_name,
        norm_glyph_name     =norm_glyph_name,
        norm_base_glyph_name=norm_base_glyph_name,
        filename            =None,
        glyph               =glyph,
        name_is_arbitrary   =name_is_arbitrary,
        as_tuple            =as_tuple,
    ]

def verify_glyphs(svg_list, svg_dict, glyph_list, glyph_dict):
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
        glyphname = item.norm_glyph_name
        code = item.code
        if noindex(item):
            continue
        svg_filename = item.filename
        if glyphname not in glyph_dict:
            print(f"SVG:   {repr(glyphname)} from {svg_filename} not in glyphs")
            success = False
            svg_only_list.append(item)
            svg_only_dict[glyphname] = item
        else:
            verified_svg_list.append(item)
            verified_svg_dict[glyphname] = item

    for item in glyph_list:
        glyphname = item.norm_glyph_name
        code = item.code
        glyph = item.glyph
        if len(glyph.references):
            if len(glyph.foreground):
                print(f"GLYPH: {repr(glyphname)} contains both references AND contours")
            continue
        if noindex(item):
            continue
        if glyphname not in svg_dict:
            print(f"GLYPH: {repr(glyphname)} from {glyph.font} not found in SVG files")
            success = False
            glyph_only_list.append(item)
            glyph_only_dict[glyphname] = item
        else:
            verified_glyph_list.append(item)
            verified_glyph_dict[glyphname] = item

    return (success, 
            verified_svg_list, verified_svg_dict, verified_glyph_list, verified_glyph_dict,
            svg_only_list,     svg_only_dict,     glyph_only_list,     glyph_only_dict)

def noindex(item):
    glyphname = item.norm_glyph_name
    code = item.code
    return (
        glyphname.endswith(".SMOL") or
        code in SPACES or
        code in ALL
    )

