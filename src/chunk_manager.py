import glm
from chunk_builder import ChunkBuilder
from model import Model
import numpy as np
from OpenGL.GL import *


CHUNK_SIZE = 16

INITIAL_LOAD = 10

class ChunkManager:

    def __init__(self, world, player, atlas):
        self.world = world
        self.player = player
        self.atlas = atlas
        self.lastChunk = (0,0)
        self.visibleChunks = np.array([
            (-3,3), (-2,3), (-1,3), (0,3), (1,3), (2,3), (3,3),
            (-3,2), (-2,2), (-1,2), (0,2), (1,2), (2,2), (3,2),
            (-3,1), (-2,1), (-1,1), (0,1), (1,1), (2,1), (3,1),
            (-3,0), (-2,0), (-1,0), (0,0), (1,0), (2,0), (3,0),
            (-3,-1), (-2,-1), (-1,-1), (0,-1), (1,-1), (2,-1), (3,-1),
            (-3,-2), (-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2), (3,-2),
            (-3,-3), (-2,-3), (-1,-3), (0,-3), (1,-3), (2,-3), (3,-3)
        ])

        self.loadedRange = np.array([
            (-3,3), (-2,3), (-1,3), (0,3), (1,3), (2,3), (3,3),
            (-3,2), (-2,2), (-1,2), (0,2), (1,2), (2,2), (3,2),
            (-3,1), (-2,1), (-1,1), (0,1), (1,1), (2,1), (3,1),
            (-3,0), (-2,0), (-1,0), (0,0), (1,0), (2,0), (3,0),
            (-3,-1), (-2,-1), (-1,-1), (0,-1), (1,-1), (2,-1), (3,-1),
            (-3,-2), (-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2), (3,-2),
            (-3,-3), (-2,-3), (-1,-3), (0,-3), (1,-3), (2,-3), (3,-3)
        ])

        self.chunks = {}

        for i in range(-INITIAL_LOAD//2,INITIAL_LOAD//2):
            for j in range(-INITIAL_LOAD//2,INITIAL_LOAD//2):
                chunk_mesh = ChunkBuilder(atlas, self.world, (i,j))
                chunk_model = Model(chunk_mesh, position=glm.vec3(i*16,0,j*16))
                self.chunks[(i,j)] = chunk_model
                print((i,j))


    def update(self):
        current = self.getCurrentChunk()
        if current != self.lastChunk:
            displacement = (current[0] - self.lastChunk[0], current[1] - self.lastChunk[1])
            self.visibleChunks = self.visibleChunks + displacement
            self.loadedRange = self.loadedRange + displacement

            for chunkPosition in self.loadedRange:

                chunkPosition = tuple(chunkPosition)

                if chunkPosition not in self.chunks:
                    chunkMesh = ChunkBuilder(self.atlas, self.world, chunkPosition)
                    chunkModel = Model(chunkMesh, glm.vec3(chunkPosition[0]*CHUNK_SIZE, 0, chunkPosition[1]*CHUNK_SIZE))
                    self.chunks[chunkPosition] = chunkModel

            if len(self.chunks) > 300:
                positions = []
                for position in self.chunks.keys():
                    distance = abs(sum(np.array(current)-np.array(position)))
                    VAOs = []
                    VBOs = []
                    if(distance > 18):
                        VAO, VBO = self.chunks[position].mesh.freeMemory()
                        positions.append(position)
                        VAOs.append(VAO)
                        VBOs.append(VBO)

                    glDeleteBuffers(len(VBOs), VBOs)
                    glDeleteVertexArrays(len(VAOs), VAOs)

                for position in positions:
                    del self.chunks[position]

            self.lastChunk = current
            


    def getCurrentChunk(self):
        xPos = int(self.player.position.x)
        zPos = int(self.player.position.z)

        return (xPos//16,zPos//16)
    
    def draw(self, shader):
        self.update()
        for position in self.visibleChunks:
            position = tuple(position)
            self.chunks[position].draw(shader)
        