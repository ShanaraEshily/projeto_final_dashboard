import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    #Carregar dados de vendas
    df = pd.read_csv('dados/vendas.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

#utiliza a função para carregar os dados e armazena em uma variável
#para uso posterior
#DataFrame do PANDAS que contém os dados de vendas
dados_vendas = carregar_dados()

st.title('𖠩 Análise Detalhada de Vendas')

#Filtros para análise
st.sidebar.header("🏪 Filtros de Vendas")

#Data: 16/03/2026

st.markdown("""
<style>
span[data-baseweb="tag"] {
  background-color: blue !important;
}
</style>
""", unsafe_allow_html=True) #colocar antes dos filtros pra dar cor

regioes = st.sidebar.multiselect(
    "Selecione as Regiões:",
    options=dados_vendas["Região"].unique(),
    default=dados_vendas["Região"].unique()
)

categorias = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=dados_vendas["Categoria"].unique(),
    default=dados_vendas["Categoria"].unique()
)

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

#aplicando os filtros selecionados pelo usuário para criar um dataframe filtrado
dados_filtrados = dados_vendas[
    (dados_vendas["Região"].isin(regioes)) &
    (dados_vendas["Categoria"].isin(categorias)) &
    (dados_vendas["Data"].between(
        data_inicio,
        data_fim
        ))
]

#métricas filtradas
col1, col2, col3 = st.columns(3)
col1.metric("Receita Filtrada", f"R$ {dados_filtrados['Vendas'].sum():,.0f}")
col2.metric("Lucro Filtrado", f"R$ {dados_filtrados['Lucro'].sum():,.0f}")

#calcula a margem média como a soma do lucro dividido pela soma das vendas, multiplicado por
#100
margem_media = 'N/A '
if dados_filtrados['Vendas'].sum() > 0:
    margem_media = (dados_filtrados['Lucro'].sum()/dados_filtrados['Vendas'].sum()*100)

col3.metric("Margem Média", f"{margem_media}%")

#Vendas por vendedor
#A análise de perfomance por vendedor é realizada agrupando os dados filtrados pelo nome do
#vendedor e calculando as seguintes métricas:
# - Receita: soma das vendas para cada vendedor
# - Lucro: soma do lucro para cada vendedor
# - Transações: contagem do número de vendas para cada vendedor
# - Ticket Médio: média do valor das vendas para cada vendedor
#Os resultados são arrendondados para 2 casas decimais e ordenados pela receita em ordem
#decrescente para destacar os vendedores com melhor performance.
st.subheader("𐦂𖨆𐀪𖠋 Perfomance por Vendedor")
vendas_vendedor = dados_filtrados.groupby("Vendedor").agg(
    Receita = ("Vendas", "sum"),
    Lucro = ("Lucro", "sum"),
    Transacoes = ("Vendas", "count"),
    Ticket_Medio =("Vendas", "mean")
).round(2).sort_values(by = "Receita", ascending=False)

v_col1,v_col2 = st.columns(2)

with v_col1:
    st.dataframe(vendas_vendedor, width='stretch')

with v_col2:
    fig = px.bar(
        vendas_vendedor.reset_index(),
        x = "Vendedor",
        y = "Receita",
        title= "Receita e Lucro por Vendedor",
        color="Lucro",
        color_continuous_scale=px.colors.sequential.Blues
    )
    st.plotly_chart(fig, width='stretch')

#Análise temporal de vendas
st.subheader("🗓 Análise Temporal")

#Cria uma nova coluna 'Mês' no dataframe filtrado, extraindo o mês e ano da coluna "Data"
#A função dt.to_period("M") converte a data para um período mensal, e astype(str) converte
#esse período para uma string no formato 'YYYY-MM'.
#Em seguida, os dados são agrupados por essa nova coluna 'Mês' para calcular a receita e o 
#lucro total para cada mês, resultando em um dataframe mensal que pode ser usado para análise
#temporal
dados_filtrados['Mês'] = dados_filtrados['Data'].dt.to_period('M').astype(str)
mensal = dados_filtrados.groupby('Mês').agg(
    Receita = ('Vendas', 'sum'),
    Lucro = ('Lucro', 'sum')
).reset_index()

#Cria um gráfico de barras para comparar a receita e o lucro mensal, usando a coluna 'Mês' no
#eixo x e as colunas 'Receita' e 'Lucro' no eixo y. O parâmetro barmode='group' é usado para
#exibir as barras de receita e lucro lado a lado para cada mês, facilitando a comparação como
#'Receita x Lucro Mensal'
fig = px.bar(
    mensal, x='Mês', y=['Receita', 'Lucro'],
    barmode='group', title='Receita x Lucro Mensal'
)

#O método update_layout é usado para ajustar a aparência do gráfico, e o parâmetro 
#xaxis_tickangle=-45 é utilizado para rotacionar os rótulos do eixo x em um âmgulo de -45 
#graus, o que pode ajudar a melhorar a legibilidade dos rótulos, especialmente quando há 
#muitos meses ou quando os rótulos são longos. Essa rotação evita que os rótulos se sobrepunham
#e torna o gráfico mais fácil de interpretar.
fig.update_layout(xaxis_tickangle=-45)

#Exibe o gráfico usando o Streamlit, com a largura configurada para se estender ao máximo do
#contêiner disponível.
st.plotly_chart(fig, width='stretch')

dados_filtrados['Mês'] = dados_filtrados['Data'].dt.to_period('M').astype(str)
with st.expander("Dados Detalhados"):
    st.dataframe(dados_filtrados)

    @st.cache_data
    def convert_for_download(df):
        return df.to_csv().encode("utf-8")

    csv = convert_for_download(dados_filtrados)

    st.download_button(
        label="Download Dados Detalhados",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv",
        icon="⬇️"
    )

#➜]

