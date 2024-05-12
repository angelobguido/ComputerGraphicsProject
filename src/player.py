import glm
from terrain.world import World
from utils.player_directions import *
from utils.block_types import *

INITIAL_POSITION = glm.vec3(0.0,100,0)
INITIAL_PLAYER_FRONT = glm.vec3(0.0, 0.0, -1.0)
PLAYER_UP  = glm.vec3(0.0, 1.0, 0.0)
SPEED = 200
SENSITIVITY = 0.1
INITIAL_FOV=45

NEAR = 0.1
FAR = 1000

class Player:

    def __init__(self, width, height, world: World):
        self.position = INITIAL_POSITION
        self.front = glm.vec3(INITIAL_PLAYER_FRONT)
        self.lastX = 800.0 / 2.0
        self.lastY = 600.0 / 2.0
        self.firstMouse = True
        self.yaw = -90.0
        self.pitch = 0.0
        self.fov = INITIAL_FOV
        self.width = width
        self.height = height
        self.world = world
        self.lastPosition = glm.vec3(INITIAL_POSITION)

    def move(self, deltaTime, direction):

        self.lastPosition.x = self.position.x
        self.lastPosition.y = self.position.y
        self.lastPosition.z = self.position.z
        
        displacement = SPEED * deltaTime

        if direction == FORWARD:
            self.position += displacement * glm.normalize(self.front-(0,self.front.y,0))
        if direction == BACK:
            self.position -= displacement * glm.normalize(self.front-(0,self.front.y,0))
        if direction == LEFT:
            self.position -= glm.normalize(glm.cross(self.front, PLAYER_UP)) * displacement
        if direction == RIGHT:
            self.position += glm.normalize(glm.cross(self.front, PLAYER_UP)) * displacement
        if direction == UP:
            self.position += glm.normalize(glm.vec3(0.0,1.0,0.0)) * displacement
        if direction == DOWN:
            self.position -= glm.normalize(glm.vec3(0.0,1.0,0.0)) * displacement

        ranges = [(0.5,0,0),(-0.5,0,0),(0,0.5,0),(0,-0.5,0),(0,0,0.5),(0,0,-0.5)]
        for range in ranges:
            self.detectCollision(range)

    def detectCollision(self, range):
        xPos = int(self.position.x+range[0])
        yPos = int(self.position.y+range[1])
        zPos = int(self.position.z+range[2])
        
        if self.world.get_block((xPos,yPos,zPos)) != NONE:
            self.position.x = self.lastPosition.x
            self.position.y = self.lastPosition.y
            self.position.z = self.lastPosition.z


    def look(self, xpos, ypos):
        
        if (self.firstMouse):

            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos 
        self.lastX = xpos
        self.lastY = ypos
 
        xoffset *= SENSITIVITY
        yoffset *= SENSITIVITY

        self.yaw += xoffset
        self.pitch += yoffset

        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(front)

    def zoom(self, yoffset):
        
        self.fov -= yoffset
        
        if (self.fov < 1.0):
            self.fov = 1.0
        if (self.fov > 45.0):
            self.fov = 45.0

    def updateDimensions(self, width, height):
        self.width = width
        self.height = height

    def getView(self):
        mat_view = glm.lookAt(self.position, self.position+self.front, PLAYER_UP)
        return mat_view

    def getSkyView(self):
        mat_view = glm.lookAt(glm.vec3(0,0,0), glm.vec3(0,0,0)+self.front, PLAYER_UP)
        return mat_view

    def getProjection(self):
        mat_projection = glm.perspective(glm.radians(self.fov), self.width/self.height, NEAR, FAR)
        return mat_projection

