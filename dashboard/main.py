import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import os
import random
import plotly.express as px

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

st.subheader("🍽️ Receita do dia")
if not df.empty:
    receita = df.sample(1).iloc[0]
    st.markdown(f"### {receita['Nome']}")
    if 'Descricao' in df.columns:
        st.write(receita['Descricao'])
    if 'ImagemURL' in df.columns:
        st.image(receita['ImagemURL'], width=400)

#Filtro por categoria
st.subheader("📋 Tabela de Receitas")
if 'Categoria' in df.columns:
    categorias = df['Categoria'].dropna().unique()
    categoria_selecionada = st.selectbox("Filtrar por categoria", options=["Todas"] + list(categorias))
if categoria_selecionada != "Todas":
    df = df[df['Categoria'] == categoria_selecionada]

#Busca por nome
busca = st.text_input("Buscar por nome de receita:")
if busca:
    df = df[df['Nome'].str.contains(busca, case=False)]

#Exibição da tabela filtrada
st.dataframe(df)

#grafico por categoria
if 'Categoria' in df.columns:
    st.subheader("📊 Receitas por Categoria")
    cat_df = df['Categoria'].value_counts().reset_index()
    cat_df.columns = ['Categoria', 'Total']
    fig_cat = px.bar(cat_df, x='Categoria', y='Total', color='Categoria',
                     title='Total de Receitas por Categoria')
    st.plotly_chart(fig_cat, use_container_width=True)

#Grafico po área
if 'Origem' in df.columns:
    st.subheader("🌍 Receitas por Origem")
    area_df = df['Origem'].value_counts().reset_index()
    area_df.columns = ['Origem', 'Total']
    fig_area = px.pie(area_df, names='Origem', values='Total', title='Distribuição por Área')
    st.plotly_chart(fig_area, use_container_width=True)
