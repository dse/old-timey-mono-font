import fontforge, unicodedata, re

def parse_char_name(char_arg, plain_hex=False, keep_name=False, one_dash=False, filename=False, default=Exception):
    """
    Given a character name of some kind, or a numeric code point of some kind,
    return the following tuple:

        (glyph_code, glyph_name, code, name, variant)

    char_arg can be one of the following:
        - a float, if its value is a round integer, e.g., 128169.0
        - an int, e.g., 128169
        - a string one character long, such as "À".
        - a string two characters long if those characters are high and low surrogates.
            - example: "\ud83d\udca9"
        - a Unicode character name string, such as "LATIN CAPITAL LETTER A WITH GRAVE".
        - an Adobe glyph name string, such as "Agrave".
        - a hex codepoint string like "U+1F4A9" or "U1F4A9"
        - a hex codepoint string like "x1f4a9" or "0x1f4a9"
        - If plain_hex is true, a hex codepoint string like "1f4a9"

    Any of the string arguments can be suffixed with one of the following:
        - "." then a character variant code (typically 4 characters)
            example: "Agrave.ss07"

    Return Value

    glyph_code will be the glyph codepoint, which can be -1 if a character variant string is supplied.
    glyph_name will be the character's Adobe glyph name, suffixed by ".vari" if one is supplied.
    code will be the base codepoint of the glyph, or of the glyph of which this is a variant.
    name will be the base Adobe glyph name of the glyph, or of the glyph of which this is a variant.
    variant is either None or the character variant ("." not included)

    Parsing Options

    plain_hex - whether strings like "1f4a9" are allowed.
    double_dash - whether "--variant" suffixes are allowed.
    keep_name - whether alternate glyph names are preserved.
    default - supply a default return value in lieu of throwing an error if invalid data is supplied.
    """
    orig_char_arg = char_arg

    if filename:
        plain_hex = True
        one_dash = True

    if default == (None,):
        default = (None, None, None, None, None)
    elif default == (-1,):
        default = (-1, "", -1, "", None)

    if type(char_arg) == float:
        if char_arg != round(char_arg):
            if default is Exception:
                raise ValueError("invalid codepoint: %s" % orig_char_arg)
            return default
        char_arg = int(char_arg)
    if type(char_arg) == int:
        if char_arg not in range(0, 0x110000):
            if default is Exception:
                raise ValueError("invalid codepoint: %s" % orig_char_arg)
            return default
        name = fontforge.nameFromUnicode(char_arg)
        return (char_arg, name, char_arg, name, None)

    if type(char_arg) != str:
        if default is Exception:
            raise TypeError("invalid argument type: %s" % orig_char_arg)
        return default

    variant = None
    glyph_name = None
    if char_arg.find(".") in range(1, len(char_arg)-1):
        # first "." cannot be at start or end of string
        (char_arg, variant) = char_arg.split(".", 1)

    if one_dash:
        char_arg = char_arg.split("-")[0]
        variant = variant.split("-")[0]

    if len(char_arg) == 1:
        code = ord(char_arg)
        name = fontforge.nameFromUnicode(code)
    elif len(char_arg) == 2 and ord(char_arg[0]) in range(0xd800, 0xdc00) and ord(char_arg[1]) in range(0xdc00, 0xe000):
        code = 0x10000 + (ord(char_arg[0]) - 0xd800) * 1024 + ord(char_arg[1]) - 0xdc00
        name = fontforge.nameFromUnicode(code)
    elif match := re.fullmatch(r'(?:u\+?|0?x)([0-9a-f]+)', char_arg, flags=re.I):
        code = int(match[1], 16)
        name = fontforge.nameFromUnicode(code)
    elif plain_hex and re.fullmatch(r'[0-9a-f]+', char_arg, flags=re.I):
        code = int(char_arg, 16)
        name = fontforge.nameFromUnicode(code)
    elif (code := code_from_unicode_name(char_arg)) is not None:
        name = fontforge.nameFromUnicode(code)
    elif (code := fontforge.unicodeFromName(char_arg)) in range(0, 0x110000):
        name = char_arg if keep_name else fontforge.nameFromUnicode(code)
    else:
        if default is Exception:
            raise ValueError("invalid character: %s" % orig_char_arg)
        return default

    glyph_code = code if variant is None else -1
    glyph_name = name + ("" if variant is None else "." + variant)
    return (glyph_code, glyph_name, code, name, variant)

def code_from_unicode_name(name):
    try:
        return ord(unicodedata.lookup(name))
    except:
        return None

if __name__ == "__main__":
    assert(parse_char_name(65, default=None)                            == (65, "A", 65, "A", None))
    assert(parse_char_name(65.0, default=None)                          == (65, "A", 65, "A", None))
    assert(parse_char_name(65.4321, default=None)                       == None)
    assert(parse_char_name("", default=None)                            == None)
    assert(parse_char_name("fhqwhgads", default=None)                   == None)
    assert(parse_char_name("fhqwhgads", default=(-1,))                  == (-1, "", -1, "", None))
    assert(parse_char_name("fhqwhgads", default=(None,))                == (None, None, None, None, None))
    assert(parse_char_name({}, default=None)                            == None)
    assert(parse_char_name("uni0041", default=None)                     == (65, "A", 65, "A", None))
    assert(parse_char_name("A", default=None)                           == (65, "A", 65, "A", None))
    assert(parse_char_name("A.ss07", default=None)                      == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("LATIN CAPITAL LETTER A", default=None)      == (65, "A", 65, "A", None))
    assert(parse_char_name("LATIN CAPITAL LETTER A.ss07", default=None) == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("U+0041", default=None)                      == (65, "A", 65, "A", None))
    assert(parse_char_name("u+0041.ss07", default=None)                 == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("U0041", default=None)                       == (65, "A", 65, "A", None))
    assert(parse_char_name("u0041.ss07", default=None)                  == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("0x0041", default=None)                      == (65, "A", 65, "A", None))
    assert(parse_char_name("0X0041.ss07", default=None)                 == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("x0041", default=None)                       == (65, "A", 65, "A", None))
    assert(parse_char_name("X0041.ss07", default=None)                  == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("0041", default=None)                        == None)
    assert(parse_char_name("0041", plain_hex=True, default=None)        == (65, "A", 65, "A", None))
    assert(parse_char_name("0041.ss07", plain_hex=True, default=None)   == (-1, "A.ss07", 65, "A", "ss07"))
    assert(parse_char_name("\ud83d\udca9", default=None)                == (128169, "u1F4A9", 128169, "u1F4A9", None))
    assert(parse_char_name("\ud83d\udca9.ss07", default=None)           == (-1, "u1F4A9.ss07", 128169, "u1F4A9", "ss07"))
    assert(parse_char_name(".ss07", default=None)                       == None)
    assert(parse_char_name("period.", default=None)                     == None)
    assert(parse_char_name(-1, default=None)                            == None)
    assert(parse_char_name(0, default=None)                             == (0, "uni0000", 0, "uni0000", None))
    assert(parse_char_name(1, default=None)                             == (1, "uni0001", 1, "uni0001", None))
    assert(parse_char_name(0x10ffff, default=None)                      == (0x10ffff, "u10FFFF", 0x10ffff, "u10FFFF", None))
    assert(parse_char_name(0x110000, default=None)                      == None)
    print("OK")
