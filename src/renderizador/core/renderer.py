#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Core renderer for OpenGL.
"""

import numpy as np
from OpenGL.GL import *
import glfw
import time
import re

from renderizador.core.window import create_window
#from renderizador.core.gui import create_gui_interface
#from renderizador.graphics.geometry import parse_geometry
from renderizador.graphics.shaders import compile_shader, link_shader, default_vertex_shader, default_fragment_shader
from renderizador.graphics.texture import Texture
#from renderizador.utils import uniforms
from renderizador.utils.callbacks import Callbacks
from renderizador.utils.uniforms import parse_uniforms
from renderizador.audio.audio import Audio
from renderizador.audio.fft_processor import process_audio_fft

# Usado para checar a plataforma Mac e saber se compatível com chamadas de OpenGL
#import platform

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
    """Main renderer class that coordinates the rendering pipeline."""

    # Define a cor de fundo da renderização
    def set_title(self, text):
        self.title = text

    # Define a cor de fundo da renderização
    def set_background_color(self, color):
        self.background_color = color

    # Cria a janela de renderização
    def __init__(self, resolution=(1024, 768), lock_mouse=False):
        self.window = None
 
        Callbacks.resolution = resolution

        # Faz o mouse não aparecer e ficar preso no meio da tela
        self.lock_mouse = lock_mouse

        # Cor padrão para o fundo da janela (para apagar o buffer de cores)
        self.background_color = (0.0, 0.0, 0.0, 1.0)

        # Título padrão da janela de renderização
        self.title = "Computação Gráfica"
       
        # Armazena as texturas
        self.textures = []

        # Armazena os audios
        self.audios = []

        self.data = []
        self.mode = None
        self.count = 0

        self.vertex_shader_source = default_vertex_shader
        self.fragment_shader_source = default_fragment_shader
        self.uniforms_source = {}

        self.play = True
        self.time = 0
        self.fps = 0

        # audio control state
        self._audio_initialized = False
        self._prev_play_state = None
        self.mute = False

        # ShaderToy flags
        self.shader_toy = True
        self.shader_toy_mIsLowEnd = True  # Muda o parâmetro para HW_PERFORMANCE
        
        # Parâmetros de visualização de áudio (ajustáveis)
        self.audio_db_min = -100.0  # piso em dB
        self.audio_db_max = 40.0  # topo em dB
        self.audio_decay_tau = 0.20  # constante de tempo do decaimento (s)
        self.audio_gain = 1.0       # ganho linear antes do log/dB
        
        # Camera management
        self.camera = None

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

    def set_texture(self, filename, channel, filter=GL_LINEAR, wrap=GL_REPEAT, vflip=True):
        self.textures.append(Texture(filename, channel, filter=filter, wrap=wrap, vflip=vflip))

    def set_audio(self, filename, channel):
        self.audios.append(Audio(filename, channel))
        
    def set_camera(self, camera):
        """
        Set the camera for the renderer and connect it to the callback system.
        
        Args:
            camera: A Camera object to use for rendering
        """
        self.camera = camera
        Callbacks.camera = camera
        
    def add_geometry(self, mode, vertices, normals=None, colors=None, uvs=None, create_normals=False, index=None):
        from renderizador.graphics.geometry import create_geometry_data
        self.data, self.mode, self.count = create_geometry_data(
            mode, vertices, normals, colors, uvs, create_normals, index
        )

    def _stop_audio_streams(self):
        for audio in self.audios:
            stream = getattr(audio, '_sd_stream', None)
            if stream is not None:
                try:
                    stream.stop()
                    stream.close()
                except Exception:
                    pass

    def _pause_audio_streams(self):
        """Pause streams but preserve audio._pos so resume continues where left off."""
        if not self._audio_initialized:
            return
        for audio in self.audios:
            stream = getattr(audio, '_sd_stream', None)
            if stream is not None and getattr(audio, '_sd_stream_active', False):
                try:
                    stream.stop()
                except Exception:
                    pass
                audio._sd_stream_active = False

    def _resume_audio_streams(self):
        """Resume previously created streams. Streams must have been created by _init_audio_streams()."""
        if not self._audio_initialized:
            return
        for audio in self.audios:
            stream = getattr(audio, '_sd_stream', None)
            if stream is not None and not getattr(audio, '_sd_stream_active', False):
                try:
                    stream.start()
                    audio._sd_stream_active = True
                except Exception:
                    # se start falhar, ignore para não quebrar render loop
                    audio._sd_stream_active = False

    def _reset_audio_streams(self):
        """Reset audio position to start (0) and pause streams."""
        if not self._audio_initialized:
            return
        for audio in self.audios:
            with audio._pos_lock:
                audio._pos = 0

    def _set_audio_volume(self, volume=None):
        """Set volume for all audio streams. If volume is None, use self.mute state."""
        if not self._audio_initialized:
            return
        if volume is None:
            volume = 0.0 if self.mute else 1.0
        volume = float(max(0.0, min(1.0, volume)))
        for audio in self.audios:
            # aplicar no callback (stream não tem .volume)
            setattr(audio, "_volume", volume)

    def render(self):
        """Main rendering loop."""
        import imgui
        from renderizador.core.window import configure_window
        from renderizador.core.gui import init_imgui
        from renderizador.graphics.texture import parse_textures
        from renderizador.audio.audio import init_audio_streams, parse_audios
        from renderizador.graphics.geometry import parse_geometry

        imgui.create_context()

        with create_window(self) as window:
            if self.window is None:
                raise Exception("Janela não foi criada")
            
            impl = init_imgui(window)
            configure_window(self, window)

            if self.mode is None:
                self.add_geometry(GL_TRIANGLE_STRIP, vertices, colors=colors, uvs=uvs, create_normals=True)

            vao, count = parse_geometry(self.data, self.mode, self.count)
            parse_textures(self.textures)
            parse_audios(self.audios)

            init_audio_streams(self)

            self.vertex_shader_source = str(self.vertex_shader_source)

            # Configura os Uniforms para os shaders
            uniforms = {}

            # Caso os parâmetros do Shader Toy estejam habilidatos
            if self.shader_toy:
                # Adiciona os parâmetros automaticamente do Shader Toy
                shadertoy_frag = f"#define HW_PERFORMANCE {0 if self.shader_toy_mIsLowEnd else 1}\n"
                shadertoy_uniforms = "uniform vec2 iResolution;"+ \
                                    "uniform float iTime;"+ \
                                    "uniform float iTimeDelta;"+ \
                                    "uniform float iFrameRate;"+ \
                                    "uniform uint iFrame;"+ \
                                    "uniform vec4 iMouse;"+ \
                                    "uniform vec4 iDate;"+ \
                                    "uniform sampler2D iChannel0;" + \
                                    "uniform sampler2D iChannel1;" + \
                                    "uniform sampler2D iChannel2;" + \
                                    "uniform sampler2D iChannel3;" + \
                                    "uniform vec2 iChannelResolution[4];\n"  # (x=width,y=height)

                shadertoy_frag += shadertoy_uniforms

                # Define a nonlocal reference to shadertoy_frag that can be modified inside the function
                nonlocal_shadertoy_frag = [shadertoy_frag]
                
                def mainImage(match):
                    signature = str(match.group())
                    signature = re.search(r'\((.*?)\)',signature).group(1)
                    result = [x.strip() for x in signature.split(',')]
                    
                    for r in result:
                        txt = r.split()
                        if txt[0] == "out":
                            nonlocal_shadertoy_frag[0] += f"out vec4 {txt[2]};\n"
                        elif txt[0] == "in":
                            nonlocal_shadertoy_frag[0] += f"in vec4 gl_FragCoord;vec2 {txt[2]} = gl_FragCoord.xy;\n"
                    return "void main(){\n"
            
                self.fragment_shader_source = re.sub("void\s*mainImage\(([^\)]+)\)\s*\{", mainImage, self.fragment_shader_source)
                self.fragment_shader_source = nonlocal_shadertoy_frag[0] + self.fragment_shader_source

            self.vertex_shader_source = "#version 330 core\n" + self.vertex_shader_source
            self.fragment_shader_source = "#version 330 core\n" + self.fragment_shader_source

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
                uniforms["iDate"] = glGetUniformLocation(program_id, 'iDate')
                uniforms["iChannel0"] = glGetUniformLocation(program_id, 'iChannel0')
                uniforms["iChannel1"] = glGetUniformLocation(program_id, 'iChannel1')
                uniforms["iChannel2"] = glGetUniformLocation(program_id, 'iChannel2')
                uniforms["iChannel3"] = glGetUniformLocation(program_id, 'iChannel3')

                uniforms["iChannelResolution"] = [
                    glGetUniformLocation(program_id, f'iChannelResolution[{i}]') for i in range(4)
                ]
                uniforms["iChannelTime"] = [
                    glGetUniformLocation(program_id, f'iChannelTime{i}') for i in range(4)
                ]  # iChannelTime0, 1, 2, 3 = tempo do áudio em segundos
                
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
                from renderizador.core.gui import gui_interface
                gui_interface(self)
                
                # Limpa a janela com a cor de fundo e apagar o z-buffer
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # use our own rendering program
                glUseProgram(program_id)

                # controla play/pause do render e do áudio
                if self.play:
                    self.time = glfw.get_time()  # returna o tempo passado desde que a aplicação começou
                else:
                    glfw.set_time(self.time)

                # detectar mudança de estado do play para pausar/resumir áudio
                if self._prev_play_state is None:
                    # primeira frame: iniciar áudio se play=True
                    self._prev_play_state = self.play
                    if self.play:
                        self._resume_audio_streams()
                elif self._prev_play_state != self.play:
                    # transição detectada
                    if self.play:
                        # resume áudio
                        self._resume_audio_streams()
                    else:
                        # pause áudio
                        self._pause_audio_streams()
                    self._prev_play_state = self.play

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

                    # pass date as (year, month, day, seconds in day)
                    ts = time.time()  # epoch com fração
                    lt = time.localtime(ts)
                    seconds_in_day = lt.tm_hour * 3600 + lt.tm_min * 60 + lt.tm_sec + (ts % 1.0)
                    glUniform4f(uniforms["iDate"], float(lt.tm_year), float(lt.tm_mon - 1), float(lt.tm_mday), float(seconds_in_day))

                # Case existam texturas
                for texture in self.textures:
                    # Liga a textura para o OpenGL
                    glActiveTexture(GL_TEXTURE0 + texture.channel)
                    glBindTexture(GL_TEXTURE_2D, texture.texture_id)

                    # Se for shaderToy, faça o binding do sampler iChannelN -> texture unit N
                    if self.shader_toy:
                        glUniform2f(uniforms["iChannelResolution"][texture.channel], texture.image.shape[1], texture.image.shape[0])
                        sampler_name = f"iChannel{texture.channel}"
                        if sampler_name in uniforms and uniforms[sampler_name] != -1:
                            # define qual texture unit o sampler deve usar
                            glUniform1i(uniforms[sampler_name], int(texture.channel))
                
                # Atualiza texturas de audio (FFT)
                for audio in self.audios:
                    # Process FFT if available
                    if getattr(audio, '_fft_tex', None) is not None:
                        process_audio_fft(audio, time_delta, self.audio_db_min, self.audio_db_max, 
                                          self.audio_decay_tau, self.audio_gain)
                        
                        #bind audio FFT texture to texture unit and set sampler uniform (iChannelN)
                        glActiveTexture(GL_TEXTURE0 + audio.channel)
                        glBindTexture(GL_TEXTURE_2D, audio._fft_tex)
                    if self.shader_toy:
                        glUniform2f(uniforms["iChannelResolution"][audio.channel], 512, 2)  # FFT texture size
                        glUniform1f(uniforms["iChannelTime"][audio.channel], float(passed_time))  # Passed time for audio channel
                        sampler_name = f"iChannel{audio.channel}"
                        if sampler_name in uniforms and uniforms[sampler_name] != -1:
                            glUniform1i(uniforms[sampler_name], int(audio.channel))

                    #pass audio position/time uniform if present
                    pos_uniform = f"iChannelTime{audio.channel}"
                    if pos_uniform in uniforms and uniforms[pos_uniform] != -1:
                        # pass normalized time in seconds - safely read position with lock
                        with audio._pos_lock:
                            current_pos = float(audio._pos)
                        glUniform1f(uniforms[pos_uniform], current_pos / float(audio.sf))

                # Passa todos os uniforms para os shaders
                parse_uniforms(self.uniforms_source, uniforms)

                # Ativa (bind) VAO
                glBindVertexArray(vao)

                # Desenha os vértices como triângulos
                glDrawArrays(self.mode, 0, self.count)
                
                # Desativa (unbind) o VAO
                glBindVertexArray(0)

                # Detecta e armazena as chamadas de teclado
                if Callbacks.camera is not None:
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

            self._stop_audio_streams()

            impl.shutdown()

            # finaliza o glfw
            glfw.terminate()
