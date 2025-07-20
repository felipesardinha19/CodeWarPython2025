from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Receitas(SQLModel, table=True):
    ID: Optional[int] = Field(default=None, primary_key=True)
    Nome: str = Field(index=True)
    Descricao: Optional[str] = Field(default=None, description="Breve descrição da receita")
    Ingredientes: Optional[str] = Field(default=None)
    TempoPreparo: Optional[int] = Field(default=None)
    Categoria: Optional[str] = Field(default=None)
    Origem: Optional[str] = Field(default=None)
    ImagemURL: Optional[str] = Field(default=None)  
    DataInclusao: datetime = Field(default_factory=datetime.utcnow)
    DataEdicao: Optional[datetime] = Field(default_factory=datetime.utcnow)
    DataExclusao: Optional[datetime] = Field(default=None)