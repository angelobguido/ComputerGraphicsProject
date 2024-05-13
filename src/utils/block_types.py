NONE = 0
PLANK = 1
BRICK = 2
COBBLE = 3
LEAVES = 4
LOG = 5
GRASS = 6
GLASS = 7
DIRT = 8
DIAMOND = 9
FURNACE = 10
TABLE = 11



def get_textures(type):
    if type == NONE:
        return []
    elif type == PLANK: 
        return [8,8,8,8,8,8]
    elif type == BRICK:
        return [11,11,11,11,11,11]
    elif type == COBBLE:
        return [2,2,2,2,2,2]
    elif type == LEAVES:
        return [3,3,3,3,3,3]
    elif type == LOG:
        return [14,14,4,4,4,4]
    elif type == GRASS:
        return [15,5,10,10,10,10]
    elif type == GLASS:
        return [16,16,16,16,16,16]
    elif type == DIRT:
        return [5,5,5,5,5,5]
    elif type == DIAMOND:
        return [6,6,6,6,6,6]
    elif type == FURNACE:
        return [7,7,9,12,12,12]
    elif type == TABLE:
        return [0,0,13,1,1,1]
    

def is_transparent(type):
    return type in [GLASS, LEAVES, NONE]
