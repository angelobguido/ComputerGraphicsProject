import numpy as np
from utils.block_types import *
from shader import Shader
from model import Model
from mesh import Mesh
import glm


SCALE = glm.vec3(0.5,0.5,0.5)
STEP = 1

class BlockGroup:
    def __init__(self, blockMesh: Mesh, array: np.ndarray, blockDict: dict, position: glm.vec3 = glm.vec3(0,0,0)):
        self.blocks = {}
        self.blockMesh = blockMesh
        self.blockDict = blockDict
        self.position = position
        
        self.setupBlocks(array)

    def setupBlocks(self, array: np.ndarray):

        M = array.shape[0]
        N = array.shape[1]
        P = array.shape[2]

        for i in range(M):
            for j in range(N):
                for k in range(P):
                    
                    if array[i,j,k] != NONE:
                        newBlock = Model(self.blockMesh, position=glm.vec3(-j*STEP+self.position.x,-i*STEP+M+self.position.y,k*STEP+self.position.z), scale=SCALE)
                    
                        if array[i,j,k] not in self.blocks:
                            self.blocks[array[i,j,k]] = []   

                        self.blocks[array[i,j,k]].append(newBlock)

    def draw(self, shader):

        for key in self.blocks:

            self.blockMesh.textures = [(self.blockDict[key],0)]

            for block in self.blocks[key]:
                block.draw(shader)
        