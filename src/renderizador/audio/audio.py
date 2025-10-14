#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025

Módulo de manipulação de áudio.
"""

import soundfile as sf
import sounddevice as sd
import numpy as np
import threading
from OpenGL.GL import *

class Audio:
    """Class representing an audio file."""
    
    def __init__(self, filename, channel):
        """
        Initialize an audio object.
        
        Args:
            filename: Path to the audio file
            channel: Channel to bind to
        """
        self.filename = filename
        self.channel = channel
        self._volume = 1.0  # volume level (0.0 to 1.0)
        self.data = None
        self.sf = None
        
def parse_audios(audios):
    """
    Load and parse audio files.
    
    Args:
        audios: List of Audio objects
    """
    for audio in audios:
        audio.data, audio.sf = sf.read(audio.filename)
        # inicializa parâmetros para FFT->textura
        # FFT size chosen so we get 512 frequency bins (N/2)
        audio._fft_size = 1024
        audio._fft_bins = audio._fft_size // 2
        # create a GL texture to hold the FFT and waveform (512 x 2)
        # Row 0: FFT (frequency domain)
        # Row 1: Waveform (time domain)
        audio._fft_tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, audio._fft_tex)
        # allocate float RED texture (single channel, 512x2)
        try:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, audio._fft_bins, 2, 0, GL_RED, GL_FLOAT, None)
        except Exception:
            # fallback if GL_R32F not available
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, audio._fft_bins, 2, 0, GL_RED, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_2D, 0)
        # position for FFT read (we will base on audio._pos updated by callback)
        audio._fft_pos = 0

def init_audio_streams(renderer):
    """
    Initialize audio streams for all loaded audio files.
    
    Args:
        renderer: Renderizador object containing the audio files
    """
    # criar um OutputStream por arquivo de audio carregado    
    def make_callback(audio):
        n_samples = audio.data.shape[0]
        channels = 1 if audio.data.ndim == 1 else audio.data.shape[1]
        audio._pos = 0
        audio._pos_lock = threading.Lock()

        def callback(outdata, frames, time_info, status):
            if status:
                # opcional: log
                # print("sounddevice status:", status)
                pass
            with audio._pos_lock:
                start = audio._pos
                end = start + frames
                if end <= n_samples:
                    chunk = audio.data[start:end]
                    audio._pos = end % n_samples
                else:
                    # concatena tail + head para fazer loop
                    part1 = audio.data[start:n_samples]
                    part2 = audio.data[0:(end - n_samples)]
                    chunk = np.concatenate([part1, part2], axis=0)
                    audio._pos = (end - n_samples) % n_samples

            # aplica volume e assegura shape (frames, channels)
            vol = float(getattr(audio, "_volume", 1.0))
            if channels == 1:
                out = (chunk * vol).reshape(-1, 1)
            else:
                out = chunk * vol
            # clip para evitar saturação e garantir dtype
            out = np.clip(out, -1.0, 1.0).astype('float32', copy=False)
            outdata[:] = out

        return callback

    for audio in renderer.audios:
        # garante float32 no intervalo -1..1
        audio.data = audio.data.astype('float32')
        channels = 1 if audio.data.ndim == 1 else audio.data.shape[1]
        # inicializa posição e cria stream, mas NÃO inicia automaticamente
        audio._pos = 0
        audio._pos_lock = threading.Lock()
        audio._sd_stream = sd.OutputStream(
            samplerate=audio.sf,
            channels=channels,
            dtype='float32',
            callback=make_callback(audio)
        )
        audio._sd_stream_active = False
        audio._looping = True
    renderer._audio_initialized = True
    # iniciar streams somente se já estiver em play
    if renderer.play:
        renderer._resume_audio_streams()