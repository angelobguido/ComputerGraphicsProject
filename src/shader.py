from OpenGL.GL import *

import glm

class Shader:
    def __init__(self, vertexPath: str, fragmentPath: str):
        # 1. retrieve the vertex/fragment source code from filePath
        try:
            # open files
            vShaderFile = open(vertexPath)
            fShaderFile = open(fragmentPath)
            
            # read file's buffer contents into strings
            vertexCode = vShaderFile.read()
            fragmentCode = fShaderFile.read()
            # close file handlers
            vShaderFile.close()
            fShaderFile.close()

            # 2. compile shaders
            # vertex shader
            vertex = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(vertex, vertexCode)
            glCompileShader(vertex)
            self.checkCompileErrors(vertex, "VERTEX")
            # fragment Shader
            fragment = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(fragment, fragmentCode)
            glCompileShader(fragment)
            self.checkCompileErrors(fragment, "FRAGMENT")
            # shader Program
            self.ID = glCreateProgram()
            glAttachShader(self.ID, vertex)
            glAttachShader(self.ID, fragment)
            glLinkProgram(self.ID)
            self.checkCompileErrors(self.ID, "PROGRAM")
            # delete the shaders as they're linked into our program now and no longer necessary
            glDeleteShader(vertex)
            glDeleteShader(fragment)
        
        except IOError:
            print("ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ")
            
        

    def use(self) -> None:
        glUseProgram(self.ID)
        
    
    def setVec4(self, name: str, vec: glm.vec4) -> None:
        glUniform4fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(vec))
    
    def setMat4(self, name: str, mat: glm.mat4) -> None:
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(mat))

    def checkCompileErrors(self, shader: int, type: str) -> None:
        if (type != "PROGRAM"):
            success = glGetShaderiv(shader, GL_COMPILE_STATUS)
            if (not success):
                infoLog = glGetShaderInfoLog(shader)
                print("ERROR::SHADER_COMPILATION_ERROR of type: " + type + "\n" + infoLog.decode() + "\n -- --------------------------------------------------- -- ")
        else:
            success = glGetProgramiv(shader, GL_LINK_STATUS)
            if (not success):
                infoLog = glGetProgramInfoLog(shader)
                print("ERROR::PROGRAM_LINKING_ERROR of type: " + type + "\n" + infoLog.decode() + "\n -- --------------------------------------------------- -- ")

                