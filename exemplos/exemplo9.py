
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

fragment_shader_source = r'''

    /*
    2D LED Spectrum - Visualiser
    Based on Led Spectrum Analyser by: simesgreen - 27th February, 2013 https://www.shadertoy.com/view/Msl3zr
    2D LED Spectrum by: uNiversal - 27th May, 2015
    Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
    */

    void mainImage( out vec4 fragColor, in vec2 fragCoord )
    {
        // create pixel coordinates
        vec2 uv = fragCoord.xy / iResolution.xy;

        // quantize coordinates
        const float bands = 30.0;
        const float segs = 40.0;
        vec2 p;
        p.x = floor(uv.x*bands)/bands;
        p.y = floor(uv.y*segs)/segs;

        // read frequency data from first row of texture
        float fft  = texture( iChannel0, vec2(p.x,0.0) ).x;

        // led color
        vec3 color = mix(vec3(0.0, 2.0, 0.0), vec3(2.0, 0.0, 0.0), sqrt(uv.y));

        // mask for bar graph
        float mask = (p.y < fft) ? 1.0 : 0.1;

        // led shape
        vec2 d = fract((uv - p) *vec2(bands, segs)) - 0.5;
        float led = smoothstep(0.5, 0.35, abs(d.x)) *
                    smoothstep(0.5, 0.35, abs(d.y));
        vec3 ledColor = led*color*mask;

        // output final color
        fragColor = vec4(ledColor, 1.0);
    }


'''


if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=fragment_shader_source)

    base = os.path.dirname(os.path.abspath(__file__))

    audio_file = os.path.join(base, "audio/8_bit_mentality.mp3")
    renderizador.set_audio(audio_file, 0)  # ShaderToy

    renderizador.render()
