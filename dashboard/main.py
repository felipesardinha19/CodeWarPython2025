import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

st.set_page_config(page_title="Cadê Meu Prato?", layout="wide")
st.title("Dashboard - Receitas cadastradas")

caminho_banco = Path(__file__).resolve().parent.parent/"database.db"
engine = create_engine(f'sqlite:///{caminho_banco}')

def carregar_dados():
    query = "SELECT * FROM receitas"
    return pd.read_sql(query, engine)

df = carregar_dados()

st.subheader("Estatisticas")
st.write("Total de receitas:", len(df))

