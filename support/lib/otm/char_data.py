import os, re, fontforge

from otm.util import u

ATTRS = [
    "code",
    "variant",
    "orig_glyph_name",
    "orig_base_glyph_name",
    "norm_glyph_name",
    "norm_base_glyph_name",
    "svg_filename",
    "glyph",
    "name_is_arbitrary",
    "u_code",
    "u_orig_code",
    "orig_code",
    "orig_encoding",
    "orig_altuni",
    "font_path",
    "norm_code",
    "u_norm_code",
    "key",
    "font_weight",
    "font_familyname",
    "font_fullname",
    "font_fontname",
]

class CharData:
    def __init__(self, item=None):
        """Object constructor.

        if a CharData object is passed as the item parameter, clone
        that object.

        if a list or tuple is passed, assume it's a return value from
        converting a CharData object to a list(obj) or tuple(obj) and
        populate its values appropriately.

        if nothing is passed, create a blank object.

        The following are the attributes of this object.  Not all
        attributes are populated from all CharData subclasses.

            - code --- first parameter to font.createChar()

            - variant

            - orig_glyph_name

            - orig_base_glyph_name

            - norm_glyph_name --- second parameter to font.createChar()

            - norm_base_glyph_name

            - svg_filename

            - glyph

            - name_is_arbitrary

            - u_code

            - u_orig_code

            - orig_code

            - orig_encoding

            - orig_altuni

            - font_path

            - norm_code

            - u_norm_code

            - key
        """
        for attr in ATTRS:
            setattr(self, attr, None)
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
        u_code = self.u_code
        u_orig_code = self.u_orig_code
        return f"KEY={name:<24s} ({orig_name:<24s}) {u_code:<8s} ({u_orig_code:<8s})"
    def as_char(self):
        return (
            chr(self.norm_code)
            if
            type(self.norm_code) is int and self.norm_code >= 0 and self.norm_code < 0x110000
            else
            "(no char)"
        )

class GlyphNameCharData(CharData):
    def __init__(self, name):
        super().__init__()
        name_is_arbitrary = False
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
                name_is_arbitrary    = True
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
                name_is_arbitrary    = True
            else:
                char_name            = fontforge.nameFromUnicode(norm_code)
                norm_glyph_name      = char_name + variant
                norm_base_glyph_name = char_name
        else:
            raise Exception(f'glyph name {repr(name)} cannot be parsed')

        self.key                  = norm_glyph_name
        self.code                 = code
        self.u_code               = u(code)
        self.norm_code            = norm_code
        self.u_norm_code          = u(norm_code)
        self.orig_code            = None
        self.u_orig_code          = u(None)
        self.variant              = variant
        self.orig_glyph_name      = orig_glyph_name
        self.orig_base_glyph_name = orig_base_glyph_name
        self.norm_glyph_name      = norm_glyph_name
        self.norm_base_glyph_name = norm_base_glyph_name
        self.svg_filename         = None
        self.glyph                = None
        self.name_is_arbitrary    = name_is_arbitrary
        self.orig_altuni          = None
        self.orig_encoding        = None
        self.font_path            = None
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
        orig_altuni = glyph.altuni
        orig_encoding = glyph.encoding

        if match := re.fullmatch(r'([^\.]+)(\.[^\.]+)', glyph.glyphname):
            orig_base_glyph_name = match[1]
            variant = match[2]
        else:
            orig_base_glyph_name = glyph.glyphname
            variant = ""

        name_is_arbitrary = False

        norm_code = fontforge.unicodeFromName(orig_base_glyph_name)
        if norm_code < 0:
            norm_code = glyph.unicode
            name_is_arbitrary = True

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
        self.u_code               = u(code)

        self.norm_code            = norm_code
        self.u_norm_code          = u(norm_code)

        self.orig_code            = orig_code
        self.u_orig_code          = u(orig_code)

        self.variant              = variant
        self.orig_glyph_name      = orig_glyph_name
        self.orig_base_glyph_name = orig_base_glyph_name
        self.norm_glyph_name      = norm_glyph_name
        self.norm_base_glyph_name = norm_base_glyph_name
        self.svg_filename         = None
        self.glyph                = glyph
        self.name_is_arbitrary    = name_is_arbitrary
        self.orig_altuni          = orig_altuni
        self.orig_encoding        = orig_encoding

        font = self.glyph.font
        self.font_path            = os.path.relpath(font.path)
        self.font_fontname        = font.fontname
        self.font_fullname        = font.fullname
        self.font_familyname      = font.familyname
        self.font_weight          = font.weight
    def __str__(self):
        substr = super().__str__()
        return f"GLYPH:  {substr} from {self.font_path}"
