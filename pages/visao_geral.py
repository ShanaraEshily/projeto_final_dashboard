import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    #Carregar os dados de vendas
    df = pd.read_csv('dados/vendas.csv')
    return df

#utuliza a função para carregar dados e armazena uma variável para
#uso posterior
#é um dataframe do pandas que contém os dados de vendas
dados_vendas = carregar_dados()

st.title(":rainbow[𓁹 𓁹 Visão Geral do Negócio]")

#KPIs principais
col1, col2, col3, col4 = st.columns(4)

#coluna 1 exibe a receita total, formatada como moeda brasileira
col1.metric(":blue[💰 Receita Total]", f"R$ {dados_vendas['Vendas'].sum():,.2f}")

#coluna 2 exibe o lucro total, formatado como moeda brasileira
col2.metric(":orange[💲 Lucro Total]", f"R$ {dados_vendas['Lucro'].sum():,.2f}")

#coluna 3 exibe o total de transações, que é o número de linhas no dataframe de vendas
col3.metric(":yellow[💳 Total de Transações]", f"{len(dados_vendas)}")

#coluna 4 exibe o ticket médio, que é a média do valor das vendas, formatada como moeda
#brasileira
col4.metric(":green[📈 Ticket Médio]", f"R$ {dados_vendas['Vendas'].mean():,.2f}")

st.divider()

#gráfico de resumos
colA, colB = st.columns(2)

#cria um gráfico de pizza para mostrar a distribuição por região
with colA:
    #agrupando os dados por região e soma as vendas
    vendas_regiao = dados_vendas.groupby('Região')['Vendas'].sum().reset_index()
    fig = px.pie(vendas_regiao, names='Região', values='Vendas',
                 title='Distribuição de Vendas por Região',
                 hole=0.4)
    
    #exibir gráfico usando Streamlit
    st.plotly_chart(fig, width='stretch')

with colB:
    #converte a coluna 'Data' para o tipo DateFrame
    dados_vendas['Data'] = pd.to_datetime(dados_vendas['Data'])
    dados_vendas['Mês'] = dados_vendas['Data'].dt.to_period('M').astype(str)

    #agrupa os dados por mês e soma as vendas
    vendas_mensal = dados_vendas.groupby('Mês')['Vendas'].sum().reset_index()
    
    #cria um gráfico de linha para mostrar a evolução mensal das vendas
    fig = px.line(vendas_mensal, x='Mês', y='Vendas',
                  title='Evolução Mensal de Vendas',
                  markers=True)
    
    #exibir gráfico usando Streamlit
    st.plotly_chart(fig, width='stretch')

#Top 5 produtos
st.subheader(":rainbow[🧾 Top 5 Produtos por Receita]")

#Agrupa os dados por produto e soma as vendas, depois de selecionar os 5 produtos com maior
#receita

top5_produtos = dados_vendas.groupby('Produto')['Vendas'].sum().nlargest(5).reset_index()

#Cria um gráfico de barras para mostrar os top 5 produtos por receita, com as barras coloridas
#de acordo com o valor das vendas
#O gráfico tem o título "Top 5 Produtos", o eixo x mostra os nomes dos produtos, o eixo y mostra
#o valor das vendas
fig = px.bar(top5_produtos, x = 'Produto', y = 'Vendas',
             title='Top 5 Produtos',
             color='Vendas',
             color_continuous_scale='pinkyl')

st.plotly_chart(fig, width='stretch')

###############################################################
st.markdown("""
<style>
.stApp {
    background-color: #62227B;
}
</style>
""", unsafe_allow_html=True)
