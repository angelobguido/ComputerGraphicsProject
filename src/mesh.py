from OpenGL.GL import *

STRIDE = 4*5
OFFSET_POSITION = ctypes.c_void_p(0)
OFFSET_TEXTURE = ctypes.c_void_p(4*3)

class Mesh:
    def __init__(self, vertices, textures = []):
        self.vertices = vertices
        self.textures = textures

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

        if len(self.textures) != 0:

            for i in range(len(self.textures)):
            
                numberOfVertices = self.vertices.nbytes//STRIDE - self.textures[i][1]
                
                if i != len(self.textures)-1:
                    numberOfVertices = self.textures[i+1][1] - self.textures[i][1] + 1

                glBindTexture(GL_TEXTURE_2D, self.textures[i][0])
                glDrawArrays(GL_TRIANGLES, self.textures[i][1], numberOfVertices)

            glBindTexture(GL_TEXTURE_2D, 0)

        else:
            glDrawArrays(GL_TRIANGLES, 0, self.vertices.nbytes//STRIDE)

        glBindVertexArray(0)