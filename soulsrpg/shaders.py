from OpenGL.GL import *
import sys
from pathlib import Path
import numpy as np
from typing import TypeVar

T = TypeVar("T", int, float, np.array)
class Shader:
    # The program id and its state
    program: GLuint
    in_use:  bool

    def __init__(self, name: str):
        # Load the shader sources
        vs_path = f"assets/shaders/{name}.vert"
        fs_path = f"assets/shaders/{name}.frag"
        vs = Path(vs_path).read_text()
        fs = Path(fs_path).read_text()

        # Compile the shaders and link them to generate a program
        self.program = link_program(
            compile_shader(vs, GL_VERTEX_SHADER),
            compile_shader(fs, GL_FRAGMENT_SHADER)
        )

        self.in_use = False

    def use(self):
        """ Use the shader only if its not in use, otherwise crash """
        if not self.in_use:
            glUseProgram(self.program)
            self.in_use = True
        else:
            sys.exit("Shader already in use")

    def detach(self):
        """ Detach the shader only if its in use, otherwise crash """
        if self.in_use:
            glUseProgram(0)
            self.in_use = False 
        else:
            sys.exit("Shader isn't in use")

    def upload(self, name: str, value: T):
        """ Upload a unifrom variable with name `name` and type `T` """ 
        # The shader must be in use to upload uniforms
        if not self.in_use:
            sys.exit("Shader ins't in use, cannot upload")

        # Get the uniform location
        loc = glGetUniformLocation(self.program, name)
        if loc == -1:
            sys.exit("Invalid uniform name")

        # Matchs its type and if its a `np.ndarray` also its shape to upload correctly
        match value.__class__.__name__:
            case "float":
                glUniform1f(loc, value)
            case "int":
                glUniform1i(loc, value)
            case "ndarray":
                # OpenGL works with 32 bits by default but numpy with 64 bits
                if value.dtype != "float32":
                   sys.exit("Numpy float64 types not supported")

                match value.shape:
                    case (2, 2):
                        glUniformMatrix2fv(loc, 1, GL_FALSE, value)
                    case (3, 3):
                        glUniformMatrix3fv(loc, 1, GL_FALSE, value)
                    case (4, 4):
                        glUniformMatrix4fv(loc, 1, GL_FALSE, value)
                    case (3,):
                        glUniform3f(loc, 1, GL_FALSE, value)
                    case (4,):
                        glUniform4f(loc, 1, GL_FALSE, value)
                    case s:
                        sys.exit(f"np.ndarray with shape {s} not supported for uniform upload")
            case t:
                sys.exit(f"Type {t} not supported for uniform upload")

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

