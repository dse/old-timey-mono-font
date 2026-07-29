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
    data = json.loads(open(args.json_filename).read())

    # clear all lookups
    lookup_names = font.gsub_lookups
    for lookup_name in lookup_names:
        lookup_info = font.getLookupInfo(lookup_name)
        (lookup_type, lookup_flags, feature_script_lang_tuple) = lookup_info
        if lookup_type == "gsub_single":
            font.removeLookup(lookup_name)

    script_lang_tuples = [deep_tuple(t) for t in data["substitutions"]["scriptLangTuples"]]

    for lookup_name, lookup_data in data["substitutions"]["lookups"].items():
        fslt = []
        for feature_name, feature_data_items in data["substitutions"]["features"].items():
            for script_lang_tuple_idx, each_lookup_name in feature_data_items:
                if lookup_name == each_lookup_name:
                    fslt.append([feature_name, data["substitutions"]["scriptLangTuples"][script_lang_tuple_idx]])
        fslt = deep_tuple(fslt)
        font.addLookup(lookup_name, "gsub_single", (), fslt)
        for subtable_name, subtable_data in lookup_data.items():
            font.addLookupSubtable(lookup_name, subtable_name)
            for glyph_name, repl_glyph_name in subtable_data.items():
                font[glyph_name].addPosSub(subtable_name, repl_glyph_name)

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
