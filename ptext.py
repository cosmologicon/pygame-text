# ptext module: place this in your import directory.

# ptext.draw(text, topleft=None, surf=None, **options)

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

import pygame

DEFAULT_FONT_SIZE = 18
REFERENCE_FONT_SIZE = 100
DEFAULT_FONT_NAME = None
FONT_NAME_TEMPLATE = "%s"

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
			lines.append(text)
	return lines

if __name__ == "__main__":
	pygame.font.init()
	getfont(None, 18)
	text = " ".join("abcdefghijk"[:(n % 5 + n % 7 + 1)] for n in range(100))
	print text
	print "\n".join(wrap(text, None, 18, width=200))
