#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, json, unicodedata, unicodedataplus

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
    glyphs_data = []

    glyphs = list(font.glyphs())
    glyphs.sort(key = lambda glyph: glyph.encoding)

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
        if base_char is not None:
            glyph_data["unicodeName"] = unicodedata.name(base_char, None)
            glyph_data["unicodeCategory"] = unicodedata.category(base_char)
            glyph_data["unicodeBlock"] = unicodedataplus.block(base_char)
            glyph_data["unicodeScript"] = unicodedataplus.script(base_char)
            if base_char in CONTROL_NAMES:
                glyph_data["unicodeControlName"] = CONTROL_NAMES[base_char]
        glyphs_data.append(glyph_data)
    print(json.dumps(glyphs_data, indent=4))

main()
