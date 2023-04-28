#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

# Pacotes para o desenvolvimento do sistema
from OpenGL.GL import *
import glfw
import numpy as np


# Diversos includes para o projeto do Renderizador OpenGL
from renderizador.transformations import *
from renderizador.camera import *
from renderizador.callbacks import *
from renderizador.uniforms import *
from renderizador.programmable_shaders import *

# Usado para checar a plataforma Mac e saber se compatível com chamadas de OpenGL
import platform
   

default_vertex_shader = r'''
    #version 330 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 normal;
    layout (location = 2) in vec3 color;
    layout (location = 3) in vec2 uv;

    out vec3 bColor;
    out vec3 bNormal;
    out vec2 bUV;

    void main() {
        gl_Position = vec4(position, 1.0);
        bNormal = normal;
        bColor = color;
        bUV=uv;
    }
'''

default_fragment_shader = r'''
    #version 330 core
    layout (location = 0) out vec4 FragColor;
    in vec3 bNormal;
    in vec3 bColor;
    in vec2 bUV;
    void main() {
        FragColor = vec4(bColor, 1.0f);
    }
'''

# Vertices (forçando ser float32 para evitar que algum vire outro tipo)
vertices = np.array(
    [-1.0, -1.0, -1.0,
      1.0, -1.0, -1.0,
     -1.0,  1.0, -1.0,
      1.0,  0.5, -1.0,
    ], np.float32
)

# Cores (forçando ser float32 para evitar que algum vire outro tipo)
colors = np.array(
    [1.0, 0.0, 0.0,
     0.0, 1.0, 0.0,
     0.0, 0.0, 1.0,
     1.0, 1.0, 0.0
    ], np.float32
)

# Coordenadas UV (forçando ser float32 para evitar que algum vire outro tipo)
uvs = np.array(
    [0.0, 0.0,
     1.0, 0.0,
     0.0, 1.0,
     1.0, 1.0,
    ], np.float32
)


# Vertices (forçando ser float32 para evitar que algum vire outro tipo)
vertices = np.array([
    -1.0,  1.0, -1.0,
    -1.0,  1.0,  1.0,
    1.0,  1.0,  1.0,
    1.0,  1.0, -1.0,
    -1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
    1.0, -1.0,  1.0,
    1.0, -1.0, -1.0,
], np.float32)

index = np.array([
    0, 1, 3,
    1, 2, 3,
    0, 4, 1,
    4, 5, 1,
    1, 5, 2,
    5, 6, 2,
    2, 6, 3,
    6, 7, 3,
    3, 7, 0,
    7, 4, 0,
    4, 7, 5,
    7, 6, 5,
])


def add_geometry(mode, vertices, normals=None, colors=None, uvs=None, create_normals=False, index=None):

    data = []
    
    # Valores padrões (normal, cor)
    normal = [0.0, 0.0, 1.0]
    color = [1.0, 1.0, 1.0]
    uv = [0.0 ,0.0]

    if mode == GL_TRIANGLE_STRIP:
        for f in range(0, len(vertices), 3):
            
            # identificando vértice
            vertex = vertices[f:f+3]

            # identificando normal
            if normals is not None:
                normal = normals[f:f+3]
            elif create_normals and f < vertices.size - (2*3):
                vertex1 = vertices[f+3:f+6]
                vertex2 = vertices[f+6:f+9]
                if f%6==0:
                    normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                else:
                    normal = normalize(np.cross(vertex2 - vertex, vertex1 - vertex))
            
            # identificando cor
            if colors is not None:
                color = colors[f:f+3]

            # identificando coordenadas de textura
            if uvs is not None:
                uv = uvs[(f//3)*2:((f//3)*2)+2]
            else:
                # Deixa os UVs proporcionais a posição na tela
                uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2])

            data.append(np.concatenate([vertex, normal, color, uv]))

        count = vertices.size

    if mode == GL_TRIANGLES:

        if index is not None:
            for f in range(len(index)):

                # identificando vértice
                vertex = vertices[index[f]*3:(index[f]*3)+3]

                # identificando normal
                if normals is not None:
                    normal = normals[index[f+1]*3:(index[f+1]*3)+3]
                elif create_normals:
                    if f%3==0:
                        vertex1 = vertices[(index[f+1]*3):(index[f+1]*3)+3]
                        vertex2 = vertices[(index[f+2]*3):(index[f+2]*3)+3]
                        normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                
                # identificando cor
                if colors is not None:
                    color = colors[index[f]*3:(index[f]*3)+3]

                # identificando coordenadas de textura
                if uvs is not None:
                    uv = uvs[(index[f]//3)*2:((index[f]//3)*2)+2]
                else:
                    # Deixa os UVs proporcionais a posição na tela
                    uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2])

                data.append(np.concatenate([vertex, normal, color, uv]))

        count = len(index)*3

    
    data = np.array(data, np.float32).flatten()

    # Cria o VBO (Vertex Buffer Object) para armazenar vértices
    verticesVBO = arrays.vbo.VBO(data, usage='GL_STATIC_DRAW')
    verticesVBO.create_buffers()

    # Cria e ativa o VAO (Vertex Array Object) para gerenciar os VBOs
    triangleVAO = glGenVertexArrays(1)
    glBindVertexArray(triangleVAO)

    # Ativa o VBO para o contexto atual
    verticesVBO.bind()

    # buffer data into OpenGL
    verticesVBO.copy_data()

    # Configuração para posição dos vértices
    # Coloca no ID 0, vértices 3D, com um stride de 3*4 (3 vertices de float = 4)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Configuração para normal dos vértices
    # Coloca no ID 1, vértices 3D, com um stride de 3*4 (3 vertices de float = 4) e um ofset de (3*4)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    # Configuração para cor dos vértices
    # Coloca no ID 2, vértices 3D, com um stride de 3*4 (3 vertices de float = 4) e um ofset de (3*4)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(6 * 4))
    glEnableVertexAttribArray(2)

    # Configuração para coordenadas uv de textura dos vértices
    # Coloca no ID 3, vértices 3D, com um stride de 3*4 (3 vertices de float = 4) e um ofset de (3*4)
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(9 * 4))
    glEnableVertexAttribArray(3)

    # Desativa (unbind) o VBO
    verticesVBO.unbind()

    # Desativa (unbind) o VAO
    glBindVertexArray(0)

    return triangleVAO, count

class Renderizador:

    # Define a cor de fundo da renderização
    def set_title(self, text):
        self.title = text

    # Define a cor de fundo da renderização
    def set_background_color(self, color):
        self.background_color = color

    # Cria a jenala de renderização
    def __init__(self, resolution, near, far):

        self.window = None

        # Cor padrão para o fundo da janela (para apagar o buffer de cores)
        self.background_color = (0.0, 0.0, 0.0, 1.0)

        # Título padrão da janela de renderização
        self.title = "Computação Gráfica"



        # Cria recursos de manipulação de câmera
        #self.camera = Camera("fly", resolution, near=near, far=far)
        self.camera = Camera("examine", resolution, near=near, far=far)
        Callbacks.camera  = self.camera


        # Inicia e configura o glfw
        if not glfw.init():
            raise Exception("Não foi possível iniciar o glfw")
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # Chamada para Mac para suportar chamadas antigas (deprecated)
        if platform.system().lower() == 'darwin':
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        # Cria a janela principal e colocar no contexto atual
        Callbacks.resolution = resolution
        self.window = glfw.create_window(resolution[0], resolution[1], self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Não foi possível criar a janela glfw")
        glfw.make_context_current(self.window)
        #glfw.set_window_pos(window, 0, 0) # define a posição da janela

    def render(self, vertex_shader_source=None, fragment_shader_source=None, uniforms_source={}):

        if self.window == None:
            raise Exception("Janela não foi criada")
        
        if vertex_shader_source == None:
            vertex_shader_source = default_vertex_shader

        if fragment_shader_source == None:
            fragment_shader_source = default_fragment_shader

        # Versões de Mac não suportam debug
        if platform.system().lower() != 'darwin':
            # Exibe mensagens de Debug
            glEnable(GL_DEBUG_OUTPUT)
            glDebugMessageCallback(GLDEBUGPROC(Callbacks.debug_message_callback), None)

        # inicializa a posição do cursor
        Callbacks.cursor_pos = glfw.get_cursor_pos(self.window)

        # Define o callback para caso a janela seja redimensionada, teclas pressionadas ou movimento do mouse
        glfw.set_framebuffer_size_callback(self.window, Callbacks.framebuffer_size_callback)
        glfw.set_key_callback(self.window, Callbacks.key_callback)
        glfw.set_cursor_pos_callback(self.window, Callbacks.cursor_pos_callback)
        glfw.set_scroll_callback(self.window, Callbacks.scroll_callback)

        # desativa a apresentação do cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Ativa o Z-Buffer
        glEnable(GL_DEPTH_TEST)




        #########
        # mode = GL_TRIANGLE_STRIP
        # vao, count  = add_geometry(GL_TRIANGLE_STRIP, vertices, colors=colors, uvs=uvs, create_normals=True)

        mode = GL_TRIANGLES
        #vao, count = set_geometry()
        vao, count  = add_geometry(GL_TRIANGLES, vertices, create_normals=True, index=index)


        # Compila os shaders
        vertexShader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_source)
        fragmentShader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source)

        # Conecta (link) os shaders para a aplicação
        program_id = link_shader(vertexShader_id, fragmentShader_id)
        
        # Configura os Uniforms para os shaders
        uniforms = {}

        # Cadastra os Uniforms básicos do ShaderToy
        uniforms["iResolution"] = glGetUniformLocation(program_id, 'iResolution')
        uniforms["iTime"] = glGetUniformLocation(program_id, 'iTime')

        # Cadastra os Uniforms
        for field in uniforms_source:
            uniforms[field] = glGetUniformLocation(program_id, field)    

        # remove os shaders da memória
        glDeleteShader(vertexShader_id)
        glDeleteShader(fragmentShader_id)

        # Define no contexto qual a cor para limpar o buffer de cores
        glClearColor(*self.background_color)

        # Realiza a renderização enquanto a janela não for fechada
        while not glfw.window_should_close(self.window):

            # Limpa a janela com a cor de fundo e apagar o z-buffer
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # use our own rendering program
            glUseProgram(program_id)

            passed_time = glfw.get_time()  # returna o tempo passado desde que a aplicação começou

            # Fazendo os uniforms básicos do ShaderToy
            glUniform2f(uniforms["iResolution"], Callbacks.resolution[0], Callbacks.resolution[1])
            glUniform1f(uniforms["iTime"], passed_time)

            parse_uniforms(uniforms_source, uniforms)

            # Ativa (bind) VAO
            glBindVertexArray(vao)

            # Desenha os vértices como triângulos
            glDrawArrays(mode, 0, count)
            
            # Desativa (unbind) o VAO
            glBindVertexArray(0)

            # Detecta e armazena as chamadas de teclado
            keyPressed = np.where(Callbacks.keyArray == True)
            for key in keyPressed[0]:
                self.camera.send_keys(key)

            # captura e processa eventos da janela
            glfw.poll_events()

            # Faz a troca dos framebuffer (swap frame buffer)
            glfw.swap_buffers(self.window)

        # Limpa o VAO 
        glDeleteVertexArrays(1, [vao])
        #glDeleteVertexArrays(2, [triangleVAO, sphereVAO])

        # Limpa o VBO
        # vbo.delete()

        # finaliza o glfw
        glfw.terminate()


# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)