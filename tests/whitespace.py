import pygame
import ptext

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
screen.fill((60, 60, 60))

ptext.DEFAULT_BACKGROUND = "#663300"
ptext.DEFAULT_FONT_SIZE = 30

for jx, (align, strip) in enumerate([("left", False), ("right", False), ("left", True), ("right", True)]):
	ptext.DEFAULT_ALIGN = align
	ptext.DEFAULT_STRIP = strip
	x = 100 + 140 * jx
	screen.fill((30, 30, 30), (x, 0, 120, 1000))
	kpos = {"right": x + 120} if align == "right" else {"left": x}

	ptext.draw("", top = 0, **kpos)
	ptext.draw("   A   ", top = 30, **kpos)
	ptext.draw("      ", top = 60, **kpos)
	ptext.draw("   \n   ", top = 90, **kpos)
	ptext.draw("one two three four", width = 120, top = 150, **kpos)
	ptext.draw("one   two   three", width = 120, top = 210, **kpos)
	ptext.draw("one                                             two", width = 120, top = 270, **kpos)
	ptext.draw("one two three four five six seven eight nine ten eleven", width = 120, top = 330, fontsize = 15, **kpos)
	ptext.draw("foobar \n zimwat", top = 420, **kpos)
	ptext.draw(None, top = 480, **kpos)

screen.blit(ptext.getfont().render("", True, (255, 255, 255), (0, 0, 255)), (0, 0))

pygame.display.flip()

while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
	pass

