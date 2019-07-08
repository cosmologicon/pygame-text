# Using ptext.layout to get the word that the mouse is pointing at.

import pygame
import ptext

ptext.FONT_NAME_TEMPLATE = "../fonts/%s.ttf"

screen = pygame.display.set_mode((854, 480))

text = (
	"alfa bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike "
	"november oscar papa quebec romeo sierra tango uniform victor whiskey xray yankee zulu\n"
) * 3

fontsizes = 10, 20, 30, 50
fontnames = "Boogaloo", "Bubblegum_Sans", "CherryCreamSoda", "Roboto_Condensed"
outlines = 0, 2, 12
shadows = None, (5, 5), (-5, 5), (-5, -5), (5, -5)
lineheights = 0.6, 1, 2

jfontsizes = 1
jfontnames = 0
joutlines = 0
jshadows = 0
jlineheights = 1

# font: a pygame.font.Font object
# text: a string line of text
# dx: the offset from the left of the line.
# Returns: the word within the given text that occurs at dx pixels into the line.
def wordat(font, text, dx):
	# Find the index i that's the largest such that text[:i] is less than dx pixels wide in the
	# given font. O(N) here can be improved to O(log N) with binary search.
	for i in range(len(text)):
		if font.size(text[:i+1])[0] > dx:
			break
	else:
		return None
	if text[i] == " ":
		return None
	# Find the word that the ith character is part of. This is a simple word split method where we
	# just assume anything that's not a space character is part of the word. A more sophisticated
	# approach would handle punctuation.
	if " " in text[i+1:]:
		text = text[:text.index(" ", i+1)]
	if " " in text:
		text = text[text.rindex(" ")+1:]
	return text

# font: the pygame.font.Font object used to draw the text
# lines: a list of (text, rect) tuples. text is the string written for this line of text, and
#   rect is the pygame.Rect that it covers.
# pos: the position of the pointer.
# Returns: either the word that appears at the position pos, or None.
def pointedword(layout, pos):
	for text, rect, font in layout:
		if rect.collidepoint(pos):
			dx = pos[0] - rect.left
			return wordat(font, text, dx)
	return None

playing = True
while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_1:
				jfontsizes = (jfontsizes + 1) % len(fontsizes)
			if event.key == pygame.K_2:
				jfontnames = (jfontnames + 1) % len(fontnames)
			if event.key == pygame.K_3:
				joutlines = (joutlines + 1) % len(outlines)
			if event.key == pygame.K_4:
				jshadows = (jshadows + 1) % len(shadows)
			if event.key == pygame.K_5:
				jlineheights = (jlineheights + 1) % len(lineheights)

	screen.fill((40, 20, 0))
	screen.fill((80, 40, 10), (40, 100, 500, 340))

	args = {
		"midtop": (290, 100),
		"width": 500,
		"fontname": fontnames[jfontnames],
		"fontsize": fontsizes[jfontsizes],
		"owidth": outlines[joutlines],
		"shadow": shadows[jshadows],
		"lineheight": lineheights[jlineheights],
	}
	ptext.draw(text, **args)
	layout = ptext.layout(text, **args)
	word = pointedword(layout, pygame.mouse.get_pos())
	if not pygame.Rect(40, 100, 500, 340).collidepoint(pygame.mouse.get_pos()):
		for line, rect, font in layout:
			surf = pygame.Surface(rect.size).convert_alpha()
			surf.fill((255, 255, 255, 40))
			screen.blit(surf, rect)

	info = [
		"Controls:",
		"1: cycle fontsize",
		"current: %d" % fontsizes[jfontsizes],
		"2: cycle fontname",
		"current: %s" % fontnames[jfontnames],
		"3: cycle outline",
		"current: %s" % outlines[joutlines],
		"4: cycle shadow",
		"current: %s" % (shadows[jshadows],),
		"5: cycle lineheight",
		"current: %s" % lineheights[jlineheights],
		"",
		"pointed word:\n%s" % (word or ""),
	]
	ptext.draw("\n".join(info), midtop = (720, 40), owidth=2, fontsize=24, fontname="Roboto_Condensed")

	pygame.display.flip()

