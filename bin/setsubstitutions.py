#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, json, re
sys.path.append(os.getenv("HOME") + "/git/dse.d/fontforge-utilities/lib")
import silence
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('json_filename')
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    if "DEBUG" in os.environ:
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
            if "DEBUG" in os.environ:
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

        variant_glyphs = [glyph for glyph in list(font.glyphs()) if re.search(r'\.cv[0-9][0-9]$', glyph.glyphname)]
        for variant_glyph in variant_glyphs:
            normal_glyphname = variant_glyph.glyphname.split('.')[0]
            if not normal_glyphname in font:
                continue
            if fontforge.unicodeFromName(normal_glyphname) < 0:
                continue
            normal_glyph = font[normal_glyphname]
            feature_tag = variant_glyph.glyphname[-4:]
            if feature_tag in font.gsub_lookups:
                continue
            if "character_variants" in json_data and feature_tag in json_data["character_variants"]:
                lookup_name = "%s (%s)" % (json_data["character_variants"][feature_tag], variant_glyph.glyphname)
                subtable_name = "%s subtable (%s)" % (json_data["character_variants"][feature_tag], variant_glyph.glyphname)
            else:
                lookup_name = variant_glyph.glyphname
                subtable_name = "%s subtable" % (variant_glyph.glyphname,)
            feature_script_lang_tuple = ((feature_tag, (('DFLT', ('dflt',)),)),)
            font.addLookup(lookup_name, "gsub_single", (), feature_script_lang_tuple)
            font.addLookupSubtable(lookup_name, subtable_name)
            normal_glyph.addPosSub(subtable_name, variant_glyph.glyphname)
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)
        font.close()
main()
