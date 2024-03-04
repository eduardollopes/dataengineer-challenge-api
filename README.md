# Desafio de Engenheiro de Dados - API

Este projeto tem como objetivo consumir dados de uma API e processá-los usando o Apache Spark.
A proposta é criar uma engine capaz de fazer requisições com base no termo de pesquisa e salvar esses dados para explorações futuras.

## Estrutura do Repositório

- `data/files`: Pasta para armazenar os resultados do processamento.
- `src/`: Contém o código-fonte do projeto.
- `utils/`: Módulos utilitários, como processamento de dados JSON.
- `Dockerfile`: Arquivo de configuração para criar a imagem Docker.
- `main.py`: Script principal responsável por consumir a API e processar os dados.
- `README.md`: Este arquivo de documentação.
- `requirements.txt`: Lista de dependências do projeto.

## Requisitos

Antes de executar o projeto, certifique-se de ter instalado:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Executando o Projeto

1. Construa a imagem Docker:
    ```bash
    docker build -t challenge-api .
    ```

2. Execute a imagem para realizar o processamento:
    ```bash
    docker run -v $PWD/data:/app/data challenge-api
    ```

Isso iniciará o processo de consumo da API, processamento dos dados e salvamento dos resultados no diretório `data/files`.

## Contribuições
Sinta-se à vontade para contribuir abrindo problemas ou enviando pull requests.
