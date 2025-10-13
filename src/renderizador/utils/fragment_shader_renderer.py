
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Código que carrega um arquivo de fragment shader e o renderiza usando o renderizador OpenGL com suporte a ShaderToy.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025
"""

import os
import sys
import argparse

from renderizador import Renderizador
from renderizador.utils.transformations import *

def load_fragment_shader(file_path):
    """
    Load fragment shader from a file.
    
    Args:
        file_path: Path to fragment shader file
        
    Returns:
        String containing the shader source code
    
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(file_path) as file:
            return file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo '{file_path}': {e}")
        sys.exit(1)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Renderiza um arquivo de fragment shader usando OpenGL.')
    parser.add_argument('frag_file', nargs='?', default=None, 
                        help='Caminho para o arquivo .frag a ser renderizado')
    parser.add_argument('--resolution', '-r', nargs=2, type=int, default=[600, 400],
                        help='Resolução da janela (largura altura), ex: -r 800 600')
    args = parser.parse_args()
    
    # Determine fragment shader file path
    if args.frag_file:
        frag_file = args.frag_file
    else:
        # Default to teste.frag in the script directory
        base = os.path.dirname(os.path.abspath(__file__))
        frag_file = os.path.join(base, "teste.frag")
        print(f"Nenhum arquivo especificado. Usando o arquivo padrão: {frag_file}")
    
    # Criando renderizador
    renderizador = Renderizador(resolution=(args.resolution[0], args.resolution[1]), lock_mouse=False)
   
    # Carregar o shader do arquivo
    text = load_fragment_shader(frag_file)
    
    # Set window title to show which file is being rendered
    file_name = os.path.basename(frag_file)
    renderizador.set_title(f"Fragment Shader: {file_name}")
    
    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=text)

    renderizador.render()

if __name__ == '__main__':
    main()

    # Set window title to show which file is being rendered
    file_name = os.path.basename(frag_file)
    renderizador.set_title(f"Fragment Shader: {file_name}")
    
    # Passando Shaders e renderizando cena
    renderizador.set_shaders(fragment_shader_source=text)

    renderizador.render()