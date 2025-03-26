# Reproducing Typewriter

A clean digital revival of Reproducing Typewriter, a monospace
typeface from as early as 1906.  Reproducing Typewriter was designed
for simulating typewritten letters in smaller point sizes for
advertisements, catalogs, etc., where readability and/or distortion
resulting from duplication were issues.

Typefaces were also available to simulate the fonts used by actual
typewriters like Remington, Smith, and Underwood; whereas Reproducing
Typewriter is more readable at smaller point sizes due to shorter
serifs and (generally) more open arpetures.

I developed this because I believe those characteristics also make
Reproducing Typewriter a good basis for a coding font (this one) with
an antique aesthetic.

You may have seen this typeface used in the [Turbo Pascal 3.0](turbo)
product manual.

At a size of 12pt (6 lines per inch), Reproducing Typewriter is a pica
font, or 10 characters per inch, like Courier.  It **should** be
suitable for screenplay writing.

## Mintty Users

Text -> Font Smoothing -> Partial

## Download All The Fonts

[ReproTypewr.zip](dist/ReproTypewr.zip)

## Download Individual Fonts

-   Reproducing Typewriter
    -   Regular - Pica (10 pitch)
        -   [Thin](dist/ttf/ReproTypewr-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewr-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewr.ttf)
    -   Condensed - Elite (12 pitch)
        -   [Thin](dist/ttf/ReproTypewrCond-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewrCond-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewrCond.ttf)
    -   Compressed (16.5 characters per inch)
        -   [Thin](dist/ttf/ReproTypewrComp-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewrComp-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewrComp.ttf)

-   Reproducing Typewriter Code
    -   Regular - Pica (10 pitch)
        -   [Thin](dist/ttf/ReproTypewrCode-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewrCode-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewrCode.ttf)
    -   Condensed - Elite (12 pitch)
        -   [Thin](dist/ttf/ReproTypewrCodeCond-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewrCodeCond-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewrCodeCond.ttf)
    -   Compressed (16.5 characters per inch)
        -   [Thin](dist/ttf/ReproTypewrCodeComp-Thin.ttf)
        -   [Light](dist/ttf/ReproTypewrCodeComp-Light.ttf)
        -   [Regular](dist/ttf/ReproTypewrCodeComp.ttf)

## Reproducing Typewriter Code

While the regular font tries to stick to the original as much as
possible, Reproducing Typewriter Code makes the following changes:

-   A modified digit `0` to be better distinguishable from the
    uppercase letter `O`.

-   A modified digit `1` to be better distinguishable from the
    lowercase letter `l`.

-   Certain punctuation marks are made larger for better visibility.

-   Certain letters, namely `a`, `c`, `e`, and `s`, are modified with
    more open apertures for better readability.
    
## Character Set Coverage

Extensive Western European (Latin) coverage, as well as Cyrillic
(Ukraine, etc.) and Greek.

Includes in their entirety:

-   ASCII
-   ISO-8859-1
-   Code Page 437
-   Code Page 850
-   Windows Glyph List 4 (WGL4)
-   Adobe Glyph List for New Fonts (AGLFN)
-   Windows 1252's additional characters
-   Mac OS Roman, except for the ff and fi ligatures (which don't belong in monospace fonts)
-   The following Unicode blocks in their entirety:
    -   U+2500–U+257F Box Drawing
    -   U+2580–U+259F Block Elements
    -   U+2800–U+28FF Braille Patterns
    -   U+0100–U+017F Latin Extended-A
-   And then some.
-   And a few extras!

## Full Disclosure

-   The percent sign had to be shifted up a bit to stay within the
    character cell without modifying the baseline, cap-height, ascent,
    descent, and other dimensions.

-   These are monoline fonts whereas the originals weren't, but in my
    view this is close enough.

-   Cap height is slightly different.

-   Not all characters in this typeface are original to Reproducing
    Typewriter.

## You May Also Like

I made these:

-   [DSE Typewriter](https://webonastick.com/fonts/dse-typewriter/)
-   [DSE Typewriter Bitmap](https://github.com/dse/dse-typewriter-bitmap-font)
-   [Canton Typewriter Bitmap](https://github.com/dse/font-canton-typewriter-bitmap/tree/master),
    a bitmap font inspired by Caxton.

Also free:

-   [TT2020](https://ctrlcctrlv.github.io/TT2020/docs/)
-   [CMU Typewriter](https://fontlibrary.org/en/font/cmu-typewriter)

Paid:

-   [LTC Remington Typewriter](https://p22.com/family-Remington_Typewriter)
-   [Bitstream Pica 10 Pitch](https://www.myfonts.com/fonts/bitstream/pica-10-pitch/)
-   [Italian Typewriter](https://www.myfonts.com/fonts/flanker/italian-typewriter/)
-   [Typist Slab](https://www.myfonts.com/fonts/vanderKeur/typist-slab/)
-   [FF Elementa](https://www.myfonts.com/fonts/fontfont/elementa-pro/)
-   [EF Techno Script](https://www.myfonts.com/fonts/ef/techno-script-ef/)
-   [Pitch](https://klim.co.nz/retail-fonts/pitch/)
-   [Vintage Type](https://luc.devroye.org/fonts-27181.html)
    Pro Screenwriter Fonts, if you can find them.

Even more fonts:

-   My [Monospace Font List](https://github.com/dse/monospace-font-list)

## I Also Made:

-   [Router Gothic](https://webonastick.com/fonts/routed-gothic/)
    
## License

[SIL OFL 1.1](OFL.md)

## Author

[Darren Embry](mailto:dsembry@gmail.com)
    
## Footnotes

[linebook]: https://www.google.com/books/edition/American_Line_Type_Book/WadRAAAAYAAJ?hl=en&gbpv=1&pg=PP5&printsec=frontcover

[turbo]: https://bitsavers.trailing-edge.com/pdf/borland/turbo_pascal/Turbo_Pascal_Version_3.0_Reference_Manual_1986.pdf
