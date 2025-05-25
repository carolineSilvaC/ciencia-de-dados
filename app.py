# importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# exibindo informações e gráficos: mostrar o título do painel e exibir a tabela
st.title("Dashboard de Vendas")
st.write("Tabela de vendas do mês:")
st.dataframe(dados)

# calcula o faturamento em cada linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# agrupa e ordena o faturamento por loja (do maior para o menor)
dados_agrupados = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

# criar um gráfico de barras com o faturamento por loja
grafico = px.bar(dados_agrupados, x='Loja', y='Faturamento', title='Faturamento por Loja')
st.plotly_chart(grafico)

# filtros: loja e produto
st.sidebar.header("Filtros")
lojas = sorted(dados['Loja'].unique())
loja_escolhida = st.sidebar.selectbox('Escolha a loja:', lojas)

produtos = ['Todos'] + sorted(dados['Produto'].unique())
produto_escolhido = st.sidebar.selectbox('Escolha o produto:', produtos)

# filtrar os dados com base na seleção
dados_filtrados = dados[dados['Loja'] == loja_escolhida]
if produto_escolhido != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'] == produto_escolhido]
    
# faturamento total considerando filtros
faturamento_total = dados_filtrados['Faturamento'].sum()
faturamento_total_texto = f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# gráfico de pizza: participação dos produtos na loja selecionada
dados_loja = dados[dados['Loja'] == loja_escolhida]
faturamento_por_produto = (
    dados_loja.groupby('Produto')['Faturamento']
    .sum()
    .reset_index()
)
grafico_pizza = px.pie(
    faturamento_por_produto,
    names='Produto',
    values='Faturamento',
    title=f'Participação dos produtos no faturamento da loja {loja_escolhida}'
)
st.plotly_chart(grafico_pizza)


# resumo textual
if produto_escolhido == 'Todos':
    texto = f"Na loja {loja_escolhida}, o faturamento total considerando todos os produtos foi de {faturamento_total_texto}."
else:
    texto = f"Na loja {loja_escolhida}, o produto '{produto_escolhido}' teve um faturamento total de {faturamento_total_texto}."
st.info(texto)