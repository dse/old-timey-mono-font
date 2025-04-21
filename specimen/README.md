<h1 align="center">Specimen Builder</h1>

Specimen Builder is a quick and easy way to build digital type specimens. It uses [Specimen Skeleton](https://github.com/kabisa/specimen-skeleton) as a base and builds on top of it with a theme design and some configuration. Specimen Skeleton is built using [Eleventy](https://www.11ty.dev/)

The design rationale for specimen builder comes from several months of design research into the effectiveness of digital type specimens. [You can read the final report of that research here](https://typespecimens.xyz/journal/specimen-research-insights/).

### Requirements
- This project requires Node.js >= 12 and [yarn](https://yarnpkg.com/).
- It builds from *woff2* font files, either individual font files or variable fonts.

### Getting started
To get started, run the following commands from the root of the repo:

- `yarn install`
- `yarn start`

This will give you a basic specimen with the default content, configuration, and fonts.

### Workflow for adding your own fonts

#### Deleting the placeholder fonts
- Delete the placegholder font files in `src/fonts`
- Delete `src/_data/fontdata.json`
- Delete the folder `src/_data/fonts`

#### Add your own fonts
- Add your font files to the `src/fonts` directory. They must be in woff2 format.
- Run `yarn fontdata`
- If you are using multiple font files, you can reorder the order in which the array has been generated in `src/_data/fontdata.json`. This will determine the order the font files will appear in the tester dropdown.

#### Editing the placeholder content
- Edit the site configuration in `src/_data/site.js`
- Edit the content configuration in `src/_data/content.js`

#### Editing the default 'main_id' variable
- `main_id` is the variable that defines the font file for the whole specimen. It is defined in `src/index.html` in this line of code: `{% assign main_id = 0 %}`.
- The '0' in this example corresponds to the first entry in the fontdata array in `src/_data/fontdata.json`.
- To change the default font, simply change this variable to the item in the array starting with 0 for the first, 1 for the second etc.
– So if I had an array of 8 font files, and I wanted my specimen to be in Regular – which is the fourth item in the array – then `main_id = 3`.

#### Changing the design
- If you'd like to change the colours, edit the variables in `src/css/theme.css`
- Assign main variable if using multiple `.woff2` files. In `index.html`, on line 16,  change the `main_id` variable number to the number in the array generated in `_data/fontdata.json`. This will determine the loading font in the type tester.
- `yarn start` - this will start the local development server, view at http://localhost:8080.

<hr />

### Information architecture

The specimen produced by this tool has vertically stacked 'containers', from top to bottom, they are:
1. *Navigation*. Containing the Light/Dark toggle.
2. *Masthead*. Containing critical information regarding the typeface, in addition to large evaluative glyphs and a call to action to download the font.
3. *Interactive Controls*. An important container for user evaluation. These controls automatically generate sliders and drop downs from either individual font files, or from variable font axis. Simple typesetting tools are available for the user to change alignment, size, and line height.
4. *Specimen*. Containing several single words set in varying weights. These should be individualised per font.
5. *Setting*. A container to demonstrate long-form content at various dense settings at sizes.
6. *Character Grid*. A comprehensive categorised list of all characters within the fonts together with a large size preview.
7. *Language*. A container displaying a list of supported languages.

HTML files in `src/_includes/` correspond to each container.

<hr />

### Extending Specimen Builder

You can extend the functionality of the specimens produced using Specimen Builder by simply editing the content or CSS. 

#### Font styles

When you ran `yarn fontdata`, Specimen Skeleton (remember: the system that is the foundation for Specimen Builder) produced font styles in a css file in `_src/css/font.css`. These can be used as utility classes for typesetting the 'specimen' or 'setting' containers.


#### Design tokens

Specimen Builder provides some simple utility classes in the design token CSS – `src/css/theme.css` – to fine-tune your typesetting. The following classes are available:

* Colours: Colours are available as CSS variables. Be mindful of the dark mode, and please ensure you provide sympathetic dark alternatives for every additional colour used.
* Spacing: Specimen Builder provides em-based spacing units with the classes `.m-1u`, `.m-2u`, and `.p-1u`, `.p-2u` etc. Where u = 1em, m = margin, and p = padding.
* Font weight. Several typesetting classes are available. eg `.italic`
* Font size: A large range of em-based font sizes are available from `type-3xs`, to `.type-8xl`.
* Line height. `.lh08` to `.lh14` represent line height values 0.8 to 1.4.
* Alignment. `.align-centre`, `.align-left`, `.align-justify`, `.align-right`.

#### Reading direction
If producing specimens for languages that read right to left, or top to bottom, you need to edit a variable in `_src/data/site.js` called 'direction' and change its value to either:

* Left to right: "ltr"
* Right to left: "rtl"
* Left to right, top to bottom: "ltrttb"
* Right to left, top to bottom: "rtlttb"

These values will change the text blocks in each container.

### Extending Specimen Builder even further!

[Specimen Skeleton](https://github.com/kabisa/specimen-skeleton) – the foundation on which Specimen Builder is built – provides us with some useful tools to extend the specimens even further:

#### Using assets

In HTML, to use an image from your `img` directory, use the following URL value with the relative path to your image:

`<img src="{% webpackAssetPath '../img/my_logo.svg' %}">`

If you want to inline an SVG image, use:

`{% include '../img/my_logo.svg' %}`

or

`{% webpackAssetContents 'img/my_logo.svg' %}`

In CSS, point to the file using the path relative to your CSS file:

`background-image: url(../img/my_logo.svg);`

In CSS, images below 8 KB will be inlined automatically. To force inlined or external, append `?inline` or `?external` respectively, e.g. `url(../img/my_logo.svg?external);`. Inlining in HTML files

#### Am I in view?

Simple example to stop CPU-melting animations when they're not in the viewport. Elements with the class `.am-i-in-view` will get a class `.in-view` when they're in the viewport, and have that class removed when they leave the viewport. Use this to start/stop heavy animations.

Note: this can be repurposed for lazy loading images, pausing video, etc.

<hr />

## Converting ttf to woff2

If you need to compress your `.ttf` font files to `.woff2`, you can use this handy utility from Google

https://github.com/google/woff2

If you're using homebrew on a Mac, you can install it with `brew install woff2`. It'll give you the tools woff2_decompress and woff2_compress.

Use this one liner to compress all .ttf fonts in the current directory: `for f in *.ttf; do woff2_compress $f; done`

## Content sources
If you are creating specimens in multiple languages, you can use these resources for sourcing content:

1. Rosetta's [Universal Specimen](https://universalspecimen.rosettatype.com)
The Universal Specimen from Rosetta displays the Universal Declaraiton of Human Rights in multiple panels in 138 languages.

2. Aksharamukha : [Script Converter](http://aksharamukha.appspot.com/texts/triratnanusmriti)
This is an excellent resource for providing sample text – from old scriptures, or religious text – across many complex scripts and languages (including derivations).

## More about Specimen Skeleton

<p align="center">
	<img width="175" height="175" src="https://user-images.githubusercontent.com/4570664/74532263-0db14500-4f2f-11ea-96e9-49bcb8699ebb.png">
</p>

[Specimen Skeleton](https://github.com/kabisa/specimen-skeleton) is an [Eleventy-based](https://www.11ty.dev/) specimen _boilerplate_. It helps you get a basic site up and running quickly, and offers you a few interactive elements to build your demos from.

It will analyse your variable font and generate the CSS necessary _and_ all the sliders, so you'll hit the ground running!