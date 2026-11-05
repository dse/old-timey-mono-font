#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    font = fontforge.open(args.input_filename)
    if args.output_filename.lower().endswith(".sfd"):
        font.save(args.output_filename)
    else:
        font.generate(args.output_filename)
    font.close()

main()
