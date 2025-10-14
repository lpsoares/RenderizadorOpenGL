# Fragment Shader Renderer

O RenderizadorOpenGL inclui uma ferramenta especializada para renderizar fragment shaders no estilo ShaderToy. Esta documentação explica como usar esta funcionalidade e seus detalhes internos.

## Usando o Renderizador de Fragment Shaders

### Linha de Comando

A maneira mais simples de usar o renderizador é através da linha de comando:

```bash
# Sintaxe básica
python render_frag.py [caminho/para/shader.frag] [opções]

# Exemplos
python render_frag.py exemplos/frag/mandelbulb.frag
python render_frag.py exemplos/frag/ray_marching.frag --resolution 800 600
```

### Opções Disponíveis

- `--resolution` ou `-r`: Define a resolução da janela de renderização (por exemplo, `-r 800 600`)
- Se nenhum arquivo for especificado, o renderizador tentará carregar `teste.frag` no diretório atual

## Estrutura Interna

O renderizador de fragment shaders é implementado no arquivo `src/renderizador/utils/fragshader_rndr.py`. Seus componentes principais são:

### 1. `load_fragment_shader(file_path)`

Esta função carrega o código fonte do shader de um arquivo:

```python
def load_fragment_shader(file_path):
    """
    Carrega o código fonte de um fragment shader a partir de um arquivo.
    
    Args:
        file_path: Caminho para o arquivo .frag
        
    Returns:
        String contendo o código fonte do shader
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
```

### 2. `main()`

Esta função principal analisa os argumentos da linha de comando, configura o renderizador e inicia o processo de renderização:

```python
def main():
    """
    Função principal que processa os argumentos da linha de comando e 
    inicia o renderizador de fragment shaders.
    """
    # Analisa os argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Renderiza um arquivo de fragment shader usando OpenGL.')
    parser.add_argument('frag_file', nargs='?', default=None, 
                      help='Caminho para o arquivo .frag a ser renderizado')
    parser.add_argument('--resolution', '-r', nargs=2, type=int, default=[600, 400],
                      help='Resolução da janela (largura altura), ex: -r 800 600')
    args = parser.parse_args()
    
    # Determina o caminho do arquivo shader
    if args.frag_file:
        frag_file = args.frag_file
    else:
        # Usa teste.frag no diretório do script por padrão
        base = os.path.dirname(os.path.abspath(__file__))
        frag_file = os.path.join(base, "teste.frag")
        print(f"Nenhum arquivo especificado. Usando o arquivo padrão: {frag_file}")
    
    # Cria o renderizador
    renderizador = Renderizador(resolution=(args.resolution[0], args.resolution[1]), lock_mouse=False)
   
    # Carrega o shader do arquivo
    text = load_fragment_shader(frag_file)
    
    # Define o título da janela para mostrar qual arquivo está sendo renderizado
    file_name = os.path.basename(frag_file)
    renderizador.set_title(f"Fragment Shader: {file_name}")
    
    # Configura os shaders e renderiza a cena
    renderizador.set_shaders(fragment_shader_source=text)
    renderizador.render()
```

## Compatibilidade com ShaderToy

O renderizador fornece suporte para shaders no estilo ShaderToy, com as seguintes características:

### Uniformes Compatíveis

- `iResolution`: Resolução da tela (vec2)
- `iTime`: Tempo desde o início da execução (float)
- `iTimeDelta`: Tempo entre frames (float)
- `iFrameRate`: Taxa de quadros (float)
- `iFrame`: Contador de frames (uint)
- `iMouse`: Posição e cliques do mouse (vec4)
- `iDate`: Data como ano, mês, dia e tempo em segundos (vec4)
- `iChannelN`: Texturas/canais de entrada (sampler2D, N=0..3)
- `iChannelResolution[N]`: Tamanho da textura (vec2)
- `iChannelTime[N]`: Tempo de playback em segundos (float)

### Estrutura do Shader

Os shaders ShaderToy devem seguir esta estrutura:

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Seu código aqui
    fragColor = vec4(1.0); // Exemplo de saída
}
```

### Conversão para OpenGL 3.3

O renderizador converte automaticamente os shaders do formato ShaderToy para o formato OpenGL 3.3 Core Profile, fazendo as seguintes alterações:

1. Adiciona a versão GLSL (`#version 330 core`)
2. Adiciona declarações para todas as uniformes compatíveis
3. Converte a função `mainImage()` para a função `main()` padrão do GLSL
4. Ajusta as entradas e saídas para compatibilidade com o pipeline OpenGL moderno

## Exemplos Práticos

### Exemplo: Padrão de Cores

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    fragColor = vec4(uv.x, uv.y, 0.5, 1.0);
}
```

### Exemplo: Animação Baseada em Tempo

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    float t = iTime * 0.5;
    
    vec3 color = 0.5 + 0.5 * cos(t + uv.xyx + vec3(0,2,4));
    fragColor = vec4(color, 1.0);
}
```

### Exemplo: Interação com Mouse

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse = iMouse.xy / iResolution.xy;
    
    float d = length(uv - mouse);
    vec3 color = vec3(1.0 - smoothstep(0.0, 0.2, d));
    
    fragColor = vec4(color, 1.0);
}
```

## Dicas de Performance

- Evite loops complexos e instruções de controle de fluxo condicionais
- Prefira operações vetoriais em vez de escalares
- Use funções built-in do GLSL para melhor desempenho