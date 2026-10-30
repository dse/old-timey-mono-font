#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-

import fontforge, json, argparse, os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    data = json.loads(open("fonts.json", "r").read())
    fonts_data = data["fonts"]
    defaults_data = data["defaults"]

    filename_stem = os.path.splitext(args.filename)
    basename_stem = os.path.splitext(os.path.basename(args.filename))[0]

    if filename_stem in fonts_data:
        font_data = fonts_data[filename_stem]
    elif basename_stem in fonts_data:
        font_data = fonts_data[basename_stem]
    else:
        raise Exception(f"{filename_stem}.* or {basename_stem}.* " +
                        "not found in fonts.json")
    font_data = defaults_data | font_data

    font = fontforge.font()

    if "em" in font_data:
        font.em = font_data["em"]
    font.ascent = font_data.get("ascent", round(font.em * 4/5))
    font.descent = font_data.get("descent", font.em - font.ascent)

    if "version" in font_data:
        font.version = font_data["version"]
    if "vendor" in font_data:
        font.os2_vendor = font_data["vendor"]
    if "copyright" in font_data:
        font.copyright = font_data["copyright"]
    if "comment" in font_data:
        font.comment = font_data["comment"]
    if "ttfWeight" in font_data:
        font.os2_weight = font_data["ttfWeight"]
    if "familyName" in font_data:
        font.familyname = font_data["familyName"]
    if "underlinePosition" in font_data:
        font.upos = font_data["underlinePosition"]
    if "underlineWidth" in font_data:
        font.uwidth = font_data["underlineWidth"]
    if "sfntRevision" in font_data:
        font.sfntRevision = font_data["sfntRevision"]
    if "fontName" in font_data:
        font.fontname = font_data["fontName"]
    if "fullName" in font_data:
        font.fullname = font_data["fullName"]
    if "familyName" in font_data:
        font.familyname = font_data["familyName"]
    if "weightName" in font_data:
        font.weight = font_data["weightName"]

    linegap = font_data.get("lineGap", 0)
    font.italicangle = font_data.get("italicAngle", 0)

    font.hhea_ascent = font.ascent
    font.hhea_ascent_add = 0
    font.hhea_descent = -font.descent
    font.hhea_descent_add = 0
    font.hhea_linegap = linegap
    font.os2_typoascent = font.ascent
    font.os2_typoascent_add = 0
    font.os2_typodescent = -font.descent
    font.os2_typodescent_add = 0
    font.os2_typolinegap = linegap
    font.os2_winascent = font.ascent
    font.os2_winascent_add = 0
    font.os2_windescent = font.descent
    font.os2_windescent_add = 0
    font.vhea_linegap = linegap

    if "width" not in font_data:
        raise Exception("width not in defaults or font data")

    if "panose" in font_data:
        font.os2_panose = tuple(font_data["panose"])

    font.createChar(32).width = font_data["width"]
    font.createChar(33).width = font_data["width"]
    font.createChar(34).width = font_data["width"]
    font.createChar(35).width = font_data["width"]
    font.createChar(-1, ".notdef").width = font_data["width"]


    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

main()
