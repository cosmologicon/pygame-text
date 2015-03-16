
import numpy
import os
import pygame

fontsize = 60
text = "yellowjQW"

screen = pygame.display.set_mode((600, 400))
screen.fill((20, 20, 20))
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
	array[:,:,j] *= 1.0 - m
	array[:,:,j] += m * gcolor[j]
#array *= 0.6
del array
screen.blit(surf, (100, 100))
	
pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

