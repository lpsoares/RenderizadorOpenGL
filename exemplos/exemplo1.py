
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
from renderizador.utils.transformations import *
from renderizador.graphics.camera import Camera


vertex_shader_source = r'''
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 fragPos;
out vec3 bNormal;

void main()
{
    
    // Invertendo a transformação para normal
    bNormal = mat3(transpose(inverse(model))) * normal;

    // Aplica o model na posição do vetor no modelo para uso em iluminação
    fragPos = vec3(model * vec4(position, 1.0));

    // Aplicando trasnsformações em cada vértice
    gl_Position = projection * view * model * vec4(position, 1.0);
}
'''


fragment_shader_source = r'''
layout (location = 0) out vec4 fragColor;

in vec3 fragPos;
in vec3 bNormal;

uniform vec3 material_albedo;
uniform vec3 light_color;
uniform vec3 view_position;
uniform vec3 light_position;

uniform float ambient_coefficient;
uniform int specular_coefficient;

void main()
{   

    // Vetores auxiliares
    vec3 cNormal = normalize(bNormal);
    vec3 lightDir = normalize(light_position - fragPos);
    vec3 viewDir = normalize(view_position - fragPos);

    // Calculando contribuição da luz ambiente
    vec3 ambient = ambient_coefficient * light_color;
    
    // Calculando contribuição da luz difusa
    float diffMul = max(0.0, dot(cNormal, lightDir));
    vec3 diffuse = diffMul * light_color;
    
    // Calculando contribuição da luz ambiente
    vec3 reflectDir = normalize(reflect(-lightDir, cNormal));
    float specMul = pow(max(0.0, dot(viewDir, reflectDir)), specular_coefficient);
    vec3 specular = specMul * light_color;
    
    // Juntando todos os componentes luminosos no albedo
    vec3 result = (ambient + diffuse + specular) * material_albedo;
    fragColor = vec4(result, 1.0);

}
'''


if __name__ == '__main__':


    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768), lock_mouse=False)
    
    # Criando câmera e configurando no renderizador
    camera = Camera(type="examine", near=0.1, far=100, eye=[0.0, 0.0, 10.0])
    renderizador.set_camera(camera)  # Forma correta de configurar a câmera

    # Configura os Uniforms dos Shaders
    uniforms = {}

    # Configurações de Câmera
    uniforms["projection"] = camera.get_projection_matrix
    uniforms["view"] = camera.get_view_matrix
    uniforms["model"] = translate(0, 0, 0) @ rotate([0.0, 0.0, 1.0], 0.0) @ scale(1.0, 1.0, 1.0)
    uniforms["view_position"] = camera.get_eye

    # Configurações de Materiais e Iluminação
    uniforms["light_color"] = [1.0, 1.0, 1.0]
    uniforms["material_albedo"] = [0.5, 0.7, 0.9]
    uniforms["ambient_coefficient"] = 0.4
    uniforms["specular_coefficient"] = 32
    uniforms["light_position"] = [-4.0, 2.0, 1.0]

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(vertex_shader_source, fragment_shader_source, uniforms)

    # Vertices (forçando ser float32 para evitar que algum vire outro tipo)
    vertices = np.array([
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        1.0, -1.0,  1.0,
        1.0, -1.0, -1.0,
    ], np.float32)

    index = np.array([
        0, 1, 3,
        1, 2, 3,
        0, 4, 1,
        4, 5, 1,
        1, 5, 2,
        5, 6, 2,
        2, 6, 3,
        6, 7, 3,
        3, 7, 0,
        7, 4, 0,
        4, 7, 5,
        7, 6, 5,
    ])

    renderizador.add_geometry(GL_TRIANGLES, vertices, create_normals=True, index=index)

    renderizador.render()