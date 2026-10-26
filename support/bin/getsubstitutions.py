#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    root = {
        "substitutions": {
            "lookups": {
            },
            "scriptLangTuples": [
            ]
        }
    }

    font = fontforge.open(args.filename)

    lookups_dict = root["substitutions"]["lookups"]
    script_lang_tuples_list = root["substitutions"]["scriptLangTuples"]

    for lookup_name in font.gsub_lookups:
        lookup_dict = {
            "features": {},
            "subtables": {}
        }
        lookups_dict[lookup_name] = lookup_dict
        lookup_type, lookup_flags, feature_script_lang_tuple = font.getLookupInfo(lookup_name)
        features_dict = lookup_dict["features"]
        subtables_dict = lookup_dict["subtables"]
        lookup_dict["type"] = lookup_type
        lookup_dict["flags"] = lookup_flags

        for feature_name, script_lang_tuple in feature_script_lang_tuple:
            script_lang_tuple_dict = {}
            for script, lang_tuple in script_lang_tuple:
                script_lang_tuple_dict[script] = lang_tuple
            feature_dict = {}
            features_dict[feature_name] = feature_dict
            try:
                feature_dict["scriptLangTupleIndex"] = script_lang_tuples_list.index(script_lang_tuple)
            except ValueError:
                feature_dict["scriptLangTupleIndex"] = len(script_lang_tuples_list)
                script_lang_tuples_list.append(script_lang_tuple)
        for subtable_name in font.getLookupSubtables(lookup_name):
            subtables_dict[subtable_name] = {}

    for glyph in font.glyphs():
        for subtable_name, kind, replacement_glyph_name, *_ in glyph.getPosSub("*"):
            if kind != "Substitution":
                continue
            lookup_name = font.getLookupOfSubtable(subtable_name)
            lookup_dict = lookups_dict[lookup_name]
            subtables_dict = lookup_dict["subtables"]
            subtable_dict = subtables_dict[subtable_name]
            subtable_dict[glyph.glyphname] = replacement_glyph_name

    font = fontforge.open(args.filename)
    font.close()

    print(json.dumps(root, indent=4))

main()
