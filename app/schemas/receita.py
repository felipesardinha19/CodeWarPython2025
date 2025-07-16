from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReceitaBase(BaseModel):
    Nome: str 
    Descricao: Optional[str] = None
    Ingredientes: Optional[str] = None
    TempoPreparo: Optional[int] = None
    Categoria: Optional[str] = None
    Origem: Optional[str] = None
    ImagemURL: Optional[str] = None

class ReceitaCreate(ReceitaBase):
    pass

class ReceitaRead(ReceitaBase):
    ID: int
    DataInclusao: datetime
    DataEdicao: Optional[datetime]
    DataExclusao: Optional[datetime]

    class Config:
        orm_mode = True