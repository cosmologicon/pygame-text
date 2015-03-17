# pygame-text

This module simplifies drawing text with the pygame.font module. Specifically, the `ptext` module:

* handles the pygame.font.Font objects.
* handles the separate step of generating a Surface and then blitting it.
* caches commonly-used Surfaces.
* handles word wrap.
* provides more fine-grained text positioning options.
* provides a few special effects: outlines, drop shadows, gradient fill, and transparency.

## Quick usage example

	ptext.draw("hello world", (200, 100), fontname="Arial.ttf", fontsize=60, color="orange")

## To install

Download `ptext.py` and put it in your source directory. To install from command line:

    curl https://raw.githubusercontent.com/cosmologicon/pygame-text/master/ptext.py > my-source-directory/ptext.py

## Detailed usage

`ptext.draw` requires the string you want to draw, and the position. You can either do this by
passing coordinates as the second argument (which is the top left of where the text will appear), or
use the positioning keyword arguments (described later).

	ptext.draw("hello world", (20, 100))

`ptext.draw` takes many optional keyword arguments, described below.

The `ptext` module also has many module-level globals that control the default behavior. Please set
these to your desired defaults.

## Font name and size

Keyword arguments:

* `fontname`: filename of the font to draw. Defaults to `ptext.DEFAULT_FONT_NAME`, which is set to
`None` by default.
* `fontsize`: size of the font to use, in pixels. Defaults to `ptext.DEFAULT_FONT_SIZE`, which is
set to `24` by default.
* `antialias`: whether to render with antialiasing. Defaults to `True`.

	ptext.draw("hello world", (100, 100), fontname="fonts/Viga.ttf", fontsize=32)

If you don't want to specify the whole filename for the fonts every time, it can be useful to set
`ptext.FONT_NAME_TEMPLATE`. For instance, if your fonts are in a subdirectory called `fonts` and all
have the extension `.ttf`:

	ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
	ptext.draw("hello world", (100, 100), fontname="Viga")  # Will look for fonts/Viga.ttf

`fontname=None` always refers to the system font.

## Color and background color

Keyword arguments:

* `color`: foreground color to use. Defaults to `ptext.DEFAULT_COLOR`, which is set to `"white"` by
default.
* `background`: background color to use. Defaults to `ptext.DEFAULT_BACKGROUND`, which is set to
`None` by default.

	ptext.draw("hello world", (100, 100), color=(200, 200, 200), background="gray")

`color` (as well as `background`, `ocolor`, `scolor`, and `gcolor`) can be an (r, g, b) sequence, a
`pygame.Color` object, a color name such as `"orange"`, an HTML hex color string such as
`"#FF7F00"`, or a hexadecimal color number such as `0xFF7F00`.

`background` can also be `None`, in which case the background is transparent.

Colors with alpha transparency are not supported. See the `alpha` keyword argument for transparency.

## Positioning

Keyword arguments:

	top left bottom right
	topleft bottomleft topright bottomright
	midtop midleft midbottom midright
	center centerx centery

	ptext.draw("hello world", centery=50, right=300)
	ptext.draw("hello world", midtop=(400, 0))

Positioning keyword arguments behave like the corresponding properties of `pygame.Rect`. Either
specify two arguments, corresponding to the horizontal and vertical positions of the box, or a
single argument that specifies both.

If the position is overspecified (e.g. both `left` and `right` are given), then extra specifications
will be (arbitrarily but deterministically) discarded.

## Word wrap

Keyword arguments:

* `width`: maximum width of the text to draw, in pixels. Defaults to `None`.
* `widthem`: maximum width of the text to draw, in font-based em units. Defaults to `None`.
* `lineheight`: vertical spacing between lines, in units of the font's default line height. Defaults
to `1.0`.

    ptext.draw("splitting\nlines", (100, 100))
    ptext.draw("splitting lines", (100, 100), width=60)

`ptext.draw` will always wrap lines at newline (`\n`) characters. If `width` or `widthem` is also
set, it will also try to wrap lines in order to keep each line shorter than the given width. The
text is not guaranteed to be within the given width, because wrapping only occurs at space
characters, so if a single word is too long to fit on a line, it will not be broken up. Outline and
drop shadow are also not accounted for, so they may extend beyond the given width.

You can prevent wrapping on a given space with non-breaking space characters (`\u00A0`).

## Text alignment

Keyword argument:

* `textalign`: horizontal positioning of lines with respect to each other. Defaults to `None`.

    ptext.draw("hello\nworld", bottomright=(500, 400), textalign="left")

`textalign` determines how lines are positioned horizontally with respect to each other, when more
than one line is drawn. Valid values for `textalign` are the strings `"left"`, `"center"`, or
`"right"`, a numerical value between `0.0` (for left alignment) and `1.0` (for right alignment),
or `None`.

If `textalign` is `None`, the alignment is determined based on how the text is positioned
horizontally. If the left side of the text is positioned (by specifying one of the keyword arguments
`left`, `topleft`, `bottomleft`, or `midleft`), then the text will be left-aligned. Similarly if the
right or horizontal center of the text is positioned. If `anchor` is specified, the text alignment
will be equal to `anchor[0]`. Finally, if no keyword arguments are used to specify position, the
alignment defaults to `ptext.DEFAULT_TEXT_ALIGN`, which is set to `"left"` by default.

## Outline

Keyword arguments:

* `owidth`: outline thickness, in outline units. Defaults to `None`.
* `ocolor`: outline color. Defaults to `ptext.DEFAULT_OUTLINE_COLOR`, which is set to `"black"` by
default.

	ptext.draw("hello world", (100, 100), owidth=1, ocolor="blue")

The text will be outlined if `owidth` is specified. The outlining is a crude manual method, and will
probably look bad at large font sizes. The units of `owidth` are chosen so that `1.0` is a good
typical value for outlines. Specifically, they're the font size times `ptext.OUTLINE_UNIT`, which is
set to `1/24` by default.

Valid values for `ocolor` are the same as for `color`.

## Drop shadow

Keyword arguments:

* `shadow`: (x,y) values representing the drop shadow offset, in shadow units. Defaults to `None`.
* `scolor`: drop shadow color. Defaults to `ptext.DEFAULT_SHADOW_COLOR`, which is `"black"` by
default.

	ptext.draw("hello world", (100, 100), shadow=(1.0,1.0), ocolor="blue")

The text will have a drop shadow if `shadow` is specified. It must be set to a 2-element sequence
representing the x and y offsets of the drop shadow, which can be positive, negative, or 0. For
example, `shadow=(1.0,1.0)` corresponds to a shadow down and to the right of the text.
`shadow=(0,-1.2)` corresponds to a shadow higher than the text.

The units of `shadow` are chosen so that `1.0` is a good typical value for the offset. Specifically,
they're the font size times `ptext.SHADOW_UNIT`, which is set to `1/18` by default.

Valid values for `scolor` are the same as for `color`.

## Gradient color

Keyword argument:

* `gcolor`: Lower gradient stop color. Defaults to `None`.

	ptext.draw("hello world", (100, 100), color="black", gcolor="green")

Specify `gcolor` to color the text with a vertical color gradient. The text's color will be `color`
at the top and `gcolor` at the bottom. Positioning of the gradient stops and orientation of the
gradient are hard coded and cannot be specified.

Requries `pygame.surfarray` module, which uses numpy or Numeric library.

## Alpha transparency

Keyword argument:

* `alpha`: alpha transparency value, between 0 and 1. Defaults to `1.0`.

	ptext.draw("hello world", (100, 100), alpha=0.5)

In order to maximize reuse of cached transparent surfaces, the value of `alpha` is rounded.
`ptext.ALPHA_RESOLUTION`, which is set to `16` by default, specifies the number of different values
`alpha` may take internally. Set it higher (up to `255`) for more fine-grained control over
transparency values.

Requries `pygame.surfarray` module, which uses numpy or Numeric library.

## Anchored positioning

Keyword argument:

* `anchor`: a length-2 sequence of horizontal and vertical anchor fractions. Defaults to
`ptext.DEFAULT_ANCHOR`, which is set to `(0.0, 0.0)` by default.

	ptext.draw("hello world", (100, 100), anchor=(0.3,0.7))

`anchor` specifies how the text is anchored to the given position, when no positioning keyword
arguments are passed. The two values in `anchor` can take arbitrary values between `0.0` and `1.0`.
An `anchor` value of `(0,0)`, the default, means that the given position is the top left of the
text. A value of `(1,1)` means the given position is the bettom right of the text.

## Destination surface

Keyword arugment:

* `surf`: destination `pygame.Surface` object. Defaults to the display Surface.

	mysurface = pygame.Surface((400, 400)).convert_alpha()
	ptext.draw("hello world", (100, 100), surf=mysurface)

Specify `surf` if you don't want to draw directly to the display Surface
(`pygame.display.get_surface()`).



