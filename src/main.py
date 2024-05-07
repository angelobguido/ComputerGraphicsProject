import glfw
from OpenGL.GL import *
from shader import Shader
from mesh import Mesh
from model import Model
from block_group import BlockGroup, BlockGroupParams
from utils.wave_front_reader import WaveFrontReader
from utils.texture_reader import TextureReader
import numpy as np
import glm
import math
import modelo
from utils.block_types import *
from block_arranges import *


altura = 600
largura = 800

cameraPos    = glm.vec3(0.0,5,50)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp     = glm.vec3(0.0, 1.0, 0.0)
speedMultiplier = 10

firstMouse = True
yaw   = -90.0
pitch =  0.0
lastX =  800.0 / 2.0
lastY =  600.0 / 2.0
fov=45

deltaTime = 0.0
lastFrame = 0.0

window = None
fullscreen = False
key_states = {}

polygon_mode = False


def main():
    global deltaTime, lastFrame, window

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, "Câmeras - Matriz Projection", None, None)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    skyTex = TextureReader("./models/sky/sky.png", False).textureID
    skyMesh = Mesh(WaveFrontReader("./models/sky/sky.obj").vertices, [(skyTex, 0)])
    monstroTex = TextureReader("./models/monstro/monstro.jpg").textureID
    monstro = Model(Mesh(WaveFrontReader("./models/monstro/monstro.obj").vertices, [(monstroTex,0)]), position=glm.vec3(23,0.5,0))
    sky = Model(skyMesh, scale=glm.vec3(2,2,2))
    sky2 = Model(skyMesh, scale=glm.vec3(2,-2,2))

    shader = Shader("./shaders/vertex_shader.hlsl", "./shaders/fragment_shader.hlsl")

    plank = TextureReader("./models/blocos/plank.png").textureID
    brick = TextureReader("./models/blocos/brick.png").textureID
    cobble = TextureReader("./models/blocos/cobblestone.png").textureID
    leaves = TextureReader("./models/blocos/leaves.png").textureID
    log = TextureReader("./models/blocos/log.png").textureID
    grass = TextureReader("./models/blocos/grass.png").textureID
    glass = TextureReader("./models/blocos/glass.png").textureID

    block_tex_dict = {PLANK: plank, BRICK: brick, COBBLE: cobble, LEAVES: leaves, LOG: log, GRASS: grass, GLASS: glass}
    
    bloco1mesh = Mesh(WaveFrontReader("./models/blocos/base2.obj").vertices)
    # bloco1mesh = Mesh(WaveFrontReader("./models/monstro/monstro.obj").vertices)


    tree = BlockGroupParams(bloco1mesh, tree_arrange, block_tex_dict, pivot=glm.vec3(1,0,1))
    floor = BlockGroupParams(bloco1mesh, floor_arrange, block_tex_dict)
    house = BlockGroupParams(bloco1mesh, house_arrange, block_tex_dict)

    grid = BlockGroup(house)
    grid2 = BlockGroup(tree, glm.vec3(10,0,4))
    grid3 = BlockGroup(tree, glm.vec3(13,0,4))
    grid4 = BlockGroup(tree, glm.vec3(16,0,4))
    floor = BlockGroup(floor, glm.vec3(0,-1,0))

    glfw.show_window(window)

    glEnable(GL_DEPTH_TEST) ### importante para 3D
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_ALPHA_TEST)

    shader.use()

    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        mat_view = sky_view()
        mat_projection = projection()
        
        shader.setMat4("view", mat_view)
        shader.setMat4("projection", mat_projection)

        sky.draw(shader)
        sky2.draw(shader)

        #glClear(GL_DEPTH_BUFFER_BIT)
        
        mat_view = view()
        shader.setMat4("view", mat_view)
        
        grid.draw(shader)
        grid2.draw(shader)
        grid3.draw(shader)
        grid4.draw(shader)
        floor.draw(shader)
        monstro.draw(shader)
        
        
        glfw.swap_buffers(window)

    glfw.terminate()

def framebuffer_size_callback(window, width: int, height: int):
    global altura, largura
    glViewport(0, 0, width, height)
    altura = height
    largura = width

    
def key_event(window, key, scancode, action, mods):
    global fov, cameraPos, cameraFront, fullscreen, key_states, polygon_mode

    if action == glfw.PRESS:
        key_states[key] = True
    elif action == glfw.RELEASE:
        key_states[key] = False

    cameraSpeed = speedMultiplier * deltaTime

    if key_states.get(glfw.KEY_ESCAPE, False):
        glfw.set_window_should_close(window, True)

    if key_states.get(glfw.KEY_W, False):
        cameraPos += cameraSpeed * glm.normalize(cameraFront-cameraFront.y)
    if key_states.get(glfw.KEY_S, False):
        cameraPos -= cameraSpeed * glm.normalize(cameraFront-cameraFront.y)
    if key_states.get(glfw.KEY_A, False):
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if key_states.get(glfw.KEY_D, False):
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if key_states.get(glfw.KEY_SPACE, False):
        cameraPos += glm.normalize(glm.vec3(0.0,1.0,0.0)) * cameraSpeed
    if key_states.get(glfw.KEY_Q, False):
        cameraPos -= glm.normalize(glm.vec3(0.0,1.0,0.0)) * cameraSpeed

    if cameraPos.y < 1:
        cameraPos.y = 1

    if key == glfw.KEY_P and action == glfw.PRESS:
        if not polygon_mode:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            polygon_mode = True
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            polygon_mode = False
        

    if key == glfw.KEY_F and action == glfw.PRESS:
        # Toggle between fullscreen and windowed mode
        if not fullscreen:
            # Switch to fullscreen mode
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            glfw.set_window_monitor(window, monitor, 0, 0, mode.size.width, mode.size.height, mode.refresh_rate)
            fullscreen = True
        else:
            # Switch to windowed mode
            glfw.set_window_monitor(window, None, 100, 100, 800, 600, glfw.DONT_CARE)
            fullscreen = False


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

def sky_view():
    global cameraFront
    mat_view = glm.lookAt(glm.vec3(0,0,0), glm.vec3(0,0,0)+cameraFront, cameraUp)
    return mat_view

def projection():
    global altura, largura, fov
    
    near = 0.1
    far = 200
    
    mat_projection = glm.perspective(glm.radians(fov), largura/altura, near, far)
    
    return mat_projection


main()