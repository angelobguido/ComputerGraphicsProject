import numpy as np
from utils.block_types import *
from shader import Shader
from model import Model
from mesh import Mesh
import glm


SCALE = glm.vec3(0.5,0.5,0.5)
STEP = 1

class BlockGroupParams:
    def __init__(self, blockMesh: Mesh, array: np.ndarray, blockDict: dict, pivot: glm.vec3 = glm.vec3(0,0,0)):
        self.blockMesh = blockMesh
        self.blockDict = blockDict
        self.pivot = pivot
        self.array = array

class BlockGroup:
    def __init__(self, params: BlockGroupParams, position: glm.vec3 = glm.vec3(0,0,0)):
        self.blocks = {}
        self.params = params
        self.position = position
        
        self.setupBlocks()

    def setupBlocks(self):

        M = self.params.array.shape[0]
        N = self.params.array.shape[1]
        P = self.params.array.shape[2]

        for i in range(M):
            for j in range(N):
                for k in range(P):
                    
                    if self.params.array[i,j,k] != NONE:
                        newBlock = Model(self.params.blockMesh, position=glm.vec3((k+self.position.x-self.params.pivot.x)*STEP,(-i+M+self.position.y-self.params.pivot.y)*STEP,(j+self.position.z-self.params.pivot.z)*STEP), scale=SCALE)
                    
                        if self.params.array[i,j,k] not in self.blocks:
                            self.blocks[self.params.array[i,j,k]] = []   

                        self.blocks[self.params.array[i,j,k]].append(newBlock)

    def draw(self, shader):

        for key in self.blocks:

            self.params.blockMesh.textures = [(self.params.blockDict[key],0)]

            for block in self.blocks[key]:
                block.draw(shader)
        