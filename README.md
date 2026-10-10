# API de Gerenciamento de Tarefas

Projeto desenvolvido como atividade prática da disciplina **Programação para Internet II**, do curso de Análise e Desenvolvimento de Sistemas do IFPI — Campus Piripiri.

## Sobre o projeto

A aplicação consiste em uma API REST para gerenciamento de tarefas (*To-Do API*), permitindo criar, consultar, atualizar e excluir tarefas, além de filtrar e ordenar os resultados.

O projeto utiliza o FastAPI para construção dos endpoints e o pytest para execução dos testes automatizados, verificando o comportamento da API e o tratamento de dados inválidos.

## Tecnologias utilizadas

* **Python 3.13** — linguagem de programação.
* **FastAPI** — desenvolvimento da API REST.
* **Uvicorn** — servidor ASGI para execução da aplicação.
* **Pydantic** — validação dos dados.
* **uv** — gerenciamento de dependências e ambiente de desenvolvimento.
* **pytest** — testes automatizados.
* **pytest-cov** — análise da cobertura de testes, caso instalado.

## Funcionalidades

* Criar tarefas com identificador gerado automaticamente.
* Definir título, descrição, tags e status de conclusão.
* Preencher automaticamente as datas de criação e atualização.
* Listar todas as tarefas cadastradas.
* Consultar uma tarefa pelo identificador.
* Atualizar os dados de uma tarefa.
* Excluir tarefas.
* Filtrar tarefas por status de conclusão, tag e título.
* Ordenar resultados por diferentes campos.
* Validar dados de entrada e retornar erros HTTP apropriados.
* Realizar testes automatizados dos endpoints e das regras de validação.

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.13 ou compatível.
* [uv](https://docs.astral.sh/uv/).

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd teste-api
```

> Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório no GitHub.

### 2. Instalar as dependências

```bash
uv sync
```

### 3. Executar a API

Considerando que o arquivo principal seja `app/main.py` e que a instância FastAPI se chame `app`, execute:

```bash
uv run uvicorn app.main:app --reload
```

Ajuste o caminho caso a estrutura real do projeto seja diferente.

### 4. Acessar a documentação

Com o servidor em execução, acesse pelo navegador:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc

## Executar os testes

Para executar os testes automatizados:

```bash
uv run pytest tests/test_app.py -v
```

Os testes verificam operações CRUD, filtros, ordenação, validações de entrada e respostas de erro.

### Cobertura de testes

Para gerar um relatório de cobertura, com o `pytest-cov` instalado:

```bash
uv run pytest tests/test_app.py --cov=app --cov-report=term-missing
```

O relatório apresenta as linhas executadas e as que ainda não foram cobertas pelos testes.

## Estrutura do projeto

A estrutura abaixo é ilustrativa e deve ser ajustada conforme os arquivos existentes no repositório.

```text
teste-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Objetivo acadêmico

Aplicar os conhecimentos de desenvolvimento de APIs web, organização de código, validação de dados, métodos HTTP, tratamento de erros e testes automatizados utilizando ferramentas do ecossistema Python.

Análise e Desenvolvimento de Sistemas — IFPI, Campus Piripiri.

Disciplina: Programação para Internet II.
