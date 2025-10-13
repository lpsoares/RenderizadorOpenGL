#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025

Módulo principal do renderizador.
"""

from renderizador.core.renderer import Renderizador
from renderizador.graphics.shaders import default_vertex_shader, default_fragment_shader
from renderizador.graphics.camera import Camera
from renderizador.utils.transformations import translate, rotate, scale

__all__ = [
    'Renderizador',
    'default_vertex_shader',
    'default_fragment_shader',
    'Camera',
    'translate',
    'rotate',
    'scale'
]
