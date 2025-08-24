#!/usr/bin/env -S fontforge -quiet
# -*- mode: python; coding: utf-8 -*-
import fontforge, sys
from datetime import date
def main():
    for filename in sys.argv[1:]:
        print("Opening: %s" % filename)
        font = fontforge.open(filename)
        font.os2_vendor = "DARN" # it's registered!
        font.copyright = "Copyright %s Darren Embry.  SIL Open Font License Version 1.1.  https://openfontlicense.org/open-font-license-official-text/" % \
            date.today().year
        print("Writing: %s" % filename)
        if filename.endswith('.sfd'):
            font.save(filename)
        else:
            font.generate(filename)
        font.close()
main()
