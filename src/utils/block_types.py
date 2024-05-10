NONE = 0
PLANK = 1
BRICK = 2
COBBLE = 3
LEAVES = 4
LOG = 5
GRASS = 6
GLASS = 7
DIRT = 8


def get_textures(type):
    if type == NONE:
        return []
    elif type == PLANK: 
        return [4,4,4,4,4,4]
    elif type == BRICK:
        return [6,6,6,6,6,6]
    elif type == COBBLE:
        return [0,0,0,0,0,0]
    elif type == LEAVES:
        return [1,1,1,1,1,1]
    elif type == LOG:
        return [7,7,2,2,2,2]
    elif type == GRASS:
        return [8,3,5,5,5,5]
    elif type == GLASS:
        return [9,9,9,9,9,9]
    elif type == DIRT:
        return [3,3,3,3,3,3]
    
def is_transparent(type):
    return type in [GLASS, LEAVES, NONE]
