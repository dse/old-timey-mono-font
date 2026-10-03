#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, glob, os, re, json, statistics

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output-filename", type=str, nargs="?", default=None)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--width", "--glyph-width", type=int, default=1008)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    svg_list = []
    glyph_list = []
    svg_dict = {}
    glyph_dict = {}

    font = fontforge.open(args.filename)
    svg_filenames = glob.glob("src/upright/**/*.svg", recursive=True)

    for svg_filename in svg_filenames:
        basename = os.path.basename(svg_filename)
        (stem, ext) = os.path.splitext(basename)

        if match := re.fullmatch(r'([0-9a-f]{4,})\.([^.]+)', stem, flags=re.I):
            code = int(match[1], 16)
            variant = match[2]
            final_glyphname = fontforge.nameFromUnicode(code) + "." + variant
        elif match := re.fullmatch(r'([0-9a-f]{4,})', stem, flags=re.I):
            code = int(match[1], 16)
            variant = None
            final_glyphname = fontforge.nameFromUnicode(code)
        elif match := re.fullmatch(r'([^.]+)\.([^.]+)', stem):
            code = fontforge.unicodeFromName(match[1])
            variant = match[2]
            final_glyphname = stem
        elif match := re.fullmatch(r'([^.]+)', stem):
            code = fontforge.unicodeFromName(match[1])
            variant = None
            final_glyphname = stem

        final_base_glyphname = final_glyphname.split(".", 1)[0]

        entry = [svg_filename, final_glyphname, final_base_glyphname, code, variant]
        if code < 0:
            svg_dict[final_glyphname] = entry
        else:
            svg_dict[code,variant] = entry
        svg_list.append(entry)

        if args.verbose >= 2:
            print(f'{svg_filename}: stem={stem}; code={code}; variant={variant}; glyphname={final_glyphname}')

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

    if args.verify:
        fail = False
        for svg_filename, glyphname, _, code, variant in svg_list:
            if code < 0:
                if glyphname not in glyph_dict:
                    print(f'{svg_filename}: no such glyph: {glyphname}')
                    fail = True
            else:
                if (code,variant) not in glyph_dict:
                    nom_glyphname = f'(U+{code:04X})'
                    if variant is not None:
                        nom_glyphname += "." + variant
                    print(f'{svg_filename}: no such glyph: {nom_glyphname}')
                    fail = True
        for svg_filename, glyphname, _, code, variant in glyph_list:
            if code < 0:
                if glyphname not in svg_dict:
                    print(f'{glyphname}: no SVG found')
                    fail = True
            else:
                if (code,variant) not in glyph_dict:
                    nom_glyphname = f'(U+{code:04X})'
                    if variant is not None:
                        nom_glyphname += "." + variant
                    print(f'{nom_glyphname}: no SVG found')
                    fail = True
        return

    glyphs = []
    for glyph in font.glyphs():
        if glyph.glyphname == ".notdef":
            continue
        if glyph.glyphname == ".null":
            continue
        if glyph.glyphname == "nonmarkingreturn":
            continue
        if glyph.width == 0:
            continue
        glyphs.append(glyph)

    if len(glyphs) == 0:
        new_glyph_width = args.width
    else:
        new_glyph_width = statistics.median([glyph.width for glyph in glyphs])

    glyphs_data = json.loads(open("src/data/glyphs.json").read())
    references_data = json.loads(open("src/data/references.json").read())

    for svg_filename, glyphname, _, code, variant in svg_list:
        if code < 0:
            glyph_entry = glyph_dict.get(glyphname)
            svg_entry = svg_dict.get(glyphname)
        else:
            glyph_entry = glyph_dict.get((code,variant))
            svg_entry = svg_dict.get((code,variant))
        (svg_filename, *_) = svg_entry
        if glyph_entry is None:
            glyph = font.createChar(code, glyphname)
        else:
            (*_, glyph) = glyph_entry

        import_glyphs = [glyph]
        if code == 0xfffd:      # U+FFFD REPLACEMENT CHARACTER
            import_glyphs.append(font.createChar(-1, ".notdef"))

        for glyph in import_glyphs:
            if args.verbose:
                print(f'{svg_filename}: importing into glyph {glyph.glyphname}')
            glyph.references = tuple()   # in case replacing reference glyph with contour glyph
            glyph.foreground = fontforge.layer()
            font.strokedfont = True # avoid expanding strokes to stroke-widths in SVG
            glyph.importOutlines(svg_filename)
            font.strokedfont = False
            glyph.width = new_glyph_width
            if args.verbose >= 2:
                print(f'{svg_filename}: finished importing into glyph {glyph.glyphname}')

    output_filename = args.output_filename if args.output_filename is not None else args.filename
    if output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{output_filename}: saving')
        font.save(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{output_filename}: generating')
        font.generate(output_filename)
        if args.verbose >= 2:
            print(f'{output_filename}: finished generating')

    font.close()

main()
