#Data: 17/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    #Carregar os dados de vendas
    df = pd.read_csv('dados/vendas.csv')
    return df

dados_vendas = carregar_dados()

st.title("༘⋆ 🏷 Análise de Produtos")

produtos = st.selectbox(
    "Selecione um produto:", 
    ['Headset', 'Mouse', 'Teclado', 'Headphone', 'Webcam', 'SSD',
                                 'Memória RAM'])
regioes = st.selectbox(
    "Seleciona a região desejada:",
    ['Norte', 'Sul', 'Nordeste', 'Sudeste', 'Centro-Oeste']
)

dados_filtrados = dados_vendas[
    (dados_vendas["Região"].isin(regioes)) &
    (dados_vendas["Produtos"].isin(produtos))    
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Receita", f"R$ {dados_vendas['Vendas'].sum():,.2f}")

col2.metric("Lucro", f"R$ {dados_vendas['Lucro'].sum():,.2f}")

col3.metric("Qtd. Vendida", f"{len(dados_vendas)}")

col4.metric("Preço Médio", f"R$ {dados_vendas['Custo'].mean():,.2f}")

st.divider()

colA, colB = st.columns(2)

with colA:
    fig = px.bar(
        vendas_regiao = dados_filtrados.groupby("Produtos"),
        x = 'Vendas',
        y= 'Região',
        title='Vendas por Região',
        color='Lucro',
        color_continuous_scale=px.colors.sequential.Blues
    )
    st.plotly_chart(fig, width='stretch')

with colB:
    fig = px.pie(

    )