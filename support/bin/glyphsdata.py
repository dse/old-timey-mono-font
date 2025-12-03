#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    glyphs_data = []
    for glyph in font.glyphs():
        base_unicode = glyph.unicode
        base_glyphname = glyph.glyphname
        if "." in glyph.glyphname: # alternate glyph
            idx = glyph.glyphname.find(".")
            if idx > -1:
                base_glyphname = glyph.glyphname[0:idx] # glyphname without alternate glyph suffix
                base_unicode = fontforge.unicodeFromName(base_glyphname) # "real" codepoint
                if base_unicode > -1:
                    glyph_data["baseUnicode"] = base_unicode
                    glyph_data["baseGlyphName"] = base_glyphname
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
            "baseUnicode": base_unicode,
            "baseGlyphName": base_glyphname,
        }
        glyphs_data.append(glyph_data)
    print(json.dumps(glyphs_data, indent=4))

main()
