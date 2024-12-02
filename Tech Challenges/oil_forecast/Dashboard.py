import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Configuração da página
#st.set_page_config(page_title="Dashboard Vision Consultoria", layout="wide")

# Logo na sidebar
st.sidebar.image("https://via.placeholder.com/150", width=150)

# Filtros
opcoes_periodo = ["Último Dia", "Última Semana", "Último Mês", "Últimos 12 Meses", "Últimos 5 Anos", "Todo o Período"]

# Carregar dados do CSV
df = pd.read_excel('data/petroleo.xlsx')

# Converter a coluna 'data' para datetime
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

def vision_dashboard_page():
    st.title("Vision")

    col1, col2 = st.columns((1, 3))

    with col2:
        periodo_selecionado = st.selectbox("Selecione o Período", opcoes_periodo)

        # Filtrar dados conforme o período selecionado
        if periodo_selecionado == "Último Dia":
            data_fim = df['data'].max()
            data_inicio = data_fim - pd.Timedelta(days=1)
        elif periodo_selecionado == "Última Semana":
            data_fim = df['data'].max()
            data_inicio = data_fim - pd.Timedelta(weeks=1)
        elif periodo_selecionado == "Último Mês":
            data_fim = df['data'].max()
            data_inicio = data_fim - pd.DateOffset(months=1)
        elif periodo_selecionado == "Últimos 12 Meses":
            data_fim = df['data'].max()
            data_inicio = data_fim - pd.DateOffset(years=1)
        elif periodo_selecionado == "Últimos 5 Anos":
            data_fim = df['data'].max()
            data_inicio = data_fim - pd.DateOffset(years=5)
        elif periodo_selecionado == "Todo o Período":
            data_inicio = df['data'].min()
            data_fim = df['data'].max()

        df_filtrado = df[(df['data'] >= data_inicio) & (df['data'] <= data_fim)]

        # Gráfico de linha usando Plotly para o período filtrado
        st.subheader("Gráfico do Período Selecionado")
        fig = px.line(df_filtrado, x='data', y='preco', title='Evolução de Preços no Período Selecionado', line_shape='linear')
        fig.update_layout(xaxis_title='Data', yaxis_title='Preço')
        st.plotly_chart(fig)

    # Atualizar valores com base nos dados filtrados
    rs_do_dia = df_filtrado['preco'].iloc[-1] if not df_filtrado.empty else 0
    preco_inicio_periodo = df_filtrado['preco'].iloc[0] if not df_filtrado.empty else 0
    variacao_valor = rs_do_dia - preco_inicio_periodo
    variacao_percentual = (variacao_valor / preco_inicio_periodo * 100) if preco_inicio_periodo != 0 else 0
    lista_preco_ultimos_dias = df_filtrado.tail(10)[['data', 'preco']].to_dict('records')

    with col1:
        st.metric(label="Valor do Dia", value=f"R$ {rs_do_dia}", delta=f"{variacao_percentual:.2f}%")
        
        st.subheader("Últimos 10 Dias")
        for item in lista_preco_ultimos_dias:
            st.write(f"Data: {item['data'].strftime('%d/%m/%Y')} - Preço: R$ {item['preco']}")

    col3 = st.columns((1,))[0]

    with col3:
        st.subheader("Previsão Curto Prazo")
        st.write("Previsão entre mês 08/2024 em diante")
        st.markdown("[Deixaria só o modelo que escolhermos](#)")

if __name__: 
    vision_dashboard_page()
