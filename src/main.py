import glfw
from OpenGL.GL import *
from shader import Shader
from mesh import Mesh
from model import Model
from block_grid import BlockGrid
from utils.wave_front_reader import WaveFrontReader
from utils.texture_reader import TextureReader
import numpy as np
import glm
import math
import modelo
from utils.block_types import *


altura = 1000
largura = 1000

cameraPos    = glm.vec3(0.0,0.0,3)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp     = glm.vec3(0.0, 1.0, 0.0)
cameraSpeed = 0.3

firstMouse = True
yaw   = -90.0
pitch =  0.0
lastX =  800.0 / 2.0
lastY =  600.0 / 2.0

deltaTime = 0.0
lastFrame = 0.0

fov=45

def main():
    global deltaTime, lastFrame

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, "Câmeras - Matriz Projection", None, None)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    shader = Shader("./shaders/vertex_shader.hlsl", "./shaders/fragment_shader.hlsl")

    plank = TextureReader("./models/blocos/plank.png").textureID
    brick = TextureReader("./models/blocos/brick.png").textureID
    cobble = TextureReader("./models/blocos/cobblestone.png").textureID

    block_tex_dict = {PLANK: plank, BRICK: brick, COBBLE: cobble}
    block_arrange = np.array([
        [  
            [BRICK, BRICK, BRICK],
            [BRICK, BRICK, BRICK],
            [BRICK, BRICK, BRICK]
        ],
        [
            
            [COBBLE, COBBLE, BRICK],
            [COBBLE, NONE, COBBLE],
            [COBBLE, NONE, BRICK]
        ],
        [
            [COBBLE, COBBLE, COBBLE],
            [COBBLE, NONE, COBBLE],
            [COBBLE, NONE, COBBLE]
        ],
        [
            [PLANK, PLANK, PLANK],
            [PLANK, PLANK, PLANK],
            [PLANK, PLANK, PLANK]
        ]
    ])

    bloco1mesh = Mesh(WaveFrontReader("./models/blocos/base.obj").vertices)

    grid = BlockGrid(bloco1mesh, block_arrange, block_tex_dict)

    glfw.show_window(window)

    glEnable(GL_DEPTH_TEST) ### importante para 3D
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)

    shader.use()

    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        
        mat_view = view()
        mat_projection = projection()
        
        shader.setMat4("view", mat_view)
        shader.setMat4("projection", mat_projection)

        grid.draw(shader)
        
        glfw.swap_buffers(window)

    glfw.terminate()

def framebuffer_size_callback(window, width: int, height: int) -> None:
    glViewport(0, 0, width, height)
    
def key_event(window,key,scancode,action,mods):
    global fov, cameraPos, cameraFront

    if (glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)

    cameraSpeed = 2.5 * deltaTime

    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
        cameraPos += cameraSpeed * glm.normalize(cameraFront-cameraFront.y)
    if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
        cameraPos -= cameraSpeed * glm.normalize(cameraFront-cameraFront.y)
    if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
        cameraPos += glm.normalize(glm.vec3(0.0,1.0,0.0)) * cameraSpeed
    if (glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS):
        cameraPos -= glm.normalize(glm.vec3(0.0,1.0,0.0)) * cameraSpeed

def mouse_callback(window, xpos: float, ypos: float) -> None:
    global cameraFront, lastX, lastY, firstMouse, yaw, pitch

    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos 
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1 
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    if (pitch > 89.0):
        pitch = 89.0
    if (pitch < -89.0):
        pitch = -89.0

    front = glm.vec3()
    front.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    front.y = glm.sin(glm.radians(pitch))
    front.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)

def scroll_callback(window, xoffset: float, yoffset: float) -> None:
    global fov
    
    fov -= yoffset
    if (fov < 1.0):
        fov = 1.0
    if (fov > 45.0):
        fov = 45.0

def view():
    global cameraPos, cameraFront
    mat_view = glm.lookAt(cameraPos, cameraPos+cameraFront, cameraUp)
    return mat_view

def projection():
    global altura, largura, fov
    
    near = 0.1
    far = 100
    
    mat_projection = glm.perspective(glm.radians(fov), largura/altura, near, far)
    
    return mat_projection


main()