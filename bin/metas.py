#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import re
import os
import fontforge
import argparse

LANG = "English (US)"

WEIGHT_NORMAL = 400
WEIGHT_LIGHT = 300
WEIGHT_THIN = 100

ASPECT_NORMAL = 500
ASPECT_CONDENSED = 400
ASPECT_COMPRESSED = 300

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='font filename')
    parser.add_argument('--ps-family-name', '--psfn')
    parser.add_argument('--font-family-name', '--family-name', '--ffn')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--regular', action='store_true')
    args = parser.parse_args()
    for filename in args.filenames:
        font = fontforge.open(filename)
        basename = os.path.basename(filename)
        is_code = basename.find("Code") >= 0

        # compute styles from filename
        #----------------------------------------------------------------------

        if args.font_family_name is not None:
            font_family_name = args.font_family_name
        elif match := re.match(r'RT\d+', basename):
            font_family_name = match.group(0)
        else:
            font_family_name = "Old Timey Mono"
            if is_code:
                font_family_name = "Old Timey Code"

        if args.ps_family_name is not None:
            ps_family_name = args.ps_family_name
        elif match := re.match(r'RT\d+', basename):
            ps_family_name = match.group(0)
        else:
            ps_family_name = "OldTimeyMono"
            if is_code:
                ps_family_name = "OldTimeyCode"

        weight = WEIGHT_NORMAL
        panose_2 = 5
        if basename.find("Light") >= 0:
            weight = WEIGHT_LIGHT
            panose_2 = 3
        elif basename.find("Thin") >= 0:
            weight = WEIGHT_THIN
            panose_2 = 1

        aspect = ASPECT_NORMAL
        if basename.find("Elite") >= 0:
            aspect = ASPECT_CONDENSED
        elif basename.find("Cond") >= 0:
            aspect = ASPECT_CONDENSED
        elif basename.find("17Pitch") >= 0:
            aspect = ASPECT_COMPRESSED
        elif basename.find("Comp") >= 0:
            aspect = ASPECT_COMPRESSED

        # compute names
        #----------------------------------------------------------------------

        full_name = font_family_name
        if weight == WEIGHT_LIGHT:
            full_name += " Light"
        elif weight == WEIGHT_THIN:
            full_name += " Thin"
        if aspect == ASPECT_CONDENSED:
            full_name += " Condensed"
        elif aspect == ASPECT_COMPRESSED:
            full_name += " Compressed"
        if args.regular and aspect == ASPECT_NORMAL and weight == WEIGHT_NORMAL:
            full_name += " Regular"

        ps_name = ps_family_name
        ps_name_suffix = ""
        if weight == WEIGHT_LIGHT:
            ps_name_suffix += "Light"
        elif weight == WEIGHT_THIN:
            ps_name_suffix += "Thin"
        if aspect == ASPECT_CONDENSED:
            ps_name_suffix += "Cond"
        elif aspect == ASPECT_COMPRESSED:
            ps_name_suffix += "Comp"
        if args.regular and aspect == ASPECT_NORMAL and weight == WEIGHT_NORMAL:
            ps_name_suffix += "Regular"
        if ps_name_suffix != "":
            ps_name += "-" + ps_name_suffix

        styles = []
        if weight == WEIGHT_LIGHT:
            styles.append("Light")
        elif weight == WEIGHT_THIN:
            styles.append("Thin")
        if aspect == ASPECT_CONDENSED:
            styles.append("Condensed")
        elif aspect == ASPECT_COMPRESSED:
            styles.append("Compressed")
        if len(styles) == 0:
            styles.append("Regular")

        # set font properties
        #----------------------------------------------------------------------

        font.familyname = font_family_name
        if weight == WEIGHT_LIGHT:
            font.familyname += " Light"
        elif weight == WEIGHT_THIN:
            font.familyname += " Thin"
        if aspect == ASPECT_CONDENSED:
            font.familyname += " Condensed"
        elif aspect == ASPECT_COMPRESSED:
            font.familyname += " Compressed"
        font.appendSFNTName(LANG, "Family", font.familyname)

        font.appendSFNTName(LANG, "Preferred Family", font_family_name)
        font.appendSFNTName(LANG, "WWS Family", font_family_name)

        font.fullname = full_name
        font.appendSFNTName(LANG, "Fullname", full_name)

        font.fontname = ps_name
        font.appendSFNTName(LANG, "PostScriptName", ps_name)

        if weight == WEIGHT_NORMAL:
            font.weight = "Book"
        elif weight == WEIGHT_LIGHT:
            font.weight = "Light"
        elif weight == WEIGHT_THIN:
            font.weight = "Thin"
        font.os2_weight = weight

        font.appendSFNTName(LANG, "SubFamily", "Regular") # no bolds or italics here
        font.appendSFNTName(LANG, "Preferred Styles", " ".join(styles))
        font.appendSFNTName(LANG, "WWS Subfamily", " ".join(styles))

        panose = list(font.os2_panose)
        panose[0] = 2           # Latin Text
        panose[2] = panose_2    # Weight: 3=Light [1], 4=Thin [1], 5=Book
        # [1] PANOSE documtn reverses the diffnc between Thin and Light
        # compared to other systems.
        panose[3] = 9           # Proportion: Monospace
        panose[4] = 2           # Contrast: None
        panose[5] = 2           # Stroke Variation: None
        font.os2_panose = tuple(panose)

        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)

        font.close()

main()
