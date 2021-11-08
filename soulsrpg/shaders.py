from OpenGL.GL import *
import sys
import numpy as np

VBO_POS   = 0
N_VBO     = 1

class Mesh(object):
    vertices: [np.array]
    VAO: GLuint
    VBOs: [GLuint]

    def __init__(self, vertices: [np.array]):
        self.vertices = vertices

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
    
        self.VBOs = glGenBuffers(N_VBO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOs[VBO_POS])
        glBufferData(GL_ARRAY_BUFFER, vertices.size * vertices.itemsize, vertices, GL_STATIC_DRAW)

        glEnableVertexAtribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, vertices.size)
        glBindVertexArray(0);

class Shader(object):
    # The program id and its state
    program: GLuint
    in_use:  bool

    def __init__(self, name: str):
        # Load the shader sources
        vs_path = f"assets/shaders/{name}.vert" 
        fs_path = f"assets/shaders/{name}.frag" 
        vs_fd = open(vs_path, "r")
        fs_fs = open(fs_path, "r")
    
        self.program = link_program(
            compile_shader(vs_fd.readlines(), GL_VERTEX_SHADER),
            compile_shader(fs_fd.readlines(), GL_FRAGMENT_SHADER)
        )

    def uniform_loc(self, name: str) -> GLuint:
        return glGetUniformLocation(self.program, name)

    def attrib_loc(self, name: str) -> GLuint:
        return glGetAtrribLocation(self.program, name)


def compile_shader(src: str, ty: GLenum) -> GLuint:
    # Create and compile
    shader = glCreateShader(ty)
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
    if glGetShaderiv(program, GL_LINK_STATUS) != GL_TRUE:
        info_log = glGetProgramInfoLog(program)
        sys.exit(info_log)

    return program

