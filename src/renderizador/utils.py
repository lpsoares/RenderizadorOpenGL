#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

import numpy as np
import ctypes

def normalize(vector):
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        raise Exception("Magntude do vetor == 0")
    return vector/magnitude


def cross_product(axis):
    return np.asarray(
        (
            (0, -axis[2], axis[1]),
            (axis[2], 0, -axis[0]),
            (-axis[1], axis[0], 0)
         ),
        np.float32
    )

# Função usada para recuperar o ponteiro dos dados
def get_pointer(data):
    return data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
