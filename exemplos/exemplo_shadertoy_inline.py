
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.
"""

from renderizador import Renderizador


fragment_shader_source = r'''

 void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));

    // Output to screen
    fragColor = vec4(col,1.0);
}

'''


if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))
   
    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=fragment_shader_source)

    renderizador.render()