#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse, os
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('center', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    for filename in args.filenames:
        if "DEBUG" in os.environ:
            print("underline.py %s: Opening and reading..." % filename)
        font = fontforge.open(filename)
        font.upos = int(args.center - args.width / 2)
        font.uwidth = args.width
        if "DEBUG" in os.environ:
            print("underline.py %s: position = %d; width = %d" % (filename, font.upos, font.uwidth))
        if filename.endswith('.sfd'):
            if "DEBUG" in os.environ:
                print("underline.py %s: Saving..." % filename)
            font.save(filename)
        else:
            if "DEBUG" in os.environ:
                print("underline.py %s: Generating..." % filename)
            font.generate(filename)
        font.close()

main()
