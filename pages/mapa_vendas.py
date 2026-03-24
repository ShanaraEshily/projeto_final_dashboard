#Data: 19/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px
from numpy.random import default_rng as rng

dados_vendas = pd.read_csv('dados/vendas_geolocalizacao.csv')

st.title("🗺️ Mapa de Vendas")
st.text("""Visualização da distribuição geográfica das vendas, com aplicação de filtros para
exploração de dados.""")

dados_filtrados = dados_vendas

def format_brl(x):
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")    

###########################MÉTRICAS########################################
col1, col2, col3, col4 = st.columns(4)

with col1:
    #colocar a quantidade de linhas do dataframe
    st.metric("📍 Pontos no Mapa", len(dados_filtrados))

with col2:
    st.metric("🏢 Cidades", dados_filtrados['Cidade'].nunique())

with col3:
    receita = dados_filtrados['Vendas'].sum()
    st.metric("📜 Receita Filtrada", format_brl(receita))

with col4:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric("📊 Lucro Filtrado", format_brl(lucro))

"--------"

##########################FILTROS########################################

st.sidebar.header("Filtros do Mapa")

st.markdown("""
<style>
span[data-baseweb="tag"] {
  background-color: gray !important;
}
</style>
""", unsafe_allow_html=True) #colocar antes dos filtros pra dar cor

#Região
regiao = st.sidebar.multiselect(
    "Região",
    options=dados_vendas["Região"].unique(),
    default=dados_vendas["Região"].unique()
)

#Categoria
categoria = st.sidebar.multiselect(
    "Categoria",
    options=dados_vendas["Categoria"].unique(),
    default=dados_vendas["Categoria"].unique()
)

#Produto
produto = st.sidebar.multiselect(
    "Produto",
    options=dados_vendas["Produto"].unique(),
    default=dados_vendas["Produto"].unique()
)

#Vendedor
vendedor = st.sidebar.multiselect(
    "Região",
    options=dados_vendas["Vendedor"].unique(),
    default=dados_vendas["Vendedor"].unique()
)

#Período
dados_vendas["Data"] = pd.to_datetime(dados_vendas["Data"])
#Recupera as datas mínimas e máximas do dataframe para configurar o filtro de data
data_min = dados_vendas["Data"].min().date()
data_max = dados_vendas["Data"].max().date()

#Filtro de período
#O filtro de data é configurado para permitir a seleção de um intervalo entre a data mínima e
# máxima presente nos dados
data_range = st.sidebar.date_input(
    "Selecione o período:",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if len(data_range) == 2:
    data_inicio = pd.to_datetime(data_range[0])
    data_fim = pd.to_datetime(data_range[1])
else:
    st.warning("Por favor, selecione um intervalo de datas válido")
    st.stop()



#Faixa de valor de venda(R$)
filtro_preco = st.sidebar.slider(
    "Faixa de valor de venda(R$)",
    min_value=157,
    max_value=11997,
    value=(157, 11997)
)

st.markdown("""
<style>
.stSlider > div > div > div > div {
    background: linear-gradient(to right, #7d7979, #4d4848);
}

.stSlider > div > div > div > div > div {
    background-color: gray;
    border: 2px solid black;
}

</style>
""", unsafe_allow_html=True) 

##############################MAPA############################################
st.subheader("✈︎ Distribuição Geográfica das Transações")

if "Latitude" in dados_filtrados.columns and "Longitude" in dados_filtrados.columns:
    
    fig1 = px.scatter_mapbox(
        dados_filtrados,
        lat="Latitude",         
        lon="Longitude",
        size='Vendas',
        color='Lucro',
        hover_name="Região",     
        hover_data={
            "Vendas": True,
            "Lucro": True,
            "Latitude": False,  
            "Longitude": False
        },
        color_continuous_scale=px.colors.sequential.Blues_r,
        size_max=15,
        zoom=3,
        mapbox_style="open-street-map"
    )

    st.plotly_chart(fig1, use_container_width=True)

else:
    st.warning("O dataset precisa conter as colunas 'Latitude' e 'Longitude' para exibir o mapa.")

"--------"

st.subheader("🏙 Resumo por Cidade")
st.dataframe(dados_filtrados)