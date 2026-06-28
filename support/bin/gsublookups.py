#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, json, re

sys.path.append("%s/git/dse.d/my-python/src/my_python_dse" % os.getenv("HOME"))
import silence

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    for filename in args.filenames:
        font = fontforge.open(filename)
        feature_tags = []
        feature_substitutions = {}
        for lookup_name in font.gsub_lookups:
            lookup_substitutions = []
            for subtable_name in font.getLookupSubtables(lookup_name):
                for glyph in font.glyphs():
                    for lookup_item in [item for item in glyph.getPosSub(subtable_name) if item[1] == "Substitution"]:
                        lookup_substitutions.append((glyph.glyphname, lookup_item[2]))
            if not lookup_substitutions:
                continue
            (lookup_type, lookup_flags, feature_script_lang_tuple) = font.getLookupInfo(lookup_name)
            if lookup_type != "gsub_single":
                continue
            for feature_script_lang_item in feature_script_lang_tuple:
                [feature_tag, script_lang_tuple] = feature_script_lang_item
                for script_lang_item in script_lang_tuple:
                    [script_lang, lang_tuple] = script_lang_item
                    if not lang_tuple:
                        continue
                    if feature_tag not in feature_tags:
                        feature_tags.append(feature_tag)
                    if feature_tag not in feature_substitutions:
                        feature_substitutions[feature_tag] = []
                feature_substitutions[feature_tag].append([script_lang_tuple, lookup_substitutions])
        for feature_tag in feature_tags:
            print("%s:" % feature_tag)
            for ab in feature_substitutions[feature_tag]:
                [a,b] = ab
                print("    %s:" % repr(a))
                for bb in b:
                    print("        %s => %s" % bb)
main()
