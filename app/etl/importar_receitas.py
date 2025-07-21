import httpx
import httpx
from datetime import datetime
from sqlmodel import Session, select
from app.models.receita import Receitas

# ---------------------------
# importar receitas da API pública (TheMealDB)
# ---------------------------
def importar_receitas_externas(session: Session): 
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    # Abre uma sessão HTTP assíncrona para realizar a requisição
    with httpx.Client() as client:
        response = client.get(url)
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

        receita = Receitas(
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
