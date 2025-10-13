
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.

Desenvolvido por: <SEU NOME AQUI>
Disciplina: Computação Gráfica
Data: <DATA DE INÍCIO DA IMPLEMENTAÇÃO>
"""

import numpy as np
import os
from OpenGL.GL import *  # para constantes GL_*

from renderizador import Renderizador
from renderizador.utils.transformations import *
from renderizador.graphics.camera import Camera

vertex_shader_source = r'''
layout (location = 0) in vec3 position;
layout (location = 3) in vec2 uv;  // Texture coordinates are 2D (u,v)

out vec2 texture_uv;

void main() {
    gl_Position = vec4(position, 1.0);
    texture_uv = uv;
}
'''


fragment_shader_source = r'''
layout (location = 0) out vec4 fragColor;

in vec2 texture_uv;

uniform sampler2D textureSample;
//layout(binding=0) uniform sampler2D textureSample;

void main() {   
    vec4 sampled = texture(textureSample, texture_uv);
    fragColor = sampled;
}
'''


if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    base = os.path.dirname(os.path.abspath(__file__))
    texture_file = os.path.join(base, "texture/tree-gf3fdc00cd_640.jpg")
    renderizador.set_texture(texture_file, 0)

    # Vertices (forçando ser float32 para evitar que algum vire outro tipo)
    vertices = np.array(
        [-0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        -0.5, 0.5, 0.0,
        0.5, 0.5, 0.0,
        ], np.float32
    )

    uvs = np.array(
        [0.0, 0.0,
        1.0, 0.0, 
        0.0, 1.0, 
        1.0, 1.0, 
        ], np.float32
    )

    index = np.array([
        0, 1, 2, 3
    ])

    renderizador.add_geometry(GL_TRIANGLE_STRIP, vertices, uvs=uvs, index=index)

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(vertex_shader_source, fragment_shader_source)
   
    renderizador.render()