#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, math

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

from otm.util import draw_rel_poly, get_font_glyph_width

RANGES = [
    range(0x1fb3c, 0x1fb70),
    range(0x1fb9a, 0x1fb9f),
]

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-c", "--clear", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)

    if args.clear:
        for r in RANGES:
            for code in r:
                try:
                    font.removeGlyph(code)
                except ValueError as e:
                    if str(e) != "This glyph is not in the font":
                        raise
        return
                
    new_glyph_width = get_font_glyph_width(font)

    for r in RANGES:
        for code in r:
            glyph = font.createChar(code)
            glyph.foreground = fontforge.layer()
            glyph.width = new_glyph_width

    draw_1FB3C(font.createChar(0x1FB3C))
    draw_1FB3D(font.createChar(0x1FB3D))
    draw_1FB3E(font.createChar(0x1FB3E))
    draw_1FB3F(font.createChar(0x1FB3F))
    draw_1FB40(font.createChar(0x1FB40))
    draw_1FB41(font.createChar(0x1FB41))
    draw_1FB42(font.createChar(0x1FB42))
    draw_1FB43(font.createChar(0x1FB43))
    draw_1FB44(font.createChar(0x1FB44))
    draw_1FB45(font.createChar(0x1FB45))
    draw_1FB46(font.createChar(0x1FB46))
    draw_1FB47(font.createChar(0x1FB47))
    draw_1FB48(font.createChar(0x1FB48))
    draw_1FB49(font.createChar(0x1FB49))
    draw_1FB4A(font.createChar(0x1FB4A))
    draw_1FB4B(font.createChar(0x1FB4B))
    draw_1FB4C(font.createChar(0x1FB4C))
    draw_1FB4D(font.createChar(0x1FB4D))
    draw_1FB4E(font.createChar(0x1FB4E))
    draw_1FB4F(font.createChar(0x1FB4F))
    draw_1FB50(font.createChar(0x1FB50))
    draw_1FB51(font.createChar(0x1FB51))
    draw_1FB52(font.createChar(0x1FB52))
    draw_1FB53(font.createChar(0x1FB53))
    draw_1FB54(font.createChar(0x1FB54))
    draw_1FB55(font.createChar(0x1FB55))
    draw_1FB56(font.createChar(0x1FB56))
    draw_1FB57(font.createChar(0x1FB57))
    draw_1FB58(font.createChar(0x1FB58))
    draw_1FB59(font.createChar(0x1FB59))
    draw_1FB5A(font.createChar(0x1FB5A))
    draw_1FB5B(font.createChar(0x1FB5B))
    draw_1FB5C(font.createChar(0x1FB5C))
    draw_1FB5D(font.createChar(0x1FB5D))
    draw_1FB5E(font.createChar(0x1FB5E))
    draw_1FB5F(font.createChar(0x1FB5F))
    draw_1FB60(font.createChar(0x1FB60))
    draw_1FB61(font.createChar(0x1FB61))
    draw_1FB62(font.createChar(0x1FB62))
    draw_1FB63(font.createChar(0x1FB63))
    draw_1FB64(font.createChar(0x1FB64))
    draw_1FB65(font.createChar(0x1FB65))
    draw_1FB66(font.createChar(0x1FB66))
    draw_1FB67(font.createChar(0x1FB67))
    draw_1FB68(font.createChar(0x1FB68))
    draw_1FB69(font.createChar(0x1FB69))
    draw_1FB6A(font.createChar(0x1FB6A))
    draw_1FB6B(font.createChar(0x1FB6B))
    draw_1FB6C(font.createChar(0x1FB6C))
    draw_1FB6D(font.createChar(0x1FB6D))
    draw_1FB6E(font.createChar(0x1FB6E))
    draw_1FB6F(font.createChar(0x1FB6F))

    draw_1FB9A(font.createChar(0x1FB9A))
    draw_1FB9B(font.createChar(0x1FB9B))
    draw_1FB9C(font.createChar(0x1FB9C))
    draw_1FB9D(font.createChar(0x1FB9D))
    draw_1FB9E(font.createChar(0x1FB9E))
    draw_1FB9F(font.createChar(0x1FB9F))

    for r in RANGES:
        for code in r:
            glyph = font.createChar(code)
            glyph.removeOverlap()
            glyph.simplify()

    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')

    font.close()

A = (0   ,0   )                 # J K L
B = (1/2 ,0   )                 # G H I
C = (1   ,0   )                 # D E F
D = (0   ,1/3 )                 # A B C
E = (1/2 ,1/3 )
F = (1   ,1/3 )
G = (0   ,2/3 )
H = (1/2 ,2/3 )
I = (1   ,2/3 )
J = (0   ,1   )
K = (1/2 ,1   )
L = (1   ,1   )

def draw_1FB3C(glyph): draw_rel_poly(glyph, [A, D, B])
def draw_1FB3D(glyph): draw_rel_poly(glyph, [A, D, C])
def draw_1FB3E(glyph): draw_rel_poly(glyph, [A, G, B])
def draw_1FB3F(glyph): draw_rel_poly(glyph, [A, G, C])
def draw_1FB40(glyph): draw_rel_poly(glyph, [A, J, C])
def draw_1FB41(glyph): draw_rel_poly(glyph, [A, G, K, L, C])
def draw_1FB42(glyph): draw_rel_poly(glyph, [A, G, L, C])
def draw_1FB43(glyph): draw_rel_poly(glyph, [A, D, K, L, C])
def draw_1FB44(glyph): draw_rel_poly(glyph, [A, D, L, C])
def draw_1FB45(glyph): draw_rel_poly(glyph, [A, K, L, C])
def draw_1FB46(glyph): draw_rel_poly(glyph, [A, D, I, C])
def draw_1FB47(glyph): draw_rel_poly(glyph, [B, F, C])
def draw_1FB48(glyph): draw_rel_poly(glyph, [A, F, C])
def draw_1FB49(glyph): draw_rel_poly(glyph, [B, I, C])
def draw_1FB4A(glyph): draw_rel_poly(glyph, [A, I, C])
def draw_1FB4B(glyph): draw_rel_poly(glyph, [B, L, C])
def draw_1FB4C(glyph): draw_rel_poly(glyph, [A, J, K, I, C])
def draw_1FB4D(glyph): draw_rel_poly(glyph, [A, J, I, C])
def draw_1FB4E(glyph): draw_rel_poly(glyph, [A, J, K, F, C])
def draw_1FB4F(glyph): draw_rel_poly(glyph, [A, J, F, C])
def draw_1FB50(glyph): draw_rel_poly(glyph, [A, J, K, C])
def draw_1FB51(glyph): draw_rel_poly(glyph, [A, G, F, C])
def draw_1FB52(glyph): draw_rel_poly(glyph, [D, J, L, C, B])
def draw_1FB53(glyph): draw_rel_poly(glyph, [D, J, L, C])
def draw_1FB54(glyph): draw_rel_poly(glyph, [B, G, J, L, C])
def draw_1FB55(glyph): draw_rel_poly(glyph, [G, J, L, C])
def draw_1FB56(glyph): draw_rel_poly(glyph, [B, J, L, C])

def draw_1FB57(glyph): draw_rel_poly(glyph, [G, J, K], debug=True) # ???
def draw_1FB58(glyph): draw_rel_poly(glyph, [G, J, L], debug=True) # ???
def draw_1FB59(glyph): draw_rel_poly(glyph, [D, J, K])
def draw_1FB5A(glyph): draw_rel_poly(glyph, [D, J, L])
def draw_1FB5B(glyph): draw_rel_poly(glyph, [A, J, K])
def draw_1FB5C(glyph): draw_rel_poly(glyph, [D, J, L, I])
def draw_1FB5D(glyph): draw_rel_poly(glyph, [A, J, L, F, B])
def draw_1FB5E(glyph): draw_rel_poly(glyph, [A, J, L, F])
def draw_1FB5F(glyph): draw_rel_poly(glyph, [A, J, L, I, B])
def draw_1FB60(glyph): draw_rel_poly(glyph, [A, J, L, I])
def draw_1FB61(glyph): draw_rel_poly(glyph, [A, J, L, B])
def draw_1FB62(glyph): draw_rel_poly(glyph, [K, L, I], debug=True) # ???
def draw_1FB63(glyph): draw_rel_poly(glyph, [J, L, I], debug=True) # ???
def draw_1FB64(glyph): draw_rel_poly(glyph, [K, L, F])
def draw_1FB65(glyph): draw_rel_poly(glyph, [J, L, F])
def draw_1FB66(glyph): draw_rel_poly(glyph, [K, L, C])
def draw_1FB67(glyph): draw_rel_poly(glyph, [G, J, L, F])

M = (0   ,0   )                 # S T U
N = (1/2 ,0   )                 # P Q R
O = (1   ,0   )                 # M N O
P = (0   ,1/2 )
Q = (1/2 ,1/2 )
R = (1   ,1/2 )
S = (0   ,1   )
T = (1/2 ,1   )
U = (1   ,1   )

def draw_1FB68(glyph): draw_rel_poly(glyph, [M, Q, S, U, O])
def draw_1FB69(glyph): draw_rel_poly(glyph, [M, S, Q, U, O])
def draw_1FB6A(glyph): draw_rel_poly(glyph, [M, S, U, Q, O])
def draw_1FB6B(glyph): draw_rel_poly(glyph, [M, S, U, O, Q])
def draw_1FB6C(glyph): draw_rel_poly(glyph, [Q, M, S])
def draw_1FB6D(glyph): draw_rel_poly(glyph, [Q, S, U])
def draw_1FB6E(glyph): draw_rel_poly(glyph, [Q, U, O])
def draw_1FB6F(glyph): draw_rel_poly(glyph, [Q, O, M])

def draw_1FB9A(glyph):
    draw_rel_poly(glyph, [A, E, C])
    draw_rel_poly(glyph, [E, G, I])
def draw_1FB9B(glyph):
    draw_rel_poly(glyph, [A, G, E])
    draw_rel_poly(glyph, [E, I, G])
def draw_1FB9C(glyph):
def draw_1FB9D(glyph):
def draw_1FB9E(glyph):
def draw_1FB9F(glyph):

def draw_block_sextant(glyph):
    code = glyph.unicode
    if code < 0:
        glyph = fontforge.unicodeFromName(glyph.glyphname.split(".", 1)[0])
    if code < 0:
        return
    parts = unicodedata.name(chr(code)).removeprefix("BLOCK SEXTANT-")
    for part in parts:
        if   part == "1": draw_rel_rect(glyph, 0, 2/3, 1/2, 1)
        elif part == "2": draw_rel_rect(glyph, 1/2, 2/3, 1, 1)
        elif part == "3": draw_rel_rect(glyph, 0, 1/3, 1/2, 2/3)
        elif part == "4": draw_rel_rect(glyph, 1/2, 1/3, 1, 2/3)
        elif part == "5": draw_rel_rect(glyph, 0, 0, 1/2, 1/3)
        elif part == "6": draw_rel_rect(glyph, 1/2, 0, 1, 1/3)

def draw_upper_left_sextant(glyph):   draw_rel_rect(glyph, 0, 2/3, 0.5, 1)
def draw_upper_right_sextant(glyph):  draw_rel_rect(glyph, 0.5, 2/3, 1, 1)
pdef draw_middle_left_sextant(glyph):  draw_rel_rect(glyph, 0, 1/3, 0.5, 2/3)
def draw_middle_right_sextant(glyph): draw_rel_rect(glyph, 0.5, 1/3, 1, 2/3)
def draw_lower_left_sextant(glyph):   draw_rel_rect(glyph, 0, 0, 0.5, 1/3)
def draw_lower_right_sextant(glyph):  draw_rel_rect(glyph, 0.5, 0, 1, 1/3)
def draw_upper_third(glyph):          draw_rel_rect(glyph, 0, 2/3, 1, 1)
def draw_middle_third(glyph):         draw_rel_rect(glyph, 0, 1/3, 1, 2/3)
def draw_lower_third(glyph):          draw_rel_rect(glyph, 0, 0, 1, 1/3)

main()

