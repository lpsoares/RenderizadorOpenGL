
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

    vec2 uv = fragCoord/iResolution.xy;
	
	vec4 col1 = texture( iChannel0, uv );
	vec4 col2 = texture( iChannel1, uv );
    
    vec4 col;
    if (uv.x > 0.5)
        col=col1;
    else
        col=col2;

	fragColor = col;

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
    texture_file2 = os.path.join(base, "texture/daylily-7390789_1280.jpg")
    renderizador.set_texture(texture_file2, 1)

    audio_file = os.path.join(base, "audio/synth.wav")
    renderizador.set_audio(audio_file, 2)  # https://github.com/pdx-cs-sound/wavs/blob/main/synth.wav

    renderizador.render()
