#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025

Script wrapper para renderizar arquivos de fragment shader.
"""

import sys
import os

# Garantir que o módulo renderizador esteja no path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o renderizador de frag
if __name__ == '__main__':
    # Apenas redireciona para o script principal
    from src.renderizador.utils.fragment_shader_renderer import main
    main()