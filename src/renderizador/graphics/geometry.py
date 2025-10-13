#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Geometry handling module.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
import ctypes

def create_geometry_data(mode, vertices, normals=None, colors=None, uvs=None, create_normals=False, index=None):
    """
    Create geometry data from input parameters.
    
    Args:
        mode: OpenGL drawing mode (GL_TRIANGLE_STRIP, GL_TRIANGLES, etc.)
        vertices: Array of vertex coordinates
        normals: Array of normal vectors
        colors: Array of color values
        uvs: Array of texture coordinates
        create_normals: Whether to automatically create normals
        index: Optional index array for indexed geometry
    
    Returns:
        Tuple of (data, mode, count)
    """
    data = []
    count = 0
    
    # Valores padrões (normal, cor)
    normal = np.array([0.0, 0.0, 1.0], np.float32)
    color = np.array([1.0, 1.0, 1.0], np.float32)
    uv = np.array([0.0, 0.0], np.float32)

    if mode == GL_TRIANGLE_STRIP:
        for f in range(0, len(vertices), 3):
            
            # identificando vértice
            vertex = vertices[f:f+3]

            # identificando normal
            if normals is not None:
                normal = normals[f:f+3]
            elif create_normals and f < vertices.size - (2*3):
                vertex1 = vertices[f+3:f+6]
                vertex2 = vertices[f+6:f+9]
                if f%6==0:
                    normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                else:
                    normal = normalize(np.cross(vertex2 - vertex, vertex1 - vertex))
            
            # identificando cor
            if colors is not None:
                color = colors[f:f+3]

            # identificando coordenadas de textura
            if uvs is not None:
                uv = uvs[(f//3)*2:((f//3)*2)+2]
            else:
                # Deixa os UVs proporcionais a posição na tela
                uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2])

            data.append(np.concatenate([vertex, normal, color, uv]))

        count = vertices.size

    if mode == GL_TRIANGLES:
        if index is not None:
            for f in range(len(index)):
                # identificando vértice
                vertex = vertices[index[f]*3:(index[f]*3)+3]

                if len(vertex) != 3:
                    raise Exception("Vetor não possui 3 dimensões")

                # identificando normal
                if normals is not None:
                    normal = normals[index[f+1]*3:(index[f+1]*3)+3]
                elif create_normals:
                    if f%3==0:
                        vertex1 = vertices[(index[f+1]*3):(index[f+1]*3)+3]
                        vertex2 = vertices[(index[f+2]*3):(index[f+2]*3)+3]
                        normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                
                # identificando cor
                if colors is not None:
                    color = colors[index[f]*3:(index[f]*3)+3]

                # identificando coordenadas de textura
                if uvs is not None:
                    uv = uvs[(index[f]//3)*2:((index[f]//3)*2)+2]
                else:
                    # Deixa os UVs proporcionais a posição na tela
                    uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2])

                data.append(np.concatenate([vertex, normal, color, uv]))

        count = len(index)*3

    return np.array(data, np.float32).flatten(), mode, count

def normalize(v):
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def parse_geometry(data, mode, count):
    """
    Parse geometry data into OpenGL buffers.
    
    Args:
        data: Flattened array of vertex data
        mode: OpenGL drawing mode
        count: Number of vertices
    
    Returns:
        Tuple of (VAO, count)
    """
    # Cria o VBO (Vertex Buffer Object) para armazenar vértices
    verticesVBO = vbo.VBO(data, usage='GL_STATIC_DRAW')
    verticesVBO.create_buffers()

    # Cria e ativa o VAO (Vertex Array Object) para gerenciar os VBOs
    triangleVAO = glGenVertexArrays(1)
    glBindVertexArray(triangleVAO)

    # Ativa o VBO para o contexto atual
    verticesVBO.bind()

    # buffer data into OpenGL
    verticesVBO.copy_data()

    # Configuração para posição dos vértices
    # Coloca no ID 0, vértices 3D, com um stride de 3*4 (3 vertices de float = 4)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Configuração para normal dos vértices
    # Coloca no ID 1, vértices 3D, com um stride de 3*4 (3 vertices de float = 4) e um ofset de (3*4)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    # Configuração para cor dos vértices
    # Coloca no ID 2, vértices 3D, com um stride de 3*4 (3 vertices de float = 4) e um ofset de (3*4)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(6 * 4))
    glEnableVertexAttribArray(2)

    # Configuração para coordenadas uv de textura dos vértices
    # Coloca no ID 3, vértices 2D (u,v), com um stride de 11*4 (11 floats total) e um ofset de (9*4)
    glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, (3+3+3+2) * 4, ctypes.c_void_p(9 * 4))
    glEnableVertexAttribArray(3)

    # Desativa (unbind) o VBO
    verticesVBO.unbind()

    # Desativa (unbind) o VAO
    glBindVertexArray(0)

    return triangleVAO, count