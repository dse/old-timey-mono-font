import fontforge, psMat
from otm.point import rel_to_abs_point
from otm.constants import KAPPA
from math import pi
import re

NORTHEAST = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)   # identity
NORTHWEST = (0.0, 1.0, -1.0, 0.0, 0.0, 0.0)  # rotate pi/2
SOUTHWEST = (-1.0, 0.0, 0.0, -1.0, 0.0, 0.0) # rotate pi
SOUTHEAST = (0.0, -1.0, 1.0, 0.0, 0.0, 0.0)  # rotate 3pi/2

UP_AND_LEFT = SOUTHEAST
UP_AND_RIGHT = SOUTHWEST
DOWN_AND_LEFT = NORTHEAST
DOWN_AND_RIGHT = NORTHWEST

DIRECTION_ALIASES = {
    "northwest": NORTHWEST,
    "northeast": NORTHEAST,
    "southwest": SOUTHWEST,
    "southeast": SOUTHEAST,
    "nw": NORTHWEST,
    "ne": NORTHEAST,
    "sw": SOUTHWEST,
    "se": SOUTHEAST,
    "up and left": UP_AND_LEFT,
    "up and right": UP_AND_RIGHT,
    "down and left": DOWN_AND_LEFT,
    "down and right": DOWN_AND_RIGHT,
    "up left": UP_AND_LEFT,
    "up right": UP_AND_RIGHT,
    "down left": DOWN_AND_LEFT,
    "down right": DOWN_AND_RIGHT,
    "left and up": UP_AND_LEFT,
    "right and up": UP_AND_RIGHT,
    "left and down": DOWN_AND_LEFT,
    "right and down": DOWN_AND_RIGHT,
    "left up": UP_AND_LEFT,
    "right up": UP_AND_RIGHT,
    "left down": DOWN_AND_LEFT,
    "right down": DOWN_AND_RIGHT,
}

def normalize_direction(direction, default=Exception):
    if type(direction) is str:
        direction = direction.lower()
        direction = re.sub(r'[\x27]+', '', direction)
        direction = re.sub(r'[^\x27A-Za-z0-9]+', ' ', direction)
        direction = direction.strip()
    if direction in DIRECTION_ALIASES:
        direction = direction[DIRECTION_ALIASES]
    if direction not in [NORTHWEST, NORTHEAST, SOUTHEAST, SOUTHWEST]:
        if default is Exception:
            raise Exception("invalid direction")
        else:
            return default
    return direction

def quarter_arc_contour(glyph, center, r_in, r_out, direction, withershins=False):
    direction = normalize_direction(direction)
    return elliptic_quarter_arc_contour(glyph, center, r_in, r_out, r_in, r_out, direction, withershins=withershins)

def elliptic_quarter_arc_contour(glyph, center, r_in_x, r_out_x, r_in_y, r_out_y, direction, withershins=False, kappa_x=1, kappa_y=1):
    direction = normalize_direction(direction)

    # down and left
    p0  = (r_in_x,                    0)
    p1  = (r_in_x,                    r_in_y * KAPPA * kappa_y)
    p2  = (r_in_x * KAPPA * kappa_x,  r_in_y)
    p3  = (0,                         r_in_y)
    p4  = (0,                         r_out_y)
    p5  = (r_out_x * KAPPA * kappa_x, r_out_y)
    p6  = (r_out_x,                   r_out_y * KAPPA * kappa_y)
    p7  = (r_out_x,                   0)
    
    contour = fontforge.contour()
    contour.closed = True

    if withershins:
        contour.moveTo(*p7)
        contour.cubicTo(p6, p5, p4)
        contour.lineTo(*p3)
        contour.cubicTo(p2, p1, p0)
    else:
        contour.moveTo(*p0)
        contour.cubicTo(p1, p2, p3)
        contour.lineTo(*p4)
        contour.cubicTo(p5, p6, p7)

    if direction in [UP_AND_LEFT, UP_AND_RIGHT]:
        contour.transform(psMat.scale(1,-1))
    if direction in [UP_AND_RIGHT, DOWN_AND_RIGHT]:
        contour.transform(psMat.scale(-1,1))
    if direction in [UP_AND_LEFT, DOWN_AND_RIGHT]:
        contour.reverseDirection()
        
    contour.transform((1, 0, 0, 1, *center))
    return contour
