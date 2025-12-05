#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, math, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    font_data = {
        "ascent": font.ascent,
        "capHeight": font.capHeight,
        "comment": font.comment,
        "copyright": font.copyright,
        "descent": font.descent,
        "designSize": font.design_size,
        "em": font.em,
        "familyName": font.familyname,
        "fondName": font.fondname,
        "fontLog": font.fontlog,
        "fontName": font.fontname,
        "fullName": font.fullname,
        "hheaAscent": font.hhea_ascent,
        "hheaDescent": font.hhea_descent,
        "hheaAscentAdd": font.hhea_ascent_add,
        "hheaDescentAdd": font.hhea_descent_add,
        "hheaLineGap": font.hhea_linegap,
        "italicAngle": font.italicangle,
        "macStyle": {
            "numeric": font.macstyle,
            "bold": font.macstyle & 1 != 0,
            "italic": font.macstyle & 2 != 0,
            "underline": font.macstyle & 4 != 0,
            "outline": font.macstyle & 8 != 0,
            "shadow": font.macstyle & 16 != 0,
            "condensed": font.macstyle & 32 != 0,
            "extended": font.macstyle & 64 != 0,
        },
        "os2CapHeight": font.os2_capheight,
        "os2FamilyClass": font.os2_family_class,
        "os2FsType": font.os2_fstype,
        "os2Panose": font.os2_panose,
        "os2StrikeYPosition": font.os2_strikeypos,
        "os2StrikeYSize": font.os2_strikeysize,
        "os2StyleMap": font.os2_stylemap,
        "os2SubscriptXOffset": font.os2_subxoff,
        "os2SubscriptXSize": font.os2_subxsize,
        "os2SubscriptYOffset": font.os2_subyoff,
        "os2SubscriptYSize": font.os2_subysize,
        "os2SuperscriptXOffset": font.os2_supxoff,
        "os2SuperscriptXSize": font.os2_supxsize,
        "os2SuperscriptYOffset": font.os2_supyoff,
        "os2SuperscriptYSize": font.os2_supysize,
        "os2TypoAscent": font.os2_typoascent,
        "os2TypoAscentAdd": font.os2_typoascent_add,
        "os2TypoDescent": font.os2_typodescent,
        "os2TypoDescentAdd": font.os2_typodescent_add,
        "os2TypoLineGap": font.os2_typolinegap,
        "os2UseTypoMetrics": font.os2_use_typo_metrics,
        "os2Vendor": font.os2_vendor,
        "os2Version": font.os2_version,
        "os2Weight": font.os2_weight,
        "os2WeightWidthSlopeOnly": font.os2_weight_width_slope_only,
        "os2Width": font.os2_width,
        "os2WinAscent": font.os2_winascent,
        "os2WinAscentAdd": font.os2_winascent_add,
        "os2WinDescent": font.os2_windescent,
        "os2WinDescentAdd": font.os2_windescent_add,
        "os2ExHeight": font.os2_xheight,
        "sfntRevision": int(font.sfntRevision * 10000) / 10000,
        "strokedFont": font.strokedfont,
        "strokeWidth": font.strokewidth,
        "uniqueId": font.uniqueid,
        "underlinePosition": font.upos,
        "underlineWidth": font.uwidth,
        "version": font.version,
        "vheaLineGap": font.vhea_linegap,
        "weight": font.weight,
        "exHeight": font.xHeight,
    }

    panose_file = os.path.join(os.path.dirname(__file__), "../../src/data/panose.json")
    with open(panose_file, "r") as fh:
        panose_json = fh.read()
    panose_data = json.loads(panose_json)
    family_kinds_data = panose_data["familyKinds"][font.os2_panose[0]]
    family_kind_name = family_kinds_data["name"]
    family_kind_fields = family_kinds_data["fields"]
    panose_fields = {}
    for idx in range(0, len(family_kind_fields)):
        field_data = family_kind_fields[idx]
        field_name = field_data["name"]
        field_values = field_data["values"]
        panose_fields[field_name] = field_values[font.os2_panose[idx]]

    font_data["panose"] = panose_fields

    print(json.dumps(font_data, indent=4))


main()
