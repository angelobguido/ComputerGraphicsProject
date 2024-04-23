from OpenGL.GL import *

STRIDE = 4*5
OFFSET_POSITION = ctypes.c_void_p(0)
OFFSET_TEXTURE = ctypes.c_void_p(4*3)

class Mesh:
    def __init__(self, vertices):
        self.vertices = vertices

        self.setupMesh()

    def setupMesh(self):

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        #vertex positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, STRIDE, OFFSET_POSITION)
        glEnableVertexAttribArray(0); 

        #vertex texture coords
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, STRIDE, OFFSET_TEXTURE)
        glEnableVertexAttribArray(1); 
        

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertices.nbytes//STRIDE)
        glBindVertexArray(0)