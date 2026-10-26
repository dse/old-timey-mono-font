def round_point(point):
    (x, y) = point
    x = round(x)
    y = round(y)
    return (x, y)

def rel_to_abs_point(glyph, point):
    font = glyph.font
    (x, y) = point
    x = round(glyph.width * x)
    y = round(-font.descent + font.em * y)
    return (x, y)

def clamp_point(point, a=None, b=None):
    (a, b) = normalize_clamp_point_args(a, b)
    (ax, ay) = a
    (bx, by) = b
    (x, y) = point
    return (clamp(x, ax, bx), clamp(y, ay, by))

def normalize_clamp_point_args(a=None, b=None):
    (ax, ay) = (None, None) if a is None else a
    (bx, by) = (None, None) if b is None else b
    (ax, bx) = normalize_clamp_args(ax, bx)
    (ay, by) = normalize_clamp_args(ay, by)
    return ((ax, ay), (bx, by))
