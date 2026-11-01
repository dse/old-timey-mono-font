import unicodedata

__all__ = [
    "U2500_BOX_DRAWING",
    "U2580_BLOCK_ELEMENTS",
    "U2800_BRAILLE",
    "U1FB00_SEGMENTED_DIGITS",
    "U1FB3C_MOSAICS",
    "U1FB70_ONE_EIGHTH_BLOCKS",
    "U1FB8C_RECTANGULAR_SHADES",
    "U1FB95_CHECKERBOARD_FILL",
    "U1FB96_INVERSE_CHECKERBOARD_FILL",
    "U1FB9A_TRIANGULAR_HALF_BLOCKS",
    "U1FBCE_THIRD_BLOCKS",
    "U1FBE4_CENTER_QUADRANTS",
    "U1FBF0_BLOCK_SEXTANTS",
    "UFAF00_PUA_EXTRAS",
    "GENERATED_GLYPH_CODES",
    "SMOL_GLYPH_CODES",
    "GENERATED_SPACE_CODES",
    "NON_GRAPHIC_CODES",
]

U2500_BOX_DRAWING             = range(0x2500, 0x2580) # draw-box-drawing.py
U2580_BLOCK_ELEMENTS          = range(0x2580, 0x25a0) # draw-block-elements.py
U2800_BRAILLE                 = range(0x2800, 0x2900) # draw-braille.py
U1FB00_BLOCK_SEXTANTS         = range(0x1fb00, 0x1fb3c) # draw-block-sextants.py
U1FB3C_MOSAICS                = range(0x1fb3c, 0x1fb70) # draw-mosaics.py
U1FB70_ONE_EIGHTH_BLOCKS      = range(0x1fb70, 0x1fb8c) # draw-block-elements.py
U1FB8C_RECTANGULAR_SHADES     = range(0x1fb8c, 0x1fb95) # draw-block-elements.py
U1FB95_CHECKERBOARD_FILL      = range(0x1fb95, 0x1fb96) # draw-block-elements.py
U1FB9A_TRIANGULAR_HALF_BLOCKS = range(0x1fb9a, 0x1fb9c) # draw-mosaics.py
U1FBCE_THIRD_BLOCKS           = range(0x1fbce, 0x1fbd0) # draw-block-elements.py
U1FBE4_CENTER_QUADRANTS       = range(0x1fbe4, 0x1fbe8) # draw-block-elements.py
U1FBF0_SEGMENTED_DIGITS       = range(0x1fbf0, 0x1fbfa) # draw-segmented-digits.py
UFAF00_PUA_EXTRAS             = range(0xfaf00, 0xfaf70)

GENERATED_GLYPH_CODES = [
    *(
        list(U2500_BOX_DRAWING) +
        list(U2580_BLOCK_ELEMENTS) +
        list(U2800_BRAILLE) +
        list(U1FB00_BLOCK_SEXTANTS) +
        list(U1FB3C_MOSAICS) +
        list(U1FB70_ONE_EIGHTH_BLOCKS) +
        list(U1FB8C_RECTANGULAR_SHADES) +
        list(U1FB95_CHECKERBOARD_FILL) +
        list(U1FB9A_TRIANGULAR_HALF_BLOCKS) +
        list(U1FBCE_THIRD_BLOCKS) +
        list(U1FBE4_CENTER_QUADRANTS) +
        list(U1FBF0_SEGMENTED_DIGITS) +
        list(UFAF00_PUA_EXTRAS) +
        []
    )
]

SMOL_GLYPH_CODES = [
    *range(32, 127),
    ord(unicodedata.lookup("LATIN SMALL LETTER SCHWA")),
    ord(unicodedata.lookup("GREEK SMALL LETTER BETA")),
    ord(unicodedata.lookup("GREEK SMALL LETTER GAMMA")),
    ord(unicodedata.lookup("GREEK SMALL LETTER RHO")),
    ord(unicodedata.lookup("GREEK SMALL LETTER PHI")),
    ord(unicodedata.lookup("GREEK SMALL LETTER CHI")),
]

# ones we populate
GENERATED_SPACE_CODES = [
    0x0020,                       # SPACE
    0x00a0,                       # NO-BREAK SPACE
    0x2000,                       # EN QUAD
    0x2001,                       # EM QUAD
    0x2002,                       # EN SPACE
    0x2003,                       # EM SPACE
    0x2007,                       # FIGURE SPACE
    0x2008,                       # PUNCTUATION SPACE
    0x205f,                       # MEDIUM MATHEMATICAL SPACE
    0x3000,                       # IDEOGRAPHIC SPACE
]

NON_GRAPHIC_CODES = [
    *GENERATED_SPACE_CODES,
    *list(range(0x0000, 0x0020)), # C0 controls
    0x007f,                       # "
    *list(range(0x0080, 0x00a0)), # C1 controls
    0x2004,                       # THREE-PER-EM SPACE
    0x2005,                       # FOUR-PER-EM SPACE
    0x2006,                       # SIX-PER-EM SPACE
    0x2009,                       # THIN SPACE
    0x200a,                       # HAIR SPACE
    0x200b,                       # ZERO WIDTH SPACE
    0x200c,                       # ZERO WIDTH NON-JOINER
    0x200d,                       # ZERO WIDTH JOINER
    0x200e,                       # LEFT-TO-RIGHT MARK
    0x200f,                       # RIGHT-TO-LEFT MARK
    0x2028,                       # LINE SEPARATOR
    0x2029,                       # PARAGRAPH SEPARATOR
    0x202f,                       # NARROW NO-BREAK SPACE
    0x1680,                       # OGHAM SPACE MARK
    0xfeff,              # ZERO WIDTH NO-BREAK SPACE (BYTE ORDER MARK)
]

# the first three glyphs in the font IN ORDER
SPECIAL_GLYPH_NAMES = [
    ".notdef",
    ".null",
    "nonmarkingreturn"
]

SPECIAL_GLYPH_CODES = {
    ".notdef": 0,
    ".null": 0,
    "nonmarkingreturn": 0x000d,
}
