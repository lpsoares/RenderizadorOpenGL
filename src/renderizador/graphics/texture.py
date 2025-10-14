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
    
    def __init__(self, filename, channel, **kwargs):
        """
        Initialize a texture.
        
        Args:
            filename: Path to the texture image file
            channel: Texture unit to bind to
            kwargs: Optional parameters:
                - filter: Texture filtering mode (default: GL_LINEAR)
                - wrap: Texture wrapping mode (default: GL_REPEAT)
                - vflip: Whether to vertically flip the image on load (default: True)
        """

        self.filename = filename
        self.channel = channel
        self.filter = kwargs.get("filter", GL_LINEAR)   # Optional: GL_NEAREST, GL_LINEAR, GL_NEAREST_MIPMAP_NEAREST, etc.
        self.wrap = kwargs.get("wrap", GL_REPEAT)     # Optional: GL_CLAMP_TO_EDGE, GL_MIRROR, GL_REPEAT
        self.vflip = kwargs.get("vflip", True)      # Whether to vertically flip the image on load
        
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

        # inverter verticalmente (topo <-> base)
        if texture.vflip:
            texture.image = texture.image.transpose(Image.FLIP_TOP_BOTTOM)

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
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, texture.wrap)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, texture.wrap)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, texture.filter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, texture.filter)

        # unbind textura
        glBindTexture(GL_TEXTURE_2D, 0)