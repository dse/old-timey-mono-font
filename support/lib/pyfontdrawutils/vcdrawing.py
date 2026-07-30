import math

from . import settings
from .constants import KAPPA
from .draw import rect, poly, create_char

ARC_TYPE_A = 0
ARC_TYPE_B = 1

def draw_light_vertical(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    x1 = glyph.width / 2 - stroke_width / 2
    x2 = glyph.width / 2 + stroke_width / 2
    rect(glyph, x1, x2, font.ascent, -font.descent, clockwise=clockwise)

def draw_light_horizontal(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - stroke_width / 2
    y2 = glyph.font.capHeight / 2 + stroke_width / 2
    rect(glyph, 0, glyph.width, y1, y2, clockwise=clockwise)

def draw_light_horizontal_left(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - stroke_width / 2
    y2 = glyph.font.capHeight / 2 + stroke_width / 2
    x1 = 0
    x2 = glyph.width / 2 + stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_horizontal_right(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - stroke_width / 2
    y2 = glyph.font.capHeight / 2 + stroke_width / 2
    x1 = glyph.width / 2 - stroke_width / 2
    x2 = glyph.width
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_vertical_top(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    y1 = glyph.font.capHeight / 2 - stroke_width / 2
    y2 = glyph.font.ascent
    x1 = glyph.width / 2 - stroke_width / 2
    x2 = glyph.width / 2 + stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_vertical_bottom(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font
    y1 = -glyph.font.descent
    y2 = glyph.font.capHeight / 2 + stroke_width / 2
    x1 = glyph.width / 2 - stroke_width / 2
    x2 = glyph.width / 2 + stroke_width / 2
    rect(glyph, x1, x2, y1, y2, clockwise=clockwise)

def draw_light_arc(glyph, upper=True, left=True, arc_type=ARC_TYPE_A, clockwise=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font

    x_sign = 1 if left else -1
    y_sign = 1 if upper else -1

    if arc_type == ARC_TYPE_A:
        rx = compute_arc_radius_A(glyph)
        ry = compute_arc_radius_A(glyph)
    elif arc_type == ARC_TYPE_B:
        (rx, ry) = compute_arc_radius_B(glyph)

    rx1 = rx - stroke_width / 2
    rx2 = rx + stroke_width / 2
    ry1 = ry - stroke_width / 2
    ry2 = ry + stroke_width / 2

    x = glyph.width / 2
    y = glyph.font.capHeight / 2
    x1 = x - x_sign * stroke_width / 2
    x2 = x + x_sign * stroke_width / 2
    y1 = y + y_sign * stroke_width / 2
    y2 = y - y_sign * stroke_width / 2

    x3 = x - x_sign * rx
    y3 = y + y_sign * ry

    x4 = x3 + x_sign * rx1 * KAPPA
    x5 = x3 + x_sign * rx2 * KAPPA
    y4 = y3 - y_sign * ry1 * KAPPA
    y5 = y3 - y_sign * ry2 * KAPPA

    x0 = 0 if left else glyph.width
    y0 = font.ascent if upper else -font.descent

    this_way = True
    if not clockwise:
        this_way = not this_way
    if upper != left:
        this_way = not this_way

    p00 = (x0, y1)
    p01 = (x3, y1)
    p02x = (x4, y1)
    p03x = (x1, y4)
    p04 = (x1, y3)
    p05 = (x1, y0)
    p06 = (x2, y0)
    p07 = (x2, y3)
    p08x = (x2, y5)
    p09x = (x5, y2)
    p10 = (x3, y2)
    p11 = (x0, y2)

    pen = glyph.glyphPen(replace=False)
    if this_way:
        # this path is clockwise if upper left or lower right arc
        pen.moveTo(p00)
        pen.lineTo(p01)
        pen.curveTo(p02x, p03x, p04)
        pen.lineTo(p05)
        pen.lineTo(p06)
        pen.lineTo(p07)
        pen.curveTo(p08x, p09x, p10)
        pen.lineTo(p11)
        pen.lineTo(p00)
    else:
        # this path is clockwise if upper right or lower left arc
        pen.moveTo(p00)
        pen.lineTo(p11)
        pen.lineTo(p10)
        pen.curveTo(p09x, p08x, p07)
        pen.lineTo(p06)
        pen.lineTo(p05)
        pen.lineTo(p04)
        pen.curveTo(p03x, p02x, p01)
        pen.lineTo(p00)
    pen.closePath()
    pen = None

def draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=True, left=True, arc_type=arc_type, clockwise=clockwise)

def draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=True, left=False, arc_type=arc_type, clockwise=clockwise)

def draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=False, left=True, arc_type=arc_type, clockwise=clockwise)

def draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_A, clockwise=True):
    draw_light_arc(glyph, upper=False, left=False, arc_type=arc_type, clockwise=clockwise)

def draw_dot(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    draw_heavy_circle(glyph, r = stroke_width * 1.25)

def draw_heavy_circle(glyph, r=None, clockwise=True):
    if r is None:
        r = settings.get_heavy_circle_radius_factor() * glyph.width / 2
    x0 = glyph.width / 2
    y0 = glyph.font.capHeight / 2
    x1 = x0 - r
    x2 = x0 + r
    y1 = y0 + r
    y2 = y0 - r
    cp = r * KAPPA
    x3 = x0 - r * KAPPA
    x4 = x0 + r * KAPPA
    y3 = y0 + r * KAPPA
    y4 = y0 - r * KAPPA
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y0))
    if clockwise:
        pen.curveTo((x1, y3), (x3, y1), (x0, y1))
        pen.curveTo((x4, y1), (x2, y3), (x2, y0))
        pen.curveTo((x2, y4), (x4, y2), (x0, y2))
        pen.curveTo((x3, y2), (x1, y4), (x1, y0))
    else:
        pen.curveTo((x1, y4), (x3, y2), (x0, y2))
        pen.curveTo((x4, y2), (x2, y4), (x2, y0))
        pen.curveTo((x2, y3), (x4, y1), (x0, y1))
        pen.curveTo((x3, y1), (x1, y3), (x1, y0))
    pen.closePath()
    pen = None

def hollow_out_heavy_circle(glyph, clockwise=False):
    stroke_width = settings.get_stroke_width()
    r = settings.get_heavy_circle_radius_factor() * glyph.width / 2 - stroke_width
    draw_heavy_circle(glyph, r=r, clockwise=clockwise)

def compute_arc_radius_A(glyph):
    font = glyph.font
    rx = glyph.width / 2 * settings.get_arc_drawing_radius_factor()
    ry1 = (font.ascent - glyph.font.capHeight / 2) * settings.get_arc_drawing_radius_factor()
    ry2 = (glyph.font.capHeight / 2 + font.descent) * settings.get_arc_drawing_radius_factor()
    return min(rx, ry1, ry2)

def compute_arc_radius_B(glyph):
    font = glyph.font
    rx = glyph.width / 2 * settings.get_arc_drawing_radius_factor()
    ry1 = (font.ascent - glyph.font.capHeight / 2) * settings.get_arc_drawing_radius_factor()
    ry2 = (glyph.font.capHeight / 2 + font.descent) * settings.get_arc_drawing_radius_factor()
    return (rx, min(ry1, ry2))

def draw_x_for_hollowed_out_heavy_circle(glyph, clockwise=True):
    stroke_width = settings.get_stroke_width()
    r = glyph.width / 2 * settings.get_heavy_circle_radius_factor() - stroke_width / 2
    print("r = %.4f" % r)
    xc = glyph.width / 2
    yc = glyph.font.capHeight / 2
    print("xc = %.4f; yc = %.4f" % (xc, yc));

    x5 = xc - stroke_width / math.sqrt(2)
    x6 = xc + stroke_width / math.sqrt(2)
    y5 = yc + stroke_width / math.sqrt(2)
    y6 = yc - stroke_width / math.sqrt(2)

    x_left  = xc - r / math.sqrt(2)
    x_right = xc + r / math.sqrt(2)
    y_upper = yc + r / math.sqrt(2)
    y_lower = yc - r / math.sqrt(2)

    x1 = x_left - stroke_width / math.sqrt(2) / 2
    x2 = x_left + stroke_width / math.sqrt(2) / 2
    x3 = x_right - stroke_width / math.sqrt(2) / 2
    x4 = x_right + stroke_width / math.sqrt(2) / 2

    y1 = y_upper + stroke_width / math.sqrt(2) / 2
    y2 = y_upper - stroke_width / math.sqrt(2) / 2
    y3 = y_lower + stroke_width / math.sqrt(2) / 2
    y4 = y_lower - stroke_width / math.sqrt(2) / 2

    print("x = %.4f, %.4f, %.4f, %.4f, %.4f, %.4f" % (x1, x2, x5, x6, x3, x4))
    print("y = %.4f, %.4f, %.4f, %.4f, %.4f, %.4f" % (y1, y2, y5, y6, y3, y4))

    pen = glyph.glyphPen(replace=False)
    if clockwise:
        pen.moveTo((x1, y2))
        pen.lineTo((x2, y1))
        pen.lineTo((xc, y5))
        pen.lineTo((x3, y1))
        pen.lineTo((x4, y2))
        pen.lineTo((x6, yc))
        pen.lineTo((x4, y3))
        pen.lineTo((x3, y4))
        pen.lineTo((xc, y6))
        pen.lineTo((x2, y4))
        pen.lineTo((x1, y3))
        pen.lineTo((x5, yc))
    else:
        pen.moveTo((x1, y2))
        pen.lineTo((x5, yc))
        pen.lineTo((x1, y3))
        pen.lineTo((x2, y4))
        pen.lineTo((xc, y6))
        pen.lineTo((x3, y4))
        pen.lineTo((x4, y3))
        pen.lineTo((x6, yc))
        pen.lineTo((x4, y2))
        pen.lineTo((x3, y1))
        pen.lineTo((xc, y5))
        pen.lineTo((x2, y1))
    pen.closePath()
    pen = None

def draw_vertical_diagonal(glyph, clockwise=True, left=True, upper=False):
    draw_horizontal_diagonal(glyph, clockwise=clockwise, left=left, upper=upper, horizontal=False)

def draw_horizontal_diagonal(glyph, clockwise=True, left=True, upper=False, horizontal=True):
    stroke_width = settings.get_stroke_width()
    font = glyph.font

    this_way = clockwise
    if not left:
        this_way = not this_way
    if upper:
        this_way = not this_way

    w = glyph.width
    h = font.ascent + font.descent

    x1 = 0
    y1 = -font.descent
    x1a = x1 - stroke_width/2 * h / math.sqrt(w*w + h*h)
    y1a = y1 + stroke_width/2 * w / math.sqrt(w*w + h*h)
    x1b = x1 + stroke_width/2 * h / math.sqrt(w*w + h*h)
    y1b = y1 - stroke_width/2 * w / math.sqrt(w*w + h*h)

    if horizontal:
        x3a = glyph.width
        x3b = glyph.width
        y3a = (font.ascent - font.descent) / 2 + stroke_width/2
        y3b = (font.ascent - font.descent) / 2 - stroke_width/2
        y2a = y3a
        y2b = y3b
        x2a = x1a + w/h * (y2a - y1a)
        x2b = x1b + w/h * (y2b - y1b)
    else:
        x3a = glyph.width/2 - stroke_width/2
        x3b = glyph.width/2 + stroke_width/2
        y3a = font.ascent
        y3b = font.ascent
        x2a = x3a
        x2b = x3b
        y2a = y1a + h/w * (x2a - x1a)
        y2b = y1b + h/w * (x2b - x1b)

    if not left:
        (x1, x1a, x1b, x2a, x2b, x3a, x3b) = [
            glyph.width - x for x in
            (x1, x1a, x1b, x2a, x2b, x3a, x3b)
        ]
    if upper:
        (y1, y1a, y1b, y2a, y2b, y3a, y3b) = [
            font.ascent - font.descent - y for y in
            (y1, y1a, y1b, y2a, y2b, y3a, y3b)
        ]

    pen = glyph.glyphPen(replace=False)
    if this_way:
        pen.moveTo((x1a, y1a))
        pen.lineTo((x2a, y2a))
        pen.lineTo((x3a, y3a))
        pen.lineTo((x3b, y3b))
        pen.lineTo((x2b, y2b))
        pen.lineTo((x1b, y1b))
    else:
        pen.moveTo((x1a, y1a))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x2b, y2b))
        pen.lineTo((x3b, y3b))
        pen.lineTo((x3a, y3a))
        pen.lineTo((x2a, y2a))
    pen.closePath()
    pen = None

def draw_diagonal_piece(glyph, clockwise=True, left=True, upper=False):
    stroke_width = settings.get_stroke_width()

    font = glyph.font

    this_way = clockwise
    if not left:
        this_way = not this_way
    if upper:
        this_way = not this_way

    w = glyph.width
    h = font.ascent + font.descent

    x0 = 0
    y0 = -font.descent
    x0a = x0 - stroke_width/2 * h / math.sqrt(w*w + h*h)
    y0a = y0 + stroke_width/2 * w / math.sqrt(w*w + h*h)
    x0b = x0 + stroke_width/2 * h / math.sqrt(w*w + h*h)
    y0b = y0 - stroke_width/2 * w / math.sqrt(w*w + h*h)

    x1 = glyph.width / 2
    y1 = (font.ascent - font.descent) / 2
    x1a = x1 - stroke_width/2 * h / math.sqrt(w*w + h*h)
    y1a = y1 + stroke_width/2 * w / math.sqrt(w*w + h*h)
    x1b = x1 + stroke_width/2 * h / math.sqrt(w*w + h*h)
    y1b = y1 - stroke_width/2 * w / math.sqrt(w*w + h*h)

    if not left:
        (x0, x0a, x0b, x1, x1a, x1b) = [
            glyph.width - x for x in
            (x0, x0a, x0b, x1, x1a, x1b)
        ]
    if upper:
        (y0, y0a, y0b, y1, y1a, y1b) = [
            font.ascent - font.descent - y for y in
            (y0, y0a, y0b, y1, y1a, y1b)
        ]

    pen = glyph.glyphPen(replace=False)
    if this_way:
        pen.moveTo((x0a, y0a))
        pen.lineTo((x1a, y1a))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x0b, y0b))
    else:
        pen.moveTo((x0a, y0a))
        pen.lineTo((x0b, y0b))
        pen.lineTo((x1b, y1b))
        pen.lineTo((x1a, y1a))
    pen.closePath()
    pen = None

def draw(font):

    codepoint = 0xfaf00

    # revision mark, heavy circle
    for glyph in create_char(font, 0xfaf00):
        # heavy circle revision mark
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf01):
        # heavy circle revision mark light horizontal
        draw_light_horizontal(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf02):
        # heavy circle revision mark light vertical
        draw_light_vertical(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf03):
        # heavy circle revision mark light vertical upper
        draw_light_vertical_top(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf04):
        # heavy circle revision mark light vertical lower
        draw_light_vertical_bottom(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf05):
        # heavy circle revision mark light horizontal left
        draw_light_horizontal_left(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf06):
        # heavy circle revision mark light horizontal right
        draw_light_horizontal_right(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark, light circle
    for glyph in create_char(font, 0xfaf07):
        # light circle revision mark
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf08):
        # light circle revision mark light horizontal
        draw_light_horizontal(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf09):
        # light circle revision mark light vertical
        draw_light_vertical(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf0a):
        # light circle revision mark light vertical upper
        draw_light_vertical_top(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf0b):
        # light circle revision mark light vertical lower
        draw_light_vertical_bottom(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf0c):
        # light circle revision mark light horizontal left
        draw_light_horizontal_left(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf0d):
        # light circle revision mark light horizontal right
        draw_light_horizontal_right(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark, light circle with x
    for glyph in create_char(font, 0xfaf0e):
        # light circle with x revision mark
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf0f):
        # light circle with x revision mark light horizontal
        draw_light_horizontal(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf10):
        # light circle with x revision mark light vertical
        draw_light_vertical(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf11):
        # light circle with x revision mark light vertical upper
        draw_light_vertical_top(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf12):
        # light circle with x revision mark light vertical lower
        draw_light_vertical_bottom(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf13):
        # light circle with x revision mark light horizontal left
        draw_light_horizontal_left(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf14):
        # light circle with x revision mark light horizontal right
        draw_light_horizontal_right(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark, light circle with dot
    for glyph in create_char(font, 0xfaf15):
        # light circle with dot revision mark
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf16):
        # light circle with dot revision mark light horizontal
        draw_light_horizontal(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf17):
        # light circle with dot revision mark light vertical
        draw_light_vertical(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf18):
        # light circle with dot revision mark light vertical upper
        draw_light_vertical_top(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf19):
        # light circle with dot revision mark light vertical lower
        draw_light_vertical_bottom(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf1a):
        # light circle with dot revision mark light horizontal left
        draw_light_horizontal_left(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf1b):
        # light circle with dot revision mark light horizontal right
        draw_light_horizontal_right(glyph)
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # merge drawing
    for glyph in create_char(font, 0xfaf1c):
        # vertical merge upper from left
        draw_light_vertical(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf1d):
        # vertical merge upper from right
        draw_light_vertical(glyph)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf1e):
        # vertical merge lower from left
        draw_light_vertical(glyph)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf1f):
        # vertical merge lower from right
        draw_light_vertical(glyph)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf20):
        # vertical merge upper from left and right
        draw_light_vertical(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf21):
        # vertical merge lower from left and right
        draw_light_vertical(glyph)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    for glyph in create_char(font, 0xfaf22):
        # horizontal merge left from upper
        draw_light_horizontal(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf23):
        # horizontal merge right from upper
        draw_light_horizontal(glyph)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf24):
        # horizontal merge left from lower
        draw_light_horizontal(glyph)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf25):
        # horizontal merge right from lower
        draw_light_horizontal(glyph)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf26):
        # horizontal merge left from upper and lower
        draw_light_horizontal(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf27):
        # horizontal merge right from upper and lower
        draw_light_horizontal(glyph)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    # merge drawing
    for glyph in create_char(font, 0xfaf28):
        # box drawings light horizontal and vertical with upper left arc
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf29):
        # box drawings light horizontal and vertical with upper right arc
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf2a):
        # box drawings light horizontal and vertical with lower left arc
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf2b):
        # box drawings light horizontal and vertical with lower right arc
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf2c):
        # box drawings light horizontal and vertical with upper left and right arcs
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf2d):
        # box drawings light horizontal and vertical with lower left and right arcs
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    for glyph in create_char(font, 0xfaf2e):
        # box drawings light horizontal and vertical with upper and lower left arcs
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf2f):
        # box drawings light horizontal and vertical with upper and lower right arcs
        draw_light_vertical(glyph)
        draw_light_horizontal(glyph)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    # alternate style arcs
    for glyph in create_char(font, 0xfaf30):
        # revision log drawing upper left arc
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf31):
        # revision log drawing upper right arc
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf32):
        # revision log drawing lower left arc
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf33):
        # revision log drawing lower right arc
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    # double-arcs
    for glyph in create_char(font, 0xfaf34):
        # revision log drawing upper left and right arcs
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf35):
        # revision log drawing lower left and right arcs
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf36):
        # revision log drawing lower and upper left arcs
        draw_light_upper_left_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_left_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf37):
        # revision log drawing lower and upper right arcs
        draw_light_upper_right_arc(glyph, arc_type=ARC_TYPE_B)
        draw_light_lower_right_arc(glyph, arc_type=ARC_TYPE_B)
        glyph.removeOverlap()
        codepoint += 1

    # diagonal to horizontal/vertical
    for glyph in create_char(font, 0xfaf38):
        # light diagonal upper left to down
        draw_vertical_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf39):
        # light diagonal upper right to down
        draw_vertical_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3a):
        # light diagonal lower left to up
        draw_vertical_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3b):
        # light diagonal lower right to up
        draw_vertical_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3c):
        # light dialgonal upper left to right
        draw_horizontal_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3d):
        # light diagonal upper right to left
        draw_horizontal_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3e):
        # light diagonal lower left to right
        draw_horizontal_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf3f):
        # light diagonal lower right to left
        draw_horizontal_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark heavy circle with diagonal to horizontal/vertical
    for glyph in create_char(font, 0xfaf40):
        # revision mark heavy circle with light diagonal upper left to down
        draw_vertical_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf41):
        # revision mark heavy circle with light diagonal upper right to down
        draw_vertical_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf42):
        # revision mark heavy circle with light diagonal lower left to up
        draw_vertical_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf43):
        # revision mark heavy circle with light diagonal lower right to up
        draw_vertical_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf44):
        # revision mark heavy circle with light dialgonal upper left to right
        draw_horizontal_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf45):
        # revision mark heavy circle with light diagonal upper right to left
        draw_horizontal_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf46):
        # revision mark heavy circle with light diagonal lower left to right
        draw_horizontal_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf47):
        # revision mark heavy circle with light diagonal lower right to left
        draw_horizontal_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf48):
        # revision mark heavy circle with light diagonal lower left
        draw_diagonal_piece(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf49):
        # revision mark heavy circle with light diagonal lower right
        draw_diagonal_piece(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf4a):
        # revision mark heavy circle with light diagonal upper left
        draw_diagonal_piece(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf4b):
        # revision mark heavy circle with light diagonal upper right
        draw_diagonal_piece(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark light circle with diagonal to horizontal/vertical
    for glyph in create_char(font, 0xfaf4c):
        # revision mark light circle with light diagonal upper left to down
        draw_vertical_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf4d):
        # revision mark light circle with light diagonal upper right to down
        draw_vertical_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf4e):
        # revision mark light circle with light diagonal lower left to up
        draw_vertical_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf4f):
        # revision mark light circle with light diagonal lower right to up
        draw_vertical_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf50):
        # revision mark light circle with light dialgonal upper left to right
        draw_horizontal_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf51):
        # revision mark light circle with light diagonal upper right to left
        draw_horizontal_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf52):
        # revision mark light circle with light diagonal lower left to right
        draw_horizontal_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf53):
        # revision mark light circle with light diagonal lower right to left
        draw_horizontal_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf54):
        # revision mark light circle with light diagonal lower left
        draw_diagonal_piece(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf55):
        # revision mark light circle with light diagonal lower right
        draw_diagonal_piece(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf56):
        # revision mark light circle with light diagonal upper left
        draw_diagonal_piece(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf57):
        # revision mark light circle with light diagonal upper right
        draw_diagonal_piece(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark light circle with x with diagonal to horizontal/vertical
    for glyph in create_char(font, 0xfaf58):
        # revision mark light circle with x with light diagonal upper left to down
        draw_vertical_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf59):
        # revision mark light circle with x with light diagonal upper right to down
        draw_vertical_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5a):
        # revision mark light circle with x with light diagonal lower left to up
        draw_vertical_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5b):
        # revision mark light circle with x with light diagonal lower right to up
        draw_vertical_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5c):
        # revision mark light circle with x with light dialgonal upper left to right
        draw_horizontal_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5d):
        # revision mark light circle with x with light diagonal upper right to left
        draw_horizontal_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5e):
        # revision mark light circle with x with light diagonal lower left to right
        draw_horizontal_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf5f):
        # revision mark light circle with x with light diagonal lower right to left
        draw_horizontal_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf60):
        # revision mark light circle with x with light diagonal lower left
        draw_diagonal_piece(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf61):
        # revision mark light circle with x with light diagonal lower right
        draw_diagonal_piece(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf62):
        # revision mark light circle with x with light diagonal upper left
        draw_diagonal_piece(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf63):
        # revision mark light circle with x with light diagonal upper right
        draw_diagonal_piece(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_x_for_hollowed_out_heavy_circle(glyph)
        glyph.removeOverlap()
        codepoint += 1

    # revision mark light circle with dot with diagonal to horizontal/vertical
    for glyph in create_char(font, 0xfaf64):
        # revision mark light circle with dot with light diagonal upper left to down
        draw_vertical_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf65):
        # revision mark light circle with dot with light diagonal upper right to down
        draw_vertical_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf66):
        # revision mark light circle with dot with light diagonal lower left to up
        draw_vertical_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf67):
        # revision mark light circle with dot with light diagonal lower right to up
        draw_vertical_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf68):
        # revision mark light circle with dot with light dialgonal upper left to right
        draw_horizontal_diagonal(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf69):
        # revision mark light circle with dot with light diagonal upper right to left
        draw_horizontal_diagonal(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6a):
        # revision mark light circle with dot with light diagonal lower left to right
        draw_horizontal_diagonal(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6b):
        # revision mark light circle with dot with light diagonal lower right to left
        draw_horizontal_diagonal(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6c):
        # revision mark light circle with dot with light diagonal lower left
        draw_diagonal_piece(glyph, left=True, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6d):
        # revision mark light circle with dot with light diagonal lower right
        draw_diagonal_piece(glyph, left=False, upper=False)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6e):
        # revision mark light circle with dot with light diagonal upper left
        draw_diagonal_piece(glyph, left=True, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
    for glyph in create_char(font, 0xfaf6f):
        # revision mark light circle with dot with light diagonal upper right
        draw_diagonal_piece(glyph, left=False, upper=True)
        glyph.removeOverlap()
        draw_heavy_circle(glyph)
        glyph.removeOverlap()
        hollow_out_heavy_circle(glyph)
        glyph.removeOverlap()
        draw_dot(glyph)
        glyph.removeOverlap()
        codepoint += 1
