#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
3D Transformation utilities for OpenGL rendering.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 23 de Abril de 2023
"""

import numpy as np

def normalize(v):
    """
    Normalize a vector.
    
    Args:
        v: Vector to normalize
        
    Returns:
        Normalized vector
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def cross_product(v):
    """
    Create cross product matrix from vector.
    
    Args:
        v: Input vector [x, y, z]
        
    Returns:
        Cross product matrix
    """
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]], dtype=np.float32)

def translate(x, y, z):
    """
    Create a translation matrix.
    
    Args:
        x, y, z: Translation amounts
        
    Returns:
        4x4 translation matrix
    """
    result = np.identity(4, dtype=np.float32)
    result[0, 3] = x
    result[1, 3] = y
    result[2, 3] = z
    
    return result

def rotate(axis, angle):
    """
    Create a rotation matrix around an arbitrary axis.
    
    Args:
        axis: 3D vector specifying rotation axis
        angle: Angle of rotation in radians
        
    Returns:
        4x4 rotation matrix
    """
    axis = normalize(axis)

    mat3 = np.cos(angle) * np.identity(3, dtype=np.float32) + np.sin(angle) * cross_product(axis) + \
           (1 - np.cos(angle)) * np.outer(axis, axis)

    result = np.zeros((4, 4), np.float32)
    result[:3, :3] = mat3
    result[3, 3] = 1.0

    return result

def scale(x, y, z):
    """
    Create a scaling matrix.
    
    Args:
        x, y, z: Scale factors
        
    Returns:
        4x4 scaling matrix
    """
    result = np.zeros((4, 4), np.float32)
    result[0, 0] = x
    result[1, 1] = y
    result[2, 2] = z
    result[3, 3] = 1.0

    return result