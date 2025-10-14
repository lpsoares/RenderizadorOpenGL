#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Primitive mesh builders.

Provide small helpers that return Mesh objects for common primitives like
the fullscreen quad used for ShaderToy-style rendering.
"""

import numpy as np
from OpenGL.GL import GL_TRIANGLE_STRIP
from .mesh import Mesh


def fullscreen_quad(color=(1.0, 1.0, 1.0), with_uv=True) -> Mesh:
    """Create a fullscreen quad in NDC with optional UVs.

    The quad covers the full screen and is drawn as GL_TRIANGLE_STRIP with 4 vertices.
    Position z is set to 0.0. UVs follow the conventional [0,1] square.
    """
    vertices = np.array([
        [-1.0, -1.0, 0.0],
        [ 1.0, -1.0, 0.0],
        [-1.0,  1.0, 0.0],
        [ 1.0,  1.0, 0.0],
    ], dtype=np.float32)

    colors = np.tile(np.array(color, dtype=np.float32), (4, 1))
    uvs = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=np.float32) if with_uv else None

    return Mesh(vertices=vertices, colors=colors, uvs=uvs, mode=GL_TRIANGLE_STRIP)
