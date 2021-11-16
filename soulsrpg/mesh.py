import sys, ctypes
from OpenGL.GL import *
import numpy as np

class Mesh:
    # Data to upload to the gpu
    vertices: np.array
    indices:  np.array

    # GPU structures id
    VAO: GLuint
    VBO: GLuint
    EBO: GLuint

    def __init__(self, vertices: np.array, indices: np.array):
        # Check `vertices` and `indices` type
        if vertices.dtype != np.float32 and indices.dtype != np.uint32:
            sys.exit(f"Vertices or indices type not supported, {vertices.dtype}, {indices.dtype}")
        self.vertices = vertices
        self.indices  = indices

        # Generate 1 VAO that will contain the VBOs (or the layout to certain data inside a VBO)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Setup the indices, this element buffer keeps binded until another element buffer 
        # gets binded
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

        # Setup all the model data inside a VBO, this array buffer keeps binded until another
        # buffer of any kind gets binded 
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        # Arrange the locations 0 and 1 of the VAO to a certain data in the VBO
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 
            self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
            self.vertices.itemsize * 5,
            ctypes.c_void_p(self.vertices.itemsize * 3))
        glEnableVertexAttribArray(1)

        # Unbind just in case
        glBindVertexArray(0)

    def draw(self):
        # Bind the current EBO and VAO (otherwise we would use the last EBO because it is
        # not detached)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBindVertexArray(self.VAO)

        # Draw the mesh using idices inside the vertices (layout=0) that create triangles
        glDrawElements(GL_TRIANGLES, len(self.vertices), GL_UNSIGNED_INT, None)

        # Unbind the VAO, otherwise weird errors happen with vertex upload and uniforms
        glBindVertexArray(0)
