import numpy as np
from utils.block_types import *
from noise.perlin import SimplexNoise
from perlin_noise import PerlinNoise
import random
from block_arranges import *
import pickle


class World:

    def __init__(self, seed = 0, load = False):

        self.noise = PerlinNoise(octaves=0.2,seed=seed)
        self.noiseValues = {}
        self.blocks = {}
        self.seed = seed
        random.seed(seed)

        if load:
            self.load()

    def save(self):
        f = open("save.pkl","wb")

        pickle.dump(self.blocks,f)

        f.close()


    def load(self):
        f = open("save.pkl","rb")

        self.blocks = pickle.load(f)

        f.close()

    def get_block(self,position):
        x,y,z = position

        if (x,y,z) in self.blocks:
            return self.blocks[(x,y,z)]

        noiseValue = 0

        if (x,z) in self.noiseValues:
            noiseValue = self.noiseValues[(x,z)]
        else:
            noiseValue = self.noise.noise((float(x/32), float(z/32)))
            self.noiseValues[(x,z)] = noiseValue

        #print(noiseValue)

        noiseValue = int((noiseValue+1)/2*128)


        if y == noiseValue:
            self.blocks[(x,y,z)] = GRASS
            
            if (x,z) in [(2,2), (40,40), (-20,-20)]:
                self.placeStructure((x,y,x), house_arrange)

            if random.random() > 0.999:
                self.placeStructure((x,y+1,z), tree_arrange, (1,1))

        elif y < noiseValue and y > noiseValue - 10:
            self.blocks[(x,y,z)] = DIRT
        elif y <= noiseValue - 10:
            self.blocks[(x,y,z)] = COBBLE
        else:
            self.blocks[(x,y,z)] = NONE

        return self.blocks[(x,y,z)]

    def breakBlock(self, position):
        self.blocks[position] = NONE

    def placeBlock(self, position):
        self.blocks[position] = BRICK

    def placeStructure(self, position, block_arrange, pivot = (0,0)):
        
        for y in range(block_arrange.shape[0]):
            for z in range(block_arrange.shape[1]):
                for x in range(block_arrange.shape[2]):
                    if block_arrange[y,z,x] != NONE:
                        self.blocks[(position[0] + x - pivot[0], position[1] + block_arrange.shape[0] - y - 1, position[2] + z -pivot[1])] = block_arrange[y,z,x]