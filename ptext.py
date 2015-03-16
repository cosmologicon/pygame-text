# ptext module: place this in your import directory.

# ptext.draw(text, pos=None, surf=None, **options)

# options:
#   fontsize: defaults to 18
#   fontname: path to the font file. Defaults to None
#   
#   color: defaults to white
#   ocolor: outline color - defaults to None
#   scolor: shadow color - defaults to None
#   angle: counterclockwise rotation angle in degrees - defaults to 0
#   alpha: defaults to 1.0


# If pos is specified, the text is drawn with 
# If topleft is not specified, you must specify a keyword arg for the position of the text,
# corresponding to one of the keyword args that pygame.Surface.get_rect takes.

# If surf is not specified, it defaults to the current display surface.

# Wordwrap occurs anywhere text contains \n characters. It will also wrap f

from __future__ import division

from math import ceil
import pygame

DEFAULT_FONT_SIZE = 22
REFERENCE_FONT_SIZE = 100
DEFAULT_LINE_HEIGHT = 1.0
DEFAULT_FONT_NAME = None
FONT_NAME_TEMPLATE = "%s"
DEFAULT_COLOR = "white"
DEFAULT_BACKGROUND = None
DEFAULT_OUTLINE_COLOR = "black"
DEFAULT_SHADOW_COLOR = "black"
OUTLINE_UNIT = 1 / 24
SHADOW_UNIT = 1 / 18
DEFAULT_TEXT_ALIGN = "left"  # left, center, or right
DEFAULT_HORIZONTAL_ANCHOR = 0  # 0 = left, 0.5 = center, 1 = right
DEFAULT_VERTICAL_ANCHOR = 0  # 0 = top, 0.5 = center, 1 = bottom
ALPHA_RESOLUTION = 16

AUTO_CLEAN = True
MEMORY_LIMIT_MB = 64
MEMORY_REDUCTION_FACTOR = 0.5

_font_cache = {}
def getfont(fontname, fontsize):
	if fontname is None: fontname = DEFAULT_FONT_NAME
	if fontsize is None: fontsize = DEFAULT_FONT_SIZE
	key = fontname, fontsize
	if key in _font_cache: return _font_cache[key]
	if fontname is not None: fontname = FONT_NAME_TEMPLATE % fontname
	font = pygame.font.Font(fontname, fontsize)
	_font_cache[key] = font
	return font

def wrap(text, fontname, fontsize, width=None, widthem=None):
	if widthem is None:
		font = getfont(fontname, fontsize)
	elif width is not None:
		raise ValueError("Can't set both width and widthem")
	else:
		font = getfont(fontname, REFERENCE_FONT_SIZE)
		width = widthem * font.size("m")[0]
	texts = text.replace("\t", "    ").split("\n")
	if width is None:
		return texts
	lines = []
	for text in texts:
		a = len(text) - len(text.lstrip())
		if " " not in text[a:]:
			lines.append(text)
			continue
		# At any time, a is the leftmost index you can legally split a line (text[:a]).
		a = text.index(" ", a)
		while " " in text[a+1:]:
			b = text.index(" ", a+1)
			w, h = font.size(text[:b])
			if w <= width:
				a = b
			else:
				lines.append(text[:a])
				text = text[a+1:]
				a = (text + " ").index(" ")
		if text:
			lines.append(text[:a])
			if text[a+1:]:
				lines.append(text[a+1:])
	return lines

def _resolvecolor(color, default):
	if color is None: color = default
	if color is None: return None
	if isinstance(color, basestring): color = pygame.Color(color)
	return tuple(color)

_surf_cache = {}
_surf_tick_usage = {}
_surf_size_total = 0
_tick = 0
def getsurf(text, fontname=None, fontsize=None, width=None, widthem=None, color=None,
	background=None, antialias=True, ocolor=None, owidth=None, scolor=None, shadow=None,
	gcolor=None, alpha=1.0, textalign=None, lineheight=None):
	global _tick, _surf_size_total
	if fontname is None: fontname = DEFAULT_FONT_NAME
	if fontsize is None: fontsize = DEFAULT_FONT_SIZE
	fontsize = int(round(fontsize))
	if textalign is None: textalign = DEFAULT_TEXT_ALIGN
	if textalign in ["left", "center", "right"]:
		textalign = [0, 0.5, 1][["left", "center", "right"].index(textalign)]
	if lineheight is None: lineheight = DEFAULT_LINE_HEIGHT
	color = _resolvecolor(color, DEFAULT_COLOR)
	background = _resolvecolor(background, DEFAULT_BACKGROUND)
	gcolor = _resolvecolor(gcolor, None)
	ocolor = None if owidth is None else _resolvecolor(ocolor, DEFAULT_OUTLINE_COLOR)
	scolor = None if shadow is None else _resolvecolor(scolor, DEFAULT_SHADOW_COLOR)
	opx = None if owidth is None else ceil(owidth * fontsize * OUTLINE_UNIT)
	spx = None if shadow is None else tuple(ceil(s * fontsize * SHADOW_UNIT) for s in shadow)
	alpha = int(round(alpha * ALPHA_RESOLUTION)) / ALPHA_RESOLUTION
	key = (text, fontname, fontsize, width, widthem, color, background, antialias, ocolor, opx, spx,
		gcolor, alpha, textalign)
	if key in _surf_cache:
		_surf_tick_usage[key] = _tick
		_tick += 1
		return _surf_cache[key]
	texts = wrap(text, fontname, fontsize, width=width, widthem=widthem)
	if alpha < 1.0:
		surf0 = getsurf(text, fontname, fontsize, width, widthem, color, background, antialias,
			ocolor, owidth, scolor, shadow, gcolor=gcolor, textalign=textalign,
			lineheight=lineheight)
		surf = surf0.copy()
		array = pygame.surfarray.pixels_alpha(surf)
		array *= alpha
	elif spx is not None:
		surf0 = getsurf(text, fontname, fontsize, width, widthem, color=color,
			background=(0,0,0,0), antialias=antialias, gcolor=gcolor, textalign=textalign,
			lineheight=lineheight)
		ssurf = getsurf(text, fontname, fontsize, width, widthem, color=scolor,
			background=(0,0,0,0), antialias=antialias, textalign=textalign, lineheight=lineheight)
		w0, h0 = surf0.get_size()
		sx, sy = spx
		surf = pygame.Surface((w0 + abs(sx), h0 + abs(sy))).convert_alpha()
		surf.fill(background or (0, 0, 0, 0))
		dx, dy = max(sx, 0), max(sy, 0)
		surf.blit(ssurf, (dx, dy))
		surf.blit(surf0, (abs(sx) - dx, abs(sy) - dy))
	elif opx is not None:
		surf0 = getsurf(text, fontname, fontsize, width, widthem, color=color,
			background=(0,0,0,0), antialias=antialias, gcolor=gcolor, textalign=textalign,
			lineheight=lineheight)
		osurf = getsurf(text, fontname, fontsize, width, widthem, color=ocolor,
			background=(0,0,0,0), antialias=antialias, textalign=textalign, lineheight=lineheight)
		w0, h0 = surf0.get_size()
		surf = pygame.Surface((w0 + 2 * opx, h0 + 2 * opx)).convert_alpha()
		surf.fill(background or (0, 0, 0, 0))
		for dx in (0, opx, 2 * opx):
			for dy in (0, opx, 2 * opx):
				surf.blit(osurf, (dx, dy))
		surf.blit(surf0, (opx, opx))
	else:
		font = getfont(fontname, fontsize)
		# pygame.Font.render does not allow passing None as an argument value for background.
		if background is None or (len(background) > 3 and background[3] == 0) or gcolor is not None:
			lsurfs = [font.render(text, antialias, color).convert_alpha() for text in texts]
		else:
			lsurfs = [font.render(text, antialias, color, background).convert_alpha() for text in texts]
		if gcolor is not None:
			import numpy
			m = numpy.clip(numpy.arange(lsurfs[0].get_height()) * 2.0 / font.get_ascent() - 1.0, 0, 1)
			for lsurf in lsurfs:
				array = pygame.surfarray.pixels3d(lsurf)
				for j in (0, 1, 2):
					array[:,:,j] *= 1.0 - m
					array[:,:,j] += m * gcolor[j]
				del array
			
		if len(lsurfs) == 1 and gcolor is None:
			surf = lsurfs[0]
		else:
			ws, hs = zip(*[lsurf.get_size() for lsurf in lsurfs])
			linesize = font.get_linesize() * lineheight
			ys = [int(round(k * linesize)) for k in range(len(hs))]
			w, h = max(ws), ys[-1] + hs[-1]
			surf = pygame.Surface((w, h)).convert_alpha()
			surf.fill(background or (0, 0, 0, 0))
			for y, lsurf in zip(ys, lsurfs):
				x = int(round(textalign * (w - lsurf.get_width())))
				surf.blit(lsurf, (x, y))
	w, h = surf.get_size()
	_surf_size_total += 4 * w * h
	_surf_cache[key] = surf
	_surf_tick_usage[key] = _tick
	_tick += 1
	return surf

def draw(text, pos=None, surf=None, fontname=None, fontsize=None, width=None, widthem=None,
	color=None, background=None, antialias=True,
	ocolor=None, owidth=None, scolor=None, shadow=None, gcolor=None,
	top=None, left=None, bottom=None, right=None,
	topleft=None, bottomleft=None, topright=None, bottomright=None,
	midtop=None, midleft=None, midbottom=None, midright=None,
	center=None, centerx=None, centery=None,
	alpha=1.0, textalign=None, lineheight=None):
	
	if topleft: top, left = topleft
	if bottomleft: bottom, left = bottomleft
	if topright: top, right = topright
	if bottomright: bottom, right = bottomright
	if midtop: centerx, top = midtop
	if midleft: left, centery = midleft
	if midbottom: centerx, bottom = midbottom
	if midright: right, centery = midright
	if center: centerx, centery = center

	hanchor, vanchor = None, None
	x, y = pos or (None, None)
	if left is not None: x, hanchor = left, 0
	if centerx is not None: x, hanchor = centerx, 0.5
	if right is not None: x, hanchor = right, 1
	if top is not None: y, vanchor = top, 0
	if centery is not None: y, vanchor = centery, 0.5
	if bottom is not None: y, vanchor = bottom, 1
	if x is None:
		raise ValueError("Unable to determine horizontal position")
	if y is None:
		raise ValueError("Unable to determine vertical position")

	if textalign is None: textalign = hanchor
	if hanchor is None: hanchor = DEFAULT_HORIZONTAL_ANCHOR
	if vanchor is None: vanchor = DEFAULT_VERTICAL_ANCHOR

	tsurf = getsurf(text, fontname, fontsize, width, widthem, color, background, antialias,
		ocolor, owidth, scolor, shadow, gcolor, alpha, textalign, lineheight)
	x = int(round(x - hanchor * tsurf.get_width()))
	y = int(round(y - vanchor * tsurf.get_height()))

	if surf is None: surf = pygame.display.get_surface()
	surf.blit(tsurf, (x, y))
	
	if AUTO_CLEAN:
		clean()

def clean():
	global _surf_size_total
	memory_limit = MEMORY_LIMIT_MB * (1 << 20)
	if _surf_size_total < memory_limit:
		return
	memory_limit *= MEMORY_REDUCTION_FACTOR
	keys = sorted(_surf_cache, key=_surf_tick_usage.get)
	for key in keys:
		w, h = _surf_cache[key].get_size()
		del _surf_cache[key]
		del _surf_tick_usage[key]
		_surf_size_total -= 4 * w * h
		if _surf_size_total < memory_limit:
			break
	print _surf_size_total

if __name__ == "__main__":
	pygame.font.init()
	screen = pygame.display.set_mode((854, 480))
	screen.fill((0, 30, 0))
	FONT_NAME_TEMPLATE = "fonts/%s.ttf"
	DEFAULT_FONT_NAME = "CherryCreamSoda"
	DEFAULT_FONT_SIZE = 60
	screen.fill((0, 30, 0))
	draw("ppp\nqpq\nbbb", (100, 100), gcolor="red", owidth=1, lineheight=0.6)
	pygame.display.flip()
	while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
		pass

