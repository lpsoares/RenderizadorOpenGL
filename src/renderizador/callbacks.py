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
    cursor_position = [0, 0]

    # stores which keys are pressed and handle key press in the main loop
    keyArray = np.array([False] * 640, bool)

    # Os callbacks usam muito a Camera, então deixei uma ligação aqui
    camera = None

    # Tamanho padrão de resolução da tela
    resolution = [1024, 768]
    framebuffer_size = [1024, 768]

    # Se mouse foi clicado
    mouse_clicked = False
    mouse_pressed = False
    mouse_pos_clicked = [0, 0]
    mouse_pos_down = [0, 0]

    # Para eventos de movimento do mouse
    def cursor_pos_callback(window, xpos, ypos):
        ypos = Callbacks.framebuffer_size[1] - ypos
        offset = [xpos - Callbacks.cursor_position[0],
                  ypos - Callbacks.cursor_position[1]]
        Callbacks.camera.send_mouse(offset)
        Callbacks.cursor_position = [xpos, ypos]


    # Para eventos do Scroll do mouse
    def scroll_callback(window, xoffset, yoffset):
        Callbacks.camera.send_scroll([xoffset, yoffset])


    # Caso as dimensões da janela principal sejam alteradas 
    def framebuffer_size_callback(window, width, height):
        
        Callbacks.window_size = [width, height]
        glViewport(0, 0, width, height)

        width, height = glfw.get_framebuffer_size(window)
        Callbacks.framebuffer_size = [width, height]
        


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

    def get_mouse_clicked():

        width = Callbacks.framebuffer_size[0]
        height = Callbacks.framebuffer_size[1]

        mag = width/Callbacks.resolution[0]

        if Callbacks.mouse_pressed:
            Callbacks.mouse_pos_down = Callbacks.cursor_position
        
        pos_clicked = np.array(Callbacks.mouse_pos_clicked)
        pos_clicked *= int(mag)
        #pos_clicked[1] = height - pos_clicked[1]
        pos_clicked[0] = max(0, min(pos_clicked[0], width))
        pos_clicked[1] = max(0, min(pos_clicked[1], height))

        pos_down = np.array(Callbacks.mouse_pos_down)
        pos_down *= int(mag)
        #pos_down[1] = height - pos_down[1]
        pos_down[0] = max(0, min(pos_down[0], width))
        pos_down[1] = max(0, min(pos_down[1], height))

        if Callbacks.mouse_clicked:
            Callbacks.mouse_clicked = False
        else:
            pos_clicked[1] = -pos_clicked[1]

        if not Callbacks.mouse_pressed:
            pos_clicked[0] = -pos_clicked[0]

        
        return [pos_down[0], pos_down[1], pos_clicked[0], pos_clicked[1]]

    def mouse_button_callback(window, button, action, mods):
        # if button == glfw.MOUSE_BUTTON_RIGHT:
        #     print("MOUSE_BUTTON_RIGHT")
        if action == glfw.PRESS:
            Callbacks.mouse_clicked = True
            Callbacks.mouse_pressed = True
            Callbacks.mouse_pos_clicked = Callbacks.cursor_position
            Callbacks.mouse_pos_down = Callbacks.cursor_position

        elif action == glfw.RELEASE:
            Callbacks.mouse_clicked = False
            Callbacks.mouse_pressed = False
            
        # if mods == glfw.MOD_NUM_LOCK:
        #     print("Mouse com MOD_NUM_LOCK")
        
        


    # Usado para exibir mensagens do OpenGL
    def debug_message_callback(source, msg_type, msg_id, severity, length, raw, user):
        message = raw[0:length]
        print('debug message:', source, msg_type, msg_id, severity, message)



