#Data: 12/03/2026

import streamlit as st
import time

placeholder = st.empty()

with placeholder.container():
    st.markdown("![Alt Text](https://media.tenor.com/k5ImtggdKh0AAAAm/melting-snowman.webp)")
    st.write("Carregando...")

time.sleep(5)

placeholder.empty()

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📝",
    layout="wide"
)

#Definindo as páginas
visao_geral = st.Page('./pages/visao_geral.py', 
                      title='Visão Geral',
                      icon='🏘',
                      default=True)

analise_vendas = st.Page('./pages/analise_vendas.py',
                        title='Análise de Vendas',
                        icon='📊')

analise_produtos = st.Page('./pages/analise_produtos.py',
                           title='Produtos',
                           icon='🛍')

analise_produtos_professor = st.Page('./pages/analise_produtos_professor.py',
                           title='Produtos - Professor',
                           icon='👨🏻‍🏫')

mapa_vendas = st.Page('./pages/mapa_vendas.py',
                title='Mapa de Vendas',
                icon='🗺')

mapa_vendas_professor = st.Page('./pages/mapa_vendas_professor.py',
                title='Mapa de Vendas - Professor',
                icon='👨🏻‍🏫')

sobre = st.Page('./pages/sobre.py',
                title='Sobre',
                icon='ℹ️')

#Configurando a navegação entre as páginas
pg = st.navigation(
    [
        visao_geral,
        analise_vendas,
        analise_produtos,
        analise_produtos_professor,
        mapa_vendas,
        mapa_vendas_professor,
        sobre
    ]
)

pg.run()

#𝒊
#############################################
st.markdown("""
<style>
.stApp {
    background-color: #76B1EC;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #5BA1E6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
