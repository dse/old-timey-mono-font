#!/usr/bin/env -S fontforge -quiet -lang=py -script
# -*- mode: python; coding: utf-8 -*-
import sys, os, argparse

dir = "%s/git/dse.d/pyfontdrawutils/src" % os.getenv("HOME")
if dir not in sys.path:
    sys.path.append(dir)

dir = "%s/git/dse.d/pyfontutils/src" % os.getenv("HOME")
if dir not in sys.path:
    sys.path.append(dir)

from pyfontdrawutils import boxdrawing
from pyfontutils.utils import get_fonts_from

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    for [font, filename, fontname] in get_fonts_from(args.filenames, with_filenames=True):
        boxdrawing.draw(font, verbose=args.verbose)
        if filename.endswith(".sfd"):
            print("Saving %s" % filename)
            font.save(filename)
        else:
            print("Generating %s" % filename)
            font.generate(filename)

main()
