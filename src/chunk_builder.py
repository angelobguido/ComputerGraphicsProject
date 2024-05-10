from OpenGL.GL import *
import numpy as np
from utils.block_types import *

STRIDE = 4
OFFSET_POSITION = ctypes.c_void_p(0)

class ChunkBuilder:
    def __init__(self, atlas, world, position):
        self.setupMesh(world, position)
        self.atlas = atlas

    def setupMesh(self, world, position):

        x_offset = position[0]*32
        z_offset = position[1]*32

        vertices = []

        for i in range(32):
            for j in range(256):
                for k in range(32):
                    
                    current = world.get_block((i+x_offset,j,k+z_offset))
                    
                    if current == NONE:
                        continue

                    textures = get_textures(current)
                    faces = get_visible_faces(world, (i+x_offset,j,k+z_offset))
                    # faces = [0,1,2,3,4,5]

                    for face in faces:
                        for vertex in [0,1,2,1,2,3]:

                            info = textures[face]
                            info = (face<<(32-3))|info
                            info = (vertex<<(32-6))|info
                            info = (i<<(32-11))|info
                            info = (j<<(32-19))|info
                            info = (k<<(32-24))|info
                            
                            vertices.append(info)


        vertices = np.array(vertices, dtype=np.uint32)

        self.num_vertices = len(vertices)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        #vertex info
        glVertexAttribIPointer(0, 1, GL_UNSIGNED_INT, STRIDE, OFFSET_POSITION)
        glEnableVertexAttribArray(0); 

        glBindVertexArray(0)

    def draw(self):

        glBindVertexArray(self.VAO)
        glBindTexture(GL_TEXTURE_2D, self.atlas)
        glDrawArrays(GL_TRIANGLES, 0, self.num_vertices)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

    
def get_visible_faces(world, position):
    faces = []
    x,y,z = position

    #UP
    if is_transparent(world.get_block((x,y+1,z))):
        faces.append(0)

    #DOWN
    if is_transparent(world.get_block((x,y-1,z))):
        faces.append(1)

    #FRONT
    if is_transparent(world.get_block((x,y,z+1))):
        faces.append(2)

    #BACK
    if is_transparent(world.get_block((x,y,z-1))):
        faces.append(3)

    #RIGHT
    if is_transparent(world.get_block((x+1,y,z))):
        faces.append(4)

    #LEFT
    if is_transparent(world.get_block((x-1,y,z))):
        faces.append(5)

    return faces

