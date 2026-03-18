#Data: 12/03/2026

import streamlit as st

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

#sobre = st.Page('./pages/sobre.py',
#                title='Sobre',
#                icon='𝒊')

#Configurando a navegação entre as páginas
pg = st.navigation(
    [
        visao_geral,
        analise_vendas,
        analise_produtos
    ]
)

pg.run()

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

st.balloons()