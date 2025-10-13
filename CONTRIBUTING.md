# Contribuindo com o RenderizadorOpenGL

Obrigado pelo seu interesse em contribuir com o RenderizadorOpenGL! Este documento fornece diretrizes e instruções para contribuir com este projeto.

## Ambiente de Desenvolvimento

1. Faça um fork do repositório
2. Clone seu fork localmente:
   ```
   git clone https://github.com/seu-username/RenderizadorOpenGL.git
   cd RenderizadorOpenGL
   ```
3. Instale em modo de desenvolvimento:
   ```
   pip install -e .
   ```
4. Crie uma branch para sua feature:
   ```
   git checkout -b feature/nome-da-sua-feature
   ```

## Estilo de Código

- Siga as diretrizes de estilo PEP 8 para código Python
- Use docstrings para funções, classes e módulos
- Mantenha linhas com menos de 100 caracteres quando possível
- Use nomes significativos para variáveis e funções
- Escreva comentários em português para facilitar a compreensão

## Estrutura do Projeto

Ao adicionar novos recursos, coloque-os no módulo apropriado:

- `core/`: Funcionalidades principais de renderização
- `graphics/`: Componentes relacionados a gráficos (câmera, texturas, etc.)
- `audio/`: Processamento e visualização de áudio
- `utils/`: Funções auxiliares e utilitárias

## Testes

Antes de submeter alterações:

1. Teste suas modificações com os exemplos existentes
2. Se estiver adicionando um novo recurso, crie um exemplo demonstrando-o
3. Garanta que o código execute sem erros no Python 3.11+
4. Verifique a compatibilidade com o OpenGL em diferentes plataformas

## Enviando Alterações

1. Faça push das suas alterações para o seu fork
2. Envie um pull request com uma descrição clara das mudanças
3. Referencie quaisquer issues relacionadas
4. Esteja aberto a feedbacks e revisões de código

## Solicitações de Recursos e Relatórios de Bugs

Use o rastreador de issues do GitHub para reportar bugs ou sugerir recursos. Por favor, inclua:

- Para bugs: Passos para reproduzir, comportamento esperado vs. real e detalhes do seu ambiente
- Para recursos: Descrição clara do recurso e por que seria valioso para o projeto
- Se possível, inclua capturas de tela ou gráficos para ilustrar problemas ou sugestões

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT do projeto.