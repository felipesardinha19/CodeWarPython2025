import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Cadê Meu Prato?", layout="wide")
st.title("Dashboard - Receitas cadastradas")

caminho_banco = "app/database/conexao.py"
engine = create_engine(f'sqlite:///{caminho_banco}')

def carregar_dados():
    query = "SELECT * FROM receitas"
    return pd.read_sql(query, engine)

df = carregar_dados()

st.subheader("Estatisticas")
st.write("Total de receirtas:", len(df))

