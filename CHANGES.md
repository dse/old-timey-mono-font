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

as of 2025-12-21

Major changes:
-   Contains 100% of the Multilingual European Subset 1 (MES-1).
-   Contains 97% of the World Glyph Set (W1G).
-   Contains 94% of the Simple European Character Set (SECS).
-   Contains 100% of the IPA Extensions block.
-   Accents:
    -   Re-re-re-did all the accent placements.
    -   More visible accent marks for lowercase characters.
-   Add small caps, along with "c2sc" and "scap" OpenType features.
-   Add petite caps, along with "c2pc" and "pcap" OpenType features.
-   Added selected symbols from Symbols for Legacy Computing.
-   Added "BASE" for underlines on the baseline (better for `snake_case_identifiers` in my opinion).
-   Added "VCEN" for vertically centered glyphs.
-   Removed:
    -   Removed numerous double-accented Latin characters not in W1G, MES-1, SECS, or WGL4
        that were in the Latin Extended Additional block.  Those were unwieldy to maintain.
    -   Removed unused combining marks.
-   Added overshoots to top- and bottom-pointy letters such as `A`,
    `N`, `V`, `W`, `v`, and `w`.

New Characters:
-   U+1E9E LATIN CAPITAL LETTER SHARP S, to accompany U+00DF LATIN SMALL LETTER SHARP S
-   U+3003 DITTO MARK

New Variants:
-   Coding variant of U+007E TILDE

Character Fixes:
-   Fixed issue where these were backwards:
    -   U+042F CYRILLIC CAPITAL LETTER YA
    -   U+044F CYRILLIC SMALL LETTER YA
-   Fixed minor alignment issue with:
    -   U+03C7 GREEK SMALL LETTER CHI
-   Fixed a minor issue with:
    -   U+0070 LATIN SMALL LETTER P
-   Fixed the following characters because I didn't like the bottom terminals:
    -   U+025B LATIN SMALL LETTER OPEN E
    -   U+025C LATIN SMALL LETTER REVERSED OPEN E
    -   U+025D LATIN SMALL LETTER REVERSED OPEN E WITH HOOK
    -   U+03B5 GREEK SMALL LETTER EPSILON
    -   U+0437 CYRILLIC SMALL LETTER ZE

Minor Changes:
-   Made sure existing OpenType features actually work.
-   Renamed vendor-defined features to ones reserved for vendor use (matching `/^[A-Z]{4}$/`).

Administrative Changes Not Affecting the Font:
-   Added some comments in README.md about opening/installation
    issues in Windows.
-   I have an official vendor ID!  I am officially registered on
    Microsoft's font vendor registry as "DARN"!
-   Numerous build process enhancements and fixes.
