import os, re, fontforge

from otm.util import u, is_valid_code

ATTRS = [
    "code",
    "variant",
    "name",
    "svg_filename",
    "glyph",
    "_norm_code",
    "key",
    "sort_key",
]

class CharData:

    def __init__(self, *args, **kwargs):
        self._real_init(*args, *kwargs)
        if is_valid_code(self.code):
            self.sort_key = (0, self.code)
            self.key = self.name
        elif is_valid_code(self._norm_code):
            self.sort_key = (1, self.variant, self.code)
            self.key = self.name
        else:
            self.sort_key = (2, self.name)
            self.key = self.name

    # we override _real_init in subclasses so the code in __init__
    # that sets self.sort_key is always called after all
    # initialization.
    def _real_init(self):
        for attr in ATTRS:
            setattr(self, attr, None)
        self.variant    = ""
        self.code       = -1
        self._norm_code = self.code

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
        name = self.name
        u_code = ("U+%04X" % self.code) if is_valid_code(self.code) else str(self.code)
        return f"<{self.__class__.__name__}> KEY={name:<24s} {u_code:<8s}"

    def as_char(self):
        return (
            chr(self._norm_code)
            if
            is_valid_code(self._norm_code)
            else
            "(no char)"
        )

class GlyphCodeCharData(CharData):
    def _real_init(self, code):
        super()._real_init()
        if is_valid_code(code):
            name = fontforge.nameFromUnicode(code)
        else:
            name = "???"
        self.code         = code
        self.variant      = ""
        self.name         = name
        self.svg_filename = None
        self.glyph        = None
        self._norm_code   = code

class GlyphNameCharData(CharData):
    def _real_init(self, name):
        super()._real_init()
        if match := re.fullmatch(r'([0-9A-Fa-f]{4,})(\.[^\.]+)', name):
            code                 = -1
            norm_code            = int(match[1], 16)
            variant              = match[2]
            char_name            = fontforge.nameFromUnicode(norm_code)
            orig_glyph_name      = char_name + variant
            name                 = char_name + variant
        elif match := re.fullmatch(r'[0-9A-Fa-f]{4,}', name):
            code                 = int(name, 16)
            norm_code            = code
            variant              = ""
            char_name            = fontforge.nameFromUnicode(norm_code)
            orig_glyph_name      = char_name
            name                 = char_name
        elif match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', name):
            variant              = match[2]
            orig_glyph_name      = match[1] + variant
            code                 = -1
            norm_code            = fontforge.unicodeFromName(match[1])
            if norm_code < 0:
                name                 = match[1] + variant
            else:
                char_name            = fontforge.nameFromUnicode(norm_code)
                name                 = char_name + variant
        elif match := re.fullmatch(r'([^\.]+)', name):
            variant              = ""
            orig_glyph_name      = match[1] + variant
            code                 = fontforge.unicodeFromName(match[1])
            norm_code            = code
            if code < 0:
                name                 = match[1] + variant
            else:
                char_name            = fontforge.nameFromUnicode(norm_code)
                name                 = char_name + variant
        else:
            raise Exception(f'glyph name {repr(name)} cannot be parsed')
        self.code         = code
        self._norm_code   = norm_code
        self.variant      = variant
        self.name         = name
        self.svg_filename = None
        self.glyph        = None
    def __str__(self):
        substr = super().__str__()
        return f"NAMED:  {substr} from {self.svg_filename} => {self.as_createchar_call()}"
    def as_createchar_call(self):
        return f"font.createChar({repr(self.code)}, {repr(self.name)}) # {repr(self.as_char())}"

class SVGCharData(GlyphNameCharData):
    def _real_init(self, svg_filename):
        _, svg_basename = os.path.split(svg_filename)
        svg_stem, _ = os.path.splitext(svg_basename)
        super()._real_init(svg_stem)
        self.svg_filename = svg_filename
    def __str__(self):
        substr = super().__str__()
        return f"SVG:    {substr[8:]}"

class GlyphCharData(CharData):
    def _real_init(self, glyph):
        super()._real_init()
        orig_glyph_name = glyph.glyphname
        orig_code       = glyph.unicode
        if match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', glyph.glyphname):
            orig_base_glyph_name = match[1]
            variant              = match[2]
        else:
            orig_base_glyph_name = glyph.glyphname
            variant              = ""
        norm_code = fontforge.unicodeFromName(orig_base_glyph_name)
        if norm_code < 0:
            norm_code = glyph.unicode
        code = norm_code
        if variant != "":
            code = -1
        if code < 0:
            name                 = orig_base_glyph_name + variant
        else:
            char_name            = fontforge.nameFromUnicode(code)
            name                 = char_name + variant
        self.code         = code
        self._norm_code   = norm_code
        self.variant      = variant
        self.name         = name
        self.svg_filename = None
        self.glyph        = glyph

    def __str__(self):
        substr = super().__str__()
        return f"GLYPH:  {substr}"
