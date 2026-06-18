#!/usr/bin/env -S fontforge -quiet -script
# -*- mode: python; coding: utf-8 -*-
import os, argparse, fontforge
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="new font filename")
    parser.add_argument("--font-name", "--fontname", help="e.g., \"Courier-Bold\", \"AvantGardeGothic\"")
    parser.add_argument("--full-name", "--fullname", help="e.g., \"Courier Bold\", \"ITC Avant Garde Gothic\"")
    parser.add_argument("--weight-name", "--weightname", "--weight", help="e.g., \"Book\", \"Bold\", etc.")
    parser.add_argument("--family-name", "--familyname", "--family", help="e.g., \"Courier\", \"ITC Avant Garde Gothic\"")
    parser.add_argument("--copyright")
    parser.add_argument("--comment")
    parser.add_argument("--version")
    parser.add_argument("--italic-angle", "--italicangle",
                        type=float, help="counterclockwise angle, typical for italic fonts is -12")
    parser.add_argument("--sfnt-revision", "--sfntrevision",
                        type=float, help="e.g., 0.900, 1.402")
    parser.add_argument("--ascent", type=int)
    parser.add_argument("--descent", type=int)
    parser.add_argument("--em", type=int)
    parser.add_argument("--upos", type=float)
    parser.add_argument("--uwidth", type=float)
    parser.add_argument("--panose", type=int, nargs=10)
    parser.add_argument("--width", type=int, help="width of space glyph")
    parser.add_argument("--vendor", help="font creator's, registered 4-character vendor string (bit.ly/fontvendors)")
    parser.add_argument("--encoding")
    parser.add_argument("--compacted", action="store_true")
    args = parser.parse_args()

    font = fontforge.font()

    if args.encoding is not None:
        font.encoding = args.encoding
    if args.compacted:
        font.encoding = "compacted"

    if args.font_name is not None:
        font.fontname = args.font_name
    if args.full_name is not None:
        font.fullname = args.full_name
    if args.weight_name is not None:
        font.weight = args.weight_name
    if args.family_name is not None:
        font.familyname = args.family_name
    if args.panose is not None:
        font.os2_panose = tuple(args.panose)

    if args.copyright is not None:
        font.copyright = args.copyright
    if args.comment is not None:
        font.comment = args.comment
    if args.version is not None:
        font.version = args.version
    if args.sfnt_revision is not None:
        font.sfntRevision = args.sfnt_revision
    if args.vendor is not None:
        font.os2_vendor = args.vendor

    if args.em is not None:
        font.em = args.em
    if args.ascent is not None:
        font.ascent = args.ascent
    if args.descent is not None:
        font.descent = args.descent
    if args.upos is not None:
        font.upos = args.upos
    if args.uwidth is not None:
        font.uwidth = args.uwidth
    if args.italic_angle is not None:
        font.italicangle = args.italic_angle

    space_glyphname = fontforge.nameFromUnicode(32)
    space_glyph = font.createChar(32, space_glyphname)
    if args.width is not None:
        space_glyph.width = args.width
    else:
        space_glyph.width = round(font.em/3)

    print("em = %d; ascent = %d; descent = %d" % (font.em, font.ascent, font.descent))
    print("macstyle = %d" % font.macstyle)
    print("os2_family_class = %s" % font.os2_family_class)
    print("os2_fstype = %s" % font.os2_fstype)
    print("os2_stylemap = %s" % font.os2_stylemap)
    print("os2_weight = %s" % font.os2_weight)
    print("os2_width = %s" % font.os2_width)
    print("sfnt_names = %s" % repr(font.sfnt_names))
    # print("style_set_names = %s" % repr(font.style_set_names))
    print("upos = %f; uwidth = %f" % (font.upos, font.uwidth))
    print("italicangle = %f" % font.italicangle)
        
    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
main()
