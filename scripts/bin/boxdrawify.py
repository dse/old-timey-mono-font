#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, unicodedata, statistics, math

STROKE_WIDTH = 96
HEAVY_STROKE_WIDTH = 288

KAPPA = 0.5519150244935105707435627

def main():
    global HEAVY_STROKE_WIDTH, STROKE_WIDTH

    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-w", "--stroke-width", "--width", type=int, default=96)
    args = parser.parse_args()

    if args.stroke_width is not None:
        STROKE_WIDTH = args.stroke_width

    font = fontforge.open(args.filename)

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

    new_glyph_width = round(statistics.median([glyph.width for glyph in glyphs]))

    x_heavy_thickness = round(new_glyph_width / math.sqrt(6))
    y_heavy_thickness = round(font.em / math.sqrt(6))
    HEAVY_STROKE_WIDTH = min(x_heavy_thickness, y_heavy_thickness)

    for code in range(0x2500, 0x2580):
        glyph = font.createChar(code)
        glyph.foreground = fontforge.layer()
        glyph.width = new_glyph_width

    draw_2500(font.createChar(0x2500))
    draw_2501(font.createChar(0x2501))
    draw_2502(font.createChar(0x2502))
    draw_2503(font.createChar(0x2503))
    draw_2504(font.createChar(0x2504))
    draw_2505(font.createChar(0x2505))
    draw_2506(font.createChar(0x2506))
    draw_2507(font.createChar(0x2507))
    draw_2508(font.createChar(0x2508))
    draw_2509(font.createChar(0x2509))
    draw_250A(font.createChar(0x250a))
    draw_250B(font.createChar(0x250b))
    draw_250C(font.createChar(0x250c))
    draw_250D(font.createChar(0x250d))
    draw_250E(font.createChar(0x250e))
    draw_250F(font.createChar(0x250f))
    draw_2510(font.createChar(0x2510))
    draw_2511(font.createChar(0x2511))
    draw_2512(font.createChar(0x2512))
    draw_2513(font.createChar(0x2513))
    draw_2514(font.createChar(0x2514))
    draw_2515(font.createChar(0x2515))
    draw_2516(font.createChar(0x2516))
    draw_2517(font.createChar(0x2517))
    draw_2518(font.createChar(0x2518))
    draw_2519(font.createChar(0x2519))
    draw_251A(font.createChar(0x251a))
    draw_251B(font.createChar(0x251b))
    draw_251C(font.createChar(0x251c))
    draw_251D(font.createChar(0x251d))
    draw_251E(font.createChar(0x251e))
    draw_251F(font.createChar(0x251f))
    draw_2520(font.createChar(0x2520))
    draw_2521(font.createChar(0x2521))
    draw_2522(font.createChar(0x2522))
    draw_2523(font.createChar(0x2523))
    draw_2524(font.createChar(0x2524))
    draw_2525(font.createChar(0x2525))
    draw_2526(font.createChar(0x2526))
    draw_2527(font.createChar(0x2527))
    draw_2528(font.createChar(0x2528))
    draw_2529(font.createChar(0x2529))
    draw_252A(font.createChar(0x252a))
    draw_252B(font.createChar(0x252b))
    draw_252C(font.createChar(0x252c))
    draw_252D(font.createChar(0x252d))
    draw_252E(font.createChar(0x252e))
    draw_252F(font.createChar(0x252f))
    draw_2530(font.createChar(0x2530))
    draw_2531(font.createChar(0x2531))
    draw_2532(font.createChar(0x2532))
    draw_2533(font.createChar(0x2533))
    draw_2534(font.createChar(0x2534))
    draw_2535(font.createChar(0x2535))
    draw_2536(font.createChar(0x2536))
    draw_2537(font.createChar(0x2537))
    draw_2538(font.createChar(0x2538))
    draw_2539(font.createChar(0x2539))
    draw_253A(font.createChar(0x253a))
    draw_253B(font.createChar(0x253b))
    draw_253C(font.createChar(0x253c))
    draw_253D(font.createChar(0x253d))
    draw_253E(font.createChar(0x253e))
    draw_253F(font.createChar(0x253f))
    draw_2540(font.createChar(0x2540))
    draw_2541(font.createChar(0x2541))
    draw_2542(font.createChar(0x2542))
    draw_2543(font.createChar(0x2543))
    draw_2544(font.createChar(0x2544))
    draw_2545(font.createChar(0x2545))
    draw_2546(font.createChar(0x2546))
    draw_2547(font.createChar(0x2547))
    draw_2548(font.createChar(0x2548))
    draw_2549(font.createChar(0x2549))
    draw_254A(font.createChar(0x254a))
    draw_254B(font.createChar(0x254b))
    draw_254C(font.createChar(0x254c))
    draw_254D(font.createChar(0x254d))
    draw_254E(font.createChar(0x254e))
    draw_254F(font.createChar(0x254f))
    draw_2550(font.createChar(0x2550))
    draw_2551(font.createChar(0x2551))
    draw_2552(font.createChar(0x2552))
    draw_2553(font.createChar(0x2553))
    draw_2554(font.createChar(0x2554))
    draw_2555(font.createChar(0x2555))
    draw_2556(font.createChar(0x2556))
    draw_2557(font.createChar(0x2557))
    draw_2558(font.createChar(0x2558))
    draw_2559(font.createChar(0x2559))
    draw_255A(font.createChar(0x255a))
    draw_255B(font.createChar(0x255b))
    draw_255C(font.createChar(0x255c))
    draw_255D(font.createChar(0x255d))
    draw_255E(font.createChar(0x255e))
    draw_255F(font.createChar(0x255f))
    draw_2560(font.createChar(0x2560))
    draw_2561(font.createChar(0x2561))
    draw_2562(font.createChar(0x2562))
    draw_2563(font.createChar(0x2563))
    draw_2564(font.createChar(0x2564))
    draw_2565(font.createChar(0x2565))
    draw_2566(font.createChar(0x2566))
    draw_2567(font.createChar(0x2567))
    draw_2568(font.createChar(0x2568))
    draw_2569(font.createChar(0x2569))
    draw_256A(font.createChar(0x256a))
    draw_256B(font.createChar(0x256b))
    draw_256C(font.createChar(0x256c))
    draw_256D(font.createChar(0x256d))
    draw_256E(font.createChar(0x256e))
    draw_256F(font.createChar(0x256f))
    draw_2570(font.createChar(0x2570))
    draw_2571(font.createChar(0x2571))
    draw_2572(font.createChar(0x2572))
    draw_2573(font.createChar(0x2573))
    draw_2574(font.createChar(0x2574))
    draw_2575(font.createChar(0x2575))
    draw_2576(font.createChar(0x2576))
    draw_2577(font.createChar(0x2577))
    draw_2578(font.createChar(0x2578))
    draw_2579(font.createChar(0x2579))
    draw_257A(font.createChar(0x257a))
    draw_257B(font.createChar(0x257b))
    draw_257C(font.createChar(0x257c))
    draw_257D(font.createChar(0x257d))
    draw_257E(font.createChar(0x257e))
    draw_257F(font.createChar(0x257f))

    for code in range(0x2500, 0x2580):
        glyph = font.createChar(code)
        glyph.removeOverlap()
        glyph.simplify()

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

def draw_2500(glyph): draw_horiz(glyph, STROKE_WIDTH)
def draw_2501(glyph): draw_horiz(glyph, HEAVY_STROKE_WIDTH)
def draw_2502(glyph): draw_vert(glyph, STROKE_WIDTH)
def draw_2503(glyph): draw_vert(glyph, HEAVY_STROKE_WIDTH)
def draw_2504(glyph): draw_horiz_dashed(glyph, STROKE_WIDTH, 3)
def draw_2505(glyph): draw_horiz_dashed(glyph, HEAVY_STROKE_WIDTH, 3)
def draw_2506(glyph): draw_vert_dashed(glyph, STROKE_WIDTH, 3)
def draw_2507(glyph): draw_vert_dashed(glyph, HEAVY_STROKE_WIDTH, 3)
def draw_2508(glyph): draw_horiz_dashed(glyph, STROKE_WIDTH, 4)
def draw_2509(glyph): draw_horiz_dashed(glyph, HEAVY_STROKE_WIDTH, 4)
def draw_250A(glyph): draw_vert_dashed(glyph, STROKE_WIDTH, 4)
def draw_250B(glyph): draw_vert_dashed(glyph, HEAVY_STROKE_WIDTH, 4)

def draw_250C(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_250D(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_250E(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)
def draw_250F(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)
def draw_2510(glyph): draw_boxdraw(glyph, 0, 0, STROKE_WIDTH, STROKE_WIDTH)
def draw_2511(glyph): draw_boxdraw(glyph, 0, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2512(glyph): draw_boxdraw(glyph, 0, 0, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2513(glyph): draw_boxdraw(glyph, 0, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2514(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, 0, 0)
def draw_2515(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, 0)
def draw_2516(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0, 0)
def draw_2517(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, 0)
def draw_2518(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, 0, STROKE_WIDTH)
def draw_2519(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, 0, HEAVY_STROKE_WIDTH)
def draw_251A(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, 0, STROKE_WIDTH)
def draw_251B(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, 0, HEAVY_STROKE_WIDTH)

def draw_251C(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_251D(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_251E(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_251F(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)
def draw_2520(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)
def draw_2521(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0)
def draw_2522(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)
def draw_2523(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0)

def draw_2524(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, STROKE_WIDTH, STROKE_WIDTH)
def draw_2525(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2526(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH, STROKE_WIDTH)
def draw_2527(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2528(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2529(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_252A(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_252B(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)

def draw_252C(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_252D(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_252E(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_252F(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2530(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2531(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2532(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2533(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)

def draw_2534(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, 0, STROKE_WIDTH)
def draw_2535(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH)
def draw_2536(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH)
def draw_2537(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH)
def draw_2538(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0, STROKE_WIDTH)
def draw_2539(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH)
def draw_253A(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH)
def draw_253B(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH)

def draw_253C(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_253D(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_253E(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_253F(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2540(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_2541(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2542(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2543(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2544(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, STROKE_WIDTH)
def draw_2545(glyph): draw_boxdraw(glyph, STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2546(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_2547(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2548(glyph): draw_boxdraw(glyph, STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_2549(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)
def draw_254A(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, STROKE_WIDTH)
def draw_254B(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH, HEAVY_STROKE_WIDTH)

def draw_254C(glyph): draw_horiz_dashed(glyph, STROKE_WIDTH, 2)
def draw_254D(glyph): draw_horiz_dashed(glyph, HEAVY_STROKE_WIDTH, 2)
def draw_254E(glyph): draw_vert_dashed(glyph, STROKE_WIDTH, 2)
def draw_254F(glyph): draw_vert_dashed(glyph, HEAVY_STROKE_WIDTH, 2)

def draw_2550(glyph): draw_boxdraw_double(glyph, 0, 2, 0, 2)
def draw_2551(glyph): draw_boxdraw_double(glyph, 2, 0, 2, 0)
def draw_2552(glyph): draw_boxdraw_double(glyph, 0, 2, 1, 0)
def draw_2553(glyph): draw_boxdraw_double(glyph, 0, 1, 2, 0)
def draw_2554(glyph): draw_boxdraw_double(glyph, 0, 2, 2, 0)
def draw_2555(glyph): draw_boxdraw_double(glyph, 0, 0, 1, 2)
def draw_2556(glyph): draw_boxdraw_double(glyph, 0, 0, 2, 1)
def draw_2557(glyph): draw_boxdraw_double(glyph, 0, 0, 2, 2)
def draw_2558(glyph): draw_boxdraw_double(glyph, 1, 2, 0, 0)
def draw_2559(glyph): draw_boxdraw_double(glyph, 2, 1, 0, 0)
def draw_255A(glyph): draw_boxdraw_double(glyph, 2, 2, 0, 0)
def draw_255B(glyph): draw_boxdraw_double(glyph, 1, 0, 0, 2)
def draw_255C(glyph): draw_boxdraw_double(glyph, 2, 0, 0, 1)
def draw_255D(glyph): draw_boxdraw_double(glyph, 2, 0, 0, 2)
def draw_255E(glyph): draw_boxdraw_double(glyph, 1, 2, 1, 0)
def draw_255F(glyph): draw_boxdraw_double(glyph, 2, 1, 2, 0)
def draw_2560(glyph): draw_boxdraw_double(glyph, 2, 2, 2, 0)
def draw_2561(glyph): draw_boxdraw_double(glyph, 1, 0, 1, 2)
def draw_2562(glyph): draw_boxdraw_double(glyph, 2, 0, 2, 1)
def draw_2563(glyph): draw_boxdraw_double(glyph, 2, 0, 2, 2)
def draw_2564(glyph): draw_boxdraw_double(glyph, 0, 2, 1, 2)
def draw_2565(glyph): draw_boxdraw_double(glyph, 0, 1, 2, 1)
def draw_2566(glyph): draw_boxdraw_double(glyph, 0, 2, 2, 2)
def draw_2567(glyph): draw_boxdraw_double(glyph, 1, 2, 0, 2)
def draw_2568(glyph): draw_boxdraw_double(glyph, 2, 1, 0, 1)
def draw_2569(glyph): draw_boxdraw_double(glyph, 2, 2, 0, 2)
def draw_256A(glyph): draw_boxdraw_double(glyph, 1, 2, 1, 2)
def draw_256B(glyph): draw_boxdraw_double(glyph, 2, 1, 2, 1)
def draw_256C(glyph): draw_boxdraw_double(glyph, 2, 2, 2, 2)

def draw_256D(glyph): draw_corner_arc(glyph, upper=False, left=False)
def draw_256E(glyph): draw_corner_arc(glyph, upper=False, left=True)
def draw_256F(glyph): draw_corner_arc(glyph, upper=True, left=True)
def draw_2570(glyph): draw_corner_arc(glyph, upper=True, left=False)

def draw_2571(glyph):
    draw_solidus(glyph, reverse=False)
def draw_2572(glyph):
    draw_solidus(glyph, reverse=True)
def draw_2573(glyph):
    draw_solidus(glyph, reverse=False)
    draw_solidus(glyph, reverse=True)

def draw_2574(glyph): draw_boxdraw(glyph, 0, 0, 0, STROKE_WIDTH)
def draw_2575(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, 0, 0)
def draw_2576(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, 0, 0)
def draw_2577(glyph): draw_boxdraw(glyph, 0, 0, STROKE_WIDTH, 0)
def draw_2578(glyph): draw_boxdraw(glyph, 0, 0, 0, HEAVY_STROKE_WIDTH)
def draw_2579(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, 0, 0)
def draw_257A(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, 0, 0)
def draw_257B(glyph): draw_boxdraw(glyph, 0, 0, HEAVY_STROKE_WIDTH, 0)
def draw_257C(glyph): draw_boxdraw(glyph, 0, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH)
def draw_257D(glyph): draw_boxdraw(glyph, STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH, 0)
def draw_257E(glyph): draw_boxdraw(glyph, 0, STROKE_WIDTH, 0, HEAVY_STROKE_WIDTH)
def draw_257F(glyph): draw_boxdraw(glyph, HEAVY_STROKE_WIDTH, 0, STROKE_WIDTH, 0)

def draw_horiz(glyph, stroke_width):
    font = glyph.font
    x1 = 0
    x2 = glyph.width
    y1 = round((font.ascent - font.descent) / 2 - stroke_width/2)
    y2 = round((font.ascent - font.descent) / 2 + stroke_width/2)
    draw_rect(glyph, x1, y1, x2, y2)

def draw_vert(glyph, stroke_width):
    font = glyph.font
    x1 = round(glyph.width/2 - stroke_width/2)
    x2 = round(glyph.width/2 + stroke_width/2)
    y1 = -font.descent
    y2 = font.ascent
    draw_rect(glyph, x1, y1, x2, y2)

def draw_horiz_dashed(glyph, stroke_width, dash_count):
    font = glyph.font
    y1 = round((font.ascent - font.descent) / 2 - stroke_width/2)
    y2 = round((font.ascent - font.descent) / 2 + stroke_width/2)
    for i in range(0, dash_count):
        x1 = round(glyph.width * (4*i+1) / (dash_count*4))
        x2 = round(glyph.width * (4*i+3) / (dash_count*4))
        draw_rect(glyph, x1, y1, x2, y2)

def draw_vert_dashed(glyph, stroke_width, dash_count):
    font = glyph.font
    x1 = round(glyph.width/2 - stroke_width/2)
    x2 = round(glyph.width/2 + stroke_width/2)
    for i in range(0, dash_count):
        y1 = round(-font.descent + font.em * (4*i+1) / (dash_count*4))
        y2 = round(-font.descent + font.em * (4*i+3) / (dash_count*4))
        draw_rect(glyph, x1, y1, x2, y2)

def draw_right_piece(glyph, stroke_width, x):
    print(f'    draw_right_piece({glyph.glyphname}, {stroke_width}, x={x})')
    font = glyph.font
    y1 = round(-font.descent + font.em/2 - stroke_width/2)
    y2 = round(-font.descent + font.em/2 + stroke_width/2)
    x1 = x
    x2 = glyph.width
    draw_rect(glyph, x1, y1, x2, y2)

def draw_left_piece(glyph, stroke_width, x):
    print(f'    draw_left_piece({glyph.glyphname}, {stroke_width}, x={x})')
    font = glyph.font
    y1 = round(-font.descent + font.em/2 - stroke_width/2)
    y2 = round(-font.descent + font.em/2 + stroke_width/2)
    x1 = 0
    x2 = x
    draw_rect(glyph, x1, y1, x2, y2)

def draw_top_piece(glyph, stroke_width, y):
    print(f'    draw_top_piece({glyph.glyphname}, {stroke_width}, y={y})')
    font = glyph.font
    x1 = round(glyph.width/2 - stroke_width/2)
    x2 = round(glyph.width/2 + stroke_width/2)
    y1 = y
    y2 = font.ascent
    draw_rect(glyph, x1, y1, x2, y2)

def draw_bottom_piece(glyph, stroke_width, y):
    print(f'    draw_bottom_piece({glyph.glyphname}, {stroke_width}, y={y})')
    font = glyph.font
    x1 = round(glyph.width/2 - stroke_width/2)
    x2 = round(glyph.width/2 + stroke_width/2)
    y1 = -font.descent
    y2 = y
    draw_rect(glyph, x1, y1, x2, y2)
    
def draw_boxdraw(glyph, top_stroke_width, right_stroke_width, bottom_stroke_width, left_stroke_width):
    print(f'draw_boxdraw({glyph.glyphname}, {top_stroke_width}, {right_stroke_width}, {bottom_stroke_width}, {left_stroke_width})')
    font = glyph.font
    if top_stroke_width:
        y = round(-font.descent + font.em/2 - max(left_stroke_width, right_stroke_width) / 2)
        draw_top_piece(glyph, top_stroke_width, y)
    if right_stroke_width:
        x = round(glyph.width/2 - max(top_stroke_width, bottom_stroke_width) / 2)
        draw_right_piece(glyph, right_stroke_width, x)
    if bottom_stroke_width:
        y = round(-font.descent + font.em/2 + max(left_stroke_width, right_stroke_width) / 2)
        draw_bottom_piece(glyph, bottom_stroke_width, y)
    if left_stroke_width:
        x = round(glyph.width/2 + max(top_stroke_width, bottom_stroke_width) / 2)
        draw_left_piece(glyph, left_stroke_width, x)

def draw_corner_arc(glyph, upper=True, left=True):
    font = glyph.font
    radius = round(min(font.em/2, glyph.width/2))
    r1 = round(radius - STROKE_WIDTH/2)
    r2 = round(radius + STROKE_WIDTH/2)
    x_left = round(glyph.width/2 - STROKE_WIDTH/2)
    x_right = round(glyph.width/2 + STROKE_WIDTH/2)
    y_bottom = round(-font.descent + font.em/2 - STROKE_WIDTH/2)
    y_top = round(-font.descent + font.em/2 + STROKE_WIDTH/2)

    (x0, y0) = (0,            y_top)
    (x1, y1) = (0 + r1*KAPPA, y_top)
    (x2, y2) = (x_left,       y_top + r1 - r1*KAPPA)
    (x3, y3) = (x_left,       y_top + r1)
    (x4, y4) = (x_left,       font.ascent)
    (x5, y5) = (x_right,      font.ascent)
    (x6, y6) = (x_right,      y_bottom + r2)
    (x7, y7) = (x_right,      y_bottom + r2 - r2*KAPPA)
    (x8, y8) = (0 + r2*KAPPA, y_bottom)
    (x9, y9) = (0,            y_bottom)

    if not upper:
        (y0, y1, y2, y3, y4, y5, y6, y7, y8, y9) = [
            font.ascent - font.descent - y
            for y in (y0, y1, y2, y3, y4, y5, y6, y7, y8, y9)
        ]

    if not left:
        (x0, x1, x2, x3, x4, x5, x6, x7, x8, x9) = [
            glyph.width - x for x in (x0, x1, x2, x3, x4, x5, x6, x7, x8, x9)
        ]

    point0 = (x0, y0)
    point1 = (x1, y1)
    point2 = (x2, y2)
    point3 = (x3, y3)
    point4 = (x4, y4)
    point5 = (x5, y5)
    point6 = (x6, y6)
    point7 = (x7, y7)
    point8 = (x8, y8)
    point9 = (x9, y9)

    clockwise = (upper and left) or (not upper and not left)

    pen = glyph.glyphPen(replace=False)
    if clockwise:
        pen.moveTo(point0)
        pen.curveTo(point1, point2, point3)
        pen.lineTo(point4)
        pen.lineTo(point5)
        pen.lineTo(point6)
        pen.curveTo(point7, point8, point9)
        pen.closePath()
    else:
        pen.moveTo(point0)
        pen.lineTo(point9)
        pen.curveTo(point8, point7, point6)
        pen.lineTo(point5)
        pen.lineTo(point4)
        pen.lineTo(point3)
        pen.curveTo(point2, point1, point0)
        pen.closePath()

    pen = None

def draw_boxdraw_double(glyph, top, right, bottom, left):
    font = glyph.font

    xl1 = round(glyph.width/2 - HEAVY_STROKE_WIDTH/2 - STROKE_WIDTH/2)
    xl2 = round(glyph.width/2 - HEAVY_STROKE_WIDTH/2 + STROKE_WIDTH/2)
    xc1 = round(glyph.width/2 - STROKE_WIDTH/2)
    xc2 = round(glyph.width/2 + STROKE_WIDTH/2)
    xr1 = round(glyph.width/2 + HEAVY_STROKE_WIDTH/2 - STROKE_WIDTH/2)
    xr2 = round(glyph.width/2 + HEAVY_STROKE_WIDTH/2 + STROKE_WIDTH/2)

    yb1 = round(-font.descent + font.em/2 - HEAVY_STROKE_WIDTH/2 - STROKE_WIDTH/2)
    yb2 = round(-font.descent + font.em/2 - HEAVY_STROKE_WIDTH/2 + STROKE_WIDTH/2)
    yc1 = round(-font.descent + font.em/2 - STROKE_WIDTH/2)
    yc2 = round(-font.descent + font.em/2 + STROKE_WIDTH/2)
    yt1 = round(-font.descent + font.em/2 + HEAVY_STROKE_WIDTH/2 - STROKE_WIDTH/2)
    yt2 = round(-font.descent + font.em/2 + HEAVY_STROKE_WIDTH/2 + STROKE_WIDTH/2)

    # draw vertical line(s)
    if top == 1:
        if left == 2 and right == 2:
            draw_rect(glyph, xc1, yt1, xc2, font.ascent)
        elif left == 2 or right == 2:
            draw_rect(glyph, xc1, yb1, xc2, font.ascent)
        else:
            draw_rect(glyph, xc1, yc1, xc2, font.ascent)
    elif top == 2:
        if left == 2:
            draw_rect(glyph, xl1, yt1, xl2, font.ascent)
        elif right == 2:
            draw_rect(glyph, xl1, yb1, xl2, font.ascent)
        else:
            draw_rect(glyph, xl1, yc1, xl2, font.ascent)
        if right == 2:
            draw_rect(glyph, xr1, yt1, xr2, font.ascent)
        elif left == 2:
            draw_rect(glyph, xr1, yb1, xr2, font.ascent)
        else:
            draw_rect(glyph, xr1, yc1, xr2, font.ascent)
    if bottom == 1:
        if left == 2 and right == 2:
            draw_rect(glyph, xc1, yb2, xc2, -font.descent)
        elif left == 2 or right == 2:
            draw_rect(glyph, xc1, yt2, xc2, -font.descent)
        else:
            draw_rect(glyph, xc1, yc2, xc2, -font.descent)
    elif bottom == 2:
        if left == 2:
            draw_rect(glyph, xl1, yb2, xl2, -font.descent)
        elif right == 2:
            draw_rect(glyph, xl1, yt2, xl2, -font.descent)
        else:
            draw_rect(glyph, xl1, yc2, xl2, -font.descent)
        if right == 2:
            draw_rect(glyph, xr1, yb2, xr2, -font.descent)
        elif left == 2:
            draw_rect(glyph, xr1, yt2, xr2, -font.descent)
        else:
            draw_rect(glyph, xr1, yc2, xr2, -font.descent)

    # draw horizontal line(s)
    if left == 1:
        if top == 2 and bottom == 2:
            draw_rect(glyph, 0, yc1, xl2, yc2)
        elif top == 2 or bottom == 2:
            draw_rect(glyph, 0, yc1, xr2, yc2)
        else:
            draw_rect(glyph, 0, yc1, xc2, yc2)
    elif left == 2:
        if top == 2:
            draw_rect(glyph, 0, yt1, xl2, yt2)
        elif bottom == 2:
            draw_rect(glyph, 0, yt1, xr2, yt2)
        else:
            draw_rect(glyph, 0, yt1, xc2, yt2)
        if bottom == 2:
            draw_rect(glyph, 0, yb1, xl2, yb2)
        elif top == 2:
            draw_rect(glyph, 0, yb1, xr2, yb2)
        else:
            draw_rect(glyph, 0, yb1, xc2, yb2)

    if right == 1:
        if top == 2 and bottom == 2:
            draw_rect(glyph, glyph.width, yc1, xr1, yc2)
        elif top == 2 or bottom == 2:
            draw_rect(glyph, glyph.width, yc1, xl1, yc2)
        else:
            draw_rect(glyph, glyph.width, yc1, xc1, yc2)
    elif right == 2:
        if top == 2:
            draw_rect(glyph, glyph.width, yt1, xr1, yt2)
        elif bottom == 2:
            draw_rect(glyph, glyph.width, yt1, xl1, yt2)
        else:
            draw_rect(glyph, glyph.width, yt1, xc1, yt2)
        if bottom == 2:
            draw_rect(glyph, glyph.width, yb1, xr1, yb2)
        elif top == 2:
            draw_rect(glyph, glyph.width, yb1, xl1, yb2)
        else:
            draw_rect(glyph, glyph.width, yb1, xc1, yb2)

def draw_solidus(glyph, reverse=False):
    font = glyph.font
    diag = math.sqrt(font.em ** 2 + glyph.width ** 2)
    dx = round(font.em / diag * STROKE_WIDTH / 2)
    dy = round(glyph.width / diag * STROKE_WIDTH / 2)

    (x0, y0) = (0, -font.descent)
    (x1, y1) = (glyph.width, font.ascent)

    (x2, y2) = (x0 - dx, y0 + dy)
    (x3, y3) = (x0 + dx, y0 - dy)
    (x4, y4) = (x1 + dx, y1 - dy)
    (x5, y5) = (x1 - dx, y1 + dy)

    if reverse:
        (x2, x3, x4, x5) = [glyph.width - x for x in (x2, x3, x4, x5)]

    clockwise = not reverse

    pen = glyph.glyphPen(replace=False)
    if clockwise:
        pen.moveTo((x2, y2))
        pen.lineTo((x3, y3))
        pen.lineTo((x4, y4))
        pen.lineTo((x5, y5))
        pen.closePath()
    else:
        pen.moveTo((x2, y2))
        pen.lineTo((x5, y5))
        pen.lineTo((x4, y4))
        pen.lineTo((x3, y3))
        pen.closePath()
    pen = None

def draw_rect(glyph, x1, y1, x2, y2):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    pen = glyph.glyphPen(replace=False)
    pen.moveTo((x1, y1))
    pen.lineTo((x1, y2))
    pen.lineTo((x2, y2))
    pen.lineTo((x2, y1))
    pen.closePath()
    pen = None

main()
