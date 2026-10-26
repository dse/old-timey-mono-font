import fontforge, statistics

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
        if glyph.glyphname == ".notdef":
            continue
        if glyph.glyphname == ".null":
            continue
        if glyph.glyphname == "nonmarkingreturn":
            continue
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
                    print(f'removedglyph at U+{code:04X}')
            except ValueError as e:
                if str(e) != "This glyph is not in the font":
                    raise
                if args.verbose:
                    print(f'U+{code:04X}: no such glyph')
    if args.verbose >= 2:
        print("finished removing glyphs")

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

def finalize_glyphs(font, ranges, args, exclude=None):
    if args.verbose:
        print("finalizing glyphs...")
    for r in ranges:
        for code in r:
            if exclude is not None and code in exclude:
                continue
            glyph = font.createChar(code)
            glyph.removeOverlap()
            glyph.simplify()
    if args.verbose >= 2:
        print("finished finalizing glyphs")

def save_font(font, args):
    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')
