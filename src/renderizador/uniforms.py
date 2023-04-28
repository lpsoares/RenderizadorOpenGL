
import numpy as np
from OpenGL.GL import *
import numbers

from renderizador.utils import *

def parse_uniforms(uniforms_source, uniforms):
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
            elif shape == (2, 3):
                glUniformMatrix2x3fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (3, 2):
                glUniformMatrix3x2fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (2, 4):
                glUniformMatrix2x4fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (4, 2):
                glUniformMatrix4x2fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (3, 4):
                glUniformMatrix3x4fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (4, 3):
                glUniformMatrix4x3fv(uniforms[field], 1, GL_TRUE, get_pointer(value))
            elif shape == (2, ):
                if all(isinstance(ele, numbers.Integral) for ele in value):
                    if isinstance(value, np.uintc): # unsigned int
                        glUniform2uiv(uniforms[field], 1, value)
                    else:
                        glUniform2iv(uniforms[field], 1, value)
                else:
                    glUniform2fv(uniforms[field], 1, value)
            elif shape == (3, ):
                if all(isinstance(ele, numbers.Integral) for ele in value):
                    if isinstance(value, np.uintc): # unsigned int
                        glUniform3uiv(uniforms[field], 1, value)
                    else:
                        glUniform3iv(uniforms[field], 1, value)
                else:
                    glUniform3fv(uniforms[field], 1, value)
            elif shape == (4, ):
                if all(isinstance(ele, numbers.Integral) for ele in value):
                    if isinstance(value, np.uintc): # unsigned int
                        glUniform4uiv(uniforms[field], 1, value)
                    else:
                        glUniform4iv(uniforms[field], 1, value)
                else:
                    glUniform4fv(uniforms[field], 1, value)

        elif isinstance(value, numbers.Integral):
            if isinstance(value, np.uintc): # unsigned int
                glUniform1ui(uniforms[field], value)
            else:
                glUniform1i(uniforms[field], value)

        elif isinstance(value, numbers.Real):
            glUniform1f(uniforms[field], value)

