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

as of 2025-12-04

Major changes:
-   Contains the entire World Glyph Set (W1G), except for the ligatures.
-   Contains the entire Multilingual European Subset 1 (MES-1).
-   Contains most of the Simple European Character Set (SECS).
-   Contains the full IPA Extensions block.
-   Removed numerous double-accented Latin characters not in W1G, MES-1, SECS, or WGL4
    that were in the Latin Extended Additional block.
-   Removed unused combining marks.
-   Redid accent placements again.
-   Add small caps.
-   Add petite caps.

Minor changes:
-   U+1E9E CAPITAL LETTER SHARP S added.
-   Fixed issue where U+042F and U+044F CYRILLIC CAPITAL AND SMALL
    LETTERS YA were backwards.
-   Fixed minor alignment issue with U+03C7 GREEK SMALL LETTER CHI.
-   Fixed a minor issue with U+0070 LATIN SMALL LETTER P
-   Added some comments in README.md about opening/installation
    issues in Windows.
-   I have an official vendor ID!  I am officially registered on
    Microsoft's font vendor registry as "DARN"!
-   Numerous build process enhancements.
