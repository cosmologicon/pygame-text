# Check how special characters appear in various fonts.

# Known special characters:

specials = {
	" ": "space",
	"\u00A0": "non-breaking space",
	"\u00AD": "soft hyphen",
	"\u200B": "zero-width space",
	"\u2011": "non-breaking hyphen",
	"\u2060": "word joiner",  # i.e. no hyphenation allowed
}

import pygame
import ptext

pygame.init()

screen = pygame.display.set_mode((640, 480))
screen.fill((60, 60, 60))

ptext.DEFAULT_FONT_SIZE = 30
ptext.DEFAULT_FONT_NAME = "fonts/Boogaloo.ttf"


ptext.draw("abcdef", (50, 50))

for j, (char, description) in enumerate(specials.items()):
	ptext.draw("abc" + char + "def", (50, 100 + 50 * j))
	ptext.draw(description, (150, 100 + 50 * j), color = "#ffffcc")

pygame.display.flip()

while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
	pass

