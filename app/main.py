from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database.conexao import engine
from app.routes.receita import router as receita_router

# Cria a aplicação FastAPI
app = FastAPI(title="CodeWar - API de Receitas")

# Registra as rotas da API
app.include_router(receita_router)


@app.on_event("startup")
def on_startup():
    """
    Evento executado quando a aplicação inicia.
    Cria as tabelas no banco, caso não existam.
    """
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    """
    Endpoint raiz da API.
    Retorna uma mensagem de boas-vindas.
    """
    return {"mensagem": "Bem-vindo à API de Receitas!"}
