import fontforge
from otm.point import rel_to_abs_point
from otm.constants import KAPPA

def circle_contour(glyph, center, r, withershins=False):
    (xc, yc) = center
    pt_1 = (xc - r, yc)
    pt_2 = (xc, yc + r)
    pt_3 = (xc + r, yc)
    pt_4 = (xc, yc - r)
    cp_1 = (xc - r, yc + r * KAPPA)
    cp_2 = (xc - KAPPA * r, yc + r)
    cp_3 = (xc + KAPPA * r, yc + r)
    cp_4 = (xc + r, yc + r * KAPPA)
    cp_5 = (xc + r, yc - r * KAPPA)
    cp_6 = (xc + KAPPA * r, yc - r)
    cp_7 = (xc - KAPPA * r, yc - r)
    cp_8 = (xc - r, yc - r * KAPPA)
    contour = fontforge.contour()
    contour.closed = True
    if withershins:
        contour.moveTo(*pt_1)
        contour.cubicTo(cp_8, cp_7, pt_4)
        contour.cubicTo(cp_6, cp_5, pt_3)
        contour.cubicTo(cp_4, cp_3, pt_2)
        contour.cubicTo(cp_2, cp_1, pt_1)
    else:
        contour.moveTo(*pt_1)
        contour.cubicTo(cp_1, cp_2, pt_2)
        contour.cubicTo(cp_3, cp_4, pt_3)
        contour.cubicTo(cp_5, cp_6, pt_4)
        contour.cubicTo(cp_7, cp_8, pt_1)
    return contour
    
def rel_circle_contour(glyph, center, r, withershins=False):
    center = rel_to_abs_point(center)
    return circle_contour(glyph, center, r, withershins=withershins)
