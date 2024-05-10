import numpy as np
from utils.block_types import *
from noise.perlin import SimplexNoise
from perlin_noise import PerlinNoise

class World:

    def __init__(self, seed = 0):
        self.noise = PerlinNoise(octaves=0.2,seed=32)
        self.dict = {}

    def get_block(self,position):
        x,y,z = position

        noiseValue = 0

        if (x,z) in self.dict:
            noiseValue = self.dict[(x,z)]
        else:
            noiseValue = self.noise.noise((float(x/32), float(z/32)))
            self.dict[(x,z)] = noiseValue

        #print(noiseValue)

        noiseValue = int((noiseValue+1)/2*255)


        if y == noiseValue:
            return GRASS
        elif y < noiseValue and y > noiseValue - 10:
            return DIRT
        elif y <= noiseValue - 10:
            return COBBLE
        else:
            return NONE

