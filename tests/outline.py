# Outline algorithm

import pygame

opx = 2  # outline size in pixels


# Return the set of points in the circle radius r, using Bresenham's circle algorithm
def _circlepoints(r):
	r = int(round(r))
	x, y, e = r, 0, 1 - r
	points = []
	while x >= y:
		points.append((x, y))
		y += 1
		if e < 0:
			e += 2 * y - 1
		else:
			x -= 1
			e += 2 * (y - x) - 1
	points += [(y, x) for x, y in points if x > y]
	points += [(-x, y) for x, y in points if x]
	points += [(x, -y) for x, y in points if y]
	points.sort()
	return points

screen = pygame.display.set_mode((1000, 600))
screen.fill((100, 100, 200))
pygame.font.init()
font = pygame.font.Font(None, 60)

def getsurf(color):
	return font.render("hello", True, color).convert_alpha()

def getoutlinesurf(blendmode = None):
	surf = pygame.Surface((300, 100)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for dx, dy in _circlepoints(opx):
		if blendmode is not None:
			surf.blit(osurf, (dx + opx, dy + opx), None, blendmode)
		else:
			surf.blit(osurf, (dx + opx, dy + opx))
	surf.blit(tsurf, (opx, opx))
	return surf
	

osurf = getsurf((0, 0, 0, 0))
tsurf = getsurf((255, 255, 255, 0))
for offset, blendmax in [(0, False), (300, True)]:
	surf = pygame.Surface((300, 100)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	for dx, dy in _circlepoints(opx):
		if blendmax:
			surf.blit(osurf, (dx + opx, dy + opx), None, pygame.BLEND_RGBA_MAX)
		else:
			surf.blit(osurf, (dx + opx, dy + opx))
	surf.blit(tsurf, (opx, opx))
	screen.blit(pygame.transform.scale(surf, (300*6, 100*6)), (0, offset))

pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

