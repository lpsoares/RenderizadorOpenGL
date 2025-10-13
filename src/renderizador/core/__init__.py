#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Core module containing main renderer and window management.
"""

from renderizador.core.renderer import Renderizador
from renderizador.core.window import create_window, configure_window
from renderizador.core.gui import create_gui_interface, gui_interface, init_imgui

__all__ = [
    'Renderizador',
    'create_window',
    'configure_window',
    'create_gui_interface',
    'gui_interface',
    'init_imgui'
]
