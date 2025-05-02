#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-

import fontforge
import argparse

REPLACEMENT_CHARACTER = 0xfffd

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    font = fontforge.open(args.filename)
    
    replCharName = fontforge.nameFromUnicode(REPLACEMENT_CHARACTER)
    if replCharName in font:
        replChar = font[replCharName]
        notdef = font.createChar(-1, ".notdef")
        notdef.foreground = replChar.foreground
        notdef.background = replChar.background
        notdef.dhints = replChar.dhints
        notdef.hhints = replChar.hhints
        notdef.vhints = replChar.vhints
    else:
        notdef = font.createChar(-1, ".notdef")
        notdef.foreground = fontforge.layer()
        notdef.background = fontforge.layer()
        notdef.dhints = ()
        notdef.hhints = ()
        notdef.vhints = ()
    
    if args.filename.endswith('.sfd'):
        font.save(args.filename)
    else:
        font.generate(args.filename)
    font.close()
    
main()

