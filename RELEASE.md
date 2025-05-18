# A New Relase

## QUICKLY

`make clean version fonts zip unversionedzip specimen`

## Detailed

1.  Edit `Makefile` to change the `SFNT_REVISION` and `VERSION`
    variables.
    
2.  Run `make version` to update the source font to the new version
    number.

2.  Run `make fonts` to generate the fonts with the new version
    number.

3.  Run `make zip` to generate `OldTimeyMono-x.x.x.zip` with the
    new version number.
    
4.  Run `make unversionedzip` to generate `OldTimeyMono.zip`.

5.  Run `make specimen` then `cd specimen ; yarn build ; cd ..`
    Second step is done separately in case you're using `nvm` or
    suchlike.
    
## The Rest

6.  Be sure to edit `CHANGELOG.md` to summarize your changes.

7.  Be sure to `git commit` and `git push` everything.

8.  Run `make publish`.

9.  Run `git tag x.x.x && git tag vx.x.x && git push --tags`

10. Create a new release: https://github.com/dse/old-timey-mono-font/releases/new

    -   Choose a tag.  I've been using `x.x.x`.
    
    -   Choose the previous tag.
    
    -   Generate release notes.
    
    -   Keep this line:
    
            **Full Changelog**: https://github.com/dse/old-timey-mono-font/compare/v0.9.1...0.9.2
            
    -   Summarize above.
    
    -   Be sure to attach binaries.
