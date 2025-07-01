from fastapi import FastAPI
from app.routes import receitas

# Cria a instância da aplicação FastAPI com título
app = FastAPI(title= "CodeWar - API de Receitas")

# Inclui a rota de receitas, agrupando os endpoints sob /receitas
app.include_router(receitas.router)

@app.get("/")
def read_root():
    """
    Endpoint raiz da API.
    Retorna uma mensagem simples de boas-vindas.
    """
    return {"mensagem": "Bem-vindo à API de Receitas!"}
