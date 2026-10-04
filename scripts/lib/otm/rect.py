import fontforge
from otm.point import rel_to_abs_point
from otm.clamp import clamp

def rect_contour(glyph, x1, y1, x2, y2, withershins=False):
    contour = fontforge.contour()
    contour.closed = True
    if withershins:
        contour.moveTo(x1, y1)
        contour.lineTo(x2, y1)
        contour.lineTo(x2, y2)
        contour.lineTo(x1, y2)
    else:
        contour.moveTo(x1, y1)
        contour.lineTo(x1, y2)
        contour.lineTo(x2, y2)
        contour.lineTo(x2, y1)
    return contour

def rel_rect_contour(glyph, x1, y1, x2, y2, withershins=False):
    (x1, x2, y1, y2) = [clamp(a) for a in (x1, x2, y1, y2)]
    (x1, y1) = rel_to_abs_point(glyph, (x1, y1))
    (x2, y2) = rel_to_abs_point(glyph, (x2, y2))
    return rect_contour(glyph, x1, y1, x2, y2, withershins=withershins)
    
