# Use the ptext module to draw to the OpenGL surface.
# Must have ptext.py in the same directory.

# ptextgl.draw(text, pos=None, **options)

# https://github.com/cosmologicon/pygame-text

import pygame
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy
import ptext

AUTO_PREP = True


_vertex_shader_source = """
#version 120
attribute vec2 p;
uniform vec4 rect;
uniform vec2 viewsize;
varying vec2 tcoord;
void main() {
	vec2 p0 = rect.xy;
	vec2 size = rect.zw;
	gl_Position = vec4((p0 + p * size) / viewsize * 2.0 - 1.0, 0.0, 1.0);
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
		"alpha": glGetUniformLocation(_shader, "alpha"),
		"texture": glGetUniformLocation(_shader, "texture"),
	}
	_pdata = numpy.array([0, 0, 1, 0, 1, 1, 0, 1], numpy.float32)


def prep():
	init()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glUseProgram(_shader)
	glEnableVertexAttribArray(_locations["p"])
	glVertexAttribPointer(_locations["p"], 2, GL_FLOAT, GL_FALSE, 0, _pdata)
	glUniform2f(_locations["viewsize"], 854, 480)
	glUniform1i(_locations["texture"], 0)

def unprep(state):
	shaders.glUseProgram(0)

def draw(text, pos=None, **kwargs):
#	assert kwargs.get("surf") is None
	prep()  # TODO: make an option
	glUniform1f(_locations["alpha"], 1.0)  # TODO: handle from args
	options = ptext._DrawOptions(pos = pos, **kwargs)
	tsurf = ptext.getsurf(text, **options.togetsurfoptions())
	x, y = ptext._blitpos(options.angle, options.pos, options.anchor, tsurf, text)
	w, h = tsurf.get_size()
	y = 480 - y - h
	glUniform4f(_locations["rect"], x, y, w, h)
	glEnable(GL_TEXTURE_2D)
	glActiveTexture(GL_TEXTURE0)
	texture = glGenTextures(1)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glBindTexture(GL_TEXTURE_2D, texture)
	data = pygame.image.tostring(tsurf, "RGBA", 1)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glBindTexture(GL_TEXTURE_2D, texture)
	glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
#	return tsurf, pos





