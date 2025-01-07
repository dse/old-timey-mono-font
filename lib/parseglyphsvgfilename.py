__all__ = ["parse_glyph_svg_filename"]

import os
import re
import fontforge

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
