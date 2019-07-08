import pygame, ptext
pygame.display.set_mode((640, 480))
#ptext.draw("foobar \n zimwat",  (0, 0), strip=True)

text = "one two three four five six seven eight nine ten\neleven _twelve thirteen fourteen fifteen_ sixteen seventeen"
text = "one two three four five six seven eight nine ten"
text = "eleven _twelve thirteen fourteen fifteen_ sixteen seventeen"
for fields in ptext._wrap(text, width=150, underlinetag="_"):
	print(*fields)

ptext.draw(text, topright=(500, 0), width=150, underlinetag="_", background="#664422")

pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

