# Test out various hyphenation schemes.
# Move the mouse to adjust the column width.

# Insert a soft hyphen character ("\u00AD") anywhere you want ptext to be able to insert a hyphen.

# https://pypi.org/project/hyphenate/ is used here for splitting into syllables.
# pip install hyphenate

import hyphenate
import re
import pygame
import ptext
import random

ptext.FONT_NAME_TEMPLATE = "../fonts/%s.ttf"

w, h = 1400, 1000
screen = pygame.display.set_mode((w, h))


def betweensyllables(word):
	return "\u00AD".join(hyphenate.hyphenate_word(word))

def everywhere(word):
	return "\u00AD".join(word)

def addhyphens(text, where):
	tokens = re.split("(\W)", text)
	for j in range(0, len(tokens), 2):
		tokens[j] = where(tokens[j])
	return "".join(tokens)

text0 = "\n".join([
	"alfa bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike",
	"pneumonoultramicroscopicsilicovolcanoconiosis",
	"$1,234,567.89 $1,234,567.89 $1,234,567.89",
	"альфа браво чарли дельта эхо фокстрот гольф отель индия джульетта кило лима майк",
	"".join(random.choices("""    aeiou12345!@#$%^&*()'",./-+""", k=100)),
])

texts = [
	text0,
	addhyphens(text0, betweensyllables),
	addhyphens(text0, everywhere),
]
titles = ["None", "Between syllables", "Everywhere"]

fontnames = "Boogaloo", "Bubblegum_Sans", "CherryCreamSoda", "Roboto_Condensed"

playing = True
while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False

	mx, my = pygame.mouse.get_pos()
	if mx >= 600:
		w = mx	
		
	screen.fill((0, 0, 0))
	screen.fill((40, 20, 0), (0, 0, w, h))
	
	pw = (w - 160) // 3
	for j, (text, title) in enumerate(zip(texts, titles)):
		rect = pygame.Rect(40 + (pw + 40) * j, 40, pw, h - 80)
		screen.fill((80, 40, 10), rect)

		ptext.draw(title, bottomleft = rect.topleft, fontname = "Boogaloo", fontsize = 18)
		args = {
			"topleft": rect.topleft,
			"width": rect.width,
#			"fontname": "Boogaloo",
			"fontsize": 30,
			"pspace": 0.5,
		}
		ptext.draw(text, **args)

	pygame.display.flip()

