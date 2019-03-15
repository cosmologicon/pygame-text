# Using the tag options for inline styling.

# I use underscore (_) for underlining here, but the idea is that you can use whatever string you
# want. I recommend picking a string that you won't use in your game text, and setting
# ptext.DEFAULT_UNDERLINE_TAG to that.


import pygame
import ptext

ptext.FONT_NAME_TEMPLATE = "../fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "SourceSerifPro"

screen = pygame.display.set_mode((1000, 700))
screen.fill((0, 0, 0))

ptext.draw("Specify the tag to _underline_ words. Close tags _are optional.", (50, 50), underlinetag="_")
ptext.draw("Tags are _not_ interpreted unless the underlinetag argument is set.", (50, 100))

# Set the default value of underlinetag, so you don't have to specify it every time.
ptext.DEFAULT_UNDERLINE_TAG = "_"

ptext.draw("No _need_ to specify the _underlinetag_ now!", (50, 150))
ptext.draw("Use the same tag to _remove_ underlining!", (50, 200), underline=True)
ptext.draw("You can over_ride the tag to use under_scores without tagging.", (50, 250), underlinetag=None)
ptext.draw("What about XYZmulticharacterXYZ tags?", (50, 300), underlinetag="XYZ")
ptext.draw("Testing _underlining with word wrap...._ one _two three_ four _five six seven_ eight.", (50, 350), width=180)


pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass


