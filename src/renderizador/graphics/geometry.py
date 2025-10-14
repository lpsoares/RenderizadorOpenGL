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

    # Normalize inputs to flattened 1D float32 arrays (Mesh inputs may be 2D)
    vertices = np.asarray(vertices, dtype=np.float32)
    if vertices.ndim == 2:
        # Expect (N,3)
        if vertices.shape[1] != 3:
            raise ValueError("vertices must have shape (N,3) when 2D")
        vertices_flat = vertices.reshape(-1)
        vertex_count = vertices.shape[0]
    elif vertices.ndim == 1:
        if vertices.size % 3 != 0:
            raise ValueError("vertices 1D array size must be multiple of 3")
        vertices_flat = vertices
        vertex_count = vertices.size // 3
    else:
        raise ValueError("vertices must be either 1D (flat) or 2D with shape (N,3)")

    normals_flat = None
    colors_flat = None
    uvs_flat = None

    if normals is not None:
        normals = np.asarray(normals, dtype=np.float32)
        if normals.ndim == 2:
            if normals.shape != (vertex_count, 3):
                raise ValueError("normals must match vertices shape (N,3)")
            normals_flat = normals.reshape(-1)
        elif normals.ndim == 1:
            if normals.size != vertex_count * 3:
                raise ValueError("normals size must be N*3")
            normals_flat = normals
        else:
            raise ValueError("normals must be either 1D or 2D (N,3)")

    if colors is not None:
        colors = np.asarray(colors, dtype=np.float32)
        if colors.ndim == 2:
            if colors.shape != (vertex_count, 3):
                raise ValueError("colors must match vertices shape (N,3)")
            colors_flat = colors.reshape(-1)
        elif colors.ndim == 1:
            if colors.size != vertex_count * 3:
                raise ValueError("colors size must be N*3")
            colors_flat = colors
        else:
            raise ValueError("colors must be either 1D or 2D (N,3)")

    if uvs is not None:
        uvs = np.asarray(uvs, dtype=np.float32)
        if uvs.ndim == 2:
            if uvs.shape != (vertex_count, 2):
                raise ValueError("uvs must match vertices shape (N,2)")
            uvs_flat = uvs.reshape(-1)
        elif uvs.ndim == 1:
            if uvs.size != vertex_count * 2:
                raise ValueError("uvs size must be N*2")
            uvs_flat = uvs
        else:
            raise ValueError("uvs must be either 1D or 2D (N,2)")
    
    # Valores padrões (normal, cor)
    normal = np.array([0.0, 0.0, 1.0], np.float32)
    color = np.array([1.0, 1.0, 1.0], np.float32)
    uv = np.array([0.0, 0.0], np.float32)

    if mode == GL_TRIANGLE_STRIP:
        for f in range(0, vertices_flat.size, 3):
            
            # identificando vértice
            vertex = vertices_flat[f:f+3]

            # identificando normal
            if normals_flat is not None:
                normal = normals_flat[f:f+3]
            elif create_normals and f < vertices_flat.size - (2*3):
                vertex1 = vertices_flat[f+3:f+6]
                vertex2 = vertices_flat[f+6:f+9]
                if f%6==0:
                    normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                else:
                    normal = normalize(np.cross(vertex2 - vertex, vertex1 - vertex))
            
            # identificando cor
            if colors_flat is not None:
                color = colors_flat[f:f+3]

            # identificando coordenadas de textura
            if uvs_flat is not None:
                uv = uvs_flat[(f//3)*2:((f//3)*2)+2]
            else:
                # Deixa os UVs proporcionais a posição na tela
                uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2], dtype=np.float32)

            data.append(np.concatenate([vertex, normal, color, uv]))

        # number of vertices, not number of floats
        count = vertex_count

    if mode == GL_TRIANGLES:
        if index is not None:
            for f in range(len(index)):
                # identificando vértice
                vertex = vertices_flat[index[f]*3:(index[f]*3)+3]

                if len(vertex) != 3:
                    raise Exception("Vetor não possui 3 dimensões")

                # identificando normal
                if normals_flat is not None:
                    normal = normals_flat[index[f+1]*3:(index[f+1]*3)+3]
                elif create_normals:
                    if f%3==0:
                        vertex1 = vertices_flat[(index[f+1]*3):(index[f+1]*3)+3]
                        vertex2 = vertices_flat[(index[f+2]*3):(index[f+2]*3)+3]
                        normal = normalize(np.cross(vertex1 - vertex, vertex2 - vertex))
                
                # identificando cor
                if colors_flat is not None:
                    color = colors_flat[index[f]*3:(index[f]*3)+3]

                # identificando coordenadas de textura
                if uvs_flat is not None:
                    uv = uvs_flat[(index[f]//3)*2:((index[f]//3)*2)+2]
                else:
                    # Deixa os UVs proporcionais a posição na tela
                    uv = np.array([(vertex[0]+1)/2, (vertex[1]+1)/2], dtype=np.float32)

                data.append(np.concatenate([vertex, normal, color, uv]))

        # number of vertices emitted equals number of indices processed
        count = len(index) if index is not None else 0

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