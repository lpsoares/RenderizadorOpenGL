#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Uniform parsing for shaders.
"""

import numpy as np
from OpenGL.GL import *
import numbers

from renderizador.utils.utils import get_pointer

def parse_uniforms(uniforms_source, uniforms):
    """
    Parse and set uniform values for the shader program.
    
    Args:
        uniforms_source: Dictionary of uniform names and values
        uniforms: Dictionary of uniform locations
    """
    for field, value in uniforms_source.items():
        if callable(value):
            value = value()

        if isinstance(value, (list, np.ndarray)):
            shape = np.asarray(value).shape
            if shape == (2, 2):
                glUniformMatrix2fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (3, 3):
                glUniformMatrix3fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (4, 4):
                glUniformMatrix4fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif len(shape) == 1 and shape[0] == 2:
                glUniform2fv(uniforms[field], 1, get_pointer(value))
            elif len(shape) == 1 and shape[0] == 3:
                glUniform3fv(uniforms[field], 1, get_pointer(value))
            elif len(shape) == 1 and shape[0] == 4:
                glUniform4fv(uniforms[field], 1, get_pointer(value))
            elif len(shape) == 1 and shape[0] > 4:
                # Vetores muito grandes são na verdade arranjo de floats para o shader
                if value.dtype == np.int32:
                    glUniform1iv(uniforms[field], shape[0], get_pointer(value))
                else:
                    glUniform1fv(uniforms[field], shape[0], get_pointer(value))
            else:
                print("Tipo não suportado no uniforms: ", field, value)
        
        elif isinstance(value, numbers.Number):
            if type(value) == bool:
                glUniform1i(uniforms[field], value)
            elif type(value) == int:
                glUniform1i(uniforms[field], value)
            else:
                glUniform1f(uniforms[field], value)
        
        elif type(value) == tuple and len(value) == 2:
            glUniform2f(uniforms[field], value[0], value[1])
        
        elif type(value) == tuple and len(value) == 3:
            glUniform3f(uniforms[field], value[0], value[1], value[2])
        
        elif type(value) == tuple and len(value) == 4:
            glUniform4f(uniforms[field], value[0], value[1], value[2], value[3])
        
        else:
            print("Tipo não suportado no uniforms: ", field, value)