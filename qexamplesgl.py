"""Version of qexamplesgl.py using ptextgl."""

import pygame
from OpenGL.GL import *
import ptextgl

screen = pygame.display.set_mode((854, 480), pygame.OPENGL | pygame.DOUBLEBUF)
glViewport(0, 0, 854, 480)
glClearColor(0, 0.12, 0.24, 1)
glClear(GL_COLOR_BUFFER_BIT)

ptextgl.draw("Font name and size", (20, 100), fontname="fonts/Boogaloo.ttf", fontsize=60)
ptextgl.draw("Font decoration", (300, 180), sysfontname="freesans", italic=True, underline=True)
ptextgl.draw("Positioned text", topright=(840, 20))
ptextgl.draw("Here's some neatly-wrapped text.", (90, 210), width=120, lineheight=1.5)
ptextgl.draw("Outlined text", (400, 70), owidth=1.5, ocolor=(255,255,0), color=(0,0,0))
ptextgl.draw("Drop shadow", (640, 110), shadow=(2,2), scolor="#202020")
ptextgl.draw("Color gradient", (540, 170), color="red", gcolor="purple")
ptextgl.draw("Transparency", (700, 240), alpha=0.1)
ptextgl.draw("Vertical text", midleft=(40, 440), angle=90)
ptextgl.draw("Inline _styling_ with tags", (630, 320), underlinetag="_")
ptextgl.draw("All together now:\nCombining the above options",
    midbottom=(427,460), width=360, fontname="fonts/Boogaloo.ttf", fontsize=48, underline=True,
    color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, angle=5)

pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass
