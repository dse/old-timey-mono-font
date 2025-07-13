#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os, sys, unicodedata, re
from functools import cmp_to_key
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--hex', '--hexadecimal', action='store_true')
    parser.add_argument('--unicode-hex', action='store_true')
    parser.add_argument('--no-sort', action='store_true')
    parser.add_argument('--cv-only', action='store_true')
    args = parser.parse_args()
    for filename in args.filenames:
        silence()
        font = fontforge.open(filename)
        silence_off()
        glyphs = list(font.glyphs())
        if args.cv_only:
            glyphs = [glyph for glyph in glyphs if bool(re.search(r'\.cv[0-9][0-9]$', glyph.glyphname))]
        for glyph in glyphs:
            glyph.temporary = {}
            codepoint = glyph.unicode if glyph.unicode >= 0 else fontforge.unicodeFromName(glyph.glyphname.split('.')[0])
            char = '' if codepoint < 0 else chr(codepoint)
            glyph.temporary["name"] = '-' if codepoint < 0 else unicodedata.name(char, '-')
            glyph.temporary["codepoint"] = codepoint
        glyphname_maxlen = max([len(glyph.glyphname) for glyph in glyphs])
        if not args.no_sort:
            glyphs.sort(key=cmp_to_key(glyph_sort))
        for glyph in glyphs:
            if args.unicode_hex:
                print("  %-8s  %-8s  %-*s  %s" % (
                    "U+%04X" % glyph.unicode if glyph.unicode >= 0 else "(None)",
                    "U+%04X" % glyph.temporary["codepoint"] if glyph.temporary["codepoint"] >= 0 else "(None)",
                    glyphname_maxlen,
                    glyph.glyphname,
                    glyph.temporary["name"]
                ))
            elif args.hex:
                print("  %-8s  %-8s  %-*s  %s" % (
                    "0x%04x" % glyph.unicode if glyph.unicode >= 0 else "(None)",
                    "0x%04x" % glyph.temporary["codepoint"] if glyph.temporary["codepoint"] >= 0 else "(None)",
                    glyphname_maxlen,
                    glyph.glyphname,
                    glyph.temporary["name"]
                ))
            else:
                print("  %7d  %7d  %-*s  %s" % (
                    glyph.unicode,
                    glyph.temporary["codepoint"], 
                    glyphname_maxlen,
                    glyph.glyphname,
                    glyph.temporary["name"]
                ))
        font.close()
stderr_fd = os.dup(2)
def silence():
    if "DISABLE_SILENCE" in os.environ:
        return
    os.close(2)
def silence_off():
    if "DISABLE_SILENCE" in os.environ:
        return
    os.dup2(stderr_fd, 2)
def glyph_sort(glyph_a, glyph_b):
    a = glyph_a.unicode
    b = glyph_b.unicode
    if a < 0 and b < 0:
        a = fontforge.unicodeFromName(glyph_a.glyphname.split('.')[0])
        b = fontforge.unicodeFromName(glyph_b.glyphname.split('.')[0])
    if a < 0 and b < 0:
        return a - b
    if a < 0:
        return 1
    if b < 0:
        return -1
    return a - b
main()
