#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, os, pickle

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from fontforge_attr_names import FONTFORGE_GLYPH_ATTR_NAMES

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.parse_args()

    data = {
        "defaults": {},
        "allErrors": {},
        "allValues": {},
        "uniqueValues": {},
    }

    defaults = data["defaults"]
    all_errors = data["allErrors"]
    all_values = data["allValues"]
    unique_values = data["uniqueValues"]

    font = fontforge.font()
    test_glyph_1 = font.createChar(32, fontforge.nameFromUnicode(32))
    test_glyph_2 = font.createChar(33, fontforge.nameFromUnicode(33))
    test_glyph_3 = font.createChar(34)
    test_glyph_4 = font.createChar(-1, "space.ss01")
    test_glyph_5 = font.createChar(-1, "space.ss02")
    test_glyph_6 = font.createChar(-1, "fhqwhgads")

    test_glyphs = [test_glyph_1, test_glyph_2, test_glyph_3, test_glyph_4, test_glyph_5, test_glyph_6]
    # list(enumerate(<list>)) => [(idx, val), (idx, val), ...]

    for (glyph_index, glyph) in enumerate(test_glyphs):
        for attr_name in FONTFORGE_GLYPH_ATTR_NAMES:
            error_type = None
            attr_val = None
            try:
                attr_val = getattr(glyph, attr_name)
                try:
                    json.dumps(attr_val) # for side effects
                except Exception as error:
                    error_type = str(type(error)).split("'")[1]
                    attr_val = ["ERROR", error_type, str(error)]
            except Exception as error:
                error_type = str(type(error)).split("'")[1]
                attr_val = ["ERROR", error_type, str(error)]
            if error_type is not None:
                if attr_name not in all_errors:
                    all_errors[attr_name] = []
                all_errors[attr_name].append(attr_val)
            else:
                if attr_name not in all_values:
                    all_values[attr_name] = []
                all_values[attr_name].append(attr_val)
                # values[attr_name] = attr_val

    for attr_name in all_values:
        values = all_values[attr_name]
        uniques = get_unique_values(values)
        if len(uniques) == 0:
            defaults[attr_name] = None
        elif len(uniques) == 1:
            defaults[attr_name] = values[0]
        else:
            unique_values[attr_name] = uniques

    for attr_name in all_errors:
        all_errors[attr_name] = get_unique_values(all_errors[attr_name])

    deletes = []
    for attr_name in all_values:
        if attr_name not in unique_values:
            deletes.append(attr_name)

    for attr_name in deletes:
        del all_values[attr_name]

    font.close()

    print(json.dumps(data, indent=4))

def get_unique_values(values):
    result = []
    for i in range(0, len(values)):
        for j in range(0, len(result)):
            if values[i] == result[j]:
                break
        else:
            result.append(values[i])
    return result

main()
