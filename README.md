# RenderizadorOpenGL - Renderizador Python com Suporte a ShaderToy

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![OpenGL](https://img.shields.io/badge/OpenGL-4.5-green.svg)](https://www.opengl.org/)
[![ShaderToy](https://img.shields.io/badge/ShaderToy-Compatible-orange.svg)](https://www.shadertoy.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Um renderizador modular em Python baseado em OpenGL, com **suporte nativo para shaders do ShaderToy**. Execute códigos do ShaderToy diretamente, além de criar gráficos 3D, usar shaders customizados, texturas e visualizações de áudio reativas.

## 🚀 Funcionalidades

- **Renderização OpenGL** com pipeline moderno (shaders programáveis)
- **Renderizador de Fragment Shaders** - Ferramenta dedicada para renderizar arquivos .frag
- **Compatibilidade com ShaderToy** - Execute shaders do ShaderToy sem modificações
- **Sistema de Câmera** com modos de visualização "examine" e "fly"
- **Visualização e processamento de áudio** em tempo real com FFT para shaders reativos
- **Iluminação** com modelos Phong/Blinn-Phong
- **Sistema de texturização** para mapeamento UV
- **Interface com ImGui** para controles em tempo real

## 📋 Requisitos

- Python 3.11 ou superior (3.13 apresenta atualmente problemas como imgui)
- OpenGL 3.3 ou superior
- Dependências Python (ver `requirements.txt`)

## 🔧 Instalação

Clone o repositório e instale em modo de desenvolvimento para poder editar o código fonte:

```bash
git clone https://github.com/lpsoares/RenderizadorOpenGL.git
cd RenderizadorOpenGL
pip install -e .
```

## 💻 Uso Básico

### Exemplos incluídos

Execute os exemplos incluídos para ver as diferentes funcionalidades:

```bash
python exemplos/exemplo0.py  # Renderização básica
python exemplos/exemplo1.py  # Câmera e iluminação
python exemplos/exemplo5.py  # Texturas
```

### Renderizador de Fragment Shaders

O projeto inclui uma ferramenta dedicada para renderizar fragment shaders no estilo ShaderToy:

```bash
# Renderizar um shader específico
python render_frag.py exemplos/frag/mandelbulb.frag

# Especificar uma resolução personalizada
python render_frag.py exemplos/frag/ray_marching.frag --resolution 800 600
```

## 🏗️ Arquitetura do Projeto

O RenderizadorOpenGL é organizado em módulos para facilitar a extensão e manutenção:

### Estrutura Principal

```
src/renderizador/
│
├── core/                  # Componentes principais
│   ├── renderer.py        # Renderizador principal
│   ├── window.py          # Gerenciamento de janelas GLFW
│   └── gui.py             # Interface ImGui
│
├── graphics/              # Recursos gráficos
│   ├── camera.py          # Sistema de câmera
│   ├── geometry.py        # Manipulação de geometria
│   ├── shaders.py         # Compilação e gerenciamento de shaders
│   └── texture.py         # Carregamento e manipulação de texturas
│
├── audio/                 # Processamento de áudio
│   ├── audio.py           # Reprodução e controle de áudio
│   └── fft_processor.py   # Processamento FFT para visualização
│
└── utils/                 # Utilidades
    ├── callbacks.py       # Callbacks de eventos
    ├── fragshader_rndr.py # Renderizador de fragment shaders
    ├── transformations.py # Transformações 3D
    └── uniforms.py        # Gerenciamento de uniforms de shaders
```

## 📝 Utilização Avançada

### Criando seu próprio renderizador

```python
from renderizador import Renderizador
from renderizador.graphics.camera import Camera
from OpenGL.GL import *

# Inicialize o renderizador
renderizador = Renderizador(resolution=(1024, 768))

# Configure uma câmera
camera = Camera(type="examine", near=0.1, far=100, eye=[0.0, 0.0, 10.0])
renderizador.set_camera(camera)

# Configure shaders e uniforms
renderizador.set_shaders(
    vertex_shader_source=meu_vertex_shader,
    fragment_shader_source=meu_fragment_shader,
    uniforms_source={
        "projection": camera.get_projection_matrix,
        "view": camera.get_view_matrix,
        "model": identity_matrix,
    }
)

# Configure geometria
renderizador.add_geometry(GL_TRIANGLES, vertices, normals=normals, uvs=uvs)

# Renderize a cena
renderizador.render()
```

### API do Renderizador de Fragment Shaders

O módulo `fragshader_rndr.py` fornece uma API simples para carregar e renderizar fragment shaders:

```python
from renderizador.utils.fragshader_rndr import load_fragment_shader, main

# Carregar um shader de um arquivo
shader_code = load_fragment_shader("caminho/para/meu_shader.frag")

# Executar o renderizador com argumentos da linha de comando
main()
```

## 📚 Documentação Adicional

Para mais detalhes sobre a API e exemplos, consulte a documentação completa em [docs/](docs/):

- [Guia de Início Rápido](docs/getting_started.md)
- [Compatibilidade com ShaderToy](docs/shadertoy_compatibility.md) - Guia completo de como usar shaders do ShaderToy
- [Renderizador de Fragment Shaders](docs/fragment_shader_renderer.md)

### Exemplo de Compatibilidade ShaderToy

O projeto inclui um exemplo demonstrativo de compatibilidade total com ShaderToy:

```bash
# Execute um exemplo de shader ShaderToy complexo
python exemplos/exemplo_shadertoy.py
```

## 🤝 Contribuições

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## 📜 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Créditos

Desenvolvido por Luciano Soares - [lpsoares@insper.edu.br](mailto:lpsoares@insper.edu.br)

