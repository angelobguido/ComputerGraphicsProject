import numpy as np
from utils.block_types import *
from noise.perlin import SimplexNoise
from perlin_noise import PerlinNoise

class World:

    def __init__(self, seed = 0):
        self.noise = PerlinNoise(octaves=0.2,seed=seed)
        self.noiseValues = {}
        self.blocks = {}

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
        elif y < noiseValue and y > noiseValue - 10:
            self.blocks[(x,y,z)] = DIRT
        elif y <= noiseValue - 10:
            self.blocks[(x,y,z)] = COBBLE
        else:
            self.blocks[(x,y,z)] = NONE

        return self.blocks[(x,y,z)]

