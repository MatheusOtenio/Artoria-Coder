# Assistente de Código Local

Um aplicativo desktop que analisa repositórios de código e fornece assistência via modelos de IA locais usando Ollama.

## Visão Geral

O Assistente de Código Local é uma ferramenta que permite aos desenvolvedores:

- Clonar repositórios GitHub automaticamente
- Analisar a estrutura e conteúdo do código
- Fazer perguntas sobre o código usando modelos de IA locais
- Obter respostas contextualizadas sem enviar código para serviços em nuvem

## Requisitos

- Python 3.8+
- Git
- [Ollama](https://ollama.ai/) com um modelo compatível instalado (recomendado: deepseek-coder)

## Dependências

- customtkinter
- CTkMessagebox
- GitPython
- tree-sitter
- requests

## Instalação

1. Clone este repositório:

   ```bash
   git clone <url-do-repositorio>
   cd assistente-codigo-local
   ```

2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Instale o Ollama seguindo as instruções em: https://ollama.ai/download

4. Baixe um modelo compatível com o Ollama:
   ```bash
   ollama pull deepseek-coder:1.3b
   ```

## Uso

1. Inicie o Ollama em um terminal:

   ```bash
   ollama serve
   ```

2. Em um novo terminal, inicie o assistente:

   ```bash
   python main.py
   ```

3. Na interface do aplicativo:
   - Cole a URL de um repositório GitHub na caixa de texto
   - Clique em "Clonar e Analisar"
   - Quando a análise for concluída, faça perguntas sobre o código

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação e interface gráfica
- `github_api.py`: Funções para clonar repositórios do GitHub
- `code_parser.py`: Analisador de código usando tree-sitter para diferentes linguagens
- `ia_local.py`: Interface com o servidor Ollama
- `cache_manager.py`: Gerenciamento de cache para repositórios
- `history_manager.py`: Gerenciamento do histórico de conversas
- `error_handling.py`: Sistema centralizado de tratamento de erros
- `project_tree.py`: Visualização da estrutura do projeto em árvore
- `settings_window.py`: Janela de configurações para o Ollama

## Configuração

Você pode configurar o modelo e endpoint do Ollama através da interface:

1. O arquivo `settings.json` será criado automaticamente na primeira execução
2. Padrões:
   - Modelo: deepseek-coder:1.3b
   - Endpoint: http://localhost:11434/api/generate

## Linguagens Suportadas

O projeto atualmente suporta análise para:

- Python
- JavaScript
- Java

## Resolução de Problemas

- **Erro ao conectar com o servidor Ollama**: Certifique-se de que o Ollama está em execução com `ollama serve` em um terminal separado.
- **Erro ao clonar repositório**: Verifique se a URL do GitHub está correta e se você tem acesso ao repositório.
- **Problemas de análise de código**: Verifique se os parsers do tree-sitter estão instalados corretamente.

## Limitações Conhecidas

- O sistema depende do Ollama executando localmente
- A análise detalhada de código é limitada às linguagens suportadas
- Alguns recursos avançados de análise ainda estão em desenvolvimento

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests ou abrir issues para melhorias.
