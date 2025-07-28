import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os
import random
import plotly.express as px
import requests

API_URL = "http://localhost:8000"

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Cadê Meu Prato?", layout="wide")
st.markdown("<h1 style='text-align: center; color: #ff6347;'>🍽️ Cadê Meu Prato?</h1>", unsafe_allow_html=True)

#Defininco caminho absoluto do banco
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(base_dir, "..", "database.db"))

engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})

@st.cache_data
def carregar_dados():
    query = "SELECT * FROM receitas"
    df = pd.read_sql(query, engine)
    return df

df = carregar_dados()

st.markdown("---")
st.subheader("Estatisticas gerais")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de receitas", len(df))
with col2:
    if 'Categoria' in df.columns:
        st.metric("Categorias unicas", df['Categoria'].nunique())
with col3:
    st.metric("Origens Diferentes", df['Origem'].nunique() if 'Origem' in df.columns else "N/D")

st.markdown("---")
st.subheader("🍽️ Receita do dia")
if not df.empty:
    receita = df.sample(1).iloc[0]
    st.markdown(f"### {receita['Nome']}")
    if 'Descricao' in df.columns:
        st.write(receita['Descricao'])
    if 'ImagemURL' in df.columns:
        st.image(receita['ImagemURL'], width=400)

st.markdown("---")
# --- FORMULÁRIO PARA CRIAR RECEITA ---
st.subheader("Cadastrar nova receita")

with st.form("form_receita"):
    Nome = st.text_input("Nome da receita")
    Ingredientes = st.text_area("Ingredientes (separados por vírgula)")
    TempoPreparo = st.number_input("Tempo de preparo (minutos)", min_value=1, step=1)
    Categoria = st.text_input("Categoria")
    Descricao = st.text_area("Descrição")
    Origem = st.text_input("Origem da receita")
    Imagem_url = st.text_input("URL da imagem")


    submitted = st.form_submit_button("Criar Receita")

    if submitted:
        data = {
            "Nome": Nome,
            "Ingredientes": Ingredientes,
            "Tempo_preparo": TempoPreparo,
            "Descrição": Descricao,
            "Origem": Origem,
            "Categoria": Categoria
        }
        response = requests.post(f"{API_URL}/receitas/", json=data)

        if response.status_code == 201:
            st.success("Receita criada com sucesso!")
            st.session_state["nome_receita"] = ""
            st.session_state["ingredientes"] = ""
            st.session_state["tempo_preparo"] = 0
            st.session_state["categoria"] = ""
            st.session_state["descricao"] = ""
            st.session_state["origem"] = ""
            st.session_state["imagem"] = ""
        else:
            st.error(f"Erro ao criar receita: {response.status_code}")

st.markdown("---")
st.subheader("Deletar Receita")
with engine.connect() as conn:
    result = conn.execute(text("SELECT id, nome FROM receitas"))
    receitas = result.fetchall()
    # Exibe o selectbox se houver receitas
    if receitas:
        receitas_dict = {f"{nome} (ID: {id})": id for id, nome in receitas}
        selected = st.selectbox("Selecione a receita para deletar", list(receitas_dict.keys()))

        if st.button("Deletar Receita"):
            id_para_deletar = receitas_dict[selected]
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM Receitas WHERE id = :id"), {"id": id_para_deletar})
            st.success(f"Receita com ID {id_para_deletar} deletada com sucesso!")
            st.rerun()  # Atualiza a tela
    else:
        st.info("Nenhuma receita cadastrada para deletar.")            

st.markdown("---")
#Filtro por categoria
filtro_col1, filtro_col2 = st.columns(2)

st.markdown("---")
st.subheader("📋 Tabela de Receitas")
with filtro_col1:
    if 'Categoria' in df.columns:
        categorias = df['Categoria'].dropna().unique()
        categoria_selecionada = st.selectbox("Filtrar por categoria", options=["Todas"] + list(categorias))
    df_filtrado = df.copy()
    if categoria_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_selecionada]
with filtro_col2:
    busca = st.text_input("🔎Buscar por nome de receita:")
    if busca:
        df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(busca, case=False)]

#Exibição da tabela filtrada
st.dataframe(df_filtrado, use_container_width=True)

#grafico por categoria
st.markdown("---")
if 'Categoria' in df.columns:
    st.subheader("📊 Receitas por Categoria")
    cat_df = df['Categoria'].value_counts().reset_index()
    cat_df.columns = ['Categoria', 'Total']
    fig_cat = px.bar(cat_df, x='Categoria', y='Total', color='Categoria',
                     title='Total de Receitas por Categoria')
    st.plotly_chart(fig_cat, use_container_width=True)

#Grafico po área
st.markdown("---")
if 'Origem' in df.columns:
    st.subheader("🌍 Receitas por Origem")
    area_df = df['Origem'].value_counts().reset_index()
    area_df.columns = ['Origem', 'Total']
    fig_area = px.pie(area_df, names='Origem', values='Total', title='Distribuição por Área')
    st.plotly_chart(fig_area, use_container_width=True)

st.markdown("---")
st.markdown("<small style= 'color:grey;'>Desenvolvido para o desafio CodeWar Python 2025</small>",unsafe_allow_html=True)