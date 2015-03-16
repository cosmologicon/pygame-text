# Example game using ptext module

import pygame
import random
import ptext

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

pygame.init()

sx, sy = 854, 480
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Clooky Clunker")

score, totalscore, clunkers = 0, 0, 0
nextgoal = 0
tgoal = -100
infos = []
t = 0

buttonrects = [pygame.Rect((50, 120 + 85 * j, 180, 70)) for j in range(4)]
buttonnames = ["auto-clunker", "clunkutron", "turbo enclunkulator", "clunx capacitor"]
buttoncosts = [10, 400, 12000, 250000]

playing = True
while playing:
	nextt = 0.001 * pygame.time.get_ticks()
	t, dt = nextt, nextt - t
	clickpos = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			clickpos = event.pos

	if clickpos:
		x, y = clickpos
		if (x - sx/2) ** 2 + (y - sy/2) ** 2 < 100 ** 2:
			score += 1
			totalscore += 1
			ix, iy = sx/2 + random.uniform(-100, 100), sy/2 + random.uniform(-100, 100)
			infos.append((t, ix, iy, "clunk"))
		for j in range(len(buttonrects)):
			rect = buttonrects[j]
			if rect.collidepoint(x, y):
				cost = buttoncosts[j]
				if score >= cost:
					score -= cost
					clunkers += 10 ** j
					buttoncosts[j] += int(round(cost * 0.2))

	score += clunkers * dt
	totalscore += clunkers * dt

	if totalscore > 100 * (1 << nextgoal):
		goaltext = "Achievement unlocked:\nCL%sKY!" % ("O" * (nextgoal + 2))
		tgoal = t
		nextgoal += 1

	screen.fill((0, 30, 30))
	pygame.draw.circle(screen, 0x0, (sx/2, sy/2), 106)
	pygame.draw.circle(screen, 0x884400, (sx/2, sy/2), 100)
	for rect, name, cost in zip(buttonrects, buttonnames, buttoncosts):
		screen.fill(pygame.Color("#553300"), rect)
		screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
		text = u"%s: %d\u00A0clunks" % (name, cost)
		color = "white" if cost <= score else "#666666"
		box = rect.inflate(-16, -16)
		ptext.drawbox(text, box, fontname="Bubblegum_Sans", lineheight=0.9, color=color, owidth=0.5)
	hudtext = "\n".join([
		"time played: %d" % t,
		"clunks: %d" % score,
		"all-time clunks: %d" % totalscore,
		"clunks per second: %d" % clunkers,
	])
	ptext.draw(hudtext, right=sx-10, top=120, fontname="Roboto_Condensed", fontsize=32,
		color="#00AA00", scolor="#005500", shadow=(-1,1), lineheight=1.3)
	ptext.draw("Clooky Clunker", midtop=(sx/2, 10), fontname="CherryCreamSoda", fontsize=64,
		owidth=1.2, color="#884400", gcolor="#442200")
	for it, ix, iy, text in infos:
		dt = t - it
		ptext.draw(text, fontname=None, fontsize=28, center=(ix, iy-60*dt), alpha=1-dt, shadow=(1,1))
	infos = filter((lambda info: t - info[0] < 1), infos)
	if t - tgoal < 2:
		alpha = min(2 - (t - tgoal), 1)
		ptext.draw(goaltext, fontname="Boogaloo", fontsize=48, bottom=sy-20, right=sx-40,
			color="#AAAAFF", gcolor="#4444AA", shadow=(1.5,1.5), alpha=alpha, textalign="center")
	pygame.display.flip()

