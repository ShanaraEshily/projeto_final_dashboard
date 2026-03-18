#Data: 18/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px

#todos os dados de vendas estão armazenados nesta variável
dados_vendas = pd.read_csv('dados/vendas.csv')

st.title("🗳 Ánalise de Produtos - Professor")

st.markdown("""
<style>
/* Targets the main selection area */
.stSelectbox div[data-baseweb="select"] > div:first-child {
    background-color: #848992; /* gray background */
    color: black; /* Text color */
}

/* Targets the dropdown list options */
div[role="listbox"] ul {
    background-color: #0D39F1; /* blue background for list items */
}
</style>
            
""", unsafe_allow_html=True)

#TODO: melhorar as opções do selectbox, para mostrar os produtos disponíveis no meu dataframe
#armazena na memória do computador a opção selecionada pelo usuário
option = st.selectbox(
    "Selecione um produto",
    ("Headphone", "Headset", "Memória RAM", "Mouse", "SSD", "Teclado", "Webcam"),
)

#quero filtrar os dados de vendas usando a opção selecionada pelo usuário
dados_filtrados = dados_vendas[dados_vendas['Produto'] == option]

#utilizado para debugar o código
# st.table(dados_filtrados.head(10))

col1, col2, col3, col4 = st.columns(4)

with col1:
    receita = dados_filtrados['Vendas'].sum()
    st.metric(label="Receita", value=f"R${receita:,.2f}")

with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="Lucro", value=f"R${lucro:,.2f}")

with col3:
    qtd = dados_filtrados['Quantidade'].sum()
    st.text(qtd)
    st.metric(label="Qtd. Vendida", value=f"{qtd:,} unidades")

with col4:
    preco_medio = receita/qtd
    st.metric(label="Preço Médio", value=f"R${preco_medio:,.2f}")

st.divider()
