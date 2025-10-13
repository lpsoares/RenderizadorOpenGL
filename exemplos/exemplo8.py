
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

from renderizador.renderizador import *
from renderizador.transformations import *

fragment_shader_source = r'''

    #define WAVES 8.0

    void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
        vec2 uv = -1.0 + 2.0 * fragCoord.xy / iResolution.xy;

        float time = iTime * 1.0;
        
        vec3 color = vec3(0.0);

        for (float i=0.0; i<WAVES + 1.0; i++) {
            float freq = texture(iChannel0, vec2(i / WAVES, 0.0)).x * 7.0;

            vec2 p = vec2(uv);

            p.x += i * 0.04 + freq * 0.03;
            p.y += sin(p.x * 10.0 + time) * cos(p.x * 2.0) * freq * 0.2 * ((i + 1.0) / WAVES);
            float intensity = abs(0.01 / p.y) * clamp(freq, 0.35, 2.0);
            color += vec3(1.0 * intensity * (i / 5.0), 0.5 * intensity, 1.75 * intensity) * (3.0 / WAVES);
        }

        fragColor = vec4(color, 1.0);
    }

'''


if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=fragment_shader_source)

    base = os.path.dirname(os.path.abspath(__file__))

    audio_file = os.path.join(base, "audio/Experiment.mp3")
    renderizador.set_audio(audio_file, 0)  # ShaderToy

    renderizador.render()
