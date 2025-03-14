import fontforge
import re
import os
import psMat

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

def parse_glyph_svg_filename(svg_filename):
    (svg_dirname, svg_basename) = os.path.split(svg_filename)
    match_1 = re.search(r'^(?:u\+|0x)?([0-9a-f]+)(?=-|\.)', svg_basename, flags=re.IGNORECASE)
    match_2 = re.search(r'^x--', svg_basename, flags=re.IGNORECASE)
    match_3 = re.search(r'--(.+)$', os.path.splitext(svg_basename)[0]) # foo--bar.svg => "bar"
    if not match_1 and not match_2:
        return [None, None, None, None, None]
    suffix = match_3.expand('\\1') if match_3 else None
    hex = match_1.expand('\\1') if match_1 else None
    codepoint = int(hex, 16) if hex is not None else -1
    if codepoint < 0:
        glyphname = suffix
    elif suffix is not None:
        glyphname = fontforge.nameFromUnicode(codepoint) + "." + suffix
        codepoint = -1
    else:
        glyphname = fontforge.nameFromUnicode(codepoint)
    plain_glyphname = glyphname.split('.')[0]
    real_codepoint = fontforge.unicodeFromName(plain_glyphname)
    return [codepoint, glyphname, real_codepoint, plain_glyphname, suffix]

def import_svg_glyph(font, svg_filename, width):
    (codepoint, glyphname, real_codepoint, plain_glyphname, suffix) = parse_glyph_svg_filename(svg_filename)
    if codepoint is None and glyphname is None:
        return
    glyph = None
    if glyphname in font:
        glyph = font[glyphname]
        if len(glyph.references):
            print("import_svg_glyph: WARNING: glyph %s U+%04X contains references but %s is present" % (glyphname, glyph.unicode, svg_filename))
            return
    glyph = font.createChar(codepoint, glyphname)
    glyph.foreground = fontforge.layer()
    if width is None:
        orig_width = glyph.width
    font.strokedfont = True
    glyph.importOutlines(svg_filename)
    font.strokedfont = False
    if width is None:
        glyph.width = orig_width
    else:
        glyph.width = width

    # WIP: outlines in background
    # glyph.background = glyph.foreground

STROKE_WIDTH_BASIS = 96

def create_smol_glyph(font, codepoint):
    plain_glyphname = fontforge.nameFromUnicode(codepoint)
    simpl_glyphname = fontforge.nameFromUnicode(codepoint) + ".simpl"
    orig_glyphname = fontforge.nameFromUnicode(codepoint) + ".orig"
    glyphname = None
    if plain_glyphname == 'equal':
        glyphname = 'equal.code'
    elif plain_glyphname == 'comma':
        glyphname = 'comma.larger'
    elif plain_glyphname == 'period':
        glyphname = 'period.larger'
    elif plain_glyphname == 'colon':
        glyphname = 'colon.larger'
    elif plain_glyphname == 'semicolon':
        glyphname = 'semicolon.larger'
    elif simpl_glyphname in font:
        glyphname = simpl_glyphname
    elif orig_glyphname in font:
        glyphname = orig_glyphname
    elif plain_glyphname in font:
        glyphname = plain_glyphname
    else:
        print("create_smol_glyph: not creating %s.smol" % plain_glyphname)
        return
    glyph = font[glyphname]
    orig_width = glyph.width

    print("create_smol_glyph: creating %s.smol from %s" % (plain_glyphname, glyph.glyphname))

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

    # WIP: outlines in background
    # glyph.background = glyph.foreground

def check_all_glyph_bounds(font, width=None):
    for glyph in font.glyphs():
        check_glyph_bounds(glyph, width)

def check_glyph_bounds(glyph, width=None):
    [xmin, ymin, xmax, ymax] = glyph.boundingBox()
    print("check_all_glyph_bounds: %s %s; xmin = %d; xmax = %d; ymin = %d; ymax = %d" % (u(glyph.unicode), glyph.glyphname, xmin, xmax, ymin, ymax))
    height = glyph.font.ascent + glyph.font.descent
    if width is None:
        width = glyph.width
    if xmin < -width/2:
        print("check_all_glyph_bounds:     left")
    if xmax > width*3/2:
        print("check_all_glyph_bounds:     right")
    if ymin < (-glyph.font.descent - height/2):
        print("check_all_glyph_bounds:     bottom")
    if ymax > glyph.font.ascent + height/2:
        print("check_all_glyph_bounds:     top")
