from __future__ import division

import numpy
import os
import pygame

fontsize = 60
text = "yellowjQW"

screen = pygame.display.set_mode((600, 400))
screen.fill((20, 120, 120))
pygame.font.init()
font = pygame.font.Font(None, fontsize)

linesize = font.get_linesize()
height = font.get_height()
ascent = font.get_ascent()
descent = font.get_descent()

color = 255, 255, 0
gcolor = 200, 100, 0

surf = font.render(text, True, color).convert_alpha()
array = pygame.surfarray.pixels3d(surf)
m = numpy.clip(numpy.arange(array.shape[1]) * 2.0 / ascent - 1.0, 0, 1)
for j in (0, 1, 2):
	array[:,:,j] = (array[:,:,j] * (1.0 - m)) + m * gcolor[j]
#array *= 0.6
del array
screen.blit(surf, (100, 100))


surf = font.render(text, True, (0, 0, 0)).convert_alpha()
w, h = surf.get_size()
gsurf = pygame.Surface((1, h))
for y in range(h):
	f = min(max(2 * y / ascent - 1, 0), 1)
	c = tuple(int(round(a * (1 - f) + b * f)) for a, b in zip(color, gcolor))
	c = pygame.Color(c[0], c[1], c[2], 255)
	gsurf.set_at((0, y), c)
gsurf = pygame.transform.scale(gsurf, (w, h))
surf.blit(gsurf, (0, 0), None, pygame.BLEND_RGB_ADD)
screen.blit(surf, (100, 200))


pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

