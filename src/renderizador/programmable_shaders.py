#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 24 de Abril de 2023
"""

from OpenGL.GL import *

# Compilador de Shaders
def compile_shader(type, source):
    shader_id = glCreateShader(type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not success:
        print('Erro em compilação de Shader', type)
        print('log = ', glGetShaderInfoLog(shader_id), "\n")
        raise RuntimeError('Erro em compilação de Shader')
    return shader_id

# Linkedita os Shaders
def link_shader(vertexShader_id, fragmentShader_id):
    program_id = glCreateProgram()
    glAttachShader(program_id, vertexShader_id)
    glAttachShader(program_id, fragmentShader_id)
    glLinkProgram(program_id)
    success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not success:
        print('Erro na linkedição de Shader')
        print('log = ', glGetProgramInfoLog(program_id))
        raise RuntimeError('Erro na linkedição de Shader')
    return program_id