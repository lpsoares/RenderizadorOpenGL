
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.

Desenvolvido por: <SEU NOME AQUI>
Disciplina: Computação Gráfica
Data: <DATA DE INÍCIO DA IMPLEMENTAÇÃO>
"""

import numpy as np

from renderizador.renderizador import *
from renderizador.transformations import *

vertex_shader_source = r'''
#version 330 core
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
#version 330 core

layout (location = 0) out vec4 FragColor;

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
    FragColor = vec4(result, 1.0);

}
'''


if __name__ == '__main__':


    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768), near=0.1, far=100.0)

    # Configura os Uniforms dos Shaders
    uniforms = {}

    # Configurações de Câmera
    uniforms["projection"] = renderizador.camera.get_projection_matrix
    uniforms["view"] = renderizador.camera.get_view_matrix
    uniforms["model"] = translate(0, 0, 0) @ rotate([0.0, 0.0, 1.0], 0.0) @ scale(1.0, 1.0, 1.0)
    uniforms["view_position"] = renderizador.camera.get_eye

    # Configurações de Materiais e Iluminação
    uniforms["light_color"] = [1.0, 1.0, 1.0]
    uniforms["material_albedo"] = [0.7, 0.4, 0.9]
    uniforms["ambient_coefficient"] = 0.4
    uniforms["specular_coefficient"] = 32
    uniforms["light_position"] = [-4.0, 2.0, 1.0]

    # Passando Shaders e renderizando cena
    renderizador.render(vertex_shader_source, fragment_shader_source, uniforms)
    #renderizador.render()