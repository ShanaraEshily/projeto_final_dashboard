#Data: 18/03/2026

import streamlit as st
import pandas as pd
import plotly.express as px
import locale

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

#############################################################################################

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
    st.metric(label="Receita", value=format_brl(receita))

with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric(label="Lucro", value=format_brl(lucro))

with col3:
    qtd = dados_filtrados['Quantidade'].sum()
    st.metric(label="Qtd. Vendida", value=f"{qtd:,} unidades")

with col4:
    preco_medio = receita/qtd
    st.metric(label="Preço Médio", value=format_brl(preco_medio))

st.divider()

st.subheader("📊 Aréa dos Gráficos")

colA, colB = st.columns(2)

with colA:
    df_agrupado = dados_filtrados.groupby('Região')['Vendas'].sum().reset_index()
    
    #Processo de debug do código
    #st.dataframe(df_agrupado)
    
    #gráfico de barra
    fig = px.bar(df_agrupado, 
                 title=f"Vendas por Região - {option}",
                 x='Região', y='Vendas',
                 color= 'Vendas')
    st.plotly_chart(fig, width='stretch')

with colB:
    df_agrupado2 = dados_filtrados.groupby('Vendedor')['Vendas'].sum().reset_index()

    #gráfico de pizza
    fig = px.pie(df_agrupado2,
                 values='Vendas',
                 names='Vendedor',
                 color_discrete_sequence=px.colors.sequential.Blues_r,
                 title = f"{option} - Vendas por Vendedor")
    st.plotly_chart(fig, width='stretch')

#criando a coluna "Mês" para análise temporal
dados_filtrados['Data'] = pd.to_datetime(dados_filtrados['Data'])

dados_filtrados['Mês'] = dados_filtrados['Data'].dt.to_period('M').astype(str)

#debugando a coluna 'Mês'
#st.dataframe(dados_filtrados.head(10))

df_agrupado3 = dados_filtrados.groupby('Mês')['Vendas'].sum().reset_index()

#gráfico de aréa
fig = px.area(df_agrupado3,
              x='Mês', y='Vendas',
              title= f"Evolução Mensal de {option}")
st.plotly_chart(fig, width='stretch')