# This module extends ptext to work on OpenGL surfaces.
# This module is not required to use the basic ptext module on regular pygame Surfaces.
# ptext.py must be in the same directory.

# ptextgl.draw(text, pos=None, **options)

# https://github.com/cosmologicon/pygame-text

import pygame, math
from OpenGL.GL import *
from OpenGL.GL import shaders
import ptext

AUTO_PREP = True

class _DrawOptions(ptext._DrawOptions):
	_fields = tuple((field for field in ptext._DrawOptions._fields if field not in
		("surf", "cache")
	)) + (
		"prep",
	)
	_defaults = { k: v for k, v in ptext._DrawOptions._defaults.items() if k not in
		("surf", "cache")
	}
	def __init__(self, **kwargs):
		ptext._DrawOptions.__init__(self, **kwargs)
		if self.prep is None:
			self.prep = AUTO_PREP
	def resolvesurf(self):
		pass



_vertex_shader_source = """
#version 120
attribute vec2 p;
uniform vec4 rect;
uniform vec2 viewsize;
uniform float angle;
varying vec2 tcoord;
void main() {
	float C = cos(angle), S = sin(angle);
	mat2 R = mat2(C, S, -S, C);
	vec2 p0 = rect.xy;
	vec2 size = rect.zw;
	gl_Position = vec4((p0 + R * (p * size)) / viewsize * 2.0 - 1.0, 0.0, 1.0);
	tcoord = p;
}
"""
_fragment_shader_source = """
#version 120
uniform float alpha;
uniform sampler2D texture;
varying vec2 tcoord;
void main() {
	gl_FragColor = texture2D(texture, tcoord);
	gl_FragColor.a *= alpha;
}
"""

_shader = None
def init():
	global _shader, _locations, _pdata
	if _shader: return
	# Generate shaders
	vertex_shader = shaders.compileShader(_vertex_shader_source, GL_VERTEX_SHADER)
	fragment_shader = shaders.compileShader(_fragment_shader_source, GL_FRAGMENT_SHADER)
	_shader = shaders.compileProgram(vertex_shader, fragment_shader)
	_locations = {
		"p": glGetAttribLocation(_shader, "p"),
		"rect": glGetUniformLocation(_shader, "rect"),
		"viewsize": glGetUniformLocation(_shader, "viewsize"),
		"angle": glGetUniformLocation(_shader, "angle"),
		"alpha": glGetUniformLocation(_shader, "alpha"),
		"texture": glGetUniformLocation(_shader, "texture"),
	}
	_pdata = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]


def prep():
	init()
	state = {
		"blend": glIsEnabled(GL_BLEND),
		"srcfunc": glGetInteger(GL_BLEND_SRC),
		"dstfunc": glGetInteger(GL_BLEND_DST),
		"program": glGetInteger(GL_CURRENT_PROGRAM),
		"penable": glGetVertexAttribiv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_ENABLED)[0],
		"psize": glGetVertexAttribiv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_SIZE)[0],
		"ptype": glGetVertexAttribiv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_TYPE)[0],
		"pnorm": glGetVertexAttribiv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_NORMALIZED)[0],
		"pstride": glGetVertexAttribiv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_STRIDE)[0],
		"ppointer": int(glGetVertexAttribPointerv(_locations["p"], GL_VERTEX_ATTRIB_ARRAY_POINTER)),
	}
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glUseProgram(_shader)
	glEnableVertexAttribArray(_locations["p"])
	glVertexAttribPointer(_locations["p"], 2, GL_FLOAT, GL_FALSE, 0, _pdata)
	x, y, w, h = glGetIntegerv(GL_VIEWPORT)
	glUniform2f(_locations["viewsize"], w, h)
	glUniform1i(_locations["texture"], 0)
	return state

def unprep(state):
	(glEnable if state["blend"] else glDisable)(GL_BLEND)
	shaders.glUseProgram(state["program"])
	glBlendFunc(state["srcfunc"], state["dstfunc"])
	(glEnableVertexAttribArray if state["penable"] else glDisableVertexAttribArray)(_locations["p"])
	glVertexAttribPointer(_locations["p"], state["psize"], state["ptype"], state["pnorm"], state["pstride"], state["ppointer"])

_texture_cache = {}
_texture_tick_usage = {}
_texture_size_total = 0
_tick = 0
def gettexture(text, **kwargs):
	global _tick, _texture_size_total
	options = ptext._GetsurfOptions(**kwargs)
	cache = options.cache
	options = options.update(cache = False)
	key = text, options.key()
	if key in _texture_cache:
		_texture_tick_usage[key] = _tick
		_tick += 1
		return _texture_cache[key]

	tsurf = ptext.getsurf(text, **options)
	w, h = tsurf.get_size()
	glEnable(GL_TEXTURE_2D)
	glActiveTexture(GL_TEXTURE0)
	texture = glGenTextures(1)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glBindTexture(GL_TEXTURE_2D, texture)
	data = pygame.image.tostring(tsurf, "RGBA", 1)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

	if cache:
		_texture_size_total += 4 * w * h
		_texture_cache[key] = texture, (w, h)
		_texture_tick_usage[key] = _tick
		_tick += 1
	return texture, (w, h)


def clean():
	global _texture_size_total
	memory_limit = ptext.MEMORY_LIMIT_MB * (1 << 20)
	if _texture_size_total < memory_limit:
		return
	memory_limit *= ptext.MEMORY_REDUCTION_FACTOR
	keys = sorted(_texture_cache, key=_texture_tick_usage.get)
	for key in keys:
		texture, (w, h) = _texture_cache[key]
		glDeleteTextures([texture])
		del _texture_cache[key]
		del _texture_tick_usage[key]
		_texture_size_total -= 4 * w * h
		if _texture_size_total < memory_limit:
			break


def draw(text, pos=None, **kwargs):
	options = _DrawOptions(pos = pos, **kwargs)
	if options.prep:
		state = prep()
	# Transparency and rotation are handled in the shader.
	alpha = options.alpha
	options.alpha = 1
	angle = options.angle
	options.angle = 0
	glUniform1f(_locations["alpha"], alpha)
	glUniform1f(_locations["angle"], math.radians(angle))
	texture, (w, h) = gettexture(text, **options.togetsurfoptions())

	x, y = ptext._blitpos(0, options.pos, options.anchor, (w, h), text)
	_, _, _, H = glGetIntegerv(GL_VIEWPORT)
	y = H - y - h
	glUniform4f(_locations["rect"], x, y, w, h)
	glEnable(GL_TEXTURE_2D)
	glActiveTexture(GL_TEXTURE0)

	glBindTexture(GL_TEXTURE_2D, texture)
	glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
	if options.prep:
		unprep(state)
	if ptext.AUTO_CLEAN:
		clean()

