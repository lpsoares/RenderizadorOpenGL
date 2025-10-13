#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Shader management module.
"""

from OpenGL.GL import *

default_vertex_shader = r'''
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 normal;
    layout (location = 2) in vec3 color;
    layout (location = 3) in vec2 uv;

    out vec3 bColor;
    out vec3 bNormal;
    out vec2 bUV;

    void main() {
        gl_Position = vec4(position, 1.0);
        bNormal = normal;
        bColor = color;
        bUV=uv;
    }
'''

default_fragment_shader = r'''
    layout (location = 0) out vec4 fragColor;
    in vec3 bNormal;
    in vec3 bColor;
    in vec2 bUV;
    void main() {
        fragColor = vec4(bColor, 1.0f);
    }
'''

def compile_shader(shader_type, source):
    """
    Compile a shader from source.
    
    Args:
        shader_type: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
        source: String containing the shader source code
    
    Returns:
        Shader ID
    """
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)
    
    # Check for compilation errors
    status = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not status:
        # Retrieve error message
        if shader_type == GL_VERTEX_SHADER:
            shader_type_str = "Vertex"
        else:
            shader_type_str = "Fragment" 
        error = glGetShaderInfoLog(shader_id)
        error_str = error.decode('utf-8') if isinstance(error, bytes) else str(error)
        raise RuntimeError(f"{shader_type_str} shader compilation error:\n{error_str}")
    
    return shader_id

def link_shader(vertex_shader_id, fragment_shader_id):
    """
    Link shader program from compiled vertex and fragment shaders.
    
    Args:
        vertex_shader_id: Compiled vertex shader ID
        fragment_shader_id: Compiled fragment shader ID
    
    Returns:
        Program ID
    """
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    
    # Check for linking errors
    status = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not status:
        error = glGetProgramInfoLog(program_id)
        error_str = error.decode('utf-8') if isinstance(error, bytes) else str(error)
        raise RuntimeError(f"Shader linking error:\n{error_str}")
    
    return program_id