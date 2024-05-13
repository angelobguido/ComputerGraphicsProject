from OpenGL.GL import *
import numpy as np
from utils.block_types import *

STRIDE = 4
OFFSET_POSITION = ctypes.c_void_p(0)

class ChunkBuilder:
    def __init__(self, atlas, world, position):
        self.atlas = atlas
        self.chunkPosition = position
        self.world = world
        self.setupMesh()

    def freeMemory(self):
        self.vertices = None
        return (self.VAO, self.VBO)


    def setupMesh(self):

        x_offset = self.chunkPosition[0]*16
        z_offset = self.chunkPosition[1]*16

        self.vertices = []

        for i in range(16):
            for j in range(128):
                for k in range(16):
                    
                    current = self.world.get_block((i+x_offset,j,k+z_offset))
                    
                    if current == NONE:
                        continue

                    textures = get_textures(current)
                    faces = self.getVisibleFaces((i+x_offset,j,k+z_offset))
                    # faces = [0,1,2,3,4,5]

                    for face in faces:
                        for vertex in [0,1,2,1,2,3]:

                            info = textures[face]
                            info = (face<<(32-3))|info
                            info = (vertex<<(32-6))|info
                            info = (i<<(32-11))|info
                            info = (j<<(32-19))|info
                            info = (k<<(32-24))|info
                            
                            self.vertices.append(info)


        self.vertices = np.array(self.vertices, dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        #vertex info
        glVertexAttribIPointer(0, 1, GL_UNSIGNED_INT, STRIDE, OFFSET_POSITION)
        glEnableVertexAttribArray(0); 

        glBindVertexArray(0)

    def updateMesh(self):
        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        #vertex info
        glVertexAttribIPointer(0, 1, GL_UNSIGNED_INT, STRIDE, OFFSET_POSITION)
        glEnableVertexAttribArray(0); 

        glBindVertexArray(0)


    def destroyBlockInMesh(self, position):
        
        info = 0
        info = (position[0]<<(32-11))|info
        info = (position[1]<<(32-19))|info
        info = (position[2]<<(32-24))|info
        
        temp = (((self.vertices & 0x03FFFF00) - info) == 0)

        self.vertices = np.delete(self.vertices, np.where(temp))

        self.updateMesh()

    def updateBlockInMesh(self, position):

        x_offset = self.chunkPosition[0]*16
        z_offset = self.chunkPosition[1]*16

        i = position[0]
        j = position[1]
        k = position[2]

        current = self.world.get_block((i+x_offset,j,k+z_offset))
        
        if current == NONE:
            return

        textures = get_textures(current)
        faces = self.getVisibleFaces((i+x_offset,j,k+z_offset))
        
        it_vertices = []
        for face in faces:
            for vertex in [0,1,2,1,2,3]:

                info = textures[face]
                info = (face<<(32-3))|info
                info = (vertex<<(32-6))|info
                info = (i<<(32-11))|info
                info = (j<<(32-19))|info
                info = (k<<(32-24))|info
                
                it_vertices.append(info)

        self.vertices = np.append(self.vertices, it_vertices).astype(np.uint32)

        self.updateMesh()


    def draw(self):

        glBindVertexArray(self.VAO)
        glBindTexture(GL_TEXTURE_2D, self.atlas)
        glDrawArrays(GL_TRIANGLES, 0, self.vertices.shape[0])
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

    
    def getVisibleFaces(self, position):
        faces = []
        x,y,z = position

        #UP
        if is_transparent(self.world.get_block((x,y+1,z))):
            faces.append(0)

        #DOWN
        if is_transparent(self.world.get_block((x,y-1,z))):
            faces.append(1)

        #FRONT
        if is_transparent(self.world.get_block((x,y,z+1))):
            faces.append(2)

        #BACK
        if is_transparent(self.world.get_block((x,y,z-1))):
            faces.append(3)

        #RIGHT
        if is_transparent(self.world.get_block((x+1,y,z))):
            faces.append(4)

        #LEFT
        if is_transparent(self.world.get_block((x-1,y,z))):
            faces.append(5)

        return faces

