
import os
import pygame

fontsize = 60
text = "yellowjQW"

screen = pygame.display.set_mode((600, 1000))
screen.fill((20, 20, 20))
pygame.font.init()
fonts = [pygame.font.Font("fonts/" + fontname, fontsize) for fontname in sorted(os.listdir("fonts"))]

for j, font in enumerate(fonts):
	x0, y0 = 40, 40 + int(1.5 * j * fontsize)
	metrics = font.metrics(text)
	linesize = font.get_linesize()
	height = font.get_height()
	ascent = font.get_ascent()
	descent = font.get_descent()
	x = x0
	for j, (minx, maxx, miny, maxy, advance) in enumerate(metrics):
		y = y0 + ascent - maxy
		if j % 4 == 0:
			screen.fill((60, 60, 0), (x, y, maxx - minx, maxy - miny))
		x += advance
	def drawline(color, dy):
		pygame.draw.line(screen, color, (0, y0 + dy), (1000, y0 + dy))
	drawline((255, 0, 0), 0)
	drawline((255, 0, 0), height)
	drawline((0, 0, 255), ascent)
#	drawline((0, 0, 255), height + descent)
#	drawline((0, 255, 0), linesize)
	surf = font.render(text, True, (255, 255, 255), (128, 128, 128)).convert_alpha()
	array = pygame.surfarray.pixels_alpha(surf)
	array *= 0.6
	del array
	screen.blit(surf, (x0, y0))
	
pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

