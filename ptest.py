import pygame, ptext
pygame.display.set_mode((640, 480))
#ptext.draw("foobar \n zimwat",  (0, 0), strip=True)

text = "one two three four five [[Rsix seven eight nine ten\neleven _twelve thirteen]] fourteen fifteen_ sixteen seventeen"
#text = "one two three four five six seven eight nine ten"
#text = "eleven _twelve thirteen fourteen fifteen_ sixteen seventeen"
#for fields in ptext._wrap(text, width=150, underlinetag="_"):
#	print(*fields)

ptext.DEFAULT_COLOR_TAG = {
	"]]": None,
	"[[R": "#FF7F7F",
}

#ptext.draw(text, topright=(500, 0), width=150, underlinetag="_", background="#664422")


ptext.DEFAULT_UNDERLINE_TAG = "__"
ptext.DEFAULT_BOLD_TAG = "**"
ptext.DEFAULT_COLOR_TAG = {
	">>": None,
	"<<R": "red",
	"<<B": "blue",
}
#ptext.draw("How about some **bold** text or some <<Rred text>>!", (0, 0), owidth=1, ocolor="gray", fontsize=40, width=300)
ptext.draw("How about some **bold** text or some <<Rred text>>!", (0, 0), shadow=(1,1), scolor="gray", fontsize=40, width=300)


pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

