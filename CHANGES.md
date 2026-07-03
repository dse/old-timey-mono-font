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

## 0.11.0

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

## 0.12.0

2026-07-03

-   redrawn U+00DF LATIN SMALL LETTER SHARP S
-   redrawn U+1E9E LATIN CAPITAL LETTER SHARP S
-   improved code variants for \( \) \[ \] \{ \}
-   redrawn U+20AC EURO SIGN
-   more accent placement fixes
-   U+2260 NOT EQUAL TO had wrong symbol; no longer does
-   some box drawing characters fixed
-   heavy box drawing characters made heavier
-   new glyphs:
    -   U+03F4    GREEK CAPITAL THETA SYMBOL
    -   U+2213    MINUS-OR-PLUS SIGN
    -   U+222C    DOUBLE INTEGRAL
    -   U+222D    TRIPLE INTEGRAL
    -   U+2235    BECAUSE
    -   U+2236    RATIO
    -   U+2237    PROPORTION
    -   U+2249    NOT ALMOST EQUAL TO
    -   U+2262    NOT IDENTICAL TO
    -   U+2263    STRICTLY EQUIVALENT TO
    -   U+22A2    RIGHT TACK
    -   U+22A3    LEFT TACK
    -   U+22A4    DOWN TACK
    -   U+27E8    MATHEMATICAL LEFT ANGLE BRACKET
    -   U+27E9    MATHEMATICAL RIGHT ANGLE BRACKET
    -   U+27EA    MATHEMATICAL LEFT DOUBLE ANGLE BRACKET
    -   U+27EB    MATHEMATICAL RIGHT DOUBLE ANGLE BRACKET
    -   U+1FB81   HORIZONTAL ONE EIGHTH BLOCK-1358 (window title bar)
    -   U+1FB95   CHECKER BOARD FILL
    -   U+1FB96   INVERSE CHECKER BOARD FILL
    -   U+1FB97   HEAVY HORIZONTAL FILL
    -   U+1FB9A   UPPER AND LOWER TRIANGULAR HALF BLOCK
    -   U+1FB9B   LEFT AND RIGHT TRIANGULAR HALF BLOCK
    -   U+1FB9C   UPPER LEFT TRIANGULAR MEDIUM SHADE
    -   U+1FB9D   UPPER RIGHT TRIANGULAR MEDIUM SHADE
    -   U+1FB9E   LOWER RIGHT TRIANGULAR MEDIUM SHADE
    -   U+1FB9F   LOWER LEFT TRIANGULAR MEDIUM SHADE
    -   U+1FBCE   LEFT TWO THIRDS BLOCK
    -   U+1FBCF   LEFT ONE THIRD BLOCK
    -   U+1FBE4   UPPER CENTRE ONE QUARTER BLOCK
    -   U+1FBE5   LOWER CENTRE ONE QUARTER BLOCK
    -   U+1FBE6   MIDDLE LEFT ONE QUARTER BLOCK
    -   U+1FBE7   MIDDLE RIGHT ONE QUARTER BLOCK
    -   Symbols for Legacy Computing:
        -   Block mosaic terminal graphic characters: U+1FB00 to U+1FB3B
        -   Smooth mosaic terminal graphic characters: U+1FB3C to U+1FB6F
        -   Block elements: U+1FB70 to U+1FB80; U+1FB82 to U+1FB8B
        -   Segmented digits 0 to 9: U+1FBF0 to U+1FBF9   SEGMENTED DIGIT NINE
