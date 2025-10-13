#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL com supporte a ShaderToy

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 12 de Outubro de 2025

Módulo de processamento de áudio FFT.
"""

import numpy as np
from OpenGL.GL import *
from renderizador.utils.utils import get_pointer

def process_audio_fft(audio, time_delta, db_min, db_max, decay_tau, audio_gain):
    """
    Process audio data for FFT visualization.
    
    Args:
        audio: Audio object containing the data
        time_delta: Time elapsed since last frame
        db_min: Minimum dB value for normalization
        db_max: Maximum dB value for normalization
        decay_tau: Time constant for decay
        audio_gain: Gain to apply before log/dB conversion
    """
    N = audio._fft_size
    bins = audio._fft_bins
    
    # use audio._pos as the 'end' index (next sample to play)
    # safely read position with lock
    with audio._pos_lock:
        end = int(audio._pos)
    
    start = end - N
    if start >= 0:
        seg = audio.data[start:end]
    else:
        # wrap-around
        seg = np.concatenate([audio.data[start:], audio.data[:end]], axis=0)
    
    # ensure mono
    if seg.ndim > 1:
        seg = np.mean(seg, axis=1)
    
    # pad if too short
    if seg.shape[0] < N:
        seg = np.pad(seg, (0, N - seg.shape[0]), mode='constant')
    
    # === ROW 0: FFT (Frequency domain) ===
    # window and FFT
    hann_window = np.hanning(N).astype('float32')
    spec = np.fft.rfft(seg * hann_window)

    # Inicializar arrays de suavização na primeira vez
    if not hasattr(audio, '_prev_fft'):
        audio._prev_fft = np.zeros(bins, dtype=np.float32)
        
    mag = np.abs(spec)[:bins]

    # === MAPEAMENTO LINEAR DE FREQUÊNCIA (compatível com ShaderToy) ===
    # ShaderToy fornece 512 bins lineares em frequência na linha 0.
    # Portanto, usamos diretamente os primeiros 512 bins do rFFT.
    fft_bins = mag.astype(np.float32)

    # === ESCALA EM DECIBEIS (evita "estouro" e normalização por frame) ===
    # Converte magnitude para dB e mapeia de [db_min, db_max] -> [0,1]
    eps = 1e-12
    fft_db = 20.0 * np.log10(audio_gain * fft_bins + eps)
    fft_norm = (fft_db - db_min) / (db_max - db_min)
    fft_norm = np.clip(fft_norm, 0.0, 1.0).astype(np.float32)

    # === SUAVIZAÇÃO TIPO PEAK-HOLD COM DECAIMENTO ===
    # Mais próximo do visual do ShaderToy do que média simples entre frames
    # Decaimento baseado no delta de tempo para consistência com FPS variável
    tau = float(decay_tau)  # tempo de decaimento em segundos (ajustável)
    # garante valor positivo para o expoente
    dt = max(float(time_delta), 1e-3)
    decay = np.exp(-dt / tau).astype(np.float32)
    prev = audio._prev_fft.astype(np.float32)
    fft_row = np.maximum(fft_norm, prev * decay)
    
    # Atualizar histórico
    audio._prev_fft = fft_row.copy()
    
    # === ROW 1: Waveform (Time domain) ===
    # resample waveform to 512 samples
    # take evenly spaced samples from the audio segment
    indices = np.linspace(0, N-1, bins, dtype=int)
    waveform_row = seg[indices]
    # normalize to 0..1 range (assuming audio is -1..1)
    waveform_row = (waveform_row + 1.0) * 0.5
    waveform_row = np.clip(waveform_row, 0.0, 1.0)
    
    # Create 512x2 texture: [row0=FFT, row1=waveform]
    tex = np.zeros((2, bins), dtype=np.float32)
    tex[0, :] = fft_row
    tex[1, :] = waveform_row
    
    # ensure contiguous memory layout for pointer
    tex = np.ascontiguousarray(tex)

    # upload to GL texture: single channel RED format, 512x2
    glActiveTexture(GL_TEXTURE0 + audio.channel)
    glBindTexture(GL_TEXTURE_2D, audio._fft_tex)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, bins, 2, GL_RED, GL_FLOAT, get_pointer(tex))
    glBindTexture(GL_TEXTURE_2D, 0)
    
    return fft_row, waveform_row