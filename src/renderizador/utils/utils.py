#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Module for file containing utility functions for the renderer.
"""

def get_pointer(data):
    """
    Get a pointer to data for use with OpenGL.
    
    Args:
        data: NumPy array or Python list
        
    Returns:
        Pointer to data
    """
    import ctypes
    import numpy as np
    
    if data is None:
        return data
    
    # Convert Python list to NumPy array if needed
    if isinstance(data, list):
        data = np.array(data, dtype=np.float32)
    
    # Handle NumPy arrays
    return data.ctypes.data_as(ctypes.c_void_p)