#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))
from otm.index import index_svg_filenames, index_glyphs, verify_glyphs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("svg_filenames", nargs="+")
    args = parser.parse_args()

    svg_filenames = walk(args.svg_filenames)
    font = fontforge.open(args.filename)

    # dicts are indexed by normalized glyph name
    svg_list, svg_dict = index_svg_filenames(svg_filenames)
    glyph_list, glyph_dict = index_glyphs(font)

    (
        success, 
        verified_svg_list,
        verified_svg_dict,
        verified_glyph_list,
        verified_glyph_dict,
        svg_only_list,
        svg_only_dict,
        glyph_only_list,
        glyph_only_dict,
    ) = verify_glyphs(svg_list, svg_dict, glyph_list, glyph_dict)

    widths = [glyph.width for glyph in font.glyphs()]
    widths.sort()
    glyph_width = statistics.median(widths)

    for item in svg_list:
        if item.name_is_arbitrary:
            glyph = font.createChar(item.code)
        else:
            glyph = font.createChar(item.code, item.norm_glyph_name)
        if len(glyph.references) and not len(glyph.foreground):
            glyph.references = ()
        glyph.foreground = fontforge.layer()

        font.strokedfont = True
        glyph.importOutline(item.svg_filename)
        font.strokedfont = False
        glyph.width = glyph_width
        glyph.comment = json.dumps({ "source": { "type": "svg", "filename": item.svg_filename } })
        
    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)

def walk(filenames):
    retval = []
    for filename in filenames:
        if os.path.isdir(filename):
            for dir_path, dir_names, dir_filenames in os.walk(filename):
                for each_filename in dir_filenames:
                    if each_filename.lower().endswith(".svg"):
                        retval.append(os.path.join(dir_path, each_filename))
        else:
            retval.append(filename)
    return retval

main()
