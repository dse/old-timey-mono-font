#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import sys, os, argparse

dir = "%s/git/dse.d/pyfontdrawutils/src" % os.getenv("HOME")
if dir not in sys.path:
    sys.path.append(dir)

dir = "%s/git/dse.d/pyfontutils/src" % os.getenv("HOME")
if dir not in sys.path:
    sys.path.append(dir)

from pyfontdrawutils.draw import rect, poly
from pyfontdrawutils import vcdrawing
from pyfontdrawutils import settings
from pyfontutils.utils import get_fonts_from

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    settings.set_arc_drawing_radius_factor(7/8)

    for [font, filename, font_in_file] in get_fonts_from(args.filenames, with_filenames=True, ttc=False):
        vcdrawing.draw(font)
        if filename.endswith(".sfd"):
            font.save(filename)
        else:
            font.generate(filename)

main()
