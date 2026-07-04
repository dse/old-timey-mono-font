#!/usr/bin/env fontforge -quiet -lang=py -script
import fontforge, argparse, re

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--erase", action="store_true")
    args = parser.parse_args()

    font = fontforge.open(args.filename)
    for glyph in font.glyphs():
        if args.erase:
            glyph.comment = ""
        else:
            if glyph.comment is not None and glyph.comment.strip() != "":
                print("%s:" % glyph.glyphname)
                print(re.sub(r'^', "> ", glyph.comment, flags=re.M))

    if args.filename.endswith(".sfd"):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()

main()
