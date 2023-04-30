#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 24 de Abril de 2023
"""

import sys
from OpenGL.GL import *

# Compilador de Shaders
def compile_shader(type, source):
    shader_id = glCreateShader(type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not success:
        print("\n"+"-"*79+"\n"+"Erro em compilação de Shader", type)
        error = glGetShaderInfoLog(shader_id).decode("utf-8")
        if type == GL_FRAGMENT_SHADER and source[18:40] == "#define HW_PERFORMANCE": # Isso indica Shadertoy
            # Ajustando linha de erro
            error = error.split(":")
            error[2] = str(int(error[2])-5) # no momento o número de linhas é 5
            error = ":".join(error)
        print(error+"-"*79)
        sys.exit('Erro em compilação de Shader')
    return shader_id

# Linkedita os Shaders
def link_shader(vertexShader_id, fragmentShader_id):
    program_id = glCreateProgram()
    glAttachShader(program_id, vertexShader_id)
    glAttachShader(program_id, fragmentShader_id)
    glLinkProgram(program_id)
    success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not success:
        print("\n"+"-"*79+"\n"+"Erro na linkedição de Shader")
        error = glGetProgramInfoLog(program_id).decode("utf-8")
        print(error+"-"*79)
        sys.exit('Erro na linkedição de Shader')
    return program_id