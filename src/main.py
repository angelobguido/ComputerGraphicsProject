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
from chunk_builder import ChunkBuilder
from chunk_manager import ChunkManager
from terrain.world import World
from player import Player
from utils.player_directions import *

HEIGHT = 600
WIDTH = 800

LOAD = True

WORLD = World(50, LOAD)
PLAYER = Player(WIDTH, HEIGHT, WORLD)
CHUNK_MANAGER = None

    
deltaTime = 0.0
lastFrame = 0.0

window = None
fullscreen = False
key_states = {}

polygon_mode = False

def main():
    global deltaTime, lastFrame, window, CHUNK_MANAGER

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(WIDTH, HEIGHT, "Minecraft 2", None, None)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_event)
    glfw.set_mouse_button_callback(window, mouse_button_event)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    skyTex = TextureReader("./models/sky/sky.png", False).textureID
    skyMesh = Mesh(WaveFrontReader("./models/sky/sky.obj").vertices, [(skyTex, 0)])
    sky = Model(skyMesh, scale=glm.vec3(2,2,2))
    sky2 = Model(skyMesh, scale=glm.vec3(2,-2,2))
    monstro = Model(Mesh(WaveFrontReader("./models/monstro/monstro.obj").vertices, [(TextureReader("./models/monstro/monstro.jpg").textureID, 0)]), position=(0,75,0), scale=(3,3,3))

    shader = Shader("./shaders/vertex_shader.hlsl", "./shaders/fragment_shader.hlsl")
    block_shader = Shader("./shaders/block_vertex_shader.hlsl", "./shaders/block_fragment_shader.hlsl")
    block_shader.use()
    block_shader.setFloat("ambientStrength", 0.4)
    block_shader.setVec3("lightColor", glm.vec3(1,1,1))
    block_shader.setVec3("lightPos", glm.vec3(100, 500, 100))

    atlas = TextureReader("./textures/atlas.png", mipmap_paths=[
        "./textures/atlas0.png",
        "./textures/atlas1.png",
        "./textures/atlas2.png",
        "./textures/atlas3.png",
        "./textures/atlas4.png"
    ]).textureID

    CHUNK_MANAGER = ChunkManager(WORLD, PLAYER, atlas)

    glfw.show_window(window)

    glEnable(GL_DEPTH_TEST) ###w importante para 3D
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_ALPHA_TEST)


    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        PLAYER.update(deltaTime)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        mat_view = PLAYER.getSkyView()
        mat_projection = PLAYER.getProjection()
        
        shader.use()
        shader.setMat4("view", mat_view)
        shader.setMat4("projection", mat_projection)

        sky.draw(shader)
        sky2.draw(shader)
        
        glClear(GL_DEPTH_BUFFER_BIT)

        mat_view = PLAYER.getView()
        shader.setMat4("view", mat_view)
        
        monstro.draw(shader)

        block_shader.use()
        block_shader.setMat4("view", mat_view)
        block_shader.setMat4("projection", mat_projection)        
        
        CHUNK_MANAGER.draw(block_shader)

        glfw.swap_buffers(window)

    glfw.terminate()

def framebuffer_size_callback(window, width: int, height: int):
    glViewport(0, 0, width, height)
    PLAYER.updateDimensions(width,height)
    
def mouse_button_event(window, key, scancode, action):
    if key == glfw.MOUSE_BUTTON_LEFT:
        positionArray = PLAYER.getBlock()
        if positionArray:
            position = positionArray[0]
            WORLD.breakBlock(position)
            CHUNK_MANAGER.breakBlock(position)

    if key == glfw.MOUSE_BUTTON_RIGHT:
        positionArray = PLAYER.getBlock()
        if positionArray:
            position = positionArray[1]
            WORLD.placeBlock(position)
            CHUNK_MANAGER.placeBlock(position)

def key_event(window, key, scancode, action, mods):
    global fullscreen, key_states, polygon_mode

    if action == glfw.PRESS:
        key_states[key] = True
    elif action == glfw.RELEASE:
        key_states[key] = False

    if key_states.get(glfw.KEY_ESCAPE, False):
        WORLD.save()
        glfw.set_window_should_close(window, True)

    if key_states.get(glfw.KEY_W, False):
        PLAYER.move(deltaTime, FORWARD)
    if key_states.get(glfw.KEY_S, False):
        PLAYER.move(deltaTime, BACK)
    if key_states.get(glfw.KEY_A, False):
        PLAYER.move(deltaTime, LEFT)
    if key_states.get(glfw.KEY_D, False):
        PLAYER.move(deltaTime, RIGHT)
    if key_states.get(glfw.KEY_SPACE, False):
        PLAYER.move(deltaTime, UP)
    if key_states.get(glfw.KEY_Q, False):
        PLAYER.move(deltaTime, DOWN)

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
            glfw.set_window_monitor(window, None, 100, 100, WIDTH, HEIGHT, glfw.DONT_CARE)
            fullscreen = False


def mouse_callback(window, xpos: float, ypos: float) -> None:
    PLAYER.look(xpos,ypos)

def scroll_callback(window, xoffset: float, yoffset: float) -> None:
    PLAYER.zoom(yoffset)


main()