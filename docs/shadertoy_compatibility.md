# ShaderToy Compatibility Guide

O RenderizadorOpenGL oferece compatibilidade nativa com shaders do [ShaderToy](https://www.shadertoy.com/), permitindo que você execute os shaders diretamente ou com modificações mínimas. Esta documentação explica como usar essa funcionalidade.

## O que é o ShaderToy?

[ShaderToy](https://www.shadertoy.com/) é uma plataforma online popular para criar e compartilhar fragment shaders interativos. É uma excelente ferramenta para aprender e experimentar computação gráfica, arte generativa e efeitos visuais.

## Como o RenderizadorOpenGL suporta o ShaderToy

O RenderizadorOpenGL implementa:

1. A API de uniformes do ShaderToy (`iResolution`, `iTime`, `iMouse`, etc.)
2. Conversão automática da função `mainImage()` para `main()`
3. Suporte para texturas via `iChannelN`
4. Suporte para entrada de áudio e FFT

## Executando Shaders do ShaderToy

Há duas maneiras principais de executar shaders do ShaderToy:

### 1. Usando o renderizador de fragment shaders

```bash
# Salve o shader do ShaderToy como um arquivo .frag
python render_frag.py meu_shader_do_shadertoy.frag
```

### 2. Em seu próprio código Python

```python
from renderizador import Renderizador

# Cole o código do ShaderToy aqui como uma string
shader_code = """
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord/iResolution.xy;
    fragColor = vec4(uv.x, uv.y, 0.5 + 0.5*sin(iTime), 1.0);
}
"""

# Crie o renderizador e configure o shader
renderizador = Renderizador()
renderizador.set_shaders(fragment_shader_source=shader_code)

# Opcionalmente, adicione texturas para iChannel0, iChannel1, etc.
renderizador.set_texture("textura.jpg", 0)  # Isto será iChannel0

# Renderize
renderizador.render()
```

## Uniformes do ShaderToy Suportados

O RenderizadorOpenGL suporta as seguintes uniformes do ShaderToy:

| Uniform | Tipo | Descrição |
|---------|------|-----------|
| `iResolution` | `vec2` | Resolução da tela em pixels |
| `iTime` | `float` | Tempo em segundos desde o início |
| `iTimeDelta` | `float` | Tempo em segundos desde o último frame |
| `iFrameRate` | `float` | Taxa de quadros (FPS) |
| `iFrame` | `uint` | Contador de frames |
| `iMouse` | `vec4` | Posição do mouse e cliques: xy=atual, zw=clique |
| `iChannel0` - `iChannel3` | `sampler2D` | Texturas de entrada |
| `iChannelResolution[N]` | `vec2` | Tamanho da textura |
| `iChannelTime[N]` | `float` | Tempo de playback em segundos |


## Exemplo Completo

Veja o arquivo `exemplos/exemplo_shadertoy.py` para um exemplo completo de como executar um shader do ShaderToy, incluindo texturas e interação com o mouse.

## Dicas de Compatibilidade

- Alguns shaders complexos do ShaderToy podem precisar de ajustes para performance
- Shaders que usam buffers múltiplos precisarão ser adaptados
- Os formatos de textura e áudio são ligeiramente diferentes do ShaderToy original
- O iChannelTime é suportado para arquivos de áudio

## Limitações

Existem várias limitações, aqui estão algumas delas:

- Buffers múltiplos não são suportados automaticamente
- Cubemaps e texturas 3D requerem adaptação
- WebCam não é suportada nativamente
- Alguns efeitos específicos do ShaderToy podem requerer modificações

## Recursos Adicionais

- [Documentação do ShaderToy](https://www.shadertoy.com/howto)
- [The Book of Shaders](https://thebookofshaders.com/)
