# Contributing to Reproducing Typewriter

## Glyphs

Use a 1008 × 1680 px SVG file, with 96px wide lines, round joins,
round caps.

See `src/chars/blank-char.svg` for a template.

## Filenames

Start its name with the codepoint in lowercase hex, minimum 4 digits
with leading zeros as needed, followed by a hyphen-minus or full-stop.

Examples:

    0041.svg                            # VALID
    0041-A.svg                          # VALID
    0061-a.svg                          # VALID
    0041-LATIN-CAPITAL-LETTER-A.svg     # VALID
    0041-latin-capital-letter-a.svg     # VALID
    0041A.svg                           # INVALID (0041A is a hex value lol)
    1f4a9.svg                           # VALID
    01f4a9-pile-of-poo.svg              # ALSO VALID

## Guideline Dimensions

In the template, note the horizontal guides at the cap height, ex
height, baseline, and descender.  Each are sets of four: the center
lines, top, bottom, and2 0px above (or below as needed) the center
line, for overshoots.

See table below for dimensions.  ACTUAL reflects final dimensions.

CL refers to points on stroke lines.

|            | ACTUAL | CL above bottom | CL below top | CL above baseline CL |
|:-----------|-------:|----------------:|-------------:|---------------------:|
| baseline   |    336 |             384 |         1296 |                      |
| ex-height  |    756 |            1044 |          636 |                  660 |
| cap-height |   1056 |            1344 |          336 |                  960 |
| descender  |    300 |              84 |         1596 |            300 below |

Overshoots are 20px.

An additional guideline between the baseline and the ex-height is for
vertically centering math/logic/etc. operator glyphs.

There is an additional guideline for the vertical center of capital
letters.

## Stroke to Path (NO!)

Don't use **Stroke to Path** in Inkscape.  This converts strokes to
filled outlines around the strokes; my build process does this already
and expects you not to.

## Object to Path

Using **Object to Path** in Inkscape is fine.  It does things like
converting circles, ellipses, arcs, and regular polygons to basic
stroke paths.  You don't have to do this unless you want to make
adjustments.
