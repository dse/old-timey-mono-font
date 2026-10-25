import fontforge, os, re, glob

def index_svg_files(filenames=None, args=None):
    if filenames is None:
        filenames = glob.glob("src/upright/**/*.svg", recursive=True)

    svg_list = []
    svg_dict = {}

    for filename in filenames:
        basename = os.path.basename(filename)
        (stem, ext) = os.path.splitext(basename)

        if match := re.fullmatch(r'([0-9a-f]{4,})\.([^.]+)', stem, flags=re.I):
            # <hex>.<variant>.svg
            code = int(match[1], 16)
            variant = match[2]
            final_glyphname = fontforge.nameFromUnicode(code) + "." + variant
        elif match := re.fullmatch(r'([0-9a-f]{4,})', stem, flags=re.I):
            # <hex>.svg
            code = int(match[1], 16)
            variant = None
            final_glyphname = fontforge.nameFromUnicode(code)
        elif match := re.fullmatch(r'([^.]+)\.([^.]+)', stem):
            # <name>.<variant>.svg
            code = fontforge.unicodeFromName(match[1])
            variant = match[2]
            final_glyphname = stem
        elif match := re.fullmatch(r'([^.]+)', stem):
            # <name>.svg
            code = fontforge.unicodeFromName(match[1])
            variant = None
            final_glyphname = stem

        final_base_glyphname = final_glyphname.split(".", 1)[0]

        entry = [filename, final_glyphname, final_base_glyphname, code, variant]
        if code < 0:
            svg_dict[final_glyphname] = entry
        else:
            svg_dict[code,variant] = entry
        svg_list.append(entry)

        if args is not None and args.verbose >= 2:
            print(f'{filename}: stem={stem}; code={code}; variant={variant}; glyphname={final_glyphname}')

    return svg_list, svg_dict

def index_glyphs(font):
    glyph_list = []
    glyph_dict = {}

    for glyph in font.glyphs():
        if "." in glyph.glyphname:
            base_glyphname, variant = glyph.glyphname.split(".", 1)
        else:
            base_glyphname, variant = glyph.glyphname, None
        code = glyph.unicode
        if code < 0:
            code = fontforge.unicodeFromName(base_glyphname)

        entry = [None, glyph.glyphname, base_glyphname, code, variant, glyph]
        if code < 0:
            glyph_dict[glyph.glyphname] = entry
        else:
            glyph_dict[code,variant] = entry
        glyph_list.append(entry)

    return glyph_list, glyph_dict

def verify(svg_list, svg_dict, glyph_list, glyph_dict):
    success = True
    for svg_filename, glyphname, _, code, variant in svg_list:
        if code < 0:
            if glyphname not in glyph_dict:
                print(f'{svg_filename}: no such glyph: {glyphname}')
                success = False
        else:
            if (code,variant) not in glyph_dict:
                nom_glyphname = f'(U+{code:04X})'
                if variant is not None:
                    nom_glyphname += "." + variant
                print(f'{svg_filename}: no such glyph: {nom_glyphname}')
                success = False
    for svg_filename, glyphname, _, code, variant, _ in glyph_list:
        if code < 0:
            if glyphname not in svg_dict:
                print(f'{glyphname}: no SVG found')
                success = False
        else:
            if (code,variant) not in glyph_dict:
                nom_glyphname = f'(U+{code:04X})'
                if variant is not None:
                    nom_glyphname += "." + variant
                print(f'{nom_glyphname}: no SVG found')
                success = False
    return success
