# Projeto IoT - API para Bancada Didática Camila

Este projeto implementa uma solução completa para consumir dados de sensores via MQTT, persistir essas informações em um banco de dados MySQL e expor os dados através de uma API RESTful construída com FastAPI.

## Funcionalidades

-   **Consumidor MQTT**: Um script que se conecta a um broker MQTT, escuta um tópico específico (`smart40n1`) e processa as mensagens recebidas.
-   **Persistência de Dados**: Os dados de sensores (temperatura e umidade) são salvos em um banco de dados MySQL utilizando SQLAlchemy.
-   **API RESTful**: Uma API robusta e documentada (com Swagger UI) para consultar os dados armazenados.

## Estrutura do Projeto

O projeto segue os princípios de **Separação de Responsabilidades (SoC)** e **Don't Repeat Yourself (DRY)**:

```
PROJETO-IOT-CAMILA/
├── app/                  # Contém toda a lógica da API FastAPI
│   ├── routers/          # Controllers da API
│   ├── crud.py           # Funções de acesso ao banco de dados
│   ├── database.py       # Configuração da conexão com o banco
│   ├── main.py           # Ponto de entrada da API
│   ├── models.py         # Modelos de tabelas (SQLAlchemy)
│   └── schemas.py        # Modelos de dados da API (Pydantic)
├── mqtt_consumer/        # Lógica do consumidor MQTT
├── .env                  # Arquivo de credenciais (local)
├── .env.example          # Template para o arquivo .env
├── README.md             # Esta documentação
└── requirements.txt      # Dependências do projeto
```

## Tecnologias Utilizadas

-   **Python 3.10+**
-   **FastAPI**: Framework para a construção da API.
-   **SQLAlchemy**: ORM para interação com o banco de dados.
-   **Paho-MQTT**: Cliente MQTT para Python.
-   **MySQL**: Banco de dados relacional.
-   **Uvicorn**: Servidor ASGI para rodar a API.
-   **Dotenv**: Para gerenciamento de variáveis de ambiente.

## Como Rodar o Projeto

### Pré-requisitos

-   Python 3.10 ou superior
-   Um servidor MySQL em execução
-   Um broker MQTT (como o [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/))

### 1. Clone o Repositório

```bash
git clone [https://github.com/seu_usuario/PROJETO-IOT-CAMILA.git](https://github.com/seu_usuario/PROJETO-IOT-CAMILA.git)
cd PROJETO-IOT-CAMILA
```

### 2. Crie um Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Copie o arquivo de exemplo e preencha com suas credenciais.

```bash
cp .env.example .env
```

Agora, edite o arquivo `.env` com as informações do seu banco de dados e do seu broker MQTT.

### 5. Rode o Consumidor MQTT

Este script ficará rodando em um terminal para receber e salvar as mensagens.

```bash
python mqtt_consumer/consumer.py
```

### 6. Rode a API

Em um **outro terminal** (com o ambiente virtual ativado), inicie o servidor da API.

```bash
uvicorn app.main:app --reload
```

A flag `--reload` faz com que o servidor reinicie automaticamente após qualquer alteração no código.

## Como Usar a API

Após iniciar o servidor, a API estará acessível em `http://127.0.0.1:8000`.

### Documentação Interativa (Swagger)

A melhor forma de explorar e testar a API é através da documentação interativa, gerada automaticamente pelo FastAPI.

-   **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Exemplo de Requisição

Você pode usar ferramentas como `curl`, Thunder Client (extensão do VS Code) ou a própria documentação para testar.

**Buscar todos os dados de sensores:**
```
GET [http://127.0.0.1:8000/sensors/](http://127.0.0.1:8000/sensors/)
```

**Buscar apenas dados de umidade:**
```
GET [http://127.0.0.1:8000/sensors/?topic=umidade](http://127.0.0.1:8000/sensors/?topic=umidade)
```

**Buscar dados de temperatura com paginação (pula os 5 primeiros e pega os próximos 10):**
```
GET [http://127.0.0.1:8000/sensors/?topic=temperatura&skip=5&limit=10](http://127.0.0.1:8000/sensors/?topic=temperatura&skip=5&limit=10)
```