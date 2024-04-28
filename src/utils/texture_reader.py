from PIL import Image
from OpenGL.GL import *

class TextureReader:
    def __init__(self, path):
        image = Image.open(path)
        image_width = image.size[0]
        image_height = image.size[1]
        image_data = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

        self.textureID = glGenTextures(1)
        self.processData(image_data, image_width, image_height)

    def processData(self, image_data, image_width, image_height):
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)