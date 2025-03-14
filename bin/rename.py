#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import sys
import os
import glob
import re
import unicodedata
import shlex

def main():
    src = os.path.dirname(__file__) + "/../src/chars"
    files = []
    for digit_count in range(4, 7):
        for appendage in [".svg", "-*.svg"]:
            pattern = src + "/**/" + "[0-9A-Fa-f]" * digit_count + appendage
            files += glob.glob(pattern, recursive=True)
    files = [file for file in files if
             not re.search(r'/scans/', file) and
             not re.search(r'/italic-', os.path.dirname(file)) and
             not re.search(r'/greek-lc/', file)]
    files.sort()
    for file in files:
        (dirname, basename) = os.path.split(file) # pathname = dirname + basename
        (root, ext) = os.path.splitext(basename)  # pathanme = dirname + root + ext
        if not (match := re.match(r'^[0-9A-Fa-f]+', root)):
            continue
        codepoint = int(match.group(0), 16)
        suffix = None
        if (match := re.match(r'^(.*?)(--.*)$', root)):
            (root, suffix) = (match.group(1), match.group(2)) # pathname = dirname + root + suffix + ext
        charname = None
        new_root = None
        try:
            charname = kebab(unicodedata.name(chr(codepoint)))
        except ValueError:
            continue
        new_filename = None
        if suffix is None:
            new_filename = "%04x-%s%s" % (codepoint, charname, ext)
        else:
            new_filename = "%04x-%s%s%s" % (codepoint, charname, suffix, ext)
        if basename == new_filename:
            continue
        print("git mv %s \\\n       %s" % (shlex.quote(file), shlex.quote(os.path.join(dirname, new_filename))))

def kebab(str):
    str = re.sub(r'\'+', '', str)
    str = re.sub(r'^[^A-Za-z0-9]+', '', str)
    str = re.sub(r'[^A-Za-z0-9]+$', '', str)
    str = re.sub(r'[^A-Za-z0-9]+', '-', str)
    str = str.lower()
    return str

main()
