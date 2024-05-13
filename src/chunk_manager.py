import glm
from chunk_builder import ChunkBuilder
from model import Model
import numpy as np
from OpenGL.GL import *

CHUNK_SIZE = 16

LOAD_RANGE = 4
VISION_RANGE = 2
MAX_RANGE_TO_LOAD = 3

INITIAL_LOAD = 5

class ChunkManager:

    def __init__(self, world, player, atlas):
        self.world = world
        self.player = player
        self.atlas = atlas
        self.lastChunk = (0,0)
        self.lastMaxLoadChunk = (0,0)
        
        self.chunks = {}

        for i in range(-INITIAL_LOAD,INITIAL_LOAD + 1):
            for j in range(-INITIAL_LOAD,INITIAL_LOAD + 1):
                chunk_mesh = ChunkBuilder(atlas, self.world, (i,j))
                chunk_model = Model(chunk_mesh, position=glm.vec3(i*16,0,j*16))
                self.chunks[(i,j)] = chunk_model
                print((i,j))


    def update(self):
        current = self.getCurrentChunk()
        if current != self.lastChunk:
            print(f"Distance: {get_distance(current, self.lastMaxLoadChunk)}")
            if get_distance(current, self.lastMaxLoadChunk) >= MAX_RANGE_TO_LOAD:
                self.lastMaxLoadChunk = current

                for i in range(-LOAD_RANGE, LOAD_RANGE + 1):
                    for j in range(-LOAD_RANGE, LOAD_RANGE + 1):

                        loadPosition = (i+current[0],j+current[1])

                        if loadPosition not in self.chunks:
                            chunkMesh = ChunkBuilder(self.atlas, self.world, loadPosition)
                            chunkModel = Model(chunkMesh, glm.vec3(loadPosition[0]*CHUNK_SIZE, 0, loadPosition[1]*CHUNK_SIZE))
                            self.chunks[loadPosition] = chunkModel

                if len(self.chunks) > 200:
                    positions = []
                    for position in self.chunks.keys():
                        distance = get_distance(current, position)
                        VAOs = []
                        VBOs = []
                        if(distance > 10):
                            VAO, VBO = self.chunks[position].mesh.freeMemory()
                            positions.append(position)
                            VAOs.append(VAO)
                            VBOs.append(VBO)

                        glDeleteBuffers(len(VBOs), VBOs)
                        glDeleteVertexArrays(len(VAOs), VAOs)

                    for position in positions:
                        del self.chunks[position]

            self.lastChunk = current
            
    def breakBlock(self, position):
        blockChunkPosition = (position[0]//CHUNK_SIZE, position[2]//CHUNK_SIZE)
        
        x = position[0]%CHUNK_SIZE
        z = position[2]%CHUNK_SIZE

        self.chunks[blockChunkPosition].mesh.destroyBlockInMesh((x, position[1], z))

        self.updateSurroundingBlocks(position)

    def placeBlock(self,position):

        blockChunkPosition = (position[0]//CHUNK_SIZE, position[2]//CHUNK_SIZE)
        
        x = position[0]%CHUNK_SIZE
        z = position[2]%CHUNK_SIZE

        self.chunks[blockChunkPosition].mesh.updateBlockInMesh((x, position[1], z))

        self.updateSurroundingBlocks(position)

    def updateSurroundingBlocks(self, position):

        for updatePosition in [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)]:
            x = position[0] + updatePosition[0]
            y = position[1] + updatePosition[1]
            z = position[2] + updatePosition[2]

            if y >= 0 and y < 128:
                otherBlockChunkPosition = (x//CHUNK_SIZE, z//CHUNK_SIZE) 
                self.chunks[otherBlockChunkPosition].mesh.updateBlockInMesh((x%CHUNK_SIZE,y,z%CHUNK_SIZE))


    def getCurrentChunk(self):
        xPos = int(self.player.position.x)
        zPos = int(self.player.position.z)

        return (xPos//16,zPos//16)
    
    def draw(self, shader):
        self.update()
        
        for i in range(-VISION_RANGE, VISION_RANGE+1):
            for j in range(-VISION_RANGE, VISION_RANGE+1):
                self.chunks[(i+self.lastChunk[0],j+self.lastChunk[1])].draw(shader)
        

def get_distance(position1, position2):
    return int(abs(sum(np.array(position1)-np.array(position2))))
                        