from OpenGL.GL import *
from PIL import Image
import numpy as np

class Texture:
    texture: GLuint
    image:   np.array

    def __init__(self, name: str):
        # Load the image bytes and info into memory
        image = Image.open(f"./assets/images/{name}")
        width, height = image.size
        mode = image.mode
        self.image = np.asarray(image)

        # Create the opengl texture
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # Setup its parameters, (wrapping and filtering)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload to the texture buffer the image data
        if mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                         width, height, 0, GL_RGB,
                         GL_UNSIGNED_BYTE, self.image)
        elif mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                         width, height, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, self.image)
        else:
            sys.exit(f"Image mode {mode} not supported")

    def bind(self, unit: int = 0):
        # TODO: Investigate when to use units
        assert 0 <= unit <= 31
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.texture)
