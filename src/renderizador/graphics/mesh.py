#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Mesh utilities: structure and interleaving of vertex attributes.

This module centralizes how we represent a mesh in Python/Numpy and how we
pack attributes into a single interleaved float32 buffer ready for OpenGL.

Benefits:
- Clear separation of authoring arrays (vertices, normals, colors, uvs)
  from the interleaved GPU buffer.
- Shape/dtype validation in one place.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict
import numpy as np


Attr = Optional[np.ndarray]


@dataclass
class Mesh:
    """Container for mesh attributes.

    All arrays are row-major with one row per vertex:
      - vertices: (N,3) float32
      - normals:  (N,3) float32 (optional)
      - colors:   (N,3) float32 (optional)
      - uvs:      (N,2) float32 (optional)

    mode: OpenGL primitive mode (e.g., GL_TRIANGLE_STRIP, GL_TRIANGLES, ...)
    """

    vertices: np.ndarray
    normals: Attr = None
    colors: Attr = None
    uvs: Attr = None
    mode: int = 0

    def validate(self) -> None:
        """Validate shapes and dtypes for safety before packing."""
        assert isinstance(self.vertices, np.ndarray), "vertices must be a numpy array"
        N = self.vertices.shape[0]
        assert self.vertices.dtype == np.float32 and self.vertices.shape[1] == 3, (
            "vertices must be float32 with shape (N,3)"
        )
        if self.normals is not None:
            assert self.normals.dtype == np.float32 and self.normals.shape == (N, 3), (
                "normals must be float32 with shape (N,3)"
            )
        if self.colors is not None:
            assert self.colors.dtype == np.float32 and self.colors.shape == (N, 3), (
                "colors must be float32 with shape (N,3)"
            )
        if self.uvs is not None:
            assert self.uvs.dtype == np.float32 and self.uvs.shape == (N, 2), (
                "uvs must be float32 with shape (N,2)"
            )

    def interleaved(self, layout: Tuple[str, ...] = ("position", "normal", "color", "uv")) -> Tuple[np.ndarray, int, Dict[str, int]]:
        """Pack attributes into a single interleaved float32 buffer.

        Args:
            layout: order of attributes in the interleaved buffer. The default order
                    matches the project's VAO attribute setup: position, normal, color, uv.

        Returns:
            data_flat: 1D float32 numpy array (contiguous) suitable for uploading to GL
            stride:    stride in bytes between consecutive vertices
            offsets:   dict mapping attribute name -> byte offset within a vertex
        """
        self.validate()

        attrs = {
            "position": self.vertices,
            "normal": self.normals,
            "color": self.colors,
            "uv": self.uvs,
        }

        cols = []
        offsets: Dict[str, int] = {}
        offset_floats = 0
        for name in layout:
            arr = attrs.get(name)
            if arr is None:
                continue
            cols.append(arr)
            offsets[name] = offset_floats * 4  # bytes (float32 = 4 bytes)
            offset_floats += arr.shape[1]

        interleaved_2d = np.concatenate(cols, axis=1).astype(np.float32, copy=False)
        data_flat = np.ascontiguousarray(interleaved_2d.reshape(-1))

        stride_floats = sum((attrs[name].shape[1] for name in layout if attrs.get(name) is not None))
        stride = stride_floats * 4  # bytes

        return data_flat, stride, offsets
