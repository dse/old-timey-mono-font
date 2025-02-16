def reconstitute_references(glyph):
    # Apparently a glyph.unlinkRef() call will replace the
    # references with the contours from when the font was
    # loaded, ignoring any changes we make to the glyph.
    references = glyph.references
    glyph.references = []
    for reference in references:
        glyph.addReference(reference[0], reference[1])
