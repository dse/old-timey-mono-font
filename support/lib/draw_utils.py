def rect(glyph, x1, x2, y1, y2):
    print("rect(%s, %d, %d, %d, %d)" % (glyph, x1, x2, y1, y2))
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()
    pen = None

def poly(glyph, pairs):
    pen = glyph.glyphPen(replace=False)
    x = pairs[0][0]
    y = pairs[0][1]
    pen.moveTo((x, y))
    for pair in pairs[1:]:
        if len(pair) > 2:
            if pair[0] == X:
                horizontal = True
            elif pair[0] == Y:
                horizontal = False
            else:
                raise Exception("tuple of more than 2 coordinates must start with X or Y")
            for i in range(1, len(pair)):
                if horizontal:
                    x = pair[i]
                else:
                    y = pair[i]
                pen.lineTo((x, y))
                horizontal = not horizontal
        elif pair[0] == X:
            x = pair[1]
            pen.lineTo((x, y))
        elif pair[0] == Y:
            y = pair[1]
            pen.lineTo((x, y))
        else:
            (x, y) = pair
            pen.lineTo((x, y))
    pen.closePath()
    pen = None

def clip(glyph, x1, y1, x2, y2):
    contour = fontforge.contour()
    contour.moveTo((x1, y1))
    contour.lineTo((x2, y1))
    contour.lineTo((x2, y2))
    contour.lineTo((x1, y2))
    contour.closed = True
    contour = None
    glyph.layers["Fore"] += clipContour
    glyph.intersect()

def GA(font, what):
    """Convenience function.

Returns an array containing a single item, that item being a FontForge
glyph object.

Used for `for glyph in GA("CHARACTER NAME")` constructs, e.g.,

    for glyph in GA("BOX DRAWINGS HEAVY TRIPLE DASH VERTICAL"):
        for i in range(0, 3):
            rect(glyph, x1_heavy, x2_heavy, dash_vert[3][i*2], dash_vert[3][i*2+1])
    for glyph in GA("BOX DRAWINGS LIGHT QUADRUPLE DASH HORIZONTAL"):
        for i in range(0, 4):
            rect(glyph, dash_horiz[4][i*2], dash_horiz[4][i*2+1], y1_light, y2_light)

for visual separation.
"""
    g = None
    if type(what) == str:
        if len(what) == 1:
            g = font.createChar(ord(what))
        else:
            g = font.createChar(ord(unicodedata.lookup(what)))
    elif type(what) == int:
        g = font.createChar(what)
    else:
        raise Exception("GA: invalid argument type")
    g.clear()
    return [g]
