import fontforge, re, os, psMat, unicodedata, json, sys

font_utils_path = "%s/git/dse.d/pyfontutils/lib" % os.getenv("HOME")

if font_utils_path not in sys.path:
    sys.path.append(font_utils_path)

from font_utils import parse_char, u

def get_base_codepoint(glyph, default=-1):
    if glyph.unicode >= 0:
        return glyph.unicode
    return fontforge.unicodeFromName(glyph.glyphname.split(".")[0])

def get_base_glyphname(glyph, default=None):
    return glyph.glyphname.split(".")[0]

def get_variant_name(glyph, default=None):
    if "." in glyph.glyphname:
        return glyph.glyphname.split(".", 1)[1]

def parse_codepoint_argument(str):
    return parse_char(str)

def reconstitute_references(glyph):
    # Apparently a glyph.unlinkRef() call will replace the
    # references with the contours from when the font was
    # loaded, ignoring any changes we make to the glyph.
    references = glyph.references
    glyph.references = []
    for reference in references:
        glyph.addReference(reference[0], reference[1])

def parse_glyph_svg_filename(filename):
    (dirname, basename) = os.path.split(filename) # "/home/dse"; "foo.svg"
    (stem, ext) = os.path.splitext(basename)      # "foo"; ".svg"
    if "-" in stem:
        stem = stem.split("-")[0]
    parse_result = parse_char(stem, default=None, plain_hex=True)
    if parse_result is None:
        return [-1, stem, None, None, None]
    return parse_result

# # FIXME: if allow_json_data is True, allow a ".svg" to override.
# def import_svg_glyph(font, svg_filename, width, allow_json_data=False):
#     font_path = os.path.relpath(font.path)
#     (codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width) = parse_glyph_svg_filename(svg_filename)
#     if codepoint is None and glyphname is None:
#         return
#     glyph = None
#     if glyphname in font:
#         glyph = font[glyphname]
#         if len(glyph.references):
#             return
#     glyph = font.createChar(codepoint, glyphname)
#     glyph.foreground = fontforge.layer()
#     if width is None:
#         orig_width = glyph.width
#     if stroke_width is not None:
#         font.strokedfont = True
#         glyph.importOutlines(svg_filename, correctdir=True)
#         font.strokedfont = False
#     else:
#         font.strokedfont = True
#         glyph.importOutlines(svg_filename)
#         font.strokedfont = False
#     if width is None:
#         glyph.width = orig_width
#     else:
#         glyph.width = width

#     data = None
#     try:
#         data = json.loads(glyph.comment)
#     except json.decoder.JSONDecodeError:
#         data = glyph.comment
#     if type(data) == str and not re.search(r'\S', data):
#         data = { }
#     elif data is not None and type(data) != dict:
#         data = { "data": data }
#     if stroke_width is None:
#         if "stroke_width" in data:
#             del data["stroke_width"]
#     else:
#         data["stroke_width"] = stroke_width
#     glyph.comment = json.dumps(data, indent=4)

STROKE_WIDTH_BASIS = 96

def create_smol_glyph(font, codepoint, special=False):
    font_path = os.path.relpath(font.path)
    plain_glyphname = fontforge.nameFromUnicode(codepoint)
    simpl_glyphname = fontforge.nameFromUnicode(codepoint) + ".ss07"
    orig_glyphname = fontforge.nameFromUnicode(codepoint) + ".ORIG"
    glyphname = None

    if special:
        # for certain regular glyphs, use a special glyph to make smaller.
        if plain_glyphname == 'equal':
            glyphname = 'equal.cv11'
        elif plain_glyphname == 'comma':
            glyphname = 'comma.ss05'
        elif plain_glyphname == 'period':
            glyphname = 'period.ss05'
        elif plain_glyphname == 'colon':
            glyphname = 'colon.ss05'
        elif plain_glyphname == 'semicolon':
            glyphname = 'semicolon.ss05'

        # for certain glyphs, if certain variants are there use them.
        elif simpl_glyphname in font:
            glyphname = simpl_glyphname
        elif orig_glyphname in font:
            glyphname = orig_glyphname
        elif plain_glyphname in font: # most of the time this is the case.
            glyphname = plain_glyphname
        else:
            return
    else:
        glyphname = plain_glyphname

    glyph = font[glyphname]
    orig_width = glyph.width

    sm_glyphname = plain_glyphname + '.SMOL'
    sm_glyph = font.createChar(-1, sm_glyphname)
    sm_glyph.foreground = fontforge.layer() # clear out any existing contours

    pen = sm_glyph.glyphPen() # pen to draw into smol glyph
    glyph.draw(pen)
    pen = None

    if len(sm_glyph.references):
        reconstitute_references(sm_glyph)
        sm_glyph.unlinkRef()

    sm_glyph.transform(psMat.scale(0.5))
    sm_glyph.transform(psMat.translate(orig_width / 4, STROKE_WIDTH_BASIS / 4))
    sm_glyph.width = glyph.width

    return sm_glyph

def check_all_glyph_bounds(font, width=None):
    for glyph in font.glyphs():
        check_glyph_bounds(glyph, width)

def check_glyph_bounds(glyph, width=None):
    font_path = os.path.relpath(glyph.font.path)
    [xmin, ymin, xmax, ymax] = glyph.boundingBox()
    if glyph.unicode < 0:
        unicodename = "%d" % glyph.unicode
    else:
        try:
            unicodename = unicodedata.name(chr(glyph.unicode))
        except ValueError:
            unicodename = "(no name)"
    height = glyph.font.ascent + glyph.font.descent
    if width is None:
        width = glyph.width
    if "DEBUG" in os.environ:
        if xmin < -width/2:
            print("check_all_glyph_bounds %s:     left" % font_path)
        if xmax > width*3/2:
            print("check_all_glyph_bounds %s:     right" % font_path)
        if ymin < (-glyph.font.descent - height/2):
            print("check_all_glyph_bounds %s:     bottom" % font_path)
        if ymax > glyph.font.ascent + height/2:
            print("check_all_glyph_bounds %s:     top" % font_path)

glyph_data = None
def get_glyph_char_data(glyph):
    global glyph_data
    if glyph_data is None:
        with open("src/data/glyphs.json") as fh:
            glyph_data = json.loads(fh.read())
    base_codepoint = get_base_codepoint(glyph)
    base_glyphname = get_base_glyphname(glyph)
    variant_name = get_variant_name(glyph)

    char_data = {}

    if "__RANGES__" in glyph_data:
        for range_item in glyph_data["__RANGES__"]:
            start_cp = parse_char(range_item["from"])[2]
            end_cp   = parse_char(range_item["to"])[2]
            print("from = %s; to = %s; start_cp = %d; end_cp = %d" % (
                range_item["from"],
                range_item["to"],
                start_cp, end_cp
            ))
            if base_codepoint in range(start_cp, end_cp + 1) and "data" in range_item:
                print("  base_codepoint %d matches" % base_codepoint)
                data = range_item["data"]
                char_data = { **char_data, **data }
            else:
                print("  base_codepoint %d does NOT match" % base_codepoint)

    if base_codepoint in range(0, 0x110000) and chr(base_codepoint) in glyph_data:
        data = glyph_data[chr(base_codepoint)]
        char_data = { **char_data, **data }

    if base_codepoint in range(0, 0x110000) and u(base_codepoint) in glyph_data:
        data = glyph_data[u(base_codepoint)]
        char_data = { **char_data, **data }

    if glyph.glyphname in glyph_data:
        data = glyph_data[glyph.glyphname]
        char_data = { **char_data, **data }

    try:
        if base_codepoint in range(0, 0x110000):
            unicodename = unicodedata.name(chr(base_codepoint))
            if unicodename in glyph_data:
                data = glyph_data[unicodename]
                char_data = { **char_data, **data }
    except ValueError:
        pass

    if "__VARIANTS__" in char_data:
        if variant_name is not None:
            if variant_name in char_data["__VARIANTS__"]:
                data = char_data["__VARIANTS__"][variant_name]
                char_data = { **char_data, **data }
        del char_data["__VARIANTS__"]

    return char_data

    # if codepoint < 0:
    #     return {}
    # variant = None
    # if (idx := glyph.glyphname.find(".")) != -1:
    #     variant = glyph.glyphname[idx+1:]
    # variant_key = "variant." + variant if variant is not None else None
    # range_char_data     = None
    # this_char_data      = None
    # variant_char_data   = None
    # if "ranges" in glyph_data:
    #     for range_item in glyph_data["ranges"]:
    #         start_cp = ord(range_item["from"])
    #         end_cp = ord(range_item["to"])
    #         if codepoint in range(start_cp, end_cp + 1) and "data" in range_item:
    #             range_char_data = range_item["data"]
    #             break
    # if chr(codepoint) in glyph_data:
    #     this_char_data = glyph_data[chr(codepoint)]
    # elif u(codepoint) in glyph_data:
    #     this_char_data = glyph_data[u(codepoint)]
    # else:
    #     this_char_data = None

    if this_char_data is not None and variant_key in this_char_data:
        variant_char_data = this_char_data[variant_key]
    if (range_char_data is None and
        this_char_data is None and
        variant_char_data is None):
        return {}
    char_data = {}
    if range_char_data is not None:
        char_data = { **char_data, **range_char_data }
    if this_char_data is not None:
        char_data = { **char_data, **this_char_data }
    if variant_char_data is not None:
        char_data = { **char_data, **variant_char_data }
    if variant_key in char_data:
        del char_data[variant_key]
    return char_data

DEBUG_GLYPHS = None
if "DEBUG_GLYPHS" in os.environ:
    strings = os.environ["DEBUG_GLYPHS"].split(',')
    DEBUG_GLYPHS = []
    for string in strings:
        if parse_codepoint_argument(string) is not None:
            DEBUG_GLYPHS.push(parse_codepoint_argument(string))
        else:
            DEBUG_GLYPHS.push(glyphname)

def debug_glyph(glyph):
    codepoint = glyph.unicode
    if codepoint < 0:
        codepoint = fontforge.unicodeFromName(glyph.glyphname[0].split('.')[0])
    return debug_glyphname(glyph.glyphname) or debug_codepoint(codepoint)

def debug_glyphname(glyphname):
    return glyphname in DEBUG_GLYPHS or glyphname.split('.')[0] in DEBUG_GLYPHS

def debug_codepoint(codepoint):
    return codepoint in DEBUG_GLYPHS

def draw_grid_shape(width, x_max, y_max, polygons, font=None, codept=None, glyph=None, pen=None):
    if font is not None and codept is not None:
        glyphname = fontforge.nameFromUnicode(codept)
        if glyphname in font:
            font.removeGlyph(glyphname)
        glyph = font.createChar(codept)
        glyph.width = width
        pen = glyph.glyphPen()
        return draw_grid_shape(width, x_max, y_max, polygons, glyph=glyph, pen=pen)
    font = glyph.font
    for polygon in polygons:
        if type(polygon[0]) in [float, int]:
            black_level = polygon[0]
            points = polygon[1:]
        else:
            black_level = 1
            points = polygon[0:]
        first_point = True
        for point in points:
            print(repr(point))
            [x,y] = point
            x = x * width / x_max
            y = font.ascent - y * (font.descent + font.ascent) / y_max
            if first_point:
                pen.moveTo((x, y))
                first_point = False
            else:
                pen.lineTo((x, y))
        pen.closePath()
    glyph.width = width

def draw_shape(width, x_max, y_max, polygons, font=None, codept=None, glyph=None, pen=None):
    if font is not None and codept is not None:
        glyphname = fontforge.nameFromUnicode(codept)
        if glyphname in font:
            font.removeGlyph(glyphname)
        glyph = font.createChar(codept)
        glyph.width = width
        pen = glyph.glyphPen()
        return draw_shape(width, x_max, y_max, polygons, glyph=glyph, pen=pen)
    font = glyph.font
    for polygon in polygons:
        if type(polygon[0]) in [float, int]:
            black_level = polygon[0]
            points = polygon[1:]
        else:
            black_level = 1
            points = polygon[0:]
        first_point = True
        for point in points:
            [x,y] = point
            x = x * width / x_max
            y = y * (font.ascent - (font.descent + font.ascent)) / y_max
            if first_point:
                pen.moveTo((x, y))
            else:
                pen.lineTo((x, y))
            first_point = False
        pen.closePath()
    glyph.width = width
