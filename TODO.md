# Known Issues

-   The following characters appear double wide in macOS Terminal.app:

    -   U+2329 LEFT-POINTING ANGLE BRACKET "〈"
    -   U+232A RIGHT-POINTING ANGLE BRACKET "〉"
    
    Those glyphs' advance widths in the font are correct.
    
    In macOS, this occurs in iTerm as well.

# TODO

-   U+00F0 LATIN SMALL LETTER ETH can go all the way to the top; there
    are never combining marks above it, and it would be easier to
    read.
    
    OR the loop can be shorter making the stroke more visible

-   SOLUTION?  Hinting?

    check box drawings for dumb shit like this that shows up in mintty:

            ######################
            ######################
            ######################
            ######################
             ###
             ###
             ###
             ###
             ###
             ###

## Petite and Small Caps

-   U+00C6 AE
-   U+00D0 ETH
-   U+00DE THORN
-   U+00DF LATIN SMALL LETTER SHARP S
-   U+0132 IJ
-   U+0152 OE
-   U+018E REVERSE E
-   U+01B7 EZH
-   U+01B8 EZH REVERSED
-   U+0245 TURNED V

-   greek capitals GAMMA, DELTA, THETA, LAMBDA, XI, PI,
    SIGMA, PHI, PSI, OMEGA, DIGAMMA

-   cyrillic capitals DJE, UKRAINIAN IE, LJE, NJE, TSHE,
    DZHE, BE, GHE, DE, ZHE, ZE, I, KA, EL, PE, U, EF, TSE,
    CHE, SHA, SHCHA, HARD SIGN, YERU, SOFT SIGN, E, YU, YA

-   cyrillic capitals 046C, 0490, 04BA

-   accented glyphs

## From Comments on Hacker News

https://news.ycombinator.com/item?id=43884418

-   Add GSUB lookups for all `cvxx`.  Call the GSUB lookups `cvxx`.

    > DONE

-   Combining marks work properly in some cases, not in others (e.g.,
    notepad).  Maybe everything needs anchors?  Probably a good idea
    anyway, since auto-generating accented glyphs will achieve better
    results with them.
    
    Y̆ y̆ <-- mintty is showing a double breve?

### These are Suggestions.

-   Dotted zero variant.

    > cv05 or cv06

-   "Looking at the examples, they look good, though one thing stands
    out, the 'w' seems to be bolder than the other letters. The 'm'
    seems fine, as do the other letters and symbols, just the 'w'."
    
    > It's that way in the Turbo Pascal manual too.  Leaving as is.

-   "You wouldn't consider changing license to Apache-2.0, or dual
    license under that?"
    
    > No.

-   "allow combining breve over Latin y as well: sometimes that's handy
    for indicating contrast"
    
    So, combining marks well sometimes and not well other times.
    
    Examples of times where they don't work: Notepad
    
    This may be due to lack of anchors.  Quite frankly they would
    solve some issues I've been experiencing with auto placement.
    
    Also here's a Unicode combining mark test page:
    
    -   https://alanwood.net/unicode/combining_diacritical_marks.html

-   "check the height of stacking diacritical marks: a perispomenos
    tonos or circumflex accent over a breathing mark over a vowel
    (like in εἶναι eĩnai) ends up stacking up tall enough to intersect
    with descenders (like on ζ zeta) from the line above"
    
    This is hard.
    
    WORK IN PROGRESS

-   the circumflex over alpha (ᾶ) looks really good, because it
    follows the curve of the alpha itself, but circumflex over eta (ῆ)
    looks off-center, because it left-aligns to the ear on the left of
    eta. The same could be said for the iota subscript (ᾳῃῳ): it looks
    great under alpha and omega, but it's a bit awkward under eta
    because of how far to the left it is.
    
    Another accent placement issue.
    
    WORKING ON

-   have you considered adding a variation for the Porsonic or
    single-curve circumflex?

    I need to figure out which combining mark that would be.
    
-   "Just the uppercase variant ẞ - the lowercase ß _is_
    there. Notably, uppercase ẞ didn't exist at the time the source
    typeface was designed – it was only officially adopted 111 years
    later in 2017."
    
    > DONE.

-   "I can't tell if you're aiming for a faithful reproduction of the
    original font, or to make the coding font modern and most useful
    to today's developer. But... Can the code variant have the
    asterisk used to represent multiplication be on the same line as
    other math operators like plus, minus, and tilde? +-~* I always
    like the asterisk to be in line with the others. Maybe I am just
    weird. Also for the code variant I think the pound or hash mark #
    could be reduced in drama a little, to fit in with the other
    punctuation marks. Thanks for listening to my two cents."
    
    > Aiming for both.
    
    There's a VCEN stylistic set but some of these can be character
    variants.

## Other

-   U+262E PEACE SYMBOL
-   U+26C4 SNOWMAN WITHOUT SNOW
-   U+23FB POWER SYMBOL
-   U+23FC POWER ON-OFF SYMBOL
-   U+23FD POWER ON SYMBOL
-   U+23FE POWER SLEEP SYMBOL
-   U+2B58 HEAVY CIRCLE (Power Off)
-   U+1F500 TWISTED RIGHTWARDS ARROWS (Shuffle)
-   U+1F501 CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS (Repeat)
-   U+26A0 WARNING SIGN
-   U+26A1 HIGH VOLTAGE SIGN
-   U+2756 BLACK DIAMOND MINUS WHITE X
-   U+2311 SQUARE LOZENGE
-   U+29EB BLACK LOZENGE

## Maybe

-   20px overshoot on VWvw41
-   no overshoot on A?
-   too late imo but
    -   possible cap height of 1104 (1008 + 96)
        -   presently ........ 1056 (960 + 96)
    -   possible ex height of 768 (672 + 96)
        -   presently ....... 756 (660 + 96)

