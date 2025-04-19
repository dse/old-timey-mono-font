#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge
import argparse
import os
import sys
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--sfnt-revision', type=float, metavar='XXX.YZZ', help='XXX = major, Y = minor, ZZ = patch; e.g., "000.902"')
    parser.add_argument('--ps-version', type=str, metavar='VERSION', help='a string containing the actual version number, e.g., "0.9.2", "9.2.0-beta", etc.')
    args = parser.parse_args()
    font = fontforge.open(args.filename)
    if args.sfnt_revision is not None:
        font.sfntRevision = args.sfnt_revision
    if args.ps_version is not None:
        font.version = args.ps_version
    if args.sfnt_revision is None and args.ps_version is None:
        print("font.sfntRevision: %07.3f" % font.sfntRevision)
        print("font.version:      %s" % repr(font.version))
    else:
        if args.filename.endswith('.sfd'):
            font.save(args.filename)
        else:
            font.generate(args.filename)
    font.close()
main()
