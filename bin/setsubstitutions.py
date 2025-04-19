#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, json
sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import silence
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('json_filename')
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    print("loading substitution data from %s" % args.json_filename)
    json_data = json.loads(open(args.json_filename).read())
    for filename in args.filenames:
        silence.on()
        font = fontforge.open(filename)
        silence.off()
        for lookup_name in font.gsub_lookups:
            (lookup_type, _, _) = font.getLookupInfo(lookup_name)
            if lookup_type != "gsub_single":
                continue
            print("removing gsub_single lookup named %s" % lookup_name)
            font.removeLookup(lookup_name)
        substitution_data = json_data["substitutions"]
        for lookup_name, lookup_data in substitution_data.items():
            features = lookup_data["features"]
            subtables = lookup_data["subtables"]
            feature_script_lang_tuple = tuple([(feature_tag, (('DFLT', ('dflt',)),)) for feature_tag in features])
            font.addLookup(lookup_name, "gsub_single", (), feature_script_lang_tuple)
            for subtable_name, subtable_data in subtables.items():
                font.addLookupSubtable(lookup_name, subtable_name)
                for glyph_name, other_glyph_name in subtable_data.items():
                    if glyph_name in font and other_glyph_name in font:
                        glyph = font[glyph_name]
                        glyph.addPosSub(subtable_name, other_glyph_name)
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)
        font.close()
main()
