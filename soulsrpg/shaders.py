from OpenGL.GL import *
import sys
import pygame
from pathlib import Path
import numpy as np
import ctypes

class Mesh(object):
    vertices: np.array
    indices:  np.array
    VAO: GLuint
    VBO: GLuint
    EBO: GLuint

    def __init__(self, vertices: np.array, indices: np.array):
        self.vertices = vertices
        self.indices  = indices

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 
            self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
            self.vertices.itemsize * 5, 
            ctypes.c_void_p(self.vertices.itemsize * 3))
        glEnableVertexAttribArray(1)

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0);

class Texture(object):
    texture: GLint
    image:   bytes

    def __init__(self, name):
        surf = pygame.image.load(f"assets/images/{name}")
        width, height = surf.get_size()
        self.image = pygame.image.tostring(surf, "RGBA", 1)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
                     width, height, 0, GL_RGBA, 
                     GL_UNSIGNED_BYTE, self.image)

    def bind(self, unit: int = 0):
        assert 0 <= unit <= 31
        glActiveTexture(GL_TEXTURE0 + unit);
        glBindTexture(GL_TEXTURE_2D, self.texture)

class Shader(object):
    # The program id and its state
    program: GLuint
    in_use:  bool

    def __init__(self, name: str):
        # Load the shader sources
        vs_path = f"assets/shaders/{name}.vert" 
        fs_path = f"assets/shaders/{name}.frag" 

        vs = Path(vs_path).read_text()
        fs = Path(fs_path).read_text()
        
        self.program = link_program(
            compile_shader(vs, GL_VERTEX_SHADER),
            compile_shader(fs, GL_FRAGMENT_SHADER)
        )

    def use(self):
        glUseProgram(self.program)

    def uniform_loc(self, name: str) -> GLuint:
        return glGetUniformLocation(self.program, name)

    def attrib_loc(self, name: str) -> GLuint:
        return glGetAtrribLocation(self.program, name)


def compile_shader(src: str, ty: GLenum) -> GLuint:
    # Create and compile
    shader = glCreateShader(ty)
    glShaderSource(shader, src)
    glCompileShader(shader)

    # Error checking and reporting (crash on error)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        info_log = glGetShaderInfoLog(shader)
        sys.exit(info_log)

    return shader

def link_program(vs: GLuint, fs: GLuint) -> GLuint:
    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)

    # Error checking and reporting (crash on error)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        info_log = glGetProgramInfoLog(program)
        sys.exit(info_log)

    return program

