import fontforge
from otm.point import rel_to_abs_point

def poly_contour(glyph, points, closed=True):
    contour = fontforge.contour()
    contour.closed = closed
    for idx, point in enumerate(points):
        if idx == 0:
            contour.moveTo(*point)
        else:
            contour.lineTo(*point)
    return contour

def rel_poly_contour(glyph, points, closed=True):
    points = [rel_to_abs_point(glyph, p) for p in points]
    return poly_contour(glyph, points, closed=closed)

