#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

# Pacotes para o desenvolvimento do sistema
from imgui.integrations.glfw import GlfwRenderer
import imgui
import contextlib
import re
from OpenGL.GL import *
import glfw
import numpy as np
import time

# import Pillow for loading images
from PIL import Image

# Diversos includes para o projeto do Renderizador OpenGL
from renderizador.transformations import *
from renderizador.camera import *
from renderizador.callbacks import *
from renderizador.uniforms import *
from renderizador.programmable_shaders import *
from renderizador.utils import *
from renderizador.texture import *

# Usado para checar a plataforma Mac e saber se compatível com chamadas de OpenGL
import platform
   

default_vertex_shader = r'''
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
    layout (location = 0) out vec4 fragColor;
    in vec3 bNormal;
    in vec3 bColor;
    in vec2 bUV;
    void main() {
        fragColor = vec4(bColor, 1.0f);
    }
'''

# Vertices (forçando ser float32 para evitar que algum vire outro tipo)
vertices = np.array(
    [-1.0, -1.0, -1.0,
      1.0, -1.0, -1.0,
     -1.0,  1.0, -1.0,
      1.0,  1.0, -1.0,
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

class Renderizador:

    # Define a cor de fundo da renderização
    def set_title(self, text):
        self.title = text

    # Define a cor de fundo da renderização
    def set_background_color(self, color):
        self.background_color = color
    

    # Cria a jenala de renderização
    def __init__(self, resolution=(1024, 768), lock_mouse=False):

        self.window = None
 
        Callbacks.resolution = resolution
        # self.near = near
        # self.far = far

        # Faz o mouse não aparecer e ficar preso no meio da tela
        self.lock_mouse = lock_mouse

        # Cor padrão para o fundo da janela (para apagar o buffer de cores)
        self.background_color = (0.0, 0.0, 0.0, 1.0)

        # Título padrão da janela de renderização
        self.title = "Computação Gráfica"
       
        # Armazena as texturas
        self.textures = []

        self.data = []
        self.mode = None
        self.count = 0

        self.vertex_shader_source = default_vertex_shader
        self.fragment_shader_source = default_fragment_shader
        self.uniforms_source = {}

        self.play = True
        self.time = 0
        self.fps = 0

        self.shader_toy = True
        self.shader_toy_mIsLowEnd = True  # Muda o parâmetro para HW_PERFORMANCE

    @contextlib.contextmanager
    def create_main_window(self):

        if not glfw.init():
            raise Exception("Não foi possível iniciar o glfw")

        try:
            # Inicia e configura o glfw
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
            #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
            # Chamada para Mac para suportar chamadas antigas (deprecated)
            if platform.system().lower() == 'darwin':
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

            self.window = glfw.create_window(Callbacks.resolution[0], Callbacks.resolution[1], self.title, None, None)

            if not self.window:
                glfw.terminate()
                raise Exception("Não foi possível criar a janela glfw")
            glfw.make_context_current(self.window)

            #glfw.set_window_pos(window, 0, 0) # define a posição da janela

            yield self.window

        finally:
            glfw.terminate()


    def set_shaders(self, vertex_shader_source=None, fragment_shader_source=None, uniforms_source={}):

        if vertex_shader_source is None:
            self.vertex_shader_source = default_vertex_shader
        else:
            self.vertex_shader_source = vertex_shader_source

        if fragment_shader_source is None:
            self.fragment_shader_source = default_fragment_shader
        else:
            self.fragment_shader_source = fragment_shader_source

        self.uniforms_source = uniforms_source

    def set_texture(self, filename, id):
        self.textures.append(Texture(filename, id))

    def add_geometry(self, mode, vertices, normals=None, colors=None, uvs=None, create_normals=False, index=None):

        data = []
        
        # Valores padrões (normal, cor)
        normal = np.array([0.0, 0.0, 1.0], np.float32)
        color = np.array([1.0, 1.0, 1.0], np.float32)
        uv = np.array([0.0 ,0.0], np.float32)

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

                    if len(vertex) != 3:
                        raise Exception("Vetor não possui 3 dimensões")

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

        self.data = np.array(data, np.float32).flatten()
        self.mode = mode
        self.count = count

    def parse_geometry(self):

        # Cria o VBO (Vertex Buffer Object) para armazenar vértices
        verticesVBO = arrays.vbo.VBO(self.data, usage='GL_STATIC_DRAW')
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

        return triangleVAO, self.count


    def parse_textures(self):

        for texture in self.textures:

            # create texture
            texture.image = Image.open(texture.filename)
            texture.image = texture.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            texture.image = np.asarray(texture.image, np.uint8)
        
            texture.texture_id = glGenTextures(1)
            #glDeleteTextures([texture.texture_id])
            
            glBindTexture(GL_TEXTURE_2D, texture.texture_id)

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                texture.image.shape[1],
                texture.image.shape[0],
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                get_pointer(texture.image)
            )

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # unbind textura
            glBindTexture(GL_TEXTURE_2D, 0)
        

    # Todos os detalhes da interfacce gráfica de usuário
    def gui_interface(self):
        viewport = imgui.get_main_viewport()
        imgui.set_next_window_position(viewport.pos.x+10, viewport.pos.y + viewport.size.y - 40)
        imgui.set_next_window_size(0, 0) # Zero calcula de forma automática
        flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_SAVED_SETTINGS
        with imgui.begin("shadertoy", flags=flags):
            if imgui.arrow_button("Back", imgui.DIRECTION_LEFT):
                self.time = 0.0
                glfw.set_time(self.time)
            imgui.same_line()
            if self.play:
                if imgui.button('||'):
                    self.play = False
            else:
                if imgui.arrow_button("Play", imgui.DIRECTION_RIGHT):
                    self.play = True
            imgui.same_line()
            imgui.text(f"   {self.time:.2f}  ")
            imgui.same_line()
            imgui.text(f"   {self.fps:.1f} fps  ")
            imgui.same_line()
            imgui.text(f"  {Callbacks.resolution[0]} x {Callbacks.resolution[1]}  ")
            imgui.same_line()
            if imgui.button('[]'):
                if glfw.get_window_attrib(self.window, glfw.MAXIMIZED):
                    glfw.restore_window(self.window)
                else:
                    glfw.maximize_window(self.window)


    def render(self):

        imgui.create_context()

        with self.create_main_window() as window:

            if self.window == None:
                raise Exception("Janela não foi criada")
            
            impl = GlfwRenderer(window)

            # Versões de Mac não suportam debug
            if platform.system().lower() != 'darwin':
                # Exibe mensagens de Debug
                glEnable(GL_DEBUG_OUTPUT)
                glDebugMessageCallback(GLDEBUGPROC(Callbacks.debug_message_callback), None)

            # inicializa a posição do cursor
            Callbacks.cursor_position = glfw.get_cursor_pos(self.window)

            # Define o callback para caso a janela seja redimensionada, teclas pressionadas ou movimento do mouse
            glfw.set_key_callback(self.window, Callbacks.key_callback)
            glfw.set_cursor_pos_callback(self.window, Callbacks.cursor_pos_callback)
            glfw.set_scroll_callback(self.window, Callbacks.scroll_callback)
            glfw.set_mouse_button_callback(self.window, Callbacks.mouse_button_callback)


            if self.mode is None:
                self.add_geometry(GL_TRIANGLE_STRIP, vertices, colors=colors, uvs=uvs, create_normals=True)

            vao, count  = self.parse_geometry()
            self.parse_textures()

            self.vertex_shader_source = str(self.vertex_shader_source)

            # Configura os Uniforms para os shaders
            uniforms = {}

            # Caso os parâmetros do Shader Toy estejam habilidatos
            if self.shader_toy:
                # Adiciona os parâmetros automaticamente do Shader Toy
                shadertoy_vertex = "#version 330 core\n"
                self.vertex_shader_source = shadertoy_vertex + self.vertex_shader_source

                Renderizador.shadertoy_frag = f"#define HW_PERFORMANCE {0 if self.shader_toy_mIsLowEnd else 1}\n"
                Renderizador.shadertoy_frag += "uniform vec2 iResolution;"+ \
                                               "uniform float iTime;"+ \
                                               "uniform float iTimeDelta;"+ \
                                               "uniform float iFrameRate;"+ \
                                               "uniform uint iFrame;"+ \
                                               "uniform vec4 iMouse;\n"
                                            #    "uniform float iChannelTime[4];"
                                            #    "uniform vec4 iDate;"
                                            #    "uniform float iSampleRate;"
                                            #    "uniform vec3 iChannelResolution[4];"
            
                def mainImage(match):
                    signature = str(match.group())
                    signature = re.search(r'\((.*?)\)',signature).group(1)
                    result = [x.strip() for x in signature.split(',')]
                    
                    for r in result:
                        txt = r.split()
                        if txt[0] == "out":
                            Renderizador.shadertoy_frag += f"out vec4 {txt[2]};\n"
                        elif txt[0] == "in":
                            Renderizador.shadertoy_frag += f"in vec4 gl_FragCoord;vec2 {txt[2]} = gl_FragCoord.xy;\n"
                    return "void main(){\n"
            
                self.fragment_shader_source = re.sub("void\s*mainImage\(([^\)]+)\)\s*\{", mainImage, self.fragment_shader_source)
                self.fragment_shader_source = "#version 330 core\n" + Renderizador.shadertoy_frag + self.fragment_shader_source
                       

            # Compila os shaders
            vertexShader_id = compile_shader(GL_VERTEX_SHADER, self.vertex_shader_source)
            fragmentShader_id = compile_shader(GL_FRAGMENT_SHADER, self.fragment_shader_source)

            # Conecta (link) os shaders para a aplicação
            program_id = link_shader(vertexShader_id, fragmentShader_id)


            # recursos usados para tratar valores gerais
            frame = 0
            time_delta = 0
            passed_time = 0
            count_second = 0
            count_frames = 0

            # Caso os parâmetros do Shader Toy estejam habilidatos
            if self.shader_toy:

                # Cadastra os Uniforms básicos do ShaderToy
                uniforms["iResolution"] = glGetUniformLocation(program_id, 'iResolution')
                uniforms["iTime"] = glGetUniformLocation(program_id, 'iTime')
                uniforms["iTimeDelta"] = glGetUniformLocation(program_id, 'iTimeDelta')
                uniforms["iFrameRate"] = glGetUniformLocation(program_id, 'iFrameRate')
                uniforms["iFrame"] = glGetUniformLocation(program_id, 'iFrame')
                uniforms["iMouse"] = glGetUniformLocation(program_id, 'iMouse')

            if self.textures:
                uniforms["texture_size"] = glGetUniformLocation(program_id, 'texture_size')

            # Cadastra os Uniforms
            for field in self.uniforms_source:
                uniforms[field] = glGetUniformLocation(program_id, field)    

            # remove os shaders da memória
            glDeleteShader(vertexShader_id)
            glDeleteShader(fragmentShader_id)

            # Define no contexto qual a cor para limpar o buffer de cores
            glClearColor(*self.background_color)

            # Passa para o Callbacks o real tamanho do Framebuffer
            width, height = glfw.get_framebuffer_size(window)
            Callbacks.framebuffer_size = [width, height]

            # desativa a apresentação do cursor
            if self.lock_mouse:
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

            # Ativa o Z-Buffer
            glEnable(GL_DEPTH_TEST)

            # Call back do resize do Framebuffer precisa ser configurado no final do processo de iniciação
            glfw.set_framebuffer_size_callback(self.window, Callbacks.framebuffer_size_callback)

            #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            # Realiza a renderização enquanto a janela não for fechada
            while (
                glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
                not glfw.window_should_close(self.window)
            ):

                # Captura e processa eventos da janela
                glfw.poll_events()

                # Processa os eventos da interface da janela
                impl.process_inputs()

                imgui.new_frame()


                # Detalhes da interface da janela
                self.gui_interface()
                
                # Limpa a janela com a cor de fundo e apagar o z-buffer
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # use our own rendering program
                glUseProgram(program_id)

                if self.play:
                    self.time = glfw.get_time()  # returna o tempo passado desde que a aplicação começou
                else:
                    glfw.set_time(self.time)

                time_delta = self.time - passed_time
                passed_time = self.time
                if passed_time - count_second > 1.0:
                    self.fps = count_frames / (passed_time - count_second)
                    count_second = passed_time
                    count_frames = 0
                else:        
                    count_frames += 1 

                # Fazendo os uniforms básicos do ShaderToy
                if self.shader_toy:    
                    glUniform2f(uniforms["iResolution"], Callbacks.framebuffer_size[0], Callbacks.framebuffer_size[1])
                    glUniform1f(uniforms["iTime"], passed_time)
                    glUniform1f(uniforms["iTimeDelta"], time_delta)
                    glUniform1f(uniforms["iFrameRate"], self.fps)
                    glUniform1ui(uniforms["iFrame"], frame)
                    glUniform4fv(uniforms["iMouse"], 1, Callbacks.get_mouse_clicked())

                # Case existam texturas
                for texture in self.textures:
                    # Liga a textura para o OpenGL
                    glActiveTexture(GL_TEXTURE0 + texture.id)
                    glBindTexture(GL_TEXTURE_2D, texture.texture_id)

                    # Tamanho da textura (se for usar)
                    glUniform2f(uniforms["texture_size"], texture.image.shape[1], texture.image.shape[0])

                # Passa todos os uniforms para os shaders
                parse_uniforms(self.uniforms_source, uniforms)

                # Ativa (bind) VAO
                glBindVertexArray(vao)

                # Desenha os vértices como triângulos
                glDrawArrays(self.mode, 0, self.count)
                
                # Desativa (unbind) o VAO
                glBindVertexArray(0)

                # Detecta e armazena as chamadas de teclado
                keyPressed = np.where(Callbacks.keyArray == True)
                for key in keyPressed[0]:
                    Callbacks.camera.send_keys(key)

                # Aumenta em um no contador de frames
                frame += 1

                imgui.render()
                impl.render(imgui.get_draw_data())

                # Faz a troca dos framebuffer (swap frame buffer)
                glfw.swap_buffers(self.window)

                time.sleep(0.01)



            # Limpa o VAO 
            glDeleteVertexArrays(1, [vao])

            # Limpa o VBO
            # vbo.delete()
    
            impl.shutdown()

            # finaliza o glfw
            glfw.terminate()
