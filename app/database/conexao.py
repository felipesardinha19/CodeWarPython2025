from sqlmodel import SQLModel, create_engine

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./database.db"

# Cria a engine de conexão com o SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)