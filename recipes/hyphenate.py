import pygame
import ptext

ptext.FONT_NAME_TEMPLATE = "../fonts/%s.ttf"

screen = pygame.display.set_mode((854, 480))

text0 = (
	"alfa bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike "
#	"november oscar papa quebec romeo sierra tango uniform victor whiskey xray yankee zulu"
)
text = "\n".join([
	text0,
	# Soft hyphens between each letter: allow hyphenation anywhere.
	" ".join("\u00AD".join(word) for word in text0.split()),
	# Zero-width spaces.
	"\u200B".join(text0.split()),
])

fontsizes = 10, 12, 15, 18, 20, 22, 25, 27, 30, 33
fontnames = "Boogaloo", "Bubblegum_Sans", "CherryCreamSoda", "Roboto_Condensed"
outlines = 0, 2, 12
shadows = None, (5, 5), (-5, 5), (-5, -5), (5, -5)
lineheights = 0.6, 1, 2

jfontsizes = 1
jfontnames = 0
joutlines = 0
jshadows = 0
jlineheights = 1

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
	]
	ptext.draw("\n".join(info), midtop = (720, 40), owidth=2, fontsize=24, fontname="Roboto_Condensed")

	pygame.display.flip()

