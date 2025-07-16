# 🍽️ CadeMeuPrato - API de Receitas Nutritivas

---

## 📖 Descrição

**CadeMeuPrato** é uma API construída com **FastAPI** para gerenciar receitas culinárias com um toque especial.
ela oferece integração com **API pública** para enriquecer os dados.

O projeto faz parte do **Code War Python 2025**, seguindo boas práticas de programação, organização, documentação e testes.

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.x  
- ⚡ FastAPI  
- 🗄️ SQLite  
- 🔗 SQLModel  
- 📡 httpx  
- 🔧 Pydantic  
- 🚀 Uvicorn  

---

## ✨ Funcionalidades Principais

- 📋 CRUD completo para receitas (criar, listar, atualizar, deletar)    
- 🌐 Integração com APIs públicas (ex: TheMealDB)  
- 🔍 Filtros por categoria, calorias e ingredientes  
- 🧪 Preparada para testes automatizados  
- 📄 Documentação interativa via Swagger UI  
- 🧠 Estrutura clara e modular, com boas práticas de código  

---

## 📂 Estrutura do Projeto

```text
CadeMeuPrato/
/CodeWarPython2025
│
├── app/                          # Código principal da aplicação
│   ├── __init__.py               # Torna 'app' um pacote Python
│   ├── main.py                   # Ponto de entrada da aplicação FastAPI
│   ├── database/                 # Configuração da conexão com banco de dados
│   │   ├── __init__.py
│   │   └── conexao.py            # Criação da engine e sessão (SQLite)
│   ├── models/                   # Modelos SQLModel (tabelas do banco)
│   │   ├── __init__.py
│   │   └── receita.py            # Modelo Receita (com campos básicos e nutricionais)
│   ├── schemas/                  # Schemas Pydantic para validação e documentação
│   │   ├── __init__.py
│   │   └── receita.py            # Schemas para entrada e saída de dados
│   ├── routes/                   # Rotas / endpoints da API
│   │   ├── __init__.py
│   │   └── receita.py            # CRUD e importação para receitas
│   ├── etl/        
│   │   └── importar_receitas.py  # Função para consumir API pública e popular o banco
│                    
│
│
├── app_dashboard.py              # Script Streamlit para dashboard visual das receitas
├── requirements.txt              # Dependências do projeto (FastAPI, SQLModel, httpx etc)
├── README.md                    # Documentação do projeto (funcionalidades, setup, etc)
├── .gitignore                   # Arquivos e pastas ignorados pelo git
└── receitas.db                  # Banco de dados SQLite (gerado automaticamente)
```

🚀 Como Rodar o Projeto
Clone o repositório
```
git clone https://github.com/seu-usuario/CadeMeuPrato.git
cd CadeMeuPrato
```
Ative o ambiente virtual

# Windows:
```
venv\Scripts\activate
```

# Linux/macOS:
```
source venv/bin/activate
```
Instale as dependências
```
pip install -r requirements.txt
```
Crie o banco de dados (executar uma vez)
```
python run.py
```
Inicie o servidor FastAPI

```
uvicorn app.main:app --reload
```
Acesse no navegador:

```
http://localhost:8000/docs
```
```text
🔧 Endpoints Principais
Método	Rota	Descrição
GET	/receitas	Lista todas as receitas
GET	/receitas/{id}	Consulta uma receita pelo ID
POST	/receitas	Cria uma nova receita
PUT	/receitas/{id}	Atualiza uma receita existente
DELETE	/receitas/{id}	Exclui uma receita (soft delete, opcional)
GET	/receitas/nutritivas	Lista receitas com dados nutricionais
```
