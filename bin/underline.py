#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge
import argparse
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('center', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    for filename in args.filenames:
        print("underline.py %s: Opening and reading..." % filename)
        font = fontforge.open(filename)
        font.upos = int(args.center - args.width / 2)
        font.uwidth = args.width
        print("underline.py %s: position = %d; width = %d" % (filename, font.upos, font.uwidth))
        if filename.endswith('.sfd'):
            print("underline.py %s: Saving..." % filename)
            font.save(filename)
        else:
            print("underline.py %s: Generating..." % filename)
            font.generate(filename)
        font.close()

main()
