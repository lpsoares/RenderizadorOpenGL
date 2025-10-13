
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Aplicação Gráfica Exemplo.

Desenvolvido por: <SEU NOME AQUI>
Disciplina: Computação Gráfica
Data: <DATA DE INÍCIO DA IMPLEMENTAÇÃO>
"""

import os

from renderizador import Renderizador
from renderizador.utils.transformations import *

if __name__ == '__main__':

    # Criando renderizador
    renderizador = Renderizador(resolution=(600, 400), lock_mouse=False)
   
    base = os.path.dirname(os.path.abspath(__file__))
    frag_file = os.path.join(base, "teste.frag")
    with open(frag_file) as file:
        text = file.read()

    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=text)

    renderizador.render()