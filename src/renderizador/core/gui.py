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
        if imgui.button('[]'):
            if glfw.get_window_attrib(renderer.window, glfw.MAXIMIZED):
                glfw.restore_window(renderer.window)
            else:
                glfw.maximize_window(renderer.window)

        # Controles de áudio (ShaderToy-like)
        if imgui.tree_node("Audio\n(Shadertoy-like)"):
            changed_min, new_min = imgui.slider_float("dB min", renderer.audio_db_min, -120.0, -20.0, '%.1f dB')
            changed_max, new_max = imgui.slider_float("dB max", renderer.audio_db_max, -40.0, 0.0, '%.1f dB')
            changed_tau, new_tau = imgui.slider_float("decay tau", renderer.audio_decay_tau, 0.03, 1.0, '%.2f s')
            changed_gain, new_gain = imgui.slider_float("gain", renderer.audio_gain, 0.1, 8.0, '%.2f x')
            if changed_min:
                renderer.audio_db_min = float(new_min)
            if changed_max:
                # manter coerência: max > min
                renderer.audio_db_max = float(max(new_max, renderer.audio_db_min + 1.0))
            if changed_tau:
                renderer.audio_decay_tau = float(new_tau)
            if changed_gain:
                renderer.audio_gain = float(new_gain)
            imgui.tree_pop()

def gui_interface(renderer):
    """Wrapper function for the GUI interface."""
    create_gui_interface(renderer)
