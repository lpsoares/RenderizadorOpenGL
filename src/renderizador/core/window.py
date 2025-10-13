#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Window management using GLFW.
"""

import contextlib
import glfw
from OpenGL.GL import *
import platform
from renderizador.utils.callbacks import Callbacks

@contextlib.contextmanager
def create_window(renderer):
    """Create and configure a GLFW window for the renderer."""
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

        renderer.window = glfw.create_window(Callbacks.resolution[0], Callbacks.resolution[1], 
                                           renderer.title, None, None)

        if not renderer.window:
            glfw.terminate()
            raise Exception("Não foi possível criar a janela glfw")
        glfw.make_context_current(renderer.window)

        yield renderer.window

    finally:
        glfw.terminate()

def configure_window(renderer, window):
    """Configure window callbacks and settings."""
    # Versões de Mac não suportam debug
    if platform.system().lower() != 'darwin':
        # Exibe mensagens de Debug
        glEnable(GL_DEBUG_OUTPUT)
        glDebugMessageCallback(GLDEBUGPROC(Callbacks.debug_message_callback), None)

    # inicializa a posição do cursor
    cursor_pos = glfw.get_cursor_pos(renderer.window)
    Callbacks.cursor_position = cursor_pos
    Callbacks.last_cursor_position = cursor_pos

    # Define o callback para caso a janela seja redimensionada, teclas pressionadas ou movimento do mouse
    glfw.set_key_callback(renderer.window, Callbacks.key_callback)
    glfw.set_cursor_pos_callback(renderer.window, Callbacks.cursor_pos_callback)
    glfw.set_scroll_callback(renderer.window, Callbacks.scroll_callback)
    glfw.set_mouse_button_callback(renderer.window, Callbacks.mouse_button_callback)
