import pygame
from OpenGL.GL import *
import ptextgl

screen = pygame.display.set_mode((640, 640), pygame.OPENGL | pygame.DOUBLEBUF)
glViewport(0, 0, 640, 640)
glClearColor(0.3, 0, 0, 1)

jframe = 0
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	glClear(GL_COLOR_BUFFER_BIT)
	ptextgl.draw("%d" % jframe, center = (320, 320), fontsize = 240, fontname = "fonts/Boogaloo.ttf")
	text = "\n".join([
		"ptextgl tick: %d" % ptextgl._tick,
		"texture count: %d" % len(ptextgl._texture_cache),
		"texture cache size: %.1fMB" % (ptextgl._texture_size_total / (1 << 20)),
	])
	ptextgl.draw(text, bottomleft = (20, 620), shadow = (1, 1), fontsize = 40, fontname = "fonts/Boogaloo.ttf")
	jframe += 1
	pygame.display.flip()

