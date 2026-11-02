import os, re, fontforge

from otm.util import u, is_valid_code

ATTRS = [
    "code",
    "variant",
    "orig_glyph_name",
    "orig_base_glyph_name",
    "norm_glyph_name",
    "norm_base_glyph_name",
    "svg_filename",
    "glyph",
    "orig_code",
    "norm_code",
    "key",
]

class CharData:
    def __init__(self, item=None):
        for attr in ATTRS:
            setattr(self, attr, None)
            self.variant = ""
            self.code = -1
            self.orig_code = self.code
            self.norm_code = self.code
        if item is None:
            pass
        elif type(item) in [list, tuple]:
            for idx, attr_name in enumerate(ATTRS):
                if idx >= len(item):
                    break
                setattr(self, attr_name, item[idx])
        elif isinstance(item, CharData):
            for idx, attr_name in enumerate(ATTRS):
                setattr(self, attr_name, item.get(attr_name, None))
        else:
            raise TypeError(f"invalid item constructor param type: {type(item)}")
    def keys(self):
        return ATTRS
    def __getitem__(self, key):
        if key in self.keys():
            return getattr(self, key)
        return KeyError(key)
    def __iter__(self):
        for key in self.keys():
            yield getattr(self, key)
    def __str__(self):
        name = self.norm_glyph_name
        orig_name = self.orig_glyph_name
        u_code      = ("U+%04X" % self.code)      if is_valid_code(self.code)      else str(self.code)
        u_orig_code = ("U+%04X" % self.orig_code) if is_valid_code(self.orig_code) else str(self.orig_code)
        return f"<{self.__class__.__name__}> KEY={name:<24s} ({orig_name:<24s}) {u_code:<8s} ({u_orig_code:<8s})"
    def as_char(self):
        return (
            chr(self.norm_code)
            if
            is_valid_code(self.norm_code)
            else
            "(no char)"
        )

class GlyphCodeCharData(CharData):
    def __init__(self, code):
        super().__init__()
        if is_valid_code(code):
            name = fontforge.nameFromUnicode(code)
        else:
            name = "???"
        self.code                 = code
        self.variant              = ""
        self.orig_glyph_name      = name
        self.orig_base_glyph_name = name
        self.norm_glyph_name      = name
        self.norm_base_glyph_name = name
        self.svg_filename         = None
        self.glyph                = None
        self.orig_code            = code
        self.norm_code            = code
        self.key                  = name

class GlyphNameCharData(CharData):
    def __init__(self, name):
        super().__init__()
        if match := re.fullmatch(r'([0-9A-Fa-f]{4,})(\.[^\.]+)', name):
            code = -1
            norm_code = int(match[1], 16)
            variant = match[2]
            char_name = fontforge.nameFromUnicode(norm_code)
            orig_glyph_name      = char_name + variant
            orig_base_glyph_name = char_name
            norm_glyph_name      = char_name + variant
            norm_base_glyph_name = char_name
        elif match := re.fullmatch(r'[0-9A-Fa-f]{4,}', name):
            code = int(name, 16)
            norm_code = code
            variant = ""
            char_name = fontforge.nameFromUnicode(norm_code)
            orig_glyph_name      = char_name
            orig_base_glyph_name = char_name
            norm_glyph_name      = char_name
            norm_base_glyph_name = char_name
        elif match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', name):
            variant = match[2]
            orig_glyph_name      = match[1] + variant
            orig_base_glyph_name = match[1]
            code = -1
            norm_code = fontforge.unicodeFromName(match[1])
            if norm_code < 0:
                norm_glyph_name      = match[1] + variant
                norm_base_glyph_name = match[1]
            else:
                char_name = fontforge.nameFromUnicode(norm_code)
                norm_glyph_name      = char_name + variant
                norm_base_glyph_name = char_name
        elif match := re.fullmatch(r'([^\.]+)', name):
            variant = ""
            orig_glyph_name      = match[1] + variant
            orig_base_glyph_name = match[1]
            code = fontforge.unicodeFromName(match[1])
            norm_code = code
            if code < 0:
                norm_glyph_name      = match[1] + variant
                norm_base_glyph_name = match[1]
            else:
                char_name            = fontforge.nameFromUnicode(norm_code)
                norm_glyph_name      = char_name + variant
                norm_base_glyph_name = char_name
        else:
            raise Exception(f'glyph name {repr(name)} cannot be parsed')

        self.key                  = norm_glyph_name
        self.code                 = code
        self.norm_code            = norm_code
        self.orig_code            = None
        self.variant              = variant
        self.orig_glyph_name      = orig_glyph_name
        self.orig_base_glyph_name = orig_base_glyph_name
        self.norm_glyph_name      = norm_glyph_name
        self.norm_base_glyph_name = norm_base_glyph_name
        self.svg_filename         = None
        self.glyph                = None
    def __str__(self):
        substr = super().__str__()
        return f"NAMED:  {substr} from {self.svg_filename} => {self.as_createchar_call()}"
    def as_createchar_call(self):
        return f"font.createChar({repr(self.code)}, {repr(self.norm_glyph_name)}) # {repr(self.as_char())}"

class SVGCharData(GlyphNameCharData):
    def __init__(self, svg_filename):
        _, svg_basename = os.path.split(svg_filename)
        svg_stem, _ = os.path.splitext(svg_basename)
        super().__init__(svg_stem)
        self.svg_filename = svg_filename
    def __str__(self):
        substr = super().__str__()
        return f"SVG:    {substr[8:]}"

class GlyphCharData(CharData):
    def __init__(self, glyph):
        super().__init__()

        orig_glyph_name = glyph.glyphname
        orig_code = glyph.unicode

        if match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', glyph.glyphname):
            orig_base_glyph_name = match[1]
            variant = match[2]
        else:
            orig_base_glyph_name = glyph.glyphname
            variant = ""

        norm_code = fontforge.unicodeFromName(orig_base_glyph_name)
        if norm_code < 0:
            norm_code = glyph.unicode

        code = norm_code
        if variant != "":
            code = -1

        if code < 0:
            norm_base_glyph_name = orig_base_glyph_name
            norm_glyph_name      = orig_base_glyph_name + variant
        else:
            char_name = fontforge.nameFromUnicode(code)
            norm_base_glyph_name = char_name
            norm_glyph_name      = char_name + variant

        self.key = norm_glyph_name

        self.code                 = code
        self.norm_code            = norm_code
        self.orig_code            = orig_code
        self.variant              = variant
        self.orig_glyph_name      = orig_glyph_name
        self.orig_base_glyph_name = orig_base_glyph_name
        self.norm_glyph_name      = norm_glyph_name
        self.norm_base_glyph_name = norm_base_glyph_name
        self.svg_filename         = None
        self.glyph                = glyph

        font = self.glyph.font
    def __str__(self):
        substr = super().__str__()
        return f"GLYPH:  {substr}"
