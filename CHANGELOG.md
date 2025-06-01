# Change Log

## 0.9.0

2025-05-01

-   initial "soft" release to the public as Old Timey Mono

## 0.9.1

2025-05-03

-   fixed: some autohints were incorrect, as they were not re-done
    after adjustments.  Re-doing them is now part of the `make`
    process.
-   fixed: U+0047 'G' did not overshoot below baseline
-   fixed: U+00A8 DIAERESIS had holes

## 0.9.2

2025-05-18

-   Minor fix to U+0077 LATIN SMALL LETTER W.
-   Add substitution lookups for the character variants (cv01 et al.),
    required to use them at all.
-   Specimen fixes.
-   Build process fixes.

## Next Version

-   U+1E9E CAPITAL LETTER SHARP S added.
-   Fixed issue where U+042F and U+044F CYRILLIC CAPITAL AND SMALL
    LETTERS YA were backwards.
-   Fixed minor alignment issue with U+03C7 GREEK SMALL LETTER CHI.
-   Fixed a minor issue with U+0070 LATIN SMALL LETTER P
-   Added some comments in README.md about opening/installation
    issues in Windows.
    
Build process and other internal things:
-   Additional information for stylistic sets on names for character
    variants and other alternate glyphs.
-   Additional Latin italic letters.
-   Added some anchors in an attempt to fix some semiautomatic accent
    placement issues.
-   Add left and right guides to the guideline (re-)applier script.
