#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import fontforge, re, os, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    parser.add_argument("-n", "--dry-run", action="store_true")
    args = parser.parse_args()

    input_dir, input_basename = os.path.split(args.input_filename)
    input_stem, input_ext = os.path.splitext(input_basename)

    output_dir, output_basename = os.path.split(args.output_filename)

    output_filename = args.output_filename
    if re.fullmatch(r'\.[^\.\/\\]+', output_filename):
        # output_filename is only a file extension
        # convert-font.py /blah/input.sfd .ttf => /blah/input.ttf
        #                 AAAAAABBBBBCCCC DDDD    AAAAAABBBBBDDDD
        # A = input_dir; B = input_stem; C = input_ext; D = output_filename
        output_filename = os.path.join(input_dir, input_stem + output_filename)
    elif re.fullmatch(r'\.[^\.\/\\]+', output_basename):
        # output_filename's basename is only a file extension
        # convert-font.py /blah/input.sfd /blargh/.ttf => /blargh/input.ttf
        #                 AAAAAABBBBBCCCC DDDDDDDDEEEE    DDDDDDDDBBBBBEEEE
        # A = input_dir; B = input_stem; C = input_ext; D = output_dir; E = output_basename
        output_filename = os.path.join(output_dir, input_stem + output_basename)

    if args.dry_run:
        print(f'convert-font.py {args.input_filename} {args.output_filename} => {output_filename}')
    else:
        font = fontforge.open(args.input_filename)
        if output_filename.lower().endswith(".sfd"):
            font.save(output_filename)
        else:
            font.generate(output_filename)
        font.close()

main()
