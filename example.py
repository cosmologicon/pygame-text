# Example game using ptext module

import pygame
import ptext

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"

pygame.init()

sx, sy = 854, 480
screen = pygame.display.set_mode((sx, sy))
pygame.display.set_caption("Clooky Clunker")

score, totalscore, clunkers = 0, 0, 0
nextgoal = 0
tgoal = -100
clunks = []
tbuy, buytext = -100, ""
t = 0

buttonrects = [pygame.Rect((50, 120 + 85 * j, 180, 70)) for j in range(4)]
buttonnames = ["auto-clunker", "clunkutron", "turbo enclunkulator", "clunx capacitor"]
buttoncosts = [10, 400, 12000, 250000]

# Pre-draw the title, using a gradient.
titleargs = ptext.draw("Clooky Clunker", midtop=(sx/2, 10), fontname="CherryCreamSoda", fontsize=64,
	owidth=1.2, color="0x884400", gcolor="0x442200", surf=None, cache=False)

playing = True
clock = pygame.time.Clock()
while playing:
	dt = 0.001 * clock.tick()
	t += dt

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
		# Click on the central circle
		if (x - sx/2) ** 2 + (y - sy/2) ** 2 < 100 ** 2:
			score += 1
			totalscore += 1
			# Add a "clunk" indicator at a pseudorandom place near the center
			ix = sx/2 + 12345678910. / (1 + t) % 1 * 200 - 100
			iy = sy/2 + 45678910123. / (1 + t) % 1 * 200 - 100
			clunks.append((t, ix, iy))
		# Click on one of the buttons
		for j in range(len(buttonrects)):
			rect, cost = buttonrects[j], buttoncosts[j]
			if rect.collidepoint(x, y) and score >= cost:
				score -= cost
				clunkers += 10 ** j
				tbuy = t
				buytext = "+%s clunk/s" % (10 ** j)
				buttoncosts[j] += int(round(cost * 0.2))

	score += clunkers * dt
	totalscore += clunkers * dt

	# Check for next achievement
	if totalscore > 100 * (1 << nextgoal):
		goaltext = "Achievement unlocked:\nCL%sKY!" % ("O" * (nextgoal + 2))
		tgoal = t
		nextgoal += 1

	screen.fill((0, 30, 30))
	# Draw the circle in the middle
	pygame.draw.circle(screen, 0x0, (sx//2, sy//2), 106)
	pygame.draw.circle(screen, 0x884400, (sx//2, sy//2), 100)
	# Draw the buttons using ptext.drawbox
	for rect, name, cost in zip(buttonrects, buttonnames, buttoncosts):
		screen.fill(pygame.Color("#553300"), rect)
		screen.fill(pygame.Color("#332200"), rect.inflate(-8, -8))
		text = u"%s: %d\u00A0clunks" % (name, cost)
		color = "white" if cost <= score else "#666666"
		box = rect.inflate(-16, -16)
		ptext.drawbox(text, box, fontname="Bubblegum_Sans", lineheight=0.9, color=color, owidth=0.5)
	# Draw the HUD
	hudtext = "\n".join([
		"time played: %d" % t,
		"clunks: %d" % score,
		"all-time clunks: %d" % totalscore,
		"clunks per second: %d" % clunkers,
	])
	ptext.draw(hudtext, right=sx-10, top=120, fontname="Roboto_Condensed", fontsize=32,
		color=(0,200,0), shade=1, scolor=(0,50,0), shadow=(-1,1), lineheight=1.3)
	# Draw the title
	screen.blit(*titleargs)
	# Draw "clunk" indicators
	for it, ix, iy in clunks:
		dt = t - it
		pos = ix, iy-60*dt
		ptext.draw("clunk", center=pos, fontname=None, fontsize=28, alpha=1-dt, shadow=(1,1))
	clunks = list(filter((lambda clunk: t - clunk[0] < 1), clunks))
	# Draw purchase indicator
	if t - tbuy < 1:
		dt = t - tbuy
		pos = sx/2, sy/2
		fontsize = 32 * (1 + 60 * dt) ** 0.2
		ptext.draw(buytext, pos, anchor=(0.5,0.9), fontname="Bubblegum_Sans",
			fontsize=fontsize, alpha=1-dt, shadow=(1,1))
	# Draw achievement unlocked text (text is centered even though we specify bottom right).
	if t - tgoal < 2:
		alpha = min(2 - (t - tgoal), 1)
		ptext.draw(goaltext, fontname="Boogaloo", fontsize=48, bottom=sy-20, right=sx-40,
			color="#AAAAFF", gcolor="#4444AA", shadow=(1.5,1.5), alpha=alpha, align="center")
	pygame.display.flip()

