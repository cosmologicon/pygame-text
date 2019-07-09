# Using the tag options for inline styling.

import pygame
import ptext

ptext.FONT_NAME_TEMPLATE = "../fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "SourceSerifPro"

screen = pygame.display.set_mode((1000, 700))
screen.fill((0, 30, 60))

# I use underscore (_) for underlining here, but the idea is that you can use whatever string you
# want.
ptext.draw("Specify the tag to _underline_ words. Close tags _are optional.", (50, 50), underlinetag="_")
ptext.draw("Tags are _not_ interpreted unless the underlinetag argument is set.", (50, 100))
ptext.draw("You can also *bold*, /italicize/, or add <color> by setting their tags.", (50, 150),
	boldtag="*", italictag="/", colortag = { "<": "red", ">": None })

# Set the default values, so you don't have to specify it every time.
# These values are just suggestions: any string can be used as a tag. You should pick tags that are
# not going to appear anywhere in your text.
ptext.DEFAULT_UNDERLINE_TAG = "_"
ptext.DEFAULT_BOLD_TAG = "*"
ptext.DEFAULT_ITALIC_TAG = "/"
ptext.DEFAULT_COLOR_TAG = {
	"<R": "red",
	"<Y": "yellow",
	"<B": "cyan",
	">": None,
}

ptext.draw("Defaults set. No _need_ to specify the <Y*tags*> every time now.", (50, 200))
ptext.draw("Use the same tag to _remove_ styling.", (50, 250), underline=True)
ptext.draw("You can over_ride the tag to use under_scores without tagging.", (50, 300), underlinetag=None)
ptext.draw("What about XYZmulticharacterXYZ tags?", (50, 350), italictag="XYZ")
ptext.draw("_Tagging_ with /word wrap..../ testing one <Ytwo three> four <Bfive six seven> eight.", (50, 400), width=180)

pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

