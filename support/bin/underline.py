#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('center', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    for filename in args.filenames:
        if args.verbose:
            print("underline.py %s: Opening and reading..." % filename)
        font = fontforge.open(filename)
        font.upos = int(args.center - args.width / 2)
        font.uwidth = args.width
        if args.verbose:
            print("underline.py %s: position = %d; width = %d" % (filename, font.upos, font.uwidth))
        if filename.endswith('.sfd'):
            if args.verbose:
                print("underline.py %s: Saving..." % filename)
            font.save(filename)
        else:
            if args.verbose:
                print("underline.py %s: Generating..." % filename)
            font.generate(filename)
        font.close()

main()
