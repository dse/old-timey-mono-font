#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    root = {
        "substitutions": {
            "scriptLangTuples": [
            ],
            "features": {
            },
            "lookups": {
            },
        },
    }

    def get_script_lang_tuple_idx(script_lang_tuple):
        for idx, each_script_lang_tuple in enumerate(data["scriptLangTuples"]):
            each_script_lang_tuple = deep_tuple(each_script_lang_tuple)
            if each_script_lang_tuple == script_lang_tuple:
                return idx
        idx = len(data["scriptLangTuples"])
        data["scriptLangTuples"].append(script_lang_tuple)
        return idx

    lookup_names = font.gsub_lookups
    for lookup_name in lookup_names:
        lookup_info = font.getLookupInfo(lookup_name)
        (lookup_type, lookup_flags, feature_script_lang_tuple) = lookup_info
        if lookup_type == "gsub_single":
            lookup_data = {}
            data["lookups"][lookup_name] = lookup_data
            for feature, script_lang_tuple in feature_script_lang_tuple:
                script_lang_tuple_idx = get_script_lang_tuple_idx(script_lang_tuple)
                data["lookups"][lookup_name]
                if feature not in data["features"]:
                    data["features"][feature] = []
                data["features"][feature].append([script_lang_tuple_idx, lookup_name])
            for subtable_name in font.getLookupSubtables(lookup_name):
                subtable_data = {}
                data["lookups"][lookup_name][subtable_name] = subtable_data
                for glyph in font.glyphs():
                    for gsub_tuple in glyph.getPosSub(subtable_name):
                        tuple_type = gsub_tuple[1]
                        if tuple_type == "Substitution":
                            replacement_glyph_name = gsub_tuple[2]
                        else:
                            raise Exception("unsupported getPosSub tuple type: %s" % repr(tuple_type))
                        subtable_data[glyph.glyphname] = replacement_glyph_name
        else:
            raise Exception("unsupported lookup type: %s" % repr(lookup_type))

    print(json.dumps(root, indent=4, sort_keys=True))
    font.close()

def deep_tuple(val):
    if type(val) in [list, tuple]:
        return tuple([deep_tuple(v) for v in val])
    return val

main()
