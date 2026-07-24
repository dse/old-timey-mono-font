#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, json, re

sys.path.append("%s/git/dse.d/my-python/src/my_python_dse" % os.getenv("HOME"))

from font_utils import parse_char
import silence

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('json_filename')
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--pyftfeatfreeze', action='store_true')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    json_data = json.loads(open(args.json_filename).read())
    for filename in args.filenames:
        silence.on()
        font = fontforge.open(filename)
        silence.off()

        for lookup_name in font.gsub_lookups:
            (lookup_type, _, _) = font.getLookupInfo(lookup_name)
            if lookup_type != "gsub_single":
                continue
            font.removeLookup(lookup_name)

        default_script_langs = json_data.get("scriptLangs")
        if default_script_langs is None:
            default_script_lang_tuple = None
        else:
            default_script_lang_tuple = [] # initialize, will convert to tuple later
            for script_lang in default_script_langs:
                [script, langs] = script_lang
                script_lang_tuple = (script, tuple(langs))
                default_script_lang_tuple.append(script_lang_tuple)
            default_script_lang_tuple = tuple(default_script_lang_tuple)

        substitution_data = json_data["substitutions"]
        for lookup_name, lookup_data in substitution_data.items():
            features = lookup_data["features"]
            subtables = lookup_data["subtables"]

            # put together feature-script-lang-tuple (or get the default)
            script_langs = lookup_data.get("scriptLangs")
            if script_langs is None:
                script_langs = default_script_langs

            # build feature-script-lang tuple from script-langs
            if script_langs is None:
                script_lang_tuples = tuple([('DFLT', ('dflt',))])
            else:
                script_lang_tuples = [] # initialize
                for script_lang in script_langs:
                    [script, langs] = script_lang
                    script_lang_tuple = (script, tuple(langs))
                    script_lang_tuples.append(script_lang_tuple)
                script_lang_tuples = tuple(script_lang_tuples)
            feature_script_lang_tuple = \
                tuple([(feature_tag, script_lang_tuples,) for feature_tag in features])

            # add lookups, lookup subtables, and substitutions
            font.addLookup(lookup_name, "gsub_single", (), feature_script_lang_tuple)
            for subtable_name, subtable_data in subtables.items():
                font.addLookupSubtable(lookup_name, subtable_name)
                for char_name, other_glyph_name in subtable_data.items():

                    codepoint = parse_char(char_name, throw=True)
                    glyph_name = fontforge.nameFromUnicode(codepoint)

                    if other_glyph_name in font: # e.g., "colon.VCEN"
                        pass                     # OK
                    elif other_glyph_name.startswith("."): # e.g., ".VCEN"
                        other_glyph_name = glyph_name + other_glyph_name # e.g., "colon.VCEN"

                    if glyph_name in font and other_glyph_name in font:
                        glyph = font[glyph_name]
                        glyph.addPosSub(subtable_name, other_glyph_name)
                    else:
                        if glyph_name not in font:
                            print("WARNING: %s (used in subtable %s) not in font" % (glyph_name, subtable_name))
                        if other_glyph_name not in font:
                            print("WARNING: %s (used in subtable %s) not in font" % (other_glyph_name, subtable_name))

        # add lookups for cvXX variants
        variant_glyphs = [glyph for glyph in list(font.glyphs())
                          if re.search(r'\.cv[0-9][0-9]$', glyph.glyphname)]
        for variant_glyph in variant_glyphs: # destination glyphs
            base_glyphname = variant_glyph.glyphname.split('.')[0] # e.g., "zero"
            base_codepoint = fontforge.unicodeFromName(base_glyphname)
            unicoded_glyphs = [glyph for glyph in font.glyphs() if glyph.unicode == base_codepoint]
            if not len(unicoded_glyphs):
                continue
            if len(unicoded_glyphs) > 1:
                print("WARNING: more than one glyph with codepoint %d" % base_codepoint)
            feature_tag = variant_glyph.glyphname[-4:] # e.g., "cv05"
            feature_script_lang_tuple = ((feature_tag, default_script_lang_tuple),)
            if "character_variants" in json_data and feature_tag in json_data["character_variants"]:
                lookup_name = "%s (%s)" % (json_data["character_variants"][feature_tag], variant_glyph.glyphname)
                subtable_name = "%s-1 (%s)" % (json_data["character_variants"][feature_tag], variant_glyph.glyphname)
            else:
                lookup_name = "%s" % (feature_tag, variant_glyph.glyphname)
                subtable_name = "'%s' %s-1" % (feature_tag, variant_glyph.glyphname)
            font.addLookup(lookup_name, "gsub_single", (), feature_script_lang_tuple)
            font.addLookupSubtable(lookup_name, subtable_name)
            for unicoded_glyph in unicoded_glyphs: # should only be one
                if unicoded_glyph.glyphname == base_glyphname: # taken care of later
                    continue
                if unicoded_glyph.glyphname != variant_glyph.glyphname:
                    unicoded_glyph.addPosSub(subtable_name, variant_glyph.glyphname)
            font[base_glyphname].addPosSub(subtable_name, variant_glyph.glyphname) # for good measure

        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)

        font.close()
main()
