# ptext module: place this in your import directory.

# ptext.draw(text, pos=None, **options)

# Please see README.md for explanation of options.
# https://github.com/cosmologicon/pygame-text

from __future__ import division

from math import ceil, sin, cos, radians, exp
from collections import namedtuple
import pygame

DEFAULT_FONT_SIZE = 24
REFERENCE_FONT_SIZE = 100
DEFAULT_LINE_HEIGHT = 1.0
DEFAULT_PARAGRAPH_SPACE = 0.0
DEFAULT_FONT_NAME = None
FONT_NAME_TEMPLATE = "%s"
DEFAULT_COLOR = "white"
DEFAULT_BACKGROUND = None
DEFAULT_SHADE = 0
DEFAULT_OUTLINE_COLOR = "black"
DEFAULT_SHADOW_COLOR = "black"
OUTLINE_UNIT = 1 / 24
SHADOW_UNIT = 1 / 18
DEFAULT_ALIGN = "left"  # left, center, or right
DEFAULT_ANCHOR = 0, 0  # 0, 0 = top left ;  1, 1 = bottom right
DEFAULT_STRIP = True
ALPHA_RESOLUTION = 16
ANGLE_RESOLUTION_DEGREES = 3

AUTO_CLEAN = True
MEMORY_LIMIT_MB = 64
MEMORY_REDUCTION_FACTOR = 0.5

pygame.font.init()


# Options object base class.
# Specify valid fields in the _fields list. Unspecified fields default to None, unless otherwise
# specified in the _defaults list.
class _Options(object):
	_fields = ()
	_defaults = {}
	def __init__(self, **kwargs):
		fields = self._allfields()
		badfields = set(kwargs) - fields
		if badfields:
			raise ValueError("Unrecognized args: " + ", ".join(badfields))
		for field in fields:
			value = kwargs[field] if field in kwargs else self._defaults.get(field)
			setattr(self, field, value)
	@classmethod
	def _allfields(cls):
		return set(cls._fields) | set(cls._defaults)
	def update(self, **newkwargs):
		kwargs = { field: getattr(self, field) for field in self._allfields() }
		kwargs.update(**newkwargs)
		return kwargs

_default_surf_sentinel = ()

# Options argument for the draw function. Specifies both text styling and positioning.
class _DrawOptions(_Options):
	_fields = ("pos",
		"fontname", "fontsize", "sysfontname",
		"antialias", "bold", "italic", "underline",
		"color", "background",
		"top", "left", "bottom", "right",
		"topleft", "bottomleft", "topright", "bottomright",
		"midtop", "midleft", "midbottom", "midright",
		"center", "centerx", "centery",
		"width", "widthem", "lineheight", "pspace", "strip",
		"align",
		"owidth", "ocolor",
		"shadow", "scolor",
		"gcolor", "shade",
		"alpha",
		"anchor",
		"angle",
		"surf",
		"cache")
	_defaults = {
		"antialias": True, "alpha": 1.0, "angle": 0,
		"surf": _default_surf_sentinel, "cache": True }

	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		self.expandposition()
		self.expandanchor()
		self.resolvesurf()

	# Expand each 2-element position specifier and overwrite the corresponding 1-element
	# position specifiers.
	def expandposition(self):
		if self.topleft: self.left, self.top = self.topleft
		if self.bottomleft: self.left, self.bottom = self.bottomleft
		if self.topright: self.right, self.top = self.topright
		if self.bottomright: self.right, self.bottom = self.bottomright
		if self.midtop: self.centerx, self.top = self.midtop
		if self.midleft: self.left, self.centery = self.midleft
		if self.midbottom: self.centerx, self.bottom = self.midbottom
		if self.midright: self.right, self.centery = self.midright
		if self.center: self.centerx, self.centery = self.center

	# Update the pos and anchor fields, if unspecified, to be specified by the positional
	# keyword arguments.
	def expandanchor(self):
		x, y = self.pos or (None, None)
		hanchor, vanchor = self.anchor or (None, None)
		if self.left is not None: x, hanchor = self.left, 0
		if self.centerx is not None: x, hanchor = self.centerx, 0.5
		if self.right is not None: x, hanchor = self.right, 1
		if self.top is not None: y, vanchor = self.top, 0
		if self.centery is not None: y, vanchor = self.centery, 0.5
		if self.bottom is not None: y, vanchor = self.bottom, 1
		if x is None:
			raise ValueError("Unable to determine horizontal position")
		if y is None:
			raise ValueError("Unable to determine vertical position")
		self.pos = x, y

		if self.align is None: self.align = hanchor
		if hanchor is None: hanchor = DEFAULT_ANCHOR[0]
		if vanchor is None: vanchor = DEFAULT_ANCHOR[1]
		self.anchor = hanchor, vanchor

	# Unspecified surf values default to the display surface.
	def resolvesurf(self):
		if self.surf is _default_surf_sentinel:
			self.surf = pygame.display.get_surface()

	def togetsurfoptions(self):
		return { field: getattr(self, field) for field in _GetsurfOptions._allfields() }


class _GetsurfOptions(_Options):
	_fields = ("fontname", "fontsize", "sysfontname", "bold", "italic", "underline", "width",
		"widthem", "strip", "color", "background", "antialias", "ocolor", "owidth", "scolor",
		"shadow", "gcolor", "shade", "alpha", "align", "lineheight", "pspace", "angle", "cache")
	_defaults = { "antialias": True, "alpha": 1.0, "angle": 0, "cache": True }

	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		if self.fontname is None: self.fontname = DEFAULT_FONT_NAME
		if self.fontsize is None: self.fontsize = DEFAULT_FONT_SIZE
		self.fontsize = int(round(self.fontsize))
		if self.align is None: self.align = DEFAULT_ALIGN
		if self.align in ["left", "center", "right"]:
			self.align = [0, 0.5, 1][["left", "center", "right"].index(self.align)]
		if self.lineheight is None: self.lineheight = DEFAULT_LINE_HEIGHT
		if self.pspace is None: self.pspace = DEFAULT_PARAGRAPH_SPACE
		self.color = _resolvecolor(self.color, DEFAULT_COLOR)
		self.background = _resolvecolor(self.background, DEFAULT_BACKGROUND)
		self.gcolor = _resolvecolor(self.gcolor, None)
		if self.shade is None: self.shade = DEFAULT_SHADE
		if self.shade:
			self.gcolor = _applyshade(self.gcolor or self.color, self.shade)
			self.shade = 0
		self.ocolor = None if self.owidth is None else _resolvecolor(self.ocolor, DEFAULT_OUTLINE_COLOR)
		self.scolor = None if self.shadow is None else _resolvecolor(self.scolor, DEFAULT_SHADOW_COLOR)

		self._opx = None if self.owidth is None else ceil(self.owidth * self.fontsize * OUTLINE_UNIT)
		self._spx = None if self.shadow is None else tuple(ceil(s * self.fontsize * SHADOW_UNIT) for s in self.shadow)
		self.alpha = _resolvealpha(self.alpha)
		self.angle = _resolveangle(self.angle)
		self.strip = DEFAULT_STRIP if self.strip is None else self.strip

	def key(self):
		return tuple(getattr(self, field) for field in sorted(self._allfields()))


_font_cache = {}
def getfont(fontname=None, fontsize=None, sysfontname=None,
	bold=None, italic=None, underline=None):
	if fontname is not None and sysfontname is not None:
		raise ValueError("Can't set both fontname and sysfontname")
	if fontname is None and sysfontname is None: fontname = DEFAULT_FONT_NAME
	if fontsize is None: fontsize = DEFAULT_FONT_SIZE
	key = fontname, fontsize, sysfontname, bold, italic, underline
	if key in _font_cache: return _font_cache[key]
	if sysfontname is not None:
		font = pygame.font.SysFont(sysfontname, fontsize, bold or False, italic or False)
	else:
		if fontname is not None: fontname = FONT_NAME_TEMPLATE % fontname
		try:
			font = pygame.font.Font(fontname, fontsize)
		except IOError:
			raise IOError("unable to read font filename: %s" % fontname)
	if bold is not None:
		font.set_bold(bold)
	if italic is not None:
		font.set_italic(italic)
	if underline is not None:
		font.set_underline(underline)
	_font_cache[key] = font
	return font

def wrap(text, fontname=None, fontsize=None, sysfontname=None,
	bold=None, italic=None, underline=None, width=None, widthem=None, strip=None):
	if widthem is None:
		font = getfont(fontname, fontsize, sysfontname, bold, italic, underline)
	elif width is not None:
		raise ValueError("Can't set both width and widthem")
	else:
		font = getfont(fontname, REFERENCE_FONT_SIZE, sysfontname, bold, italic, underline)
		width = widthem * REFERENCE_FONT_SIZE
	if strip is None:
		strip = DEFAULT_STRIP
	paras = text.replace("\t", "    ").split("\n")
	lines = []
	for jpara, para in enumerate(paras):
		if strip:
			para = para.rstrip(" ")
		if width is None:
			lines.append((para, jpara))
			continue
		if not para:
			lines.append(("", jpara))
			continue
		# Preserve leading spaces in all cases.
		a = len(para) - len(para.lstrip(" "))
		# At any time, a is the rightmost known index you can legally split a line. I.e. it's legal
		# to add para[:a] to lines, and line is what will be added to lines if para is split at a.
		a = para.index(" ", a) if " " in para else len(para)
		line = para[:a]
		while a + 1 < len(para):
			# b is the next legal place to break the line, with bline the corresponding line to add.
			if " " not in para[a+1:]:
				b = len(para)
				bline = para
			elif strip:
				# Lines may be split at any space character that immediately follows a non-space
				# character.
				b = para.index(" ", a + 1)
				while para[b-1] == " ":
					if " " in para[b+1:]:
						b = para.index(" ", b + 1)
					else:
						b = len(para)
						break
				bline = para[:b]
			else:
				# Lines may be split at any space character, or any character immediately following
				# a space character.
				b = a + 1 if para[a] == " " else para.index(" ", a + 1)
			bline = para[:b]
			if font.size(bline)[0] <= width:
				a, line = b, bline
			else:
				lines.append((line, jpara))
				para = para[a:].lstrip(" ") if strip else para[a:]
				a = para.index(" ", 1) if " " in para[1:] else len(para)
				line = para[:a]
		if para:
			lines.append((line, jpara))
	return lines

_fit_cache = {}
def _fitsize(text, fontname, sysfontname, bold, italic, underline, width, height, lineheight, pspace, strip):
	key = text, fontname, sysfontname, bold, italic, underline, width, height, lineheight, pspace, strip
	if key in _fit_cache: return _fit_cache[key]
	def fits(fontsize):
		texts = wrap(text, fontname, fontsize, sysfontname, bold, italic, underline, width, strip)
		font = getfont(fontname, fontsize, sysfontname, bold, italic, underline)
		w = max(font.size(line)[0] for line, jpara in texts)
		linesize = font.get_linesize() * lineheight
		paraspace = font.get_linesize() * pspace
		h = int(round((len(texts) - 1) * linesize + texts[-1][1] * paraspace)) + font.get_height()
		return w <= width and h <= height
	a, b = 1, 256
	if not fits(a):
		fontsize = a
	elif fits(b):
		fontsize = b
	else:
		while b - a > 1:
			c = (a + b) // 2
			if fits(c):
				a = c
			else:
				b = c
		fontsize = a
	_fit_cache[key] = fontsize
	return fontsize

def _resolvecolor(color, default):
	if color is None: color = default
	if color is None: return None
	try:
		return tuple(pygame.Color(color))
	except ValueError:
		return tuple(color)

def _applyshade(color, shade):
	f = exp(-0.4 * shade)
	r, g, b = [
		min(max(int(round((c + 50) * f - 50)), 0), 255)
		for c in color[:3]
	]
	return (r, g, b) + tuple(color[3:])

def _resolvealpha(alpha):
	if alpha >= 1:
		return 1
	return max(int(round(alpha * ALPHA_RESOLUTION)) / ALPHA_RESOLUTION, 0)

def _resolveangle(angle):
	if not angle:
		return 0
	angle %= 360
	return int(round(angle / ANGLE_RESOLUTION_DEGREES)) * ANGLE_RESOLUTION_DEGREES

# Return the set of points in the circle radius r, using Bresenham's circle algorithm
_circle_cache = {}
def _circlepoints(r):
	r = int(round(r))
	if r in _circle_cache:
		return _circle_cache[r]
	x, y, e = r, 0, 1 - r
	_circle_cache[r] = points = []
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

_surf_cache = {}
_surf_tick_usage = {}
_surf_size_total = 0
_unrotated_size = {}
_tick = 0
def getsurf(text, **kwargs):
	global _tick, _surf_size_total
	options = _GetsurfOptions(**kwargs)
	key = text, options.key()

	if key in _surf_cache:
		_surf_tick_usage[key] = _tick
		_tick += 1
		return _surf_cache[key]
	texts = wrap(text, options.fontname, options.fontsize, options.sysfontname, options.bold, options.italic, options.underline,
		width=options.width, widthem=options.widthem, strip=options.strip)
	if options.angle:
		surf0 = getsurf(text, **options.update(angle = 0))
		if options.angle in (90, 180, 270):
			surf = pygame.transform.rotate(surf0, options.angle)
		else:
			surf = pygame.transform.rotozoom(surf0, options.angle, 1.0)
		_unrotated_size[(surf.get_size(), options.angle, text)] = surf0.get_size()
	elif options.alpha < 1.0:
		surf0 = getsurf(text, **options.update(alpha = 1.0))
		surf = surf0.copy()
		array = pygame.surfarray.pixels_alpha(surf)
		array[:,:] = (array[:,:] * options.alpha).astype(array.dtype)
		del array
	elif options._spx is not None:
		surf0 = getsurf(text, **options.update(background = (0, 0, 0, 0), shadow = None, scolor = None))
		ssurf = getsurf(text, **options.update(background = (0, 0, 0, 0), color = options.scolor, shadow = None, scolor = None, gcolor = None))
		w0, h0 = surf0.get_size()
		sx, sy = options._spx
		surf = pygame.Surface((w0 + abs(sx), h0 + abs(sy))).convert_alpha()
		surf.fill(options.background or (0, 0, 0, 0))
		dx, dy = max(sx, 0), max(sy, 0)
		surf.blit(ssurf, (dx, dy))
		x0, y0 = abs(sx) - dx, abs(sy) - dy
		if len(options.color) > 3 and options.color[3] == 0:
			array = pygame.surfarray.pixels_alpha(surf)
			array0 = pygame.surfarray.pixels_alpha(surf0)
			array[x0:x0+w0,y0:y0+h0] -= array0.clip(max=array[x0:x0+w0,y0:y0+h0])
			del array, array0
		else:
			surf.blit(surf0, (x0, y0))
	elif options._opx is not None:
		surf0 = getsurf(text, **options.update(ocolor = None, owidth = None))
		osurf = getsurf(text, **options.update(color = options.ocolor, ocolor = None, owidth = None, background = (0,0,0,0), gcolor = None))
		w0, h0 = surf0.get_size()
		opx = options._opx
		surf = pygame.Surface((w0 + 2 * opx, h0 + 2 * opx)).convert_alpha()
		surf.fill(options.background or (0, 0, 0, 0))
		for dx, dy in _circlepoints(opx):
			surf.blit(osurf, (dx + opx, dy + opx))
		if len(options.color) > 3 and options.color[3] == 0:
			array = pygame.surfarray.pixels_alpha(surf)
			array0 = pygame.surfarray.pixels_alpha(surf0)
			array[opx:-opx,opx:-opx] -= array0.clip(max=array[opx:-opx,opx:-opx])
			del array, array0
		else:
			surf.blit(surf0, (opx, opx))
	else:
		font = getfont(options.fontname, options.fontsize, options.sysfontname, options.bold, options.italic, options.underline)
		# pygame.Font.render does not allow passing None as an argument value for background.
		if options.background is None or (len(options.background) > 3 and options.background[3] == 0) or options.gcolor is not None:
			lsurfs = [font.render(text, options.antialias, options.color).convert_alpha() for text, jpara in texts]
		else:
			lsurfs = [font.render(text, options.antialias, options.color, options.background).convert_alpha() for text, jpara in texts]
		if options.gcolor is not None:
			import numpy
			m = numpy.clip(numpy.arange(lsurfs[0].get_height()) * 2.0 / font.get_ascent() - 1.0, 0, 1)
			for lsurf in lsurfs:
				array = pygame.surfarray.pixels3d(lsurf)
				for j in (0, 1, 2):
					array[:,:,j] = ((1.0 - m) * array[:,:,j] + m * options.gcolor[j]).astype(array.dtype)
				del array

		if len(lsurfs) == 1 and options.gcolor is None:
			surf = lsurfs[0]
		else:
			w = max(lsurf.get_width() for lsurf in lsurfs)
			linesize = font.get_linesize() * options.lineheight
			parasize = font.get_linesize() * options.pspace
			ys = [int(round(k * linesize + jpara * parasize)) for k, (text, jpara) in enumerate(texts)]
			h = ys[-1] + font.get_height()
			surf = pygame.Surface((w, h)).convert_alpha()
			surf.fill(options.background or (0, 0, 0, 0))
			for y, lsurf in zip(ys, lsurfs):
				x = int(round(options.align * (w - lsurf.get_width())))
				surf.blit(lsurf, (x, y))
	if options.cache:
		w, h = surf.get_size()
		_surf_size_total += 4 * w * h
		_surf_cache[key] = surf
		_surf_tick_usage[key] = _tick
		_tick += 1
	return surf

# The actual position on the screen where the surf is to be blitted, rather than the specified
# anchor position.
def _blitpos(angle, pos, anchor, tsurf, text):
	x, y = pos
	hanchor, vanchor = anchor
	if angle:
		w0, h0 = _unrotated_size[(tsurf.get_size(), angle, text)]
		S, C = sin(radians(angle)), cos(radians(angle))
		dx, dy = (0.5 - hanchor) * w0, (0.5 - vanchor) * h0
		x += dx * C + dy * S - 0.5 * tsurf.get_width()
		y += -dx * S + dy * C - 0.5 * tsurf.get_height()
	else:
		x -= hanchor * tsurf.get_width()
		y -= vanchor * tsurf.get_height()
	x = int(round(x))
	y = int(round(y))
	return x, y


def draw(text, pos=None, **kwargs):
	options = _DrawOptions(pos = pos, **kwargs)

	tsurf = getsurf(text, **options.togetsurfoptions())

	pos = _blitpos(options.angle, options.pos, options.anchor, tsurf, text)

	if options.surf is not None:
		options.surf.blit(tsurf, pos)
	
	if AUTO_CLEAN:
		clean()

	return tsurf, pos

def drawbox(text, rect, fontname=None, sysfontname=None, lineheight=None, pspace=None, anchor=None,
	bold=None, italic=None, underline=None, strip=None, **kwargs):
	if fontname is None: fontname = DEFAULT_FONT_NAME
	if lineheight is None: lineheight = DEFAULT_LINE_HEIGHT
	if pspace is None: pspace = DEFAULT_PARAGRAPH_SPACE
	hanchor, vanchor = anchor = anchor or (0.5, 0.5)
	rect = pygame.Rect(rect)
	x = rect.x + hanchor * rect.width
	y = rect.y + vanchor * rect.height
	fontsize = _fitsize(text, fontname, sysfontname, bold, italic, underline,
		rect.width, rect.height, lineheight, pspace, strip)
	return draw(text, (x, y), fontname=fontname, fontsize=fontsize, lineheight=lineheight,
		pspace=pspace, width=rect.width, strip=strip, anchor=anchor, **kwargs)

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

