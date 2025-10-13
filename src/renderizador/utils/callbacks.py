#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Callbacks for window events.
"""

from datetime import datetime
import numpy as np
from OpenGL.GL import *
import glfw

# Classe para tratar Callbacks
class Callbacks:

    # Variáveis de estado
    resolution = (1024, 768)
    framebuffer_size = [1024, 768]
    keyArray = np.array([False] * 500)
    cursor_position = (0.0, 0.0)
    last_cursor_position = (0.0, 0.0)
    scroll_offset = (0.0, 0.0)
    mouse = np.array([0.0, 0.0, 0.0, 0.0], np.float32)
    camera = None
    mouse_callback = None
    mouse_dragging = False

    @staticmethod
    def error_callback(error, description):
        print('Error: %s\nDescription: %s' % (error, description))

    @staticmethod
    def debug_message_callback(source, type_, id_, severity, length, message, userParam):
        if severity == GL_DEBUG_SEVERITY_HIGH or \
           severity == GL_DEBUG_SEVERITY_MEDIUM:
            # Aqui pode receber mensagens com origem, tipo, e severidade
            #print("Mensagem OpenGL:", message)
            pass

    @staticmethod
    def key_callback(window, key, scancode, action, mode):
        # ESC para fechar a janela
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        # Quando a tecla é pressionada, armazena na lista
        if action == glfw.PRESS:
            Callbacks.keyArray[key] = True
        
        # Quando a tecla é solta, desativa da lista
        if action == glfw.RELEASE:
            Callbacks.keyArray[key] = False
        
    @staticmethod
    def cursor_pos_callback(window, xpos, ypos):
        # Calcular o deslocamento do mouse desde a última posição
        dx = xpos - Callbacks.last_cursor_position[0]
        dy = ypos - Callbacks.last_cursor_position[1]
        
        # Armazena a posicao atual e atualiza a última posição
        Callbacks.last_cursor_position = (xpos, ypos)
        Callbacks.cursor_position = (xpos, ypos)

        # Atualiza o mouse para o ShaderToy
        Callbacks.mouse[0] = xpos
        Callbacks.mouse[1] = Callbacks.resolution[1] - ypos
        
        # Se estiver arrastando e tiver uma câmera, enviar o movimento para a câmera
        if Callbacks.mouse_dragging and Callbacks.camera is not None:
            Callbacks.camera.send_mouse((dx, dy))
        
        # call the user callback, if set
        if Callbacks.mouse_callback is not None:
            Callbacks.mouse_callback(xpos, ypos)
    
    @staticmethod
    def scroll_callback(window, xoffset, yoffset):
        Callbacks.scroll_offset = (xoffset, yoffset)
        # Se tiver uma câmera, enviar o scroll para zoom
        if Callbacks.camera is not None:
            Callbacks.camera.send_scroll((xoffset, yoffset))
    
    @staticmethod
    def mouse_button_callback(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                # Mouse pressionado
                Callbacks.mouse[2] = Callbacks.mouse[0]
                Callbacks.mouse[3] = Callbacks.mouse[1]
                Callbacks.mouse_dragging = True
                # Captura a posição atual para cálculo de delta de movimento
                Callbacks.last_cursor_position = Callbacks.cursor_position
            elif action == glfw.RELEASE:
                # Mouse solto
                Callbacks.mouse[2] = -Callbacks.mouse[2]
                Callbacks.mouse[3] = -Callbacks.mouse[3]
                Callbacks.mouse_dragging = False
        if button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.PRESS:
                # Mouse pressionado - começar a capturar movimento para câmera
                Callbacks.mouse_dragging = True
                Callbacks.last_cursor_position = Callbacks.cursor_position
            elif action == glfw.RELEASE:
                # Mouse solto - parar de capturar movimento
                Callbacks.mouse_dragging = False
        if button == glfw.MOUSE_BUTTON_MIDDLE:
            if action == glfw.PRESS:
                # Mouse pressionado
                pass
            elif action == glfw.RELEASE:
                # Mouse solto
                pass

    @staticmethod
    def framebuffer_size_callback(window, width, height):
        # Ajusta o tamanho do ViewPort
        glViewport(0, 0, width, height)
        # Guarda a nova resolucao
        Callbacks.resolution = (width, height)
        Callbacks.framebuffer_size = [width, height]
    
    @staticmethod
    def get_mouse_clicked():
        return Callbacks.mouse