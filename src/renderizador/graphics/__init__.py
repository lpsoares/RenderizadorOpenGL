#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 12 de Outubro de 2025

Módulo de gráficos contendo geometria, shaders, manipulação de texturas e câmera.
"""

from renderizador.graphics.geometry import create_geometry_data, parse_geometry
from renderizador.graphics.shaders import compile_shader, link_shader, default_vertex_shader, default_fragment_shader
from renderizador.graphics.texture import Texture, parse_textures
from renderizador.graphics.camera import Camera

__all__ = [
    'create_geometry_data',
    'parse_geometry',
    'compile_shader',
    'link_shader',
    'default_vertex_shader',
    'default_fragment_shader',
    'Texture',
    'parse_textures',
    'Camera'
]