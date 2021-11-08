from OpenGL.GL import *
import sys
from pathlib import Path
import numpy as np

VBO_POS   = 0

class Mesh(object):
    vertices: [np.array]
    VAO: GLuint
    VBOs: [GLuint]

    def __init__(self, vertices: [np.array]):
        self.vertices = vertices

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
    
        self.VBOs = []
        self.VBOs.append(glGenBuffers(1))

        glBindBuffer(GL_ARRAY_BUFFER, self.VBOs[VBO_POS])
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertices.size)
        glBindVertexArray(0);

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

