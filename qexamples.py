"""Quick usage examples from the README file"""

import pygame
import ptext

screen = pygame.display.set_mode((854, 480))
screen.fill((0, 30, 60))

ptext.draw("Font name and size", (20, 100), fontname="fonts/Boogaloo.ttf", fontsize=60)
ptext.draw("Font decoration", (300, 180), sysfontname="freesans", italic=True, underline=True)
ptext.draw("Positioned text", topright=(840, 20))
ptext.draw("Allow me to demonstrate wrapped text.", (90, 210), width=180, lineheight=1.5)
ptext.draw("Outlined text", (400, 70), owidth=1.5, ocolor=(255,255,0), color=(0,0,0))
ptext.draw("Drop shadow", (640, 110), shadow=(2,2), scolor="#202020")
ptext.draw("Color gradient", (540, 170), color="red", gcolor="purple")
ptext.draw("Transparency", (700, 240), alpha=0.1)
ptext.draw("Vertical text", midleft=(40, 440), angle=90)
ptext.draw("All together now:\nCombining the above options",
    midbottom=(427,460), width=360, fontname="fonts/Boogaloo.ttf", fontsize=48, underline=True,
    color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)

pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

