import fontforge
import re
import os
import psMat

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

def import_svg_glyph(font, svg_filename):
    (codepoint, glyphname, real_codepoint, plain_glyphname, suffix) = parse_glyph_svg_filename(svg_filename)
    if codepoint is None and glyphname is None:
        return
    glyph = None
    if glyphname in font:
        glyph = font[glyphname]
        if len(glyph.references):
            print("WARNING: glyph %s U+%04X contains references but %s is present" % (glyphname, glyph.unicode, svg_filename))
            return
    glyph = font.createChar(codepoint, glyphname)
    glyph.foreground = fontforge.layer()
    orig_width = glyph.width
    font.strokedfont = True
    glyph.importOutlines(svg_filename)
    font.strokedfont = False
    glyph.width = orig_width

    # WIP: outlines in background
    # glyph.background = glyph.foreground

STROKE_WIDTH_BASIS = 96

def create_smol_glyph(font, codepoint):
    plain_glyphname = fontforge.nameFromUnicode(codepoint)
    simpl_glyphname = fontforge.nameFromUnicode(codepoint) + ".simpl"
    glyphname = None
    if simpl_glyphname in font:
        glyphname = simpl_glyphname
    elif plain_glyphname in font:
        glyphname = plain_glyphname
    else:
        return
    glyph = font[glyphname]
    orig_width = glyph.width

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
