import fontforge, re, os, psMat, unicodedata, json

def u(codepoint, pad=False):
    result = None
    if codepoint < 0:
        result = "%d" % codepoint
    else:
        result = "U+%04X" % codepoint
    if pad:
        result = "%-8s" % result
    return result

def parse_codepoint_argument(str):
    # U+1F4A9
    # 128169
    # 0x1f4a9
    if (match := re.fullmatch(r'(?:0?x|u\+?)([0-9A-Fa-f]+)', str, flags=re.IGNORECASE)):
        return int(match.group(1), 16)
    if len(str) == 1:
        return ord(str)
    if (match := re.fullmatch(r'[0-9]+', str, flags=re.IGNORECASE)):
        return int(match.group(0))
    return None

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
    codepoint = None            # -1 for variants or specials; 0+ for normal glyphs
    glyphname = None            # glyphname with optional suffix
    real_codepoint = None       # -1 for specials; 0+ for variants or normal glyphs
    plain_glyphname = None      # glyphname without suffix
    suffix = None               # suffix without "." or "--" prefix, or None
    stroke_width = None         # int if stroke width specified in SVG file; None otherwise
    stem_copy = stem
    custom = False
    while len(stem_copy):
        if match := re.search(r'^(?:u\+|0x)?([0-9A-Fa-f]+)(?:$|(?=[-.]))-?', stem_copy, flags=re.IGNORECASE):
            # filename without extension
            # hex with optional "U", "U+", or "0x" prefix (case-insens.)
            # followed by EOL, "-", or "."
            codepoint = int(match.group(1), 16)
            real_codepoint = codepoint
            stem_copy = stem_copy[match.end(0):]
            continue
        if match := re.search(r'^x--', stem_copy, flags=re.IGNORECASE):
            # for non-Unicode characters
            custom = True
            codepoint = -1
            real_codepoint = None
            stem_copy = stem_copy[match.end(0):]
            continue
        if match := re.search(r'x_', stem_copy, flags=re.IGNORECASE):
            # for non-Unicode characters
            custom = True
            codepoint = -1
            real_codepoint = None
            stem_copy = stem_copy[match.end(0):]
            continue
        if match := re.search(r'--(?:([0-9]+)(?:px)?)$', stem_copy, flags=re.IGNORECASE):
            # I'm not actually using this meaningfully.  At least not
            # at this time.  (04/20/2025)
            stroke_width = int(match.group(1))
            stem_copy = stem_copy[0:match.start()]
            continue
        if match := re.search(r'--(.+)$', stem_copy, flags=re.IGNORECASE):
            # --xxx extensions for variants
            suffix = match.group(1)
            stem_copy = stem_copy[0:match.start()]
            continue
        if match := re.search(r'\.(.+)$', stem_copy, flags=re.IGNORECASE):
            # .xxx extensions for variants
            suffix = match.group(1)
            stem_copy = stem_copy[0:match.start()]
            continue
        break
    if codepoint is None:
        return [None, None, None, None, None]
    if codepoint < 0:
        plain_glyphname = stem_copy
        glyphname = "x_" + stem_copy
        if suffix is not None:
            glyphname += ("." + suffix)
        real_codepoint = fontforge.unicodeFromName(plain_glyphname)
        return [codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width]
    if suffix is not None:
        plain_glyphname = fontforge.nameFromUnicode(codepoint)
        glyphname = (plain_glyphname + "." + suffix)
        real_codepoint = codepoint
        codepoint = -1
        return [codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width]
    plain_glyphname = fontforge.nameFromUnicode(codepoint)
    glyphname = fontforge.nameFromUnicode(codepoint)
    real_codepoint = codepoint
    return [codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width]

# FIXME: if allow_json_data is True, allow a ".svg" to override.
def import_svg_glyph(font, svg_filename, width, allow_json_data=False):
    font_path = os.path.relpath(font.path)
    (codepoint, glyphname, real_codepoint, plain_glyphname, stroke_width) = parse_glyph_svg_filename(svg_filename)
    if codepoint is None and glyphname is None:
        return
    glyph = None
    if glyphname in font:
        glyph = font[glyphname]
        if len(glyph.references):
            if "DEBUG" in os.environ:
                print("import_svg_glyph %s: WARNING: glyph %s %s contains references but %s is present" % (font_path, glyphname, u(glyph.unicode), svg_filename))
                print("import_svg_glyph %s:     not importing %s" % (font_path, svg_filename))
            return
    glyph = font.createChar(codepoint, glyphname)
    if "DEBUG" in os.environ:
        print("import_svg_glyph %s: importing SVG %s to %s %s" % (font_path, svg_filename, glyphname, u(glyph.unicode)))
    glyph.foreground = fontforge.layer()
    if width is None:
        orig_width = glyph.width
    if stroke_width is not None:
        font.strokedfont = True
        glyph.importOutlines(svg_filename, correctdir=True)
        font.strokedfont = False
    else:
        font.strokedfont = True
        glyph.importOutlines(svg_filename)
        font.strokedfont = False
    if width is None:
        glyph.width = orig_width
    else:
        glyph.width = width

    data = None
    try:
        data = json.loads(glyph.comment)
    except json.decoder.JSONDecodeError:
        data = glyph.comment
    if type(data) == str and not re.search(r'\S', data):
        data = { }
    elif data is not None and type(data) != dict:
        data = { "data": data }
    if stroke_width is None:
        if "stroke_width" in data:
            del data["stroke_width"]
    else:
        data["stroke_width"] = stroke_width
    glyph.comment = json.dumps(data, indent=4)

STROKE_WIDTH_BASIS = 96

def create_smol_glyph(font, codepoint):
    font_path = os.path.relpath(font.path)
    plain_glyphname = fontforge.nameFromUnicode(codepoint)
    simpl_glyphname = fontforge.nameFromUnicode(codepoint) + ".ss07"
    orig_glyphname = fontforge.nameFromUnicode(codepoint) + ".orig"
    forsmall_glyphname = fontforge.nameFromUnicode(codepoint) + ".ss07"
    glyphname = None

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

    elif forsmall_glyphname in font:
        glyphname = forsmall_glyphname
    elif simpl_glyphname in font:
        glyphname = simpl_glyphname
    elif orig_glyphname in font:
        glyphname = orig_glyphname
    elif plain_glyphname in font:
        glyphname = plain_glyphname
    else:
        if "DEBUG" in os.environ:
            print("create_smol_glyph %s: not creating %s.smol" % (font_path, plain_glyphname))
        return
    glyph = font[glyphname]
    orig_width = glyph.width

    if "DEBUG" in os.environ:
        print("create_smol_glyph %s: creating %s.smol from %s" % (font_path, plain_glyphname, glyph.glyphname))

    sm_glyphname = plain_glyphname + '.smol'
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
    if "DEBUG" in os.environ:
        print("check_all_glyph_bounds %s: %s - %s %s - xmin = %d; xmax = %d; ymin = %d; ymax = %d" %
              (font_path, glyph.glyphname, u(glyph.unicode), unicodename, xmin, xmax, ymin, ymax))
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

def get_glyph_real_codepoint(glyph):
    if glyph.unicode >= 0:
        return glyph.unicode
    if (idx := glyph.glyphname.find(".")) == -1:
        return -1
    return fontforge.unicodeFromName(glyph.glyphname[0:idx])

glyph_data = None
def get_glyph_char_data(glyph):
    global glyph_data
    if glyph_data is None:
        with open("data/glyphs.json") as fh:
            glyph_data = json.loads(fh.read())
    codepoint = get_glyph_real_codepoint(glyph)
    if codepoint < 0:
        return {}
    variant = None
    if (idx := glyph.glyphname.find(".")) != -1:
        variant = glyph.glyphname[idx+1:]
    variant_key = "variant." + variant if variant is not None else None
    range_char_data     = None
    this_char_data      = None
    variant_char_data   = None
    if "ranges" in glyph_data:
        for range_item in glyph_data["ranges"]:
            start_cp = ord(range_item["from"])
            end_cp = ord(range_item["to"])
            if codepoint in range(start_cp, end_cp + 1) and "data" in range_item:
                range_char_data = range_item["data"]
                break
    if chr(codepoint) in glyph_data:
        this_char_data = glyph_data[chr(codepoint)]
        if variant_key in this_char_data:
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
