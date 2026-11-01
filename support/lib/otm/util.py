import fontforge, statistics, json, os

from otm.constants import KAPPA
from otm.point import round_point, rel_to_abs_point
from otm.poly import poly_contour, rel_poly_contour
from otm.rect import rect_contour, rel_rect_contour
from otm.circle import circle_contour, rel_circle_contour

def draw_poly(glyph, points, closed=True, debug=False):
    contour = poly_contour(glyph, points, closed=closed)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def draw_rel_poly(glyph, points, closed=True, debug=False):
    contour = rel_poly_contour(glyph, points, closed=closed)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def draw_rect(glyph, x1, y1, x2, y2, withershins=False, debug=False):
    contour = rect_contour(glyph, x1, y1, x2, y2, withershins=withershins)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def draw_rel_rect(glyph, x1, y1, x2, y2, withershins=False, debug=False):
    contour = rel_rect_contour(glyph, x1, y1, x2, y2, withershins=withershins)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def draw_dot(*args, **kwargs):
    return draw_circle(*args, **kwargs)

def draw_circle(glyph, center, r, withershins=False, debug=False):
    contour = circle_contour(glyph, center, r, withershins=withershins)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def draw_rel_circle(glyph, center, r, withershins=False, debug=False):
    contour = rel_circle_contour(glyph, center, r, withershins=withershins)
    pen = glyph.glyphPen(replace=False)
    contour.draw(pen)
    pen = None

def get_font_glyph_width(font):
    glyphs = []
    for glyph in font.glyphs():
        if glyph.width == 0:
            continue
        glyphs.append(glyph)
    widths = [glyph.width for glyph in glyphs]
    return round(statistics.median(widths))

def remove_glyphs(font, ranges, args, exclude=None):
    if args.verbose:
        print("removing glyphs...")
    for r in ranges:
        for code in r:
            if exclude is not None and code in exclude:
                continue
            try:
                if args.verbose:
                    print(f'removing glyph at U+{code:04X}')
                font.removeGlyph(code)
                if args.verbose >= 2:
                    print(f'removed glyph at U+{code:04X}')
            except ValueError as e:
                if str(e) != "This glyph is not in the font":
                    raise
                if args.verbose:
                    print(f'U+{code:04X}: no such glyph')
    if args.verbose >= 2:
        print("finished removing glyphs")

# for generated glyphs
def initialize_glyphs(font, ranges, args, width, exclude=None):
    if args.verbose:
        print("initializing glyphs...")
    for r in ranges:
        for code in r:
            if exclude is not None and code in exclude:
                continue
            glyph = font.createChar(code)
            glyph.foreground = fontforge.layer()
            glyph.width = width
    if args.verbose >= 2:
        print("finished initializing glyphs")

# for generated glyphs
def finalize_glyphs(font, ranges, args, exclude=None, expand_strokes=False):
    if args.verbose:
        print("finalizing glyphs...")
    for r in ranges:
        for code in r:
            if exclude is not None and code in exclude:
                continue
            glyph = font.createChar(code)
            glyph.removeOverlap()
            glyph.simplify()
            glyph.comment = json.dumps({ "expand_strokes": expand_strokes })
    if args.verbose >= 2:
        print("finished finalizing glyphs")

def walk_svg(filenames):
    if type(filenames) is not list:
        filenames = [filenames]
    retval = []
    for filename in filenames:
        if os.path.isdir(filename):
            for dir_path, dir_names, dir_filenames in os.walk(filename):
                for each_filename in dir_filenames:
                    if each_filename.lower().endswith(".svg"):
                        retval.append(os.path.join(dir_path, each_filename))
        else:
            retval.append(filename)
    return retval

def u(code):
    # in range(0, 0x110000) was a bottleneck in this function
    return "U+%04X" % code if is_valid_code(code) else str(code)

def is_valid_code(code):
    if type(code) is float:
        if code != round(code):
            return False
        code = int(round(code))
    if type(code) is int:
        return code >= 0 and code < 0x110000
    return False
