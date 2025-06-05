# importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# calcula o faturamento em cada linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# título
st.title("Dashboard de Vendas")

# filtros na lateral
st.sidebar.header("Filtros")
lojas = sorted(dados['Loja'].unique())
loja_escolhida = st.sidebar.selectbox('Escolha a loja:', lojas)

produtos = ['Todos'] + sorted(dados['Produto'].unique())
produto_escolhido = st.sidebar.selectbox('Escolha o produto:', produtos)

# aplicar filtros
dados_filtrados = dados[dados['Loja'] == loja_escolhida]
if produto_escolhido != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'] == produto_escolhido]

# exibir tabela de vendas filtrada
st.write("Tabela de vendas do mês (após filtro):")
st.dataframe(dados_filtrados)

# faturamento total embaixo da tabela
faturamento_total = dados_filtrados['Faturamento'].sum()
faturamento_total_texto = f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
st.markdown(f"**Faturamento total: {faturamento_total_texto}**")

# gráfico de barras por loja 
dados_agrupados = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)
grafico = px.bar(dados_agrupados, x='Loja', y='Faturamento', title='Faturamento por Loja')
st.plotly_chart(grafico)

# gráfico de pizza 
if produto_escolhido != 'Todos':
    # gráfico de pizza com 100% para o produto selecionado
    grafico_pizza = px.pie(
        names=[produto_escolhido],
        values=[faturamento_total],
        title=f"Participação do produto '{produto_escolhido}' na loja {loja_escolhida}"
    )
else:
    # participação de todos os produtos
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

# texto do gráfico
if produto_escolhido == 'Todos':
    texto = f"Na loja {loja_escolhida}, o faturamento total considerando todos os produtos foi de {faturamento_total_texto}."
else:
    texto = f"Na loja {loja_escolhida}, o produto '{produto_escolhido}' teve um faturamento total de {faturamento_total_texto}."
st.info(texto)
