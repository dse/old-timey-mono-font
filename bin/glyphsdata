#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import os
import sys
import argparse
import fontforge
import unicodedata
import json
import re
from functools import cmp_to_key

sys.path.append(os.environ["HOME"] + "/.venv/lib/python3.12/site-packages")
import unicodeblocks

CHAR_TYPES = [
    "Latin",
    "Digits",
    "Greek",
    "Cyrillic",
    "IPA",
    "Combining Marks",
    "Punctuation",
    "Currency",
    "Mathematics",
    "Fractions",
    "Superscripts and Subscripts",
    "Arrows",
    "Block Elements",
    "Box Drawing",
    "Braille",
    "Dingbats",
    "Enclosed",
    "Letterlike",
    "Shapes",
    "Symbols",
    "Technical",
    "Spaces",
    "Other",
]

def main():
    global args
    parser = argparse.ArgumentParser();
    parser.add_argument('filename')
    parser.add_argument('-b', '--by-block', action='store_true')
    parser.add_argument('-t', '--by-type', action='store_true')
    args = parser.parse_args()
    font = fontforge.open(args.filename)
    if args.by_type:
        font_data = get_font_data_by_type(font)
    elif args.by_block:
        font_data = get_font_data_by_block(font)
    else:
        font_data = get_font_data_by_char(font)
    print(json.dumps(font_data, indent=4))
    font.close()

def get_font_data_by_type(font):
    """Used for a page that classifies characters according to an ad-hoc
    system I whipped up instead of Unicode blocks."""
    font_data = {
        "fontInfo": get_font_info(font),
        "types": [],
        "specials": [],
    }
    all_glyphs = [glyph for glyph in list(font.glyphs()) if glyph.unicode < 0x10000]
    for glyph in all_glyphs:
        set_glyph_temp_info(glyph)
    all_glyphs.sort(key=cmp_to_key(glyph_cmp))
    unicode_glyphs = [glyph for glyph in all_glyphs if glyph.unicode > 0]
    set_substitutions(font)
    for glyph in all_glyphs:
        glyph.temporary["glyph_type"] = get_glyph_type_name(glyph)
    for type_name in CHAR_TYPES:
        type_data = {
            "name": type_name,
            "glyphs": [],
        }
        font_data["types"].append(type_data)
        glyphs = [glyph for glyph in unicode_glyphs if glyph.temporary["glyph_type"] == type_name]
        for glyph in glyphs:
            type_data["glyphs"].append(get_glyph_info(glyph))
    return font_data

def get_font_data_by_block(font):
    blocks_data = []
    specials_data = []
    font_data = {
        "fontInfo": get_font_info(font),
        "blocks": blocks_data,
        "specials": specials_data,
    }
    all_blocks = [unicodeblocks.blocks[block] for block in unicodeblocks.blocks]
    all_blocks.sort(key=lambda block: block.start)
    all_glyphs = [glyph for glyph in list(font.glyphs()) if glyph.unicode < 0x10000]
    for glyph in all_glyphs:
        set_glyph_temp_info(glyph)
    all_glyphs.sort(key=cmp_to_key(glyph_cmp))
    set_substitutions(font)
    unicode_glyphs = [glyph for glyph in all_glyphs if glyph.unicode > 0]
    special_glyphs = [glyph for glyph in all_glyphs if glyph.unicode <= 0]
    codepoints = list(set([glyph.unicode for glyph in unicode_glyphs]))
    codepoints.sort()
    for block in all_blocks:
        block_codepoints = list(set([glyph.unicode for glyph in unicode_glyphs]))
        block_codepoints = [cp for cp in block_codepoints if cp is not None and cp >= 0 and cp in range(block.start, block.end + 1)]
        if not len(block_codepoints):
            continue
        glyphs_data = []
        block_info = { "name": block.name, "start": block.start, "end": block.end }
        block_data = {
            "info": block_info,
            "glyphs": glyphs_data,
        }
        blocks_data.append(block_data)
        glyphs = [glyph for glyph in unicode_glyphs
                  if glyph.unicode in range(block.start, block.end + 1)]
        for glyph in glyphs:
            glyphs_data.append(get_glyph_info(glyph))
    for glyph in special_glyphs:
        specials_data.append(get_glyph_info(glyph))
    return font_data

def get_font_data_by_char(font):
    glyphs_data = []
    font_data = {
        "fontInfo": get_font_info(font),
        "glyphs": glyphs_data,
    }
    all_glyphs = [glyph for glyph in list(font.glyphs()) if glyph.unicode < 0x10000]
    glyphs = [glyph for glyph in all_glyphs if glyph.unicode > 0]
    for glyph in all_glyphs:
        set_glyph_temp_info(glyph)
    all_glyphs.sort(key=cmp_to_key(glyph_cmp))
    set_substitutions(font)
    for glyph in glyphs:
        glyphs_data.append(get_glyph_info(glyph))
    
    return font_data

def get_glyphs_data(font):
    glyphs = list(font.glyphs())
    glyphs_data = []
    for glyph in glyphs:
        glyph.temporary = {
        }
        glyph_data = get_glyph_info(glyph)
        glyphs_data.append(glyph_data)
    return glyphs_data

def get_glyph_info(glyph):
    codepoint = glyph.unicode
    if codepoint >= 0:
        try:
            normal_glyphname = fontforge.nameFromUnicode(codepoint)
        except TypeError:
            normal_glyphname = None
    else:
        normal_glyphname = None
    (xmin, ymin, xmax, ymax) = glyph.boundingBox()
    normal_glyphname = get_normal_glyphname(glyph)
    normal_codepoint = get_normal_codepoint(glyph)
    isSpecial = normal_codepoint is None or normal_codepoint < 0
    isPrintable = normal_codepoint is not None and (
        normal_codepoint in range(32, 127) or
        normal_codepoint >= 160
    )
    if normal_codepoint is not None:
        try:
            char_name = unicodedata.name(chr(normal_codepoint))
        except ValueError:
            char_name = None
    else:
        char_name = None    
    glyph_info = {
        "codepoint": normal_codepoint,
        "codepoint_hex": u(normal_codepoint),
        "name": char_name,
        "isSpecial": isSpecial,
        "isPrintable": isPrintable,
        "glyphName": glyph.glyphname,
        "normalAdobeName": normal_glyphname,
        "boundingBoxXMin": xmin,
        "boundingBoxXMax": xmax,
        "boundingBoxYMin": ymin,
        "boundingBoxYMax": ymax,
        "altuni": glyph.altuni,
        "comment": glyph.comment,
        "glyphClass": glyph.glyphclass,
        "leftSideBearing": glyph.left_side_bearing,
        "rightSideBearing": glyph.right_side_bearing,
        "width": glyph.width,
        "char": chr(normal_codepoint) if isPrintable else None
    }
    if "substitutionsFromThis" in glyph.temporary:
        glyph_info["substitutionsFromThis"] = glyph.temporary["substitutionsFromThis"]
    if "substitutionsToThis" in glyph.temporary:
        glyph_info["substitutionsToThis"] = glyph.temporary["substitutionsToThis"]
    return glyph_info

def get_font_info(font):
    return {
        "ascent": font.ascent,
        "capHeight": font.capHeight,
        "comment": font.comment,
        "copyright": font.copyright,
        "descent": font.descent,
        "designSize": font.design_size,
        "em": font.em,
        "familyName": font.familyname,
        "fontName": font.fontname,
        "fullName": font.fullname,
        "italicAngle": font.italicangle,
        "uniqueId": font.uniqueid,
        "underlinePosition": font.upos,
        "underlineWidth": font.uwidth,
        "version": font.version,
        "weight": font.weight,
        "exHeight": font.xHeight,
    }

def get_normal_codepoint(glyph):
    if glyph.unicode >= 0:
        return glyph.unicode
    if match := re.search(r'^(.*?)\.(.*)$', glyph.glyphname):
        return fontforge.unicodeFromName(match.group(1))
    return None

def get_normal_glyphname(glyph):
    cp = get_normal_codepoint(glyph)
    if cp is not None and cp >= 0:
        return fontforge.nameFromUnicode(cp)
    return None

def glyph_cmp(glyph_a, glyph_b):
    cp_a = glyph_a.unicode
    cp_b = glyph_b.unicode
    if cp_a is None or cp_a < 1: # unassignable and U+0000 glyphs go after assignable ones
        cp_a = float('inf')
    if cp_b is None or cp_b < 1:
        cp_b = float('inf')
    if cp_a < 32 or cp_a in range(127, 160):
        cp_a = float('inf')
    if cp_b < 32 or cp_b in range(127, 160):
        cp_b = float('inf')
    if cp_a < cp_b:
        return -1
    if cp_a > cp_b:
        return 1
    name_a = glyph_a.glyphname
    name_b = glyph_b.glyphname
    if name_a is None:
        name_a = ""
    if name_b is None:
        name_b = ""
    if name_a < name_b:
        return -1
    if name_a > name_b:
        return 1
    return 0

def dict_get_or_create(dict, key, default_value):
    if key in dict:
        return dict[key]
    dict[key] = default_value
    return dict[key]

def u(codepoint):
    if codepoint is None:
        return None
    if codepoint < 0:
        return "%d" % codepoint
    return "U+%04X" % codepoint

def set_glyph_temp_info(glyph):
    glyph.temporary = {}

def set_substitutions(font):
    for source_glyph in font.glyphs():
        for lookup_name in font.gsub_lookups:
            lookup_info = font.getLookupInfo(lookup_name)
            feature = lookup_info[2][0][0] # e.g., "ss01"
            for subtable_name in font.getLookupSubtables(lookup_name):
                for substitution in source_glyph.getPosSub(subtable_name):
                    (subtable_name, lookup_type, dest_glyph_name) = substitution
                    if (lookup_type == 'Substitution'):
                        dest_glyph = font[dest_glyph_name]
                        source_temp = source_glyph.temporary
                        dest_temp = dest_glyph.temporary
                        substnsFromThis = dict_get_or_create(source_temp, "substitutionsFromThis", {})
                        substnsToThis = dict_get_or_create(dest_temp, "substitutionsToThis", {})
                        substnsFromThis[feature] = dest_glyph.glyphname
                        featureToThis = dict_get_or_create(substnsToThis, feature, [])
                        featureFromThis = dest_glyph.glyphname
                        featureToThis.append(source_glyph.glyphname)
    
def get_glyph_type_name(glyph):
    codepoint = glyph.unicode
    if codepoint is None or codepoint < 0:
        return None
    char = chr(codepoint)
    block = unicodeblocks.blockof(chr(codepoint))
    block_name = None if block is None else block.name
    if codepoint < 32 or codepoint in range(127, 160):
        return None
    if block_name == "Basic Latin": # 0x0000-0x007f
        if codepoint in range(65, 91):
            return "Latin"
        elif codepoint in range(97, 123):
            return "Latin"
        elif codepoint in range(48, 58):
            return "Digits"
        elif codepoint == 32:
            return "Spaces"
        elif char == '$':
            return "Currency"
        elif char in ['=', '+', '<', '=', '>']:
            return "Mathematics"
        else:
            return "Punctuation"
    elif block_name == "Latin-1 Supplement": # 0x0080-0x00ff
        if codepoint == 160:
            return "Spaces"
        elif codepoint in [0x00b1, 0x00d7, 0x00f7]:
            return "Mathematics"
        elif codepoint in range(0x00c0, 0x0100):
            return "Latin"
        elif codepoint in [0x00a2, 0x00a3, 0x00a4, 0x00a5]:
            return "Currency"
        elif codepoint in [0x00ac, 0x00bc, 0x00bd, 0x00be]:
            return "Mathematics"
        elif codepoint in [0x00b2, 0x00b3, 0x00b9]:
            return "Superscripts and Subscripts"
        else:
            return "Punctuation"
    elif block_name == "Latin Extended-A": # U+0100 - U+017F
        return "Latin"
    elif block_name == "Latin Extended-B": # U+0180 - U+024F
        return "Latin"
    elif block_name == "IPA Extensions": # U+0250 - U+02AF
        return "IPA"
    elif block_name == "Spacing Modifier Letters": # U+02B0 - U+02FF
        return "Other"
    elif block_name == "Combining Diacritical Marks": # U+0300 - U+036F
        return "Combining Marks"
    elif block_name == "Greek and Coptic": # U+0370 - U+03FF
        if codepoint in range(0x03e2, 0x03f0):
            pass # coptics
        else:
            return "Greek"
    elif block_name == "Cyrillic": # U+0400 - U+04FF
        return "Cyrillic"
    elif block_name == "Cyrillic Supplement": # U+0500 - U+052F
        return "Cyrillic"
    elif block_name == "Combining Diacritical Marks Extended": # U+1AB0 - U+1AFF
        return "Combining Marks"
    elif block_name == "Cyrillic Extended-C": # U+1C80 - U+1C8F
        return "Cyrillic"
    elif block_name == "Phonetic Extensions": # U+1D00 - U+1D7F
        return "Other"
    elif block_name == "Phonetic Extensions Supplement": # U+1D80 - U+1DBF
        return "Other"
    elif block_name == "Combining Diacritical Marks Supplement": # U+1DC0 - U+1DFF
        return "Combining Marks"
    elif block_name == "Latin Extended Additional": # U+1E00 - U+1EFF
        return "Latin"
    elif block_name == "Greek Extended": # U+1F00 - U+1FFF
        return "Greek"
    elif block_name == "General Punctuation": # U+2000 - U+206F
        return "Punctuation"
    elif block_name == "Superscripts and Subscripts": # U+2070 - U+209F
        return "Superscripts and Subscripts"
    elif block_name == "Currency Symbols": # U+20A0 - U+20CF
        return "Currency"
    elif block_name == "Combining Diacritical Marks for Symbols": # U+20D0 - U+20FF
        return "Combining Marks"
    elif block_name == "Letterlike Symbols": # U+2100 - U+214F
        return "Letterlike"
    elif block_name == "Number Forms": # U+2150 - U+218F
        if codepoint in range(0x2150, 0x2160) or codepoint == 0x2180:
            return "Fractions"
        return "Other"
    elif block_name == "Arrows": # U+2190 - U+21FF
        return "Arrows"
    elif block_name == "Mathematical Operators": # U+2200 - U+22FF
        return "Mathematics"
    elif block_name == "Miscellaneous Technical": # U+2300 - U+23FF
        if codepoint in [0x2310, 0x2319]: 
            return "Mathematics"
        return "Technical"
    elif block_name == "Control Pictures": # U+2400 - U+243F
        return "Other"
    elif block_name == "Optical Character Recognition": # U+2440 - U+245F
        return "Other"
    elif block_name == "Enclosed Alphanumerics": # U+2460 - U+24FF
        return "Enclosed"
    elif block_name == "Box Drawing": # U+2500 - U+257F
        return "Box Drawing"
    elif block_name == "Block Elements": # U+2580 - U+259F
        return "Block Elements"
    elif block_name == "Geometric Shapes": # U+25A0 - U+25FF
        return "Shapes"
    elif block_name == "Miscellaneous Symbols": # U+2600 - U+26FF
        return "Symbols"
    elif block_name == "Dingbats": # U+2700 - U+27BF
        return "Dingbats"
    elif block_name == "Miscellaneous Mathematical Symbols-A": # U+27C0 - U+27EF
        return "Mathematics"
    elif block_name == "Supplemental Arrows-A": # U+27F0 - U+27FF
        return "Arrows"
    elif block_name == "Braille Patterns": # U+2800 - U+28FF
        return "Braille"
    elif block_name == "Supplemental Arrows-B": # U+2900 - U+297F
        return "Arrows"
    elif block_name == "Miscellaneous Mathematical Symbols-B": # U+2980 - U+29FF
        return "Mathematics"
    elif block_name == "Supplemental Mathematical Operators": # U+2A00 - U+2AFF
        return "Mathematics"
    elif block_name == "Miscellaneous Symbols and Arrows": # U+2B00 - U+2BFF
        if re.search('ARROW', unicodedata.name(char)):
            return "Arrows"
        else:
            return "Symbols"
    elif block_name == "Latin Extended-C": # U+2C60 - U+2C7F
        return "Latin"
    elif block_name == "Cyrillic Extended-A": # U+2DE0 - U+2DFF
        return "Cyrillic"
    elif block_name == "Supplemental Punctuation": # U+2E00 - U+2E7F
        return "Punctuation"
    elif block_name == "Cyrillic Extended-B": # U+A640 - U+A69F
        return "Cyrillic"
    elif block_name == "Latin Extended-D": # U+A720 - U+A7FF
        return "Latin"
    elif block_name == "Latin Extended-E": # U+AB30 - U+AB6F
        return "Latin"
    elif block_name == "Alphabetic Presentation Forms": # U+FB00 - U+FB4F
        return "Letterlike"
    elif block_name == "Combining Half Marks": # U+FE20 - U+FE2F
        return "Combining Marks"
    elif block_name == "Halfwidth and Fullwidth Forms": # U+FF00 - U+FFEF
        return "Other"
    elif block_name == "Latin Extended-F": # U+10780 - U+107BF
        return "Latin"
    elif block_name == "Mathematical Alphanumeric Symbols": # U+1D400 - U+1D7FF
        return "Mathematics"
    elif block_name == "Latin Extended-G": # U+1DF00 - U+1DFFF
        return "Latin"
    elif block_name == "Cyrillic Extended-D": # U+1E030 - U+1E08F
        return "Latin"
    elif block_name == "Supplemental Arrows-C": # U+1F800 - U+1F8FF
        return "Arrows"
    elif block_name == "Supplemental Symbols and Pictographs": # U+1F900 - U+1F9FF
        return "Symbols"
    elif block_name == "Chess Symbols": # U+1FA00 - U+1FA6F
        return "Symbols"
    elif block_name == "Symbols and Pictographs Extended-A": # U+1FA70 - U+1FAFF
        return "Symbols"
    elif block_name == "Symbols for Legacy Computing": # U+1FB00 - U+1FBFF
        return "Symbols"
    else:
        return "Other"

main()
