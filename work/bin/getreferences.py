#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, json, sys, math, os, unicodedata

for dir in ["%s/git/dse.d/fonts.d/old-timey-mono-font/support/lib" % os.getenv("HOME")]:
    if dir not in sys.path:
        sys.path.append(dir)

from my_font_utils import guess_transform_sequence
from no_indent import NoIndent, NoIndentEncoder

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--unicode-names", action="store_true")
    args = parser.parse_args()

    reference_data = {}
    data = { "references": reference_data }

    def glyphname_key(glyph):
        if args.unicode_names:
            glyphname = glyph.glyphname
            variant = None
            if "." in glyphname:
                (glyphname, variant) = glyphname.split(".", 1)
            unicode = fontforge.unicodeFromName(glyphname)
            if (glyph.unicode >= 0 and glyph.unicode == unicode) or (glyph.unicode < 0 and unicode >= 0):
                try:
                    this_charname = unicodedata.name(chr(unicode))
                    if variant is not None:
                        this_charname += "." + variant
                    return this_charname
                except:
                    print("glyph.glyphname = %s; glyph.unicode = %s => glyphname = %s; variant = %s => %s; unicode = %d" % (glyph.glyphname, glyph.unicode, glyphname, variant, glyph.glyphname, unicode))
                    return glyph.glyphname
            else:
                print("glyph.glyphname = %s; glyph.unicode = %s => glyphname = %s; variant = %s => %s; unicode = %d" % (glyph.glyphname, glyph.unicode, glyphname, variant, glyph.glyphname, unicode))
                return glyph.glyphname
        return glyph.glyphname

    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        if not len(glyph.references):
            continue
        if len(glyph.foreground):
            raise Exception("%s: contains both contours and references; will not support" % glyph.glyphname)
        this_charname = glyphname_key(glyph)
        refs = []
        for glyphname, transform, _ in glyph.references:
            that_charname = glyphname_key(font[glyphname])
            if transform == (1, 0, 0, 1, 0, 0):
                refs.append(that_charname)
            else:
                sequence = [NoIndent(item) for item in guess_transform_sequence(transform)]
                refs.append([ that_charname, sequence ])
        if len(refs) == 1 and type(refs[0]) == str:
            refs = refs[0]
        reference_data[this_charname] = refs

    print(json.dumps(data, indent=4, sort_keys=True, cls=NoIndentEncoder))
    font.close()

main()
