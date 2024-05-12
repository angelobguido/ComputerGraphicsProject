from PIL import Image
from OpenGL.GL import *

class TextureReader:
    def __init__(self, path, pixel_art = True, mipmap_paths = []):
        image = Image.open(path)
        image_width = image.size[0]
        image_height = image.size[1]
        image_data = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

        mipmaps = []
        if mipmap_paths:
            for mipmap_path in mipmap_paths:
                mipmap = Image.open(mipmap_path)
                mipmaps.append(mipmap)
            # mipmaps.reverse()

        self.textureID = glGenTextures(1)
        self.processData(image_data, image_width, image_height, pixel_art, mipmaps)

    def processData(self, image_data, image_width, image_height, pixel_art, mipmaps):
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        if pixel_art:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if mipmaps:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, len(mipmaps)-1)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
            for i in range(len(mipmaps)):
                mipmap_data = mipmaps[i].convert("RGBA").tobytes("raw", "RGBA", 0, -1)
                glTexImage2D(GL_TEXTURE_2D, i, GL_RGBA, mipmaps[i].size[0], mipmaps[i].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, mipmap_data)


        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            glGenerateMipmap(GL_TEXTURE_2D)