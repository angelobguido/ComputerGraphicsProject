from OpenGL.GL import *
from shader import Shader
from mesh import Mesh
import glm

class Model:
    def __init__(self, mesh, position: glm.vec3 = glm.vec3(0,0,0), scale: glm.vec3 = glm.vec3(1,1,1), rotation_x = 0, rotation_y = 0, rotation_z = 0, pivot: glm.vec3 = glm.vec3(0,0,0)):
        self.mesh = mesh
        self.position = position
        self.scale = scale
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.pivot = pivot

    def draw(self, shader: Shader):
        shader.setMat4("model", self.getModelMatrix())
        self.mesh.draw()
        

    def getModelMatrix(self):

        matrix_transform = glm.mat4(1.0) 
        
        #position
        matrix_transform = glm.translate(matrix_transform, self.position)
        
        #rotations
        matrix_transform = glm.rotate(matrix_transform,glm.radians(self.rotation_x),glm.vec3(1,0,0))
        matrix_transform = glm.rotate(matrix_transform,glm.radians(self.rotation_y),glm.vec3(0,1,0))
        matrix_transform = glm.rotate(matrix_transform,glm.radians(self.rotation_z),glm.vec3(0,0,1))

        #scale
        matrix_transform = glm.scale(matrix_transform, self.scale)
        
        #pivot
        matrix_transform = glm.translate(matrix_transform, self.pivot)
        
        return matrix_transform