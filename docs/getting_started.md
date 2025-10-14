# Guia de Início Rápido

Este guia fornece uma introdução básica ao RenderizadorOpenGL e suas principais funcionalidades.

## Instalação

```bash
git clone https://github.com/lpsoares/RenderizadorOpenGL.git
cd RenderizadorOpenGL
pip install -e .
```

## Conceitos Básicos

O RenderizadorOpenGL é organizado em torno de algumas classes e conceitos fundamentais:

### Renderizador

A classe `Renderizador` é o componente principal que gerencia o pipeline de renderização. Ela cuida da janela, do loop de renderização, e da conexão entre os shaders e os dados geométricos.

```python
from renderizador import Renderizador

renderizador = Renderizador(resolution=(800, 600), lock_mouse=False)
renderizador.set_background_color((0.1, 0.1, 0.1, 1.0))
renderizador.set_title("Minha Aplicação")
```

### Câmera

O sistema de câmera permite navegar na cena 3D. O RenderizadorOpenGL suporta dois modos de câmera:

- **examine**: Orbita em torno de um ponto alvo
- **fly**: Movimentação em primeira pessoa

```python
from renderizador.graphics.camera import Camera

camera = Camera(type="examine", near=0.1, far=100, eye=[0.0, 0.0, 5.0])
renderizador.set_camera(camera)
```

### Shaders

Shaders são programas que rodam na GPU e definem como a geometria é processada e renderizada:

```python
vertex_shader = """
layout (location = 0) in vec3 position;

void main() {
    gl_Position = vec4(position, 1.0);
}
"""

fragment_shader = """
layout (location = 0) out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

renderizador.set_shaders(vertex_shader, fragment_shader)
```

### Geometria

Adicione geometria para renderização:

```python
import numpy as np
from OpenGL.GL import GL_TRIANGLES

vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], np.float32)

renderizador.add_geometry(GL_TRIANGLES, vertices)
```

### Uniformes

Uniformes são variáveis que você pode passar para os shaders:

```python
uniforms = {
    "color": [1.0, 0.0, 0.0],
    "scale": 2.0,
    "matrix": np.identity(4, np.float32)
}

renderizador.set_shaders(vertex_shader, fragment_shader, uniforms)
```

## Renderizador de Fragment Shaders

O RenderizadorOpenGL inclui uma ferramenta para renderizar fragment shaders no estilo ShaderToy:

```bash
python render_frag.py caminho/para/shader.frag --resolution 800 600
```

### Compatibilidade com ShaderToy

Os shaders no estilo ShaderToy devem usar a função `mainImage`:

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord/iResolution.xy;
    fragColor = vec4(uv.x, uv.y, 0.5, 1.0);
}
```

O renderizador fornece as seguintes uniformes compatíveis com ShaderToy:

- `iResolution`: resolução da tela
- `iTime`: tempo desde o início
- `iTimeDelta`: tempo entre frames
- `iFrameRate`: taxa de quadros
- `iFrame`: contador de frames
- `iMouse`: posição e cliques do mouse
- `iDate`: data como ano, mês, dia e tempo em segundos
- `iChannelN`: texturas/canais de entrada (sampler2D, N=0..3)
- `iChannelResolution[N]`: tamanho da textura (vec2)
- `iChannelTime[N]`: tempo de playback em segundos (float)


## Exemplos

O repositório contém vários exemplos que demonstram diferentes aspectos do renderizador:

- `exemplo0.py`: Renderização básica de um triângulo
- `exemplo1.py`: Cubo 3D com controle de câmera e iluminação
- `exemplo2.py`: Exemplo básico de shader estilo ShaderToy
- `exemplo3.py`: Exemplo mais complexto originário do ShaderToy
- `exemplo4.py`: Exemplo para carregar arquivos frag
- `exemplo5.py`: Exemplo com textura básica
- `exemplo6.py`: Exemplo com texturas e áudio
- `exemplo7.py`: Exemplo básico de áudio do ShaderToy
- `exemplo8.py`: Mais um exemplo de áudio do ShaderToy
- `exemplo8.py`: Outro exemplo de áudio do ShaderToy

Estude esses exemplos para entender como usar o RenderizadorOpenGL para suas próprias aplicações.

## Próximos Passos

Depois de dominar os conceitos básicos, explore:

- Implementação de técnicas de iluminação avançadas
- Criação de efeitos visuais com shaders
- Integração com processamento de áudio para visualizações reativas