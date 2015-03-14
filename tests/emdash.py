# Estimate how the size of the em dash in various fonts corresponds to font.Font.metrics.

import pygame

pygame.font.init()
font = pygame.font.Font(None, 140)
print font.size("m")

