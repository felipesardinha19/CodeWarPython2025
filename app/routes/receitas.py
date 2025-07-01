from fastapi import APIRouter
import httpx

# Cria o roteador para organizar os endpoints relacionados a receitas
router = APIRouter(prefix="/receitas", tags=["Receitas"])

@router.get("/")
async def listar_receitas(): 
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    
    # Abre uma sessão HTTP assíncrona para realizar a requisição
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # Converte a resposta para JSON
        data = response.json()
    # Extrai os nomes das receitas, caso existam no JSON
    nomes_receitas = [meal["strMeal"] for meal in data.get("meals", [])]
    
    # Retorna os nomes das receitas em formato JSON
    return {"receitas":nomes_receitas}