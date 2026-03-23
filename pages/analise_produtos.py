#Data: 17/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px
import locale

def carregar_dados():
    #Carregar os dados de vendas
    df = pd.read_csv('dados/vendas.csv')
    return df

# Função para formatar valores em reais

def format_brl(value):
    # Set the locale to Brazilian Portuguese
    # On some systems, the locale string might be slightly different (e.g., 'pt_BR.UTF-8')
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        # Fallback for systems where 'pt_BR.UTF-8' is not available
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except locale.Error:
            print("Warning: Could not set pt_BR locale. Falling back to simple formatting.")
            return f"R$ {value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')

    # Format the value as currency with grouping enabled
    # locale.currency() returns a string like 'R$ 1.234,56'
    formatted_value = locale.currency(value, symbol=True, grouping=True)
    return formatted_value

dados_vendas = carregar_dados()

st.title("༘⋆ 🏷 Análise de Produtos")

option = st.selectbox(
    "Selecione um produto:", 
    ['Headset', 'Mouse', 'Teclado', 'Headphone', 'Webcam', 'SSD',
                                 'Memória RAM'])

dados_filtrados = dados_vendas[dados_vendas['Produto'] == option]

#st.table(dados_filtrados)

col1, col2, col3, col4 = st.columns(4)

with col1:
    receita = dados_filtrados['Vendas'].sum()
    st.metric(label='Receita', value=format_brl(receita))

with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label='Lucro', value=format_brl(lucro))

with col3:
    quantidade = dados_filtrados['Quantidade'].sum()
    st.metric(label='Quantidade Vendida', value=f"{quantidade:,} unidades")

with col4:
    preco_medio = receita/quantidade
    st.metric(label="Preço Médio", value= format_brl(preco_medio))

st.divider()

colA, colB = st.columns(2)

with colA:
    df_agrupado = dados_filtrados.groupby('Região')['Vendas'].sum().reset_index()

    fig = px.bar(df_agrupado,
                 title=f"Vendas por Região - {option}",
                 x='Região',
                 y='Vendas',
                 color='Vendas')
    st.plotly_chart(fig, width='stretch')

with colB:
    df_agrupado2 = dados_filtrados.groupby('Vendedor')['Vendas'].sum().reset_index()

    fig = px.pie(df_agrupado2,
                 title=f"Vendas por Vendedor - {option}",
                 names='Vendedor',
                 values='Vendas',
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, width='stretch')

dados_filtrados['Data'] = pd.to_datetime(dados_filtrados['Data'])
dados_filtrados['Mês'] = dados_filtrados['Data'].dt.to_period('M').astype(str)

#st.dataframe(dados_filtrados.head(10))

df_agrupado3 = dados_filtrados.groupby("Mês")['Vendas'].sum().reset_index()

fig = px.area(df_agrupado3,
              title=f"Evolução Mensal - {option}",
              x='Mês',
              y='Vendas')
st.plotly_chart(fig, width='stretch')