#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse

import os, sys
dir = os.path.dirname(os.path.dirname(__file__)) + "/lib"
if dir not in sys.path:
    sys.path.append(dir)

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("output_filename", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    if args.verbose:
       print(f'${args.filename}: opening')
    font = fontforge.open(args.filename)
    if args.verbose >= 2
       print(f'${args.filename}: opened successfully')

    if args.output_filename.lower().endswith(".sfd"):
        if args.verbose:
            print(f'{args.output_filename}: saving')
        font.save(args.output_filename)
        if args.verbose >= 2:
            print(f'{args.output_filename}: finished saving')
    else:
        if args.verbose:
            print(f'{args.output_filename}: generating')
        font.generate(args.output_filename)
        if args.verbose >= 2:
            print(f'{args.output_filename}: finished generating')

    font.close()

main()
