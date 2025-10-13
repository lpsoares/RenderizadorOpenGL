#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025

Módulo de utilitários contendo funções auxiliares, transformações, callbacks e uniforms.
"""

from renderizador.utils.callbacks import Callbacks
from renderizador.utils.uniforms import parse_uniforms
from renderizador.utils.transformations import translate, rotate, scale, normalize

__all__ = [
    'Callbacks',
    'parse_uniforms',
    'get_pointer',
    'translate',
    'rotate',
    'scale',
    'normalize'
]

def get_pointer(data):
    """
    Get a pointer to data for use with OpenGL.
    
    Args:
        data: NumPy array or other data
        
    Returns:
        Pointer to data
    """
    import ctypes
    return data if data is None else data.ctypes.data_as(ctypes.c_void_p)