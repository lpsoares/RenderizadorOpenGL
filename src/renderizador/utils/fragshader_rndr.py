
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Código que carrega um arquivo de fragment shader e o renderiza usando o renderizador OpenGL com suporte a ShaderToy.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 13 de Outubro de 2025
"""

from html import parser
import os
import sys
import argparse
from pathlib import Path

from renderizador import Renderizador
from renderizador.utils.transformations import *

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.tga', '.gif', '.tiff')
AUDIO_EXTS = ('.wav', '.mp3', '.ogg')


def set_channel(res: Renderizador, path_str: str, idx: int):
    p = Path(path_str)
    ext = p.suffix.lower()
    if ext in IMG_EXTS:
        res.set_texture(str(p), idx)
    elif ext in AUDIO_EXTS:
        res.set_audio(str(p), idx)
    else:
        print(f"Erro: Formato não suportado para iChannel{idx}: {p}")
        sys.exit(1)

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
    for i in range(4):
        parser.add_argument(f'--iChannel{i}', default=None,
                            help=f'Caminho para textura ou áudio no iChannel{i}')
  
    args = parser.parse_args()
    
    # Determine fragment shader file path
    if args.frag_file:
        frag_file = args.frag_file
    else:
        # List all .frag files under the 'exemplos' folder and ask the user to pick one
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        exemplos_dir = os.path.join(repo_root, "exemplos")

        candidates = []
        if os.path.isdir(exemplos_dir):
            for dirpath, _, filenames in os.walk(exemplos_dir):
                for name in filenames:
                    if name.lower().endswith(".frag"):
                        full = os.path.join(dirpath, name)
                        rel = os.path.relpath(full, exemplos_dir)
                        candidates.append((rel, full))
            candidates.sort(key=lambda x: x[0].lower())

        if not candidates:
            # Fallback to teste.frag in the utils directory
            frag_file = os.path.join(current_dir, "teste.frag")
            print("Nenhum arquivo .frag encontrado em 'exemplos/'.")
            print(f"Usando o arquivo padrão: {frag_file}")
        else:
            print("Nenhum arquivo especificado. Escolha um dos shaders abaixo (pasta 'exemplos'):\n")
            for idx, (rel, _) in enumerate(candidates, start=1):
                print(f"  {idx:2d}) {rel}")
            print("")
            while True:
                try:
                    choice = input(f"Digite o número [1-{len(candidates)}] e pressione Enter: ").strip()
                    sel = int(choice)
                    if 1 <= sel <= len(candidates):
                        frag_file = candidates[sel - 1][1]
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
    
    # Criando renderizador
    renderizador = Renderizador(resolution=(args.resolution[0], args.resolution[1]), lock_mouse=False)
   
    for i in range(4):
        chan = getattr(args, f'iChannel{i}')
        if chan:
            set_channel(renderizador, chan, i)

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

