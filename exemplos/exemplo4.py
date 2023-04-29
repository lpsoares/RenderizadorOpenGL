
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

if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(1280, 720))
   
    #with open('silexars.frag') as file:
    with open('mandelbulb.frag') as file:
        text = file.read()

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=text)

    renderizador.render()