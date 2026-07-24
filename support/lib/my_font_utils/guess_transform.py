import fontforge, psMat, argparse, json, sys, math

def guess_transform_sequence(t):
    (a, b, c, d, dx, dy) = t
    if t == (1, 0, 0, 1, 0, 0):
        return []
    if (a, b, c, d) == (1, 0, 0, 1):
        return [
            ("translate", dx, dy)
        ]
    if (a, b, c, d) == (-1, 0, 0, -1):
        return [
            ("scale", -1, -1, { "center": (dx/2, dy/2) }),
        ]
    if (b, c) == (0, 0):
        if a == 1 or d == 1:
            return [
                ("scale", a, d),
                ("translate", e, f),
            ]
        x = e / (1-a)
        y = f / (1-d)
        return [
            ("scale", a, d, { "center": (x, y) })
        ]
    if (b, c, e, f) == (0, 0, 0, 0):
        return [
            ("scale", a, d)
        ]
    if (a, b, d, e, f) == (1, 0, 1, 0, 0):
        return [
            ("skew", atan(t[2]) * 180 / math.pi)
        ]
    if math.is_close(a, d) and math.is_close(b, -c) and \
       e == 0 and f == 0 and \
       math.is_close(t[0] ** 2 + t[1] ** 2, 1):
        if s >= 0:
            deg = math.asin(s) * 180 / math.pi
            if c < 0:
                deg = 180 - deg
        else:
            deg = math.asin(s) * 180 / math.pi + 360
            if c < 0:
                deg = 540 - deg
        return [
            ("rotate", deg)
        ]
    return [
        ("matrix", *t)
    ]
