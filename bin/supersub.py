#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, psMat, argparse, unicodedata, os

xlate_superscript = psMat.translate(0, 636)
xlate_subscript   = psMat.translate(0, -156)
xlate_numerator   = psMat.translate(0, 561)
xlate_fraction    = psMat.translate(0, 75)
xlate_denominator = psMat.translate(0, -231)

sys.path.append(os.path.dirname(__file__) + "/../lib")
from my_font_chars import UNICODE

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    print("supersub.py %s: Opening and reading..." % args.filename)
    font = fontforge.open(args.filename)
    supersubscript(font, 0x00b2, 2, xlate_superscript)
    supersubscript(font, 0x00b3, 3, xlate_superscript)
    supersubscript(font, 0x00b9, 1, xlate_superscript)
    supersubscript(font, 0x2070, 0, xlate_superscript) #    SUPERSCRIPT ZERO
    supersubscript(font, 0x2074, 4, xlate_superscript) #    SUPERSCRIPT FOUR
    supersubscript(font, 0x2075, 5, xlate_superscript) #    SUPERSCRIPT FIVE
    supersubscript(font, 0x2076, 6, xlate_superscript) #    SUPERSCRIPT SIX
    supersubscript(font, 0x2077, 7, xlate_superscript) #    SUPERSCRIPT SEVEN
    supersubscript(font, 0x2078, 8, xlate_superscript) #    SUPERSCRIPT EIGHT
    supersubscript(font, 0x2079, 9, xlate_superscript) #    SUPERSCRIPT NINE
    supersubscript(font, 0x207B, '-', xlate_superscript) #    SUPERSCRIPT MINUS
    supersubscript(font, 0x207A, '+', xlate_superscript) #    SUPERSCRIPT PLUS SIGN
    supersubscript(font, 0x207C, '=', xlate_superscript) #    SUPERSCRIPT EQUALS SIGN
    supersubscript(font, 0x207D, '(', xlate_superscript) #    SUPERSCRIPT OPENING PARENTHESIS
    supersubscript(font, 0x207E, ')', xlate_superscript) #    SUPERSCRIPT CLOSING PARENTHESIS
    supersubscript(font, 0x2071, 'i', xlate_superscript) #    SUPERSCRIPT LATIN SMALL LETTER I
    supersubscript(font, 0x207F, 'n', xlate_superscript) #    SUPERSCRIPT LATIN SMALL LETTER N
    supersubscript(font, 0x2080, 0, xlate_subscript) #    SUBSCRIPT ZERO
    supersubscript(font, 0x2081, 1, xlate_subscript) #    SUBSCRIPT ONE
    supersubscript(font, 0x2082, 2, xlate_subscript) #    SUBSCRIPT TWO
    supersubscript(font, 0x2083, 3, xlate_subscript) #    SUBSCRIPT THREE
    supersubscript(font, 0x2084, 4, xlate_subscript) #    SUBSCRIPT FOUR
    supersubscript(font, 0x2085, 5, xlate_subscript) #    SUBSCRIPT FIVE
    supersubscript(font, 0x2086, 6, xlate_subscript) #    SUBSCRIPT SIX
    supersubscript(font, 0x2087, 7, xlate_subscript) #    SUBSCRIPT SEVEN
    supersubscript(font, 0x2088, 8, xlate_subscript) #    SUBSCRIPT EIGHT
    supersubscript(font, 0x2089, 9, xlate_subscript) #    SUBSCRIPT NINE
    supersubscript(font, 0x208B, '-', xlate_subscript) #    SUBSCRIPT MINUS
    supersubscript(font, 0x208A, '+', xlate_subscript) #    SUBSCRIPT PLUS SIGN
    supersubscript(font, 0x208C, '=', xlate_subscript) #    SUBSCRIPT EQUALS SIGN
    supersubscript(font, 0x208D, '(', xlate_subscript) #    SUBSCRIPT LEFT PARENTHESIS
    supersubscript(font, 0x208E, ')', xlate_subscript) #    SUBSCRIPT RIGHT PARENTHESIS

    supersubscript(font, 0x2090, 'a', xlate_subscript)
    supersubscript(font, 0x2091, 'e', xlate_subscript)
    supersubscript(font, 0x2092, 'o', xlate_subscript)
    supersubscript(font, 0x2093, 'x', xlate_subscript)
    supersubscript(font, 0x2095, 'h', xlate_subscript)
    supersubscript(font, 0x2096, 'k', xlate_subscript)
    supersubscript(font, 0x2097, 'l', xlate_subscript)
    supersubscript(font, 0x2098, 'm', xlate_subscript)
    supersubscript(font, 0x2099, 'n', xlate_subscript)
    supersubscript(font, 0x209a, 'p', xlate_subscript)
    supersubscript(font, 0x209b, 's', xlate_subscript)
    supersubscript(font, 0x209c, 't', xlate_subscript)
    supersubscript(font, 0x1D62, 'i', xlate_subscript)
    supersubscript(font, 0x1D63, 'r', xlate_subscript)
    supersubscript(font, 0x1D64, 'u', xlate_subscript)
    supersubscript(font, 0x1D65, 'v', xlate_subscript)
    supersubscript(font, 0x2090, 'a', xlate_subscript)
    supersubscript(font, 0x2091, 'e', xlate_subscript)
    supersubscript(font, 0x2092, 'o', xlate_subscript)
    supersubscript(font, 0x2093, 'x', xlate_subscript)
    supersubscript(font, 0x2C7C, 'j', xlate_subscript)
    supersubscript(font, 0x2094, chr(UNICODE["LATIN_SMALL_LETTER_SCHWA"]), xlate_subscript)
    supersubscript(font, 0x1d66, chr(0x03b2), xlate_subscript) # l/c beta
    supersubscript(font, 0x1d67, chr(0x03b3), xlate_subscript) # l/c gamma
    supersubscript(font, 0x1d68, chr(0x03c1), xlate_subscript) # l/c rho
    supersubscript(font, 0x1d69, chr(0x03c6), xlate_subscript) # l/c phi
    supersubscript(font, 0x1d6a, chr(0x03c7), xlate_subscript) # l/c chi

    fraction(font, 0x00bc, 1, 4)
    fraction(font, 0x00bd, 1, 2)
    fraction(font, 0x00be, 3, 4)
    fraction(font, 0x2150, 1, 7) #    VULGAR FRACTION ONE SEVENTH
    fraction(font, 0x2151, 1, 9) #    VULGAR FRACTION ONE NINTH
    fraction(font, 0x2152, 1, 10) #    VULGAR FRACTION ONE TENTH
    fraction(font, 0x2153, 1, 3) #    VULGAR FRACTION ONE THIRD
    fraction(font, 0x2154, 2, 3) #    VULGAR FRACTION TWO THIRDS
    fraction(font, 0x2155, 1, 5) #    VULGAR FRACTION ONE FIFTH
    fraction(font, 0x2156, 2, 5) #    VULGAR FRACTION TWO FIFTHS
    fraction(font, 0x2157, 3, 5) #    VULGAR FRACTION THREE FIFTHS
    fraction(font, 0x2158, 4, 5) #    VULGAR FRACTION FOUR FIFTHS
    fraction(font, 0x2159, 1, 6) #    VULGAR FRACTION ONE SIXTH
    fraction(font, 0x215A, 5, 6) #    VULGAR FRACTION FIVE SIXTHS
    fraction(font, 0x215B, 1, 8) #    VULGAR FRACTION ONE EIGHTH
    fraction(font, 0x215C, 3, 8) #    VULGAR FRACTION THREE EIGHTHS
    fraction(font, 0x215D, 5, 8) #    VULGAR FRACTION FIVE EIGHTHS
    fraction(font, 0x215E, 7, 8) #    VULGAR FRACTION SEVEN EIGHTHS
    fraction(font, 0x215f, 1, '')
    fraction(font, 0x2189, 0, 3)
    if args.filename.endswith(".sfd"):
        print("supersub.py %s: Saving..." % args.filename)
        font.save(args.filename)
    else:
        print("supersub.py %s: Generating..." % args.filename)
        font.generate(args.filename)
    font.close()

def digit_xlate(idx, length):
    return psMat.translate(-252 * (length - 1) + 504 * idx, 0)

def supersubscript(font, codepoint, num, xlate):
    font_path = os.path.relpath(font.path)
    print("supersubscript %s: creating U+%04X" % (font_path, codepoint))
    glyph = font.createChar(codepoint)
    glyph.width = 1008
    glyph.foreground = fontforge.layer()
    references = []
    if type(num) == int:
        num = str(num)
    for idx in range(0, len(num)):
        char = num[idx]
        print("supersubscript %s: char[%d] = '%s'" % (font_path, idx, char))
        glyphname = fontforge.nameFromUnicode(ord(char)) + '.smol'
        print("supersubscript %s: inserting %s" % (font_path, glyphname))
        if len(num) > 1:
            xlate = psMat.compose(xlate, digit_xlate(idx, len(num)))
        references.append((glyphname, xlate))
    glyph.references = tuple(references)
    (xmin, ymin, xmax, ymax) = glyph.boundingBox()
    print("supersubscript %s: %s %s: %f, %f, %f, %f" %
          (font_path, glyph.glyphname, unicodedata.name(chr(codepoint)),
           xmin, ymin, xmax, ymax))

def fraction(font, codepoint, numer, denom):
    font_path = os.path.relpath(font.path)
    glyph = font.createChar(codepoint)
    glyph.width = 1008
    glyph.foreground = fontforge.layer()
    references = []
    if type(numer) == int:
        numer = str(numer)
    references.append(('x_nutfractionbar', xlate_fraction))
    if type(numer) == int:
        numer = str(numer)
    if type(denom) == int:
        denom = str(denom)
    for idx in range(0, len(numer)):
        char = numer[idx]
        xlate = xlate_numerator
        if len(numer) > 1:
            xlate = psMat.compose(xlate, digit_xlate(idx, len(numer)))
        glyphname = fontforge.nameFromUnicode(ord(char)) + '.smol'
        references.append((glyphname, xlate))
    for idx in range(0, len(denom)):
        char = denom[idx]
        xlate = xlate_denominator
        if len(denom) > 1:
            xlate = psMat.compose(xlate, digit_xlate(idx, len(denom)))
        glyphname = fontforge.nameFromUnicode(ord(char)) + '.smol'
        references.append((glyphname, xlate))
    print("supersub.py %s: U+%04X" % (font_path, codepoint))
    print(repr(references))
    glyph.references = tuple(references)

main()
