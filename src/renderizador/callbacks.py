#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

from datetime import datetime
import numpy as np
from OpenGL.GL import *
import glfw



# Classe para tratar Callbacks
class Callbacks:

    # Posição do cursor incial (deve ser atualizada na criação da tela)
    cursor_position = (0, 0)

    # stores which keys are pressed and handle key press in the main loop
    keyArray = np.array([False] * 300, bool)

    # Os callbacks usam muito a Camera, então deixei uma ligação aqui
    camera = None

    # Tamanho padrão de resolução da tela
    resolution = (1024, 768)

    # Para eventos de movimento do mouse
    def cursor_pos_callback(window, xpos, ypos):
        offset = [xpos - Callbacks.cursor_pos[0],
                  ypos - Callbacks.cursor_pos[1]]
        Callbacks.camera.send_mouse(offset)
        Callbacks.cursor_pos = (xpos, ypos)


    # Para eventos do Scroll do mouse
    def scroll_callback(window, xoffset, yoffset):
        Callbacks.camera.send_scroll([xoffset, yoffset])


    # Caso as dimensões da janela principal sejam alteradas 
    def framebuffer_size_callback(window, width, height):
        Callbacks.window_size = (width, height)
        glViewport(0, 0, width, height)


    # Para eventos de teclado
    def key_callback(window, key, scanCode, action, mods):
        
        if key == glfw.KEY_UNKNOWN:
            return

        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True) # Fecha a janela
            else:
                Callbacks.keyArray[key] = True
        elif action == glfw.RELEASE:
            Callbacks.keyArray[key] = False


    # Usado para exibir mensagens do OpenGL
    def debug_message_callback(source, msg_type, msg_id, severity, length, raw, user):
        message = raw[0:length]
        print('debug message:', source, msg_type, msg_id, severity, message)



