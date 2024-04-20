import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
import modelo

altura = 700
largura = 700

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


    vertex_code = """
        attribute vec3 position;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
        }
        """
    fragment_code = """
            uniform vec4 color;
            void main(){
                gl_FragColor = color;
            }
            """

    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")


    glAttachShader(program, vertex)
    glAttachShader(program, fragment)


    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    glUseProgram(program)

    vertices = modelo.vertices

    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)


    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)


    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)


    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)


    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)


    loc_color = glGetUniformLocation(program, "color")


    glfw.show_window(window)

    glEnable(GL_DEPTH_TEST) ### importante para 3D

    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        
        identity = np.identity(4)

        mat_model = model()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, glm.value_ptr(mat_model))    
        
        mat_view = view()
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, glm.value_ptr(mat_view))

        mat_projection = projection()
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_FALSE, glm.value_ptr(mat_projection))    
        
        
        # renderizando a cada três vértices (triangulos)
        gray = 0.0
        for i in range(0,len(vertices['position']),3):
            gray = i/(len(vertices))
            glUniform4f(loc_color, gray, gray, gray, 1.0) ### definindo uma cor
            glDrawArrays(GL_TRIANGLES, i, 3)
            
        
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

def model():
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade   
    matrix_transform = glm.rotate(matrix_transform,math.radians(180),glm.vec3(0.0,0.0,1.0))
    matrix_transform = glm.translate(matrix_transform,glm.vec3(0.0,0.5,-2))
    matrix_transform = glm.scale(matrix_transform,glm.vec3(1,1,1))
    return matrix_transform


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