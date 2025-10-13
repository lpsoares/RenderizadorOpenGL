
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.

Desenvolvido por: <SEU NOME AQUI>
Disciplina: Computação Gráfica
Data: <DATA DE INÍCIO DA IMPLEMENTAÇÃO>
"""

import numpy as np
from OpenGL.GL import *  # para constantes GL_*

from renderizador import Renderizador


vertex_shader_source = r'''
layout (location = 0) in vec3 position;
//out vec3 bColor;
void main() {
    gl_Position = vec4(position, 1.0);
    //bColor = vec3( 1.0, 1.0, 0.0);
    //if (gl_VertexID == 0) bColor = vec3( 1.0, 0.0, 0.0);
    //if (gl_VertexID == 1) bColor = vec3( 0.0, 1.0, 0.0);
    //if (gl_VertexID == 2) bColor = vec3( 0.0, 0.0, 1.0);
}
'''


fragment_shader_source = r'''
layout (location = 0) out vec4 fragColor;

uniform vec3 color;

void main() {   
    fragColor = vec4(color, 1.0);
}
'''


if __name__ == '__main__':


    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    # Configura os Uniforms dos Shaders
    uniforms = {}

    # Configurações de Câmera
    uniforms["color"] = [1.0, 0.0, 0.0]

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(vertex_shader_source, fragment_shader_source, uniforms)

    # Vertices (forçando ser float32 para evitar que algum vire outro tipo)
    vertices = np.array(
        [-0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0,
        ], np.float32
    )

    index = np.array([
        0, 1, 2,
    ])

    renderizador.add_geometry(GL_TRIANGLES, vertices, index=index)

    renderizador.render()