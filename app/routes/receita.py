import httpx
from app.schemas.receita import ReceitaCreate, ReceitaRead
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.etl.importar_receitas import importar_receitas_externas
from app.database.conexao import engine
from app.models.receita import Receitas  

#----------------------------
# Cria o roteador para organizar os endpoints relacionados a receitas
#----------------------------
router = APIRouter(prefix="/receitas", tags=["Receitas"])


#----------------------------
# Dependência para criar sessão de banco
#----------------------------
def get_session():
    with Session(engine) as session:
        yield session

# ---------------------------
# Endpoint para importar receitas da API pública (TheMealDB)
# ---------------------------
@router.post("/importar")
def importar_receitas(session: Session = Depends(get_session)):
    resultado = importar_receitas_externas(session)
    return resultado

# ---------------------------
# CRUD: Listar todas as receitas do banco
# ---------------------------
@router.get("/", response_model=List[Receitas])
def listar_receitas(session: Session = Depends(get_session)):
    receitas = session.exec(select(Receitas)).all()
    return receitas

# ---------------------------
# CRUD: Buscar uma receita pelo ID
# ---------------------------
@router.get("/{id}", response_model=Receitas)
def buscar_receita(id: int, session: Session = Depends(get_session)):
    """
    Retorna uma receita específica com base no ID.
    """
    receita = session.get(Receitas, id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita

# ---------------------------
# CRUD: Criar uma nova receita manualmente
# ---------------------------
@router.post("/", response_model=ReceitaRead)
def criar_receita(receita: ReceitaCreate, session: Session = Depends(get_session)):
    """
    Cadastra uma nova receita manualmente.
    """
    nova_receita = Receitas(
        Nome = receita.Nome,
        Descricao = receita.Descricao,
        Ingredientes = receita.Ingredientes,
        TempoPreparo = receita.TempoPreparo,
        Categoria = receita.Categoria,
        Origem = receita.Origem
    )

    session.add(nova_receita)
    session.commit()
    session.refresh(nova_receita)
    return nova_receita

# ---------------------------
# CRUD: Atualizar uma receita existente
# ---------------------------
@router.put("/{id}", response_model=Receitas)
def atualizar_receita(
    id: int, receita_atualizada: Receitas, session: Session = Depends(get_session)
):
    """
    Atualiza os dados de uma receita com base no ID.
    """
    receita = session.get(Receitas, id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    receita.Nome = receita_atualizada.Nome
    receita.Descricao = receita_atualizada.Descricao
    receita.Ingredientes = receita_atualizada.Ingredientes
    receita.TempoPreparo = receita_atualizada.TempoPreparo
    receita.Categoria = receita_atualizada.Categoria
    receita.Origem = receita_atualizada.Origem
    receita.ImagemURL = receita_atualizada.ImagemURL
    receita.DataEdicao = datetime.utcnow()

    session.add(receita)
    session.commit()
    session.refresh(receita)
    return receita

# ---------------------------
# CRUD: Excluir receita (exclusão lógica)
# ---------------------------
@router.delete("/{id}")
def deletar_receita(id: int, session: Session = Depends(get_session)):
    """
    Marca a receita como excluída (sem apagar do banco).
    """
    receita = session.get(Receitas, id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    receita.DataExclusao = datetime.utcnow()
    session.add(receita)
    session.commit()
    return {"detail": "Receita excluída logicamente."}