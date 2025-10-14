#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
GUI interface using ImGui.
"""

import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
from renderizador.utils.callbacks import Callbacks

def init_imgui(window):
    """Initialize ImGui context and integration with GLFW."""
    impl = GlfwRenderer(window)
    return impl


def create_gui_interface(renderer):
    """Create the GUI interface for the application."""
    viewport = imgui.get_main_viewport()
    imgui.set_next_window_position(viewport.pos.x+10, viewport.pos.y + viewport.size.y - 40)
    imgui.set_next_window_size(0, 0)  # Zero calcula de forma automática
    flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_SAVED_SETTINGS
    
    with imgui.begin("shadertoy", flags=flags):
        if imgui.arrow_button("Back", imgui.DIRECTION_LEFT):
            renderer.time = 0.0
            glfw.set_time(renderer.time)
            renderer._reset_audio_streams()
        imgui.same_line()
        if renderer.play:
            if imgui.button('||'):
                renderer.play = False
        else:
            if imgui.arrow_button("Play", imgui.DIRECTION_RIGHT):
                renderer.play = True
        imgui.same_line()
        imgui.text(f"   {renderer.time:.2f}  ")
        imgui.same_line()
        imgui.text(f"   {renderer.fps:.1f} fps  ")
        imgui.same_line()
        imgui.text(f"  {Callbacks.resolution[0]} x {Callbacks.resolution[1]}  ")
        imgui.same_line()
        label = "X" if renderer.mute else "M"
        if imgui.button(label):
            renderer.mute = not renderer.mute
            renderer._set_audio_volume(0.0 if renderer.mute else 1.0)

        imgui.same_line()
        if imgui.button('[]'):
            if glfw.get_window_attrib(renderer.window, glfw.MAXIMIZED):
                glfw.restore_window(renderer.window)
            else:
                glfw.maximize_window(renderer.window)


def gui_interface(renderer):
    """Wrapper function for the GUI interface."""
    create_gui_interface(renderer)
