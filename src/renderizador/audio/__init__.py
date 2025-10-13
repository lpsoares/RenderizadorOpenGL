#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 12 de Outubro de 2025

Módulo de manipulação de áudio.
"""

from renderizador.audio.audio import Audio, parse_audios, init_audio_streams
from renderizador.audio.fft_processor import process_audio_fft

__all__ = [
    'Audio',
    'parse_audios',
    'init_audio_streams',
    'process_audio_fft'
]