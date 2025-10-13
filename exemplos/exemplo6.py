
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

 void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    //float sound = texture(iChannel0, vec2(uv.x, 0.25)).r;

    //vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));

    vec4 texColor = texture(iChannel0, uv);
    fragColor = texColor;


    // Output to screen
    //fragColor = vec4(col,1.0);
}

'''


if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=fragment_shader_source)

    base = os.path.dirname(os.path.abspath(__file__))
    
    texture_file = os.path.join(base, "texture/tree-gf3fdc00cd_640.jpg")
    renderizador.set_texture(texture_file, 0)

    audio_file = os.path.join(base, "audio/synth.wav")
    renderizador.set_audio(audio_file, 1)  # https://github.com/pdx-cs-sound/wavs/blob/main/synth.wav

    renderizador.render()
