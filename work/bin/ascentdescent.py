#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--em', type=int)
    parser.add_argument('--ascent', type=int)
    parser.add_argument('--descent', type=int)
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    ascent = None
    descent = None
    em = None
    if args.em is not None:
        if args.ascent is not None and args.descent is not None:
            raise Exception("--em does not make sense with both --ascent and --descent")
        em = args.em
        if args.ascent is not None:
            ascent = args.ascent
            descent = em - ascent
        elif args.descent is not None:
            descent = args.descent
            ascent = em - descent
        else:
            ascent = round(em / 5)
            descent = em - ascent
    else:
        if args.ascent is None or args.descent is None:
            raise Exception("--ascent and --descent must be specified if --em is not")
        ascent = args.ascent
        descent = args.descent
        em = args.ascent + args.descent
    for filename in args.filenames:
        font = fontforge.open(filename)
        font.ascent = ascent
        font.descent = descent
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)
        font.close()
main()
