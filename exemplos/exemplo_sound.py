
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.
"""

import os
from renderizador import Renderizador

if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1024, 768))

    base = os.path.dirname(os.path.abspath(__file__))
    frag_file = os.path.join(base, "frag/sound.frag")
    with open(frag_file) as file:
        text = file.read()

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=text)

    audio_file = os.path.join(base, "audio/Electronebulae.mp3")
    renderizador.set_audio(audio_file, 0)  # ShaderToy

    renderizador.render()
