import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import os

st.set_page_config(page_title="Cadê Meu Prato?", layout="wide")
st.title("Dashboard - Receitas cadastradas")

#Defininco caminho absoluto do banco
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(base_dir, "..", "database.db"))

engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})

def carregar_dados():
    query = "SELECT * FROM receitas"
    df = pd.read_sql(query, engine)
    print(f'Tabela carregada:{df.shape[0]} registros')
    print(df.head())
    return df

df = carregar_dados()

st.subheader("Estatisticas gerais")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total de receitas", len(df))
with col2:
    if 'categoria' in df.columns:
        st.metric("CAtegorias unicas", df['categoria'].nunique())

st.subheader("Receita do dia")
if not df.empty:
    receita = df.sample(1).iloc[0]
    st.markdown(f"### {receita['Nome']}")
    if 'Descricao' in df.columns:
        st.write(receita['Descricao'])
    if 'ImagemURL' in df.columns:
        st.image(receita['ImagemURL'], width=400)

