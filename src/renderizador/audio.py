#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 12 de Outubro de 2025
"""

class Audio:
    def __init__(self, filename, id):
        self.id = id
        self.filename = filename
        self.audio_id = None
