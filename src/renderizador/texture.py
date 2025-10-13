#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 6 de Maio de 2023
"""

class Texture:
    def __init__(self, filename, channel):
        self.channel = channel
        self.filename = filename
        self.texture_id = None
        self.image = None
