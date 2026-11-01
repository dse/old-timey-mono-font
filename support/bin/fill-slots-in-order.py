#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, unicodedata, json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from otm.generated import GENERATED_GLYPH_CODES, SMOL_GLYPH_CODES, GENERATED_SPACE_CODES
from otm.util import is_valid_code, walk_svg
from otm.index import parse_glyph_name, parse_svg_filename

DEFAULT_GLYPH_WIDTH = 1008

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("svg_filenames", nargs="*")
    args = parser.parse_args()

    if len(args.svg_filenames):
        svg_filenames = walk_svg(args.svg_filenames)
    else:
        svg_filenames = walk_svg(["src/upright"])
    if not len(svg_filenames):
        raise Exception("no SVGs to import")

    font = fontforge.open(args.filename)

    references_dict = json.loads(open("src/data/new-references.json", "r").read())["references"]
    reference_glyph_names = list(references_dict.keys())
    reference_items = [parse_glyph_name(glyph_name) for glyph_name in reference_glyph_names]

    generated_glyph_names = [fontforge.nameFromUnicode(code) for code in GENERATED_GLYPH_CODES]
    generated_items = [parse_glyph_name(glyph_name) for glyph_name in generated_glyph_names]

    print("C")

    smol_glyph_names = [fontforge.nameFromUnicode(code) + ".SMOL" for code in SMOL_GLYPH_CODES]
    smol_items = [parse_glyph_name(glyph_name) for glyph_name in smol_glyph_names]

    print("D")

    matched_svg_items = [parse_svg_filename(filename) for filename in svg_filenames]

    items = [
        *reference_items,
        *generated_items,
        *smol_items,
        *matched_svg_items,
        *[
            parse_glyph_name(fontforge.nameFromUnicode(code)) for code in GENERATED_SPACE_CODES
        ]
    ]

    def items_key_fn(item):
        code      = item.code      if is_valid_code(item.code)      else float('inf')
        norm_code = item.norm_code if is_valid_code(item.norm_code) else float('inf')
        name      = item.norm_glyph_name
        variant   = item.variant
        return (variant, code, norm_code, name)

    items.sort(key=items_key_fn)

    for item in items:
        print(f"fill-slots-in-order {item}")
        print(f"createChar EEEE {item.code} {item.norm_glyph_name}")
        # if (item.code == 0x259):
        #     # fill-slots-in-order.py
        #     raise Exception("WHEEEEE")
        glyph = font.createChar(item.code, item.norm_glyph_name)
        glyph.width = DEFAULT_GLYPH_WIDTH
        glyph.changed = True

    print(f"createChar FFFF -1 DUMMY")
    glyph = font.createChar(-1, "DUMMY")
    glyph.width = DEFAULT_GLYPH_WIDTH

    if args.filename.lower().endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
