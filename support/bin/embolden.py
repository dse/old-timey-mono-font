#!/usr/bin/env -S fontforge -quiet -lang=py -script
import fontforge, argparse, psMat, os, sys, numpy

sys.path.append(os.getenv("HOME") + "/git/dse.d/pyfontutils/lib")
from font_utils import parse_char_str, u, unicodedata_name

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--widen", "-w", type=int, default=96)
    parser.add_argument("--output-filename", "--output", "-o")
    args = parser.parse_args()
    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        base_unicode = glyph.unicode
        if base_unicode < 0:
            base_unicode = fontforge.unicodeFromName(glyph.glyphname.split(".", 1)[0])
        if (base_unicode in range(0x2190,  0x2200)  or # Arrows
            base_unicode in range(0x2500,  0x2580)  or # Box Drawing
            base_unicode in range(0x2580,  0x25a0)  or # Block Elements
            base_unicode in range(0x25a0,  0x2600)  or # Geometric Shapes
            base_unicode in range(0x2600,  0x2700)  or # Miscellaneous Symbols
            base_unicode in range(0x2700,  0x27c0)  or # Dingbats
            base_unicode in range(0x27f0,  0x2800)  or # Supplemental Arrows-A
            base_unicode in range(0x2800,  0x2900)  or # Braille Patterns
            base_unicode in range(0x2900,  0x2980)  or # Supplemental Arrows-A
            base_unicode in range(0x1fb00, 0x1fc00) or # Symbols for Legacy Computing
            base_unicode in [
                0x2620,         # SKULL AND CROSSBONES
                0x2622,         # RADIOACTIVE SIGN
                0x2623,         # BIOHAZARD SIGN
                0x00b6,         # PILCROW SIGN
                0x204b,         # REVERSED PILCROW SIGN
                0x204c,
                0x204d,
                0x203b,
                0x2055,
                0x205c,
                0xfffd,         # REPLACEMENT CHARACTER
                0x23ce,
                0x23cf,
                0x23e9,
                0x23ea,
                0x23ed,
                0x23ee,
                0x23ef,
                0x23f4,
                0x23f5,
                0x23f8,
                0x23f9,
                0x23fa,
                0x2386,
                0x2387,
                0x2325,
                0x2326,
                0x2327,
                0x232b,
                0x237c,
                0x2388,
            ]):
            if args.verbose:
                print(f'embolden.py: skipping {repr(glyph.glyphname)} (U+{base_unicode:04X})')
            continue
        if args.verbose:
            print(f'embolden.py: emboldening the {repr(glyph.glyphname)} glyph (U+{base_unicode:04X})')

        layer1 = glyph.foreground.dup()
        if args.verbose:
            print(f'             {len(layer1)} contours')
        layer1.transform(psMat.translate(-args.widen / 2, 0))
        layer2 = glyph.foreground.dup()
        layer2.transform(psMat.translate(args.widen / 2, 0))
        glyph.foreground = layer1 + layer2
        glyph.removeOverlap()

    orig_fontname = font.fontname
    orig_fullname = font.fullname

    font.fontname = font.fontname.split("-", 1)[0] + "-Bold"
    font.fullname = font.fullname.replace(" Bold", "").replace(" Light", "").replace(" Thin", "") + " Bold"

    print(f'{args.output_filename}: FONT NAME CHANGE: {orig_fontname} => {font.fontname}')
    print(f'{args.output_filename}: FULL NAME CHANGE: {orig_fullname} => {font.fullname}')

    font.weight = "Bold"
    font.os2_weight = 700

    panose = list(font.os2_panose)
    panose[2] = 7
    font.os2_panose = tuple(panose)

    output_filename = args.output_filename
    if output_filename is None:
        output_filename = args.filename
    if output_filename.endswith(".sfd"):
        if args.verbose:
            print(f'Saving {output_filename} ...')
        font.save(output_filename)
    else:
        if args.verbose:
            print(f'Generating {output_filename} ...')
        font.generate(output_filename)
    font.close()
        
main()
