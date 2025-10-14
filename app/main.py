from fastapi import FastAPI
from .routers import data_router

description = """
A API **IoT - Bancada Camila** permite o acesso aos dados de sensores coletados via MQTT e armazenados em um banco de dados MySQL. 🚀

### Funcionalidades:
* **Consulta de Dados de Sensores**: Acesse os dados históricos de temperatura e umidade.
* **Filtragem Dinâmica**: Filtre os dados por tipo de sensor diretamente na rota de consulta.

Desenvolvido como parte de um projeto para monitoramento de dados da **Bancada Didática 4.0 - Nível 1 (Camila)**.
"""

app = FastAPI(
    title="API IoT - Bancada Camila",
    description=description,
    version="1.0.0",
    contact={
        "name": "Seu Nome",
        "url": "http://github.com/seu_usuario",
        "email": "seu_email@exemplo.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(data_router.router)

@app.get("/", tags=["Root"], summary="Endpoint raiz da API")
def read_root():
    """
    Retorna uma mensagem de boas-vindas e um link para a documentação interativa.
    """
    return {"message": "Bem-vindo à API da Bancada Didática Camila! Acesse /docs para a documentação."}