#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("font_filename")
    parser.add_argument("json_filename")
    args = parser.parse_args()

    font = fontforge.open(args.font_filename)
    root = json.loads(open(args.json_filename).read())

    lookups_dict = root["substitutions"]["lookups"]
    script_lang_tuples_list = root["substitutions"]["scriptLangTuples"]

    # clear all lookups
    lookup_names = font.gsub_lookups
    for lookup_name in lookup_names:
        lookup_info = font.getLookupInfo(lookup_name)
        (lookup_type, lookup_flags, feature_script_lang_tuple) = lookup_info
        if lookup_type == "gsub_single":
            font.removeLookup(lookup_name)

    for lookup_name, lookup_dict in reversed(lookups_dict.items()):
        features_dict = lookup_dict["features"]
        subtables_dict = lookup_dict["subtables"]
        lookup_type = lookup_dict["type"]
        lookup_flags = lookup_dict["flags"]
        if lookup_type != "gsub_single":
            continue
        if len(lookup_flags) == 0:
            lookup_flags = None
        else:
            lookup_flags = tuple(lookup_flags)
        feature_script_lang_tuple = []
        for feature_name, feature_dict in features_dict.items():
            script_lang_tuple = script_lang_tuples_list[feature_dict["scriptLangTupleIndex"]]
            feature_script_lang_tuple.append([feature_name, script_lang_tuple])
        feature_script_lang_tuple = deep_tuple(feature_script_lang_tuple)
        font.addLookup(lookup_name, lookup_type, lookup_flags, feature_script_lang_tuple)
        for subtable_name, subtable_dict in subtables_dict.items():
            font.addLookupSubtable(lookup_name, subtable_name)
            for glyphname, replacement_glyphname in subtable_dict.items():
                font[glyphname].addPosSub(subtable_name, replacement_glyphname)

    if args.font_filename.endswith(".sfd"):
        font.save(args.font_filename)
    else:
        font.generate(args.font_filename)
    font.close()

def deep_tuple(val):
    if type(val) in [list, tuple]:
        return tuple([deep_tuple(v) for v in val])
    return val

main()
