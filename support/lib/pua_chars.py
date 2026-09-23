UPPER_LEFT_ARC           = 100
UPPER_RIGHT_ARC          = 101
LOWER_LEFT_ARC           = 102
LOWER_RIGHT_ARC          = 103
LIGHT_HORIZONTAL               = 110
LIGHT_VERTICAL                 = 111
LIGHT_HORIZONTAL_LEFT          = 120
LIGHT_HORIZONTAL_UP            = 121
LIGHT_HORIZONTAL_RIGHT         = 122
LIGHT_HORIZONTAL_DOWN          = 123
DIAGONAL_SOLIDUS         = 130
DIAGONAL_REVERSE_SOLIDUS = 131
DIAGONAL_NORTHWEST       = 140
DIAGONAL_NORTHEAST       = 141
DIAGONAL_SOUTHWEST       = 142
DIAGONAL_SOUTHEAST       = 143
BLACK_SMALL_CIRCLE       = 150
WHITE_SMALL_CIRCLE       = 151
BLACK_CIRCLE             = 160
WHITE_CIRCLE             = 161
BLACK_LARGE_CIRCLE       = 170
WHITE_LARGE_CIRCLE       = 171
X_FOR_LARGE_CIRCLE       = 180
X_FOR_MEDIUM_CIRCLE      = 181
DOT_FOR_LARGE_CIRCLE     = 182
DOT_FOR_MEDIUM_CIRCLE    = 183

STROKE_WIDTH = 96

# inner radius = this radius - stroke_width
PROPORTIONAL_RADIUS = 3/4

# outer = one of these values * min(width,height)/2
# inner = outer - stroke_width
LARGE_CIRCLE_RADIUS = 7/8
MEDIUM_CIRCLE_RADIUS = 5/8
SMALL_CIRCLE_RADIUS = 3/8

def draw_pua_chars(font, codepoint, pieces, glyph_width=1008, stroke_width=96):

    dimen = min(glyph.width / 2, glyph.height / 2)

    glyph = font.createChar(codepoint)
    glyph.width = glyph_width
    arc_radius = dimen * PROPORTIONAL_RADIUS
    arc_radius_inner = arc_radius - STROKE_WIDTH

    large_circle_radius        = LARGE_CIRCLE_RADIUS * dimen
    large_circle_radius_inner  = LARGE_CIRCLE_RADIUS * dimen - STROKE_WIDTH
    medium_circle_radius       = MEDIUM_CIRCLE_RADIUS * dimen
    medium_circle_radius_inner = MEDIUM_CIRCLE_RADIUS * dimen - STROKE_WIDTH
    small_circle_radius        = SMALL_CIRCLE_RADIUS * dimen
    small_circle_radius_inner  = SMALL_CIRCLE_RADIUS * dimen - STROKE_WIDTH

    x_C = glyph_width / 2
    y_C = (font.ascent - font.descent) / 2
    y_C_T = center_y + STROKE_WIDTH / 2
    y_C_B = center_y - STROKE_WIDTH / 2
    x_C_L = center_x - STROKE_WIDTH / 2
    x_C_R = center_x + STROKE_WIDTH / 2
    x_L = 0
    x_R = glyph.width
    y_T = font.ascent
    y_B = -font.descent

    if pieces.includes(UPPER_LEFT_ARC):
        pass

    if pieces.includes(UPPER_RIGHT_ARC):
        pass

    if pieces.includes(LOWER_LEFT_ARC):
        pass

    if pieces.includes(LOWER_RIGHT_ARC):
        pass

    if pieces.includes(LIGHT_HORIZONTAL):
        pass

    if pieces.includes(LIGHT_VERTICAL):
        pass

    if pieces.includes(LIGHT_HORIZONTAL_LEFT):
        pass

    if pieces.includes(LIGHT_HORIZONTAL_UP):
        pass

    if pieces.includes(LIGHT_HORIZONTAL_RIGHT):
        pass

    if pieces.includes(LIGHT_HORIZONTAL_DOWN):
        pass

    if pieces.includes(DIAGONAL_SOLIDUS):
        pass

    if pieces.includes(DIAGONAL_REVERSE_SOLIDUS):
        pass

    if pieces.includes(DIAGONAL_NORTHWEST):
        pass

    if pieces.includes(DIAGONAL_NORTHEAST):
        pass

    if pieces.includes(DIAGONAL_SOUTHWEST):
        pass

    if pieces.includes(DIAGONAL_SOUTHEAST):
        pass

    if pieces.includes(BLACK_SMALL_CIRCLE):
        pass

    if pieces.includes(WHITE_SMALL_CIRCLE):
        pass

    if pieces.includes(BLACK_CIRCLE):
        pass

    if pieces.includes(WHITE_CIRCLE):
        pass

    if pieces.includes(BLACK_LARGE_CIRCLE):
        pass

    if pieces.includes(WHITE_LARGE_CIRCLE):
        pass

    if pieces.includes(X_FOR_LARGE_CIRCLE):
        pass

    if pieces.includes(X_FOR_MEDIUM_CIRCLE):
        pass

    if pieces.includes(DOT_FOR_LARGE_CIRCLE):
        pass

    if pieces.includes(DOT_FOR_MEDIUM_CIRCLE):
        pass
