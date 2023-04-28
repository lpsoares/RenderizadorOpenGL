#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

import numpy as np

from renderizador.utils import *

#### FAZER Shear  ####

#########

#######



def translate(*args):

    result = np.identity(4, dtype=np.float32)
    result[0, 3] = args[0]
    result[1, 3] = args[1]
    result[2, 3] = args[2]

    return result


def rotate(axis, angle):

    axis = normalize(axis)

    mat3 = np.cos(angle) * np.identity(3, dtype=np.float32) + np.sin(angle) * cross_product(axis) + \
           (1 - np.cos(angle)) * np.outer(axis, axis)

    result = np.zeros((4, 4), np.float32)
    result[:3, :3] = mat3
    result[3, 3] = 1.0

    return result


def scale(*args):
    
    result = np.zeros((4, 4), np.float32)
    result[0, 0] = args[0]
    result[1, 1] = args[1]
    result[2, 2] = args[2]
    result[3, 3] = 1.0

    return result
