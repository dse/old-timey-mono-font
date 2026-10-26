import os, re
from glob import glob

def index_svg_files(filenames):
    if len(filenames) == 0:
        filenames = glob("src/upright/**/*.svg")
    else:
        glob_list = [glob(f) for f in filenames]
        filenames = []
        for item in glob_list:
            filenames += item
    svg_list = []
    svg_dict = {
        "filename": {},
        "char": {},
    }
    for filename in filenames:
        basename = os.path.basename(filename)
        (glyphname, ext) = os.path.splitext(basename)
        if "." in glyphname:
            (name_or_code, variant) = glyphname.split(".", 1)
        else:
            name_or_code = glyphname
            variant = None
        if re.fullmatch('[0-9a-f]{4,}', name_or_code, flags=re.I):
            code = int(name_or_code, 16)
            name = fontforge.nameFromUnicode(code)
        else:
            code = fontforge.unicodeFromName(name_or_code)
            name = fontforge.nameFromUnicode(code)
        if variant is not None:
            code = -1
        item = {
            "fileame": filename,
            "variant": variant,
            "code": code,
            "name": name,
        }
        svg_list.append(item)
        svg_dict["filename"][filename] = item
        svg_dict["char"][name,variant] = item
    return svg_list, svg_dict

def index_glyphs(font):
    glyph_list = []
    glyph_dict = {
        "char": {}
    }
    for glyph in font.glyphs():
        glyphname = glyph.glyphname
        if "." in glyphname:
            (name, variant) = glyphname.split(".", 1)
        else:
            name = glyphname
            variant = None
        code = glyph.unicode
        item = {
            "code": code,
            "name": name,
            "variant": variant,
        }
        glyph_dict["char"][name,variant] = item
    return glyph_list, glyph_dict

def verify_font(svg_list, svg_dict, glyph_list, glyph_dict):
    success = True
    for key in svg_dict["char"].keys():
        if key not in glyph_dict["char"]:
            filename = svg_dict["char"][key]["filename"]
            print(f"{key} from {filename} is not in the font")
            success = False
    for key in glyph_dict["char"].keys():
        if key not in svg_dict["char"]:
            print(f"{key} in the font is not in the svg directory tree")
            success = False
    return success
