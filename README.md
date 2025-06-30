# 🍽️ CadeMeuPrato - API de Receitas Nutritivas

---

## 📖 Descrição

**CadeMeuPrato** é uma API construída com **FastAPI** para gerenciar receitas culinárias com um toque especial.  
Além de receitas básicas, ela oferece funcionalidades **nutricionais** (como calorias, proteínas e gorduras), e integração com **APIs públicas** para enriquecer os dados.

O projeto faz parte do **Code War Python 2025**, seguindo boas práticas de programação, organização, documentação e testes.

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.x  
- ⚡ FastAPI  
- 🗄️ SQLite  
- 🔗 SQLAlchemy  
- 📡 httpx  
- 🔧 Pydantic  
- 🚀 Uvicorn  

---

## ✨ Funcionalidades Principais

- 📋 CRUD completo para receitas (criar, listar, atualizar, deletar)  
- 🍏 Informações nutricionais (calorias, proteínas, carboidratos, gorduras)  
- 🌐 Integração com APIs públicas (ex: TheMealDB)  
- 🔍 Filtros por categoria, calorias e ingredientes  
- 🧪 Preparada para testes automatizados  
- 📄 Documentação interativa via Swagger UI  
- 🧠 Estrutura clara e modular, com boas práticas de código  

---

## 📂 Estrutura do Projeto

```text
CadeMeuPrato/
│
├── app/
│ ├── routes/ # Endpoints organizados por módulo
│ ├── models.py # Modelo ORM da tabela Receita
│ ├── database.py # Configuração do SQLite
│ └── main.py # Inicialização da API
│
├── venv/ # Ambiente virtual (não versionado)
├── receitas.db # Banco de dados SQLite
├── run.py # Script para criar o banco
├── requirements.txt # Dependências do projeto
└── README.md # Documentação do projeto
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
