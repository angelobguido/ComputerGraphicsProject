from OpenGL.GL import *
import numpy as np

STRIDE = 4
OFFSET_POSITION = ctypes.c_void_p(0)

class ChunkBuilder:
    def __init__(self):
        self.setupMesh()

    def setupMesh(self):

        vertices = []

        for i in range(1):
            for j in range(1):
                for k in range(1):
                    for face in range(6):
                        for vertex in [0,1,2,1,2,3]:

                            print(vertex)
                            
                            info = 0
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

        glDrawArrays(GL_TRIANGLES, 0, self.num_vertices)

        glBindVertexArray(0)