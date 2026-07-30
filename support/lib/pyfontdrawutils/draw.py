import fontforge

from .constants import X, Y
from . import settings
from pyfontutils.parse import parse_char

def rect(glyph, x1, x2, y1, y2, clockwise=True):
    """Draw a rectangle onto the specified glyph.  Does not clear the glyph first.

    """
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))

    contour = fontforge.contour()
    contour.moveTo(x1, y2)
    contour.lineTo(x2, y2)
    contour.lineTo(x2, y1)
    contour.lineTo(x1, y1)
    contour.closed = True

    if clockwise and not contour.isClockwise():
        contour.reverseDirection()
    elif not clockwise and contour.isClockwise():
        contour.reverseDirection()

    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def poly(glyph, pairs, clockwise=True):
    contour = fontforge.contour()
    x = pairs[0][0]
    y = pairs[0][1]
    contour.moveTo(x, y)
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
                contour.lineTo(x, y)
                horizontal = not horizontal
        elif pair[0] == X:
            x = pair[1]
            contour.lineTo(x, y)
        elif pair[0] == Y:
            y = pair[1]
            contour.lineTo(x, y)
        else:
            (x, y) = pair
            contour.lineTo(x, y)
    contour.closed = True

    if clockwise and not contour.isClockwise():
        contour.reverseDirection()
    elif not clockwise and contour.isClockwise():
        contour.reverseDirection()

    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def create_char(font, param):
    """
    Convenience function.

    for glyph in create_char(0x1f4a9):
        ...
    """
    codepoint = parse_char(param)
    glyph = font.createChar(codepoint)
    glyph.clear()
    glyph.width = settings.get_default_glyph_width()
    return [glyph]
