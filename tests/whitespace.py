import pygame
import ptext

pygame.init()

screen = pygame.display.set_mode((1000, 800))
screen.fill((60, 60, 60))

ptext.DEFAULT_BACKGROUND = "#663300"
ptext.DEFAULT_FONT_SIZE = 50

for jx, (align, strip) in enumerate([("left", False), ("right", False), ("left", True), ("right", True)]):
	ptext.DEFAULT_ALIGN = align
	ptext.DEFAULT_STRIP = strip
	x = 100 + 220 * jx
	screen.fill((30, 30, 30), (x, 100, 200, 600))
	kpos = {"right": x + 200} if align == "right" else {"left": x}

	ptext.draw("", top = 100, **kpos)
	ptext.draw("   A   ", top = 150, **kpos)
	ptext.draw("      ", top = 200, **kpos)
	ptext.draw("   \n   ", top = 250, **kpos)
	ptext.draw("one two three four", width = 200, top = 350, **kpos)
	ptext.draw("one   two   three", width = 200, top = 450, **kpos)
	ptext.draw("one                                             two", width = 200, top = 550, **kpos)

pygame.display.flip()

while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
	pass

