#Data: 19/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px

dados_vendas = pd.read_csv('dados/vendas_geo_resumo.csv')

st.title("🗺️ Mapa Vendas")
st.text("""Visualização da distribuição geográfica das vendas, com aplicação de filtros para
exploração de dados.""")

col1, col2, col3, col4 = st.columns(4)
