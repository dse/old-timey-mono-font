__all__ = [
    "U2500_BOX_DRAWING",
    "U2580_BLOCK_ELEMENTS",
    "U2800_BRAILLE",
    "U1FB00_SEGMENTED_DIGITS",
    "U1FB3C_MOSAICS",
    "U1FB70_ONE_EIGHTH_BLOCKS",
    "U1FB8C_RECTANGULAR_SHADES",
    "U1FB95_CHECKERBOARD_FILL",
    "U1FB9A_TRIANGULAR_HALF_BLOCKS",
    "U1FBCE_THIRD_BLOCKS",
    "U1FBE4_CENTER_QUADRANTS",
    "U1FBF0_BLOCK_SEXTANTS",
    "UFAF00_PUA_EXTRAS",
    "ALL",
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

ALL = (
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
