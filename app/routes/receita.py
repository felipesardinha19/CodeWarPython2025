import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import List
from datetime import datetime

from app.database.conexao import engine
from app.models.receita import Receita  

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
async def importar_receitas(session: Session = Depends(get_session)): 
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    # Abre uma sessão HTTP assíncrona para realizar a requisição
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # Converte a resposta para JSON
        data = response.json()
    
    meals = data.get("meals", [])
    for meal in meals:
        ingredientes = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            med = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                ingredientes.append(f"{med.strip()} {ing.strip()}")
        ingredientes_str = ", ".join(ingredientes)

        receita = Receita(
            Nome=meal["strMeal"],
            Descricao=meal.get("strInstructions"),
            Ingredientes=ingredientes_str,
            Categoria=meal.get("strCategory"),
            Origem=meal.get("strArea"),
            ImagemURL=meal.get("strMealThumb"),
            DataInclusao=datetime.utcnow(),
            DataEdicao=datetime.utcnow(),
        )
        session.add(receita)
    session.commit()
    return {"message": f"{len(meals)} receitas importadas com sucesso"}


# ---------------------------
# CRUD: Listar todas as receitas do banco
# ---------------------------
@router.get("/", response_model=List[Receita])
def listar_receitas(session: Session = Depends(get_session)):
    receitas = session.exec(select(Receita)).all()
    return receitas

# ---------------------------
# CRUD: Buscar uma receita pelo ID
# ---------------------------
@router.get("/{id}", response_model=Receita)
def buscar_receita(id: int, session: Session = Depends(get_session)):
    """
    Retorna uma receita específica com base no ID.
    """
    receita = Session.get(Receita, id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita

# ---------------------------
# CRUD: Criar uma nova receita manualmente
# ---------------------------
@router.post("/", response_model=Receita)
def criar_receita(receita: Receita, session: Session = Depends(get_session)):
    """
    Cadastra uma nova receita manualmente.
    """
    session.add(receita)
    session.commit()
    session.refresh(receita)
    return receita

# ---------------------------
# CRUD: Atualizar uma receita existente
# ---------------------------
@router.put("/{id}", response_model=Receita)
def atualizar_receita(
    id: int, receita_atualizada: Receita, session: Session = Depends(get_session)
):
    """
    Atualiza os dados de uma receita com base no ID.
    """
    receita = session.get(Receita, id)
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
    receita = session.get(Receita, id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    receita.DataExclusao = datetime.utcnow()
    session.add(receita)
    session.commit()
    return {"detail": "Receita excluída logicamente."}