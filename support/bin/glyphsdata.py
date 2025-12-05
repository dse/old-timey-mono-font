#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, json, unicodedata, unicodedataplus, functools

CONTROL_NAMES = {
    "\u0000": "NULL",
    "\u0001": "START OF HEADING",
    "\u0002": "START OF TEXT",
    "\u0003": "END OF TEXT",
    "\u0004": "END OF TRANSMISSION",
    "\u0005": "ENQUIRY",
    "\u0006": "ACKNOWLEDGE",
    "\u0007": "BELL",
    "\u0008": "BACKSPACE",
    "\u0009": "CHARACTER TABULATION",
    "\u000a": "LINE FEED",
    "\u000b": "LINE TABULATION",
    "\u000c": "FORM FEED",
    "\u000d": "CARRIAGE RETURN",
    "\u000e": "SHIFT OUT",
    "\u000f": "SHIFT IN",
    "\u0010": "DATA LINK ESCAPE",
    "\u0011": "DEVICE CONTROL ONE",
    "\u0012": "DEVICE CONTROL TWO",
    "\u0013": "DEVICE CONTROL THREE",
    "\u0014": "DEVICE CONTROL FOUR",
    "\u0015": "NEGATIVE ACKNOWLEDGE",
    "\u0016": "SYNCHRONOUS IDLE",
    "\u0017": "END OF TRANSMISSION BLOCK",
    "\u0018": "CANCEL",
    "\u0019": "END OF MEDIUM",
    "\u001a": "SUBSTITUTE",
    "\u001b": "ESCAPE",
    "\u001c": "INFORMATION SEPARATOR FOUR",
    "\u001d": "INFORMATION SEPARATOR THREE",
    "\u001e": "INFORMATION SEPARATOR TWO",
    "\u001f": "INFORMATION SEPARATOR ONE",
    "\u0080": None,
    "\u0081": None,
    "\u0082": "BREAK PERMITTED HERE",
    "\u0083": "NO BREAK HERE",
    "\u0084": "(INDEX)",
    "\u0085": "NEXT LINE (NEL)",
    "\u0086": "START OF SELECTED AREA",
    "\u0087": "END OF SELECTED AREA",
    "\u0088": "CHARACTER TABULATION SET",
    "\u0089": "CHARACTER TABULATION WITH JUSTIFICATION",
    "\u008a": "LINE TABULATION SET",
    "\u008b": "PARTIAL LINE FORWARD",
    "\u008c": "PARTIAL LINE BACKWARD",
    "\u008d": "REVERSE LINE FEED",
    "\u008e": "SINGLE SHIFT TWO",
    "\u008f": "SINGLE SHIFT THREE",
    "\u0090": "DEVICE CONTROL STRING",
    "\u0091": "PRIVATE USE ONE",
    "\u0092": "PRIVATE USE TWO",
    "\u0093": "SET TRANSMIT STATE",
    "\u0094": "CANCEL CHARACTER",
    "\u0095": "MESSAGE WAITING",
    "\u0096": "START OF GUARDED AREA",
    "\u0097": "END OF GUARDED AREA",
    "\u0098": "START OF STRING",
    "\u0099": None,
    "\u009a": "SINGLE CHARACTER INTRODUCER",
    "\u009b": "CONTROL SEQUENCE INTRODUCER",
    "\u009c": "STRING TERMINATOR",
    "\u009d": "OPERATING SYSTEM COMMAND",
    "\u009e": "PRIVACY MESSAGE",
    "\u009f": "APPLICATION PROGRAM COMMAND",
}

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    glyphs = list(font.glyphs())
    glyphs = [glyph for glyph in glyphs if not (glyph.unicode in range(0, 32)) and glyph.glyphname != ".notdef"]
    glyphs.sort(key = functools.cmp_to_key(glyph_cmp))

    glyphs_data = []
    data_by_block_name = {}

    for glyph in glyphs:
        glyph_data = {
            "altUni": glyph.altuni,
            "comment": glyph.comment,
            "encoding": glyph.encoding,
            "glyphClass": glyph.glyphclass,
            "glyphName": glyph.glyphname,
            "leftSideBearing": glyph.left_side_bearing,
            "originalGid": glyph.originalgid,
            "rightSideBearing": glyph.right_side_bearing,
            "script": glyph.script,
            "unicode": glyph.unicode,
            "width": glyph.width,
            "verticalWidth": glyph.vwidth,
            "baseUnicode": glyph.unicode,
            "baseGlyphName": glyph.glyphname,
            "variantName": None,
            "isBaseGlyph": True,
        }
        base_unicode = glyph.unicode
        base_glyphname = glyph.glyphname
        base_char = chr(glyph.unicode) if glyph.unicode > -1 else None
        if "." in glyph.glyphname:
            glyph_data["isBaseGlyph"] = False
            idx = glyph.glyphname.find(".")
            if idx > -1:
                variant_name = glyph.glyphname[idx+1:]
                base_glyphname = glyph.glyphname[0:idx]
                base_unicode = fontforge.unicodeFromName(base_glyphname)
                base_char = chr(base_unicode) if base_unicode in range(0, 0x10ffff + 1) else None
                if base_unicode > -1:
                    glyph_data["baseUnicode"] = base_unicode
                    glyph_data["baseGlyphName"] = base_glyphname
                    glyph_data["variantName"] = variant_name
        base_unicode_hex = "U+%04X" % base_unicode if base_unicode >= 0 else None
        unicode_hex = "U+%04X" % glyph.unicode if glyph.unicode >= 0 else None
        glyph_data["baseUnicodeHex"] = base_unicode_hex
        glyph_data["unicodeHex"] = unicode_hex
        if base_char is not None:
            glyph_data["unicodeName"] = unicodedata.name(base_char, None)
            glyph_data["unicodeCategory"] = unicodedata.category(base_char)
            glyph_data["unicodeBlock"] = unicodedataplus.block(base_char)
            glyph_data["unicodeScript"] = unicodedataplus.script(base_char)
            if base_char in CONTROL_NAMES:
                glyph_data["unicodeControlName"] = CONTROL_NAMES[base_char]
        glyphs_data.append(glyph_data)

        block_name = unicodedataplus.block(chr(base_unicode)) if base_unicode >= 0 else None
        if not block_name in data_by_block_name:
            data_by_block_name[block_name] = {}
        block_data = data_by_block_name[block_name]

        if base_unicode >= 0:
            if not "codepoints" in block_data:
                block_data["codepoints"] = []
            if not base_unicode in block_data["codepoints"]:
                block_data["codepoints"].append(base_unicode)

        if not "glyphNames" in block_data:
            block_data["glyphNames"] = []
        if not "glyphNames" in block_data["glyphNames"]:
            block_data["glyphNames"].append(glyph.glyphname)

    block_names=[*data_by_block_name.keys()]
    for block_name in block_names:
        if not "codepoints" in data_by_block_name[block_name]:
            data_by_block_name[block_name]["codepoints"] = []
        if 0 == len(data_by_block_name[block_name]["codepoints"]):
            data_by_block_name[block_name]["codepoints"].append(-1)

    block_names.sort(key = lambda block_name: data_by_block_name[block_name]["codepoints"][0])

    data = {
        "glyphs": glyphs_data,
        "blockNames": block_names,
        "dataByBlockName": data_by_block_name,
    }

    print(json.dumps(data, indent=4))

def glyph_cmp(glyph_a, glyph_b):
    unicode_a = glyph_a.unicode
    primary_a = True
    glyphname_a = glyph_a.glyphname
    if unicode_a < 0:
        if "." in glyphname_a:
            unicode_a = fontforge.unicodeFromName(glyphname_a.split(".")[0])
            primary_a = False
            variant_a = glyphname_a.split(".", maxsplit=1)[1]
            if unicode_a < 0: unicode_a = 1114112
        else:
            unicode_a = 1114113

    unicode_b = glyph_b.unicode
    primary_b = True
    glyphname_b = glyph_b.glyphname
    if unicode_b < 0:
        if "." in glyphname_b:
            unicode_b = fontforge.unicodeFromName(glyphname_b.split(".")[0])
            primary_b = False
            variant_b = glyphname_b.split(".", maxsplit=1)[1]
            if unicode_b < 0: unicode_b = 1114112
        else:
            unicode_b = 1114113

    if unicode_a < unicode_b: return -1
    if unicode_a > unicode_b: return 1

    if primary_a and not primary_b: return -1
    if primary_b and not primary_a: return 1

    if not primary_a and not primary_b:
        if variant_a is None and variant_b is not None: return -1
        if variant_a is not None and variant_b is None: return 1
        if variant_a < variant_b: return -1
        if variant_a > variant_b: return 1

    # variant names are the same???  for good measure...
    if glyphname_a < glyphname_b:
        return -1
    if glyphname_a > glyphname_b:
        return 1
    return 0

main()
