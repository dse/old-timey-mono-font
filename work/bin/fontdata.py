#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, unicodedata, argparse, json
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
font = fontforge.open(args.filename)
font_data = {
    "ascent": font.ascent,
    "descent": font.descent,
    "bitmapSizes": font.bitmapSizes,
    "capHeight": font.capHeight,
    "comment": font.comment,
    "copyright": font.copyright,
    "designSize": font.design_size,
    "em": font.em,
    "encoding": font.encoding,
    "familyName": font.familyname,
    "fontname": font.fontname,
    "fullname": font.fullname,
    "gsubLookups": font.gsub_lookups,
    "italicAngle": font.italicangle,
    "macstyle": {
        "value": font.macstyle,
        "flags": {
            "bold":      font.macstyle & 1 != 0,
            "italic":    font.macstyle & 2 != 0,
            "underline": font.macstyle & 4 != 0,
            "outline":   font.macstyle & 8 != 0,
            "shadow":    font.macstyle & 16 != 0,
            "condensed": font.macstyle & 32 != 0,
            "extended":  font.macstyle & 64 != 0,
        },
    },
    "os2FamilyClass": font.os2_family_class,
    "os2FsType": font.os2_fstype,
    "os2StyleMap": font.os2_stylemap,
    "os2Panose": font.os2_panose,
    "os2Weight": font.os2_weight,
    "sfntNames": font.sfnt_names,
    "sfntRevision": font.sfntRevision,
    "sfntRevisionNominal": round(font.sfntRevision * 10000) / 10000,
    "uniqueId": font.uniqueid,
    "underlineWidth": font.uwidth,
    "version": font.version,
    "weight": font.weight,
    "exHeight": font.xHeight,
    "glyphs": [],
    "lookups": {},
    "lookupInfo": {},
    "lookupSubtables": {},
}
for lookup_name in font.gsub_lookups:
    font_data["lookups"][lookup_name] = {
        "info": font.getLookupInfo(lookup_name),
        "subtables": font.getLookupSubtables(lookup_name),
    }
for glyph in font.glyphs():
    glyph_data = {
        "name": glyph.glyphname,
        "additionalCodepoints": glyph.altuni,
        "codepoint": glyph.unicode,
        "comment": glyph.comment,
        "encoding": glyph.encoding,
        "glyphclass": glyph.glyphclass,
        "leftSideBearing": glyph.left_side_bearing,
        "rightSideBearing": glyph.right_side_bearing,
        "manualHints": glyph.manualHints,
        "originalGid": glyph.originalgid,
        "references": glyph.references,
        "script": glyph.script,
        "userDecomp": glyph.user_decomp,
        "width": glyph.width,
        "boundingBox": glyph.boundingBox(),
        "dhints": glyph.dhints,
        "hhints": glyph.hhints,
        "vhints": glyph.vhints,
        "substitutionData": {},
    }
    for lookup_name in font.gsub_lookups:
        glyph_data["substitutionData"][lookup_name] = {}
        for subtable_name in font.getLookupSubtables(lookup_name):
            glyph_data["substitutionData"][lookup_name][subtable_name] = \
                glyph.getPosSub(subtable_name)
    font_data["glyphs"].append(glyph_data)
font.close()
print(json.dumps(font_data, indent=4))
