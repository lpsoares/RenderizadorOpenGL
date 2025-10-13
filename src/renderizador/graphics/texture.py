#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Texture handling module.
"""

from PIL import Image
import numpy as np
from OpenGL.GL import *
from renderizador.utils.utils import get_pointer

class Texture:
    """Class representing a texture."""
    
    def __init__(self, filename, channel):
        """
        Initialize a texture.
        
        Args:
            filename: Path to the texture image file
            channel: Texture unit to bind to
        """
        self.filename = filename
        self.channel = channel
        self.texture_id = None
        self.image = None

def parse_textures(textures):
    """
    Load and parse textures into OpenGL.
    
    Args:
        textures: List of Texture objects
    """
    for texture in textures:
        # create texture
        texture.image = Image.open(texture.filename)
        texture.image = np.asarray(texture.image, np.uint8)
    
        texture.texture_id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, texture.texture_id)

        # detectar número de canais e usar formato/ internalformat corretos
        if texture.image.ndim == 3:
            channels = texture.image.shape[2]
            if channels == 4:
                fmt = GL_RGBA
            else:
                fmt = GL_RGB
        else:
            # imagem em grayscale
            fmt = GL_RED
            
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            fmt,
            texture.image.shape[1],
            texture.image.shape[0],
            0,
            fmt,
            GL_UNSIGNED_BYTE,
            get_pointer(texture.image)
        )

        # The default behavior for textures should be to repeat rather than clamp or reflect
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # unbind textura
        glBindTexture(GL_TEXTURE_2D, 0)