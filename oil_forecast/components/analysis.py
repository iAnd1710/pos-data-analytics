import streamlit as st
import pandas as pd
import plotly.express as px
import os

import plotly.express as px
import re
from decimal import Decimal

def clean_production_value(value):
            cleaned_value = str(value).replace(".", "").replace("--", "0")
            try:
                return int(cleaned_value)
            except ValueError:
                return None
            
def show_analysis():
    st.title("📈 Análise de Dados")
    st.markdown("Análise detalhada dos preços históricos do petróleo.")

    tab1,tab2 = st.tabs(["Guia 1", "Guia 2"])

    with tab1:
        # Caminho para o arquivo de dados
        DATA_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/petroleo.xlsx'))
        
        # Carregar dados do Excel
        try:
            df = pd.read_excel(DATA_FILE_PATH)
        except FileNotFoundError:
            st.error(f"O arquivo 'petroleo.xlsx' não foi encontrado na pasta 'data'.")
            return
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
            return
        
        # Converter a coluna 'data' para datetime
        try:
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        except Exception as e:
            st.error(f"Erro ao converter a coluna 'data' para datetime: {e}")
            return
        
        # Renomear colunas para garantir consistência
        df.rename(columns={
            'Close': 'preco',
            'Close.1': 'preco',
            # Adicione outras renomeações se houver
        }, inplace=True)
        
        # Filtros
        opcoes_periodo = ["Último Dia", "Última Semana", "Último Mês", "Últimos 12 Meses", "Últimos 5 Anos", "Todo o Período"]
        periodo_selecionado = st.selectbox("Selecione o Período", opcoes_periodo)
        
        # Filtrar dados conforme o período selecionado
        data_fim = df['data'].max()
        if periodo_selecionado == "Último Dia":
            data_inicio = data_fim - pd.Timedelta(days=1)
        elif periodo_selecionado == "Última Semana":
            data_inicio = data_fim - pd.Timedelta(weeks=1)
        elif periodo_selecionado == "Último Mês":
            data_inicio = data_fim - pd.DateOffset(months=1)
        elif periodo_selecionado == "Últimos 12 Meses":
            data_inicio = data_fim - pd.DateOffset(years=1)
        elif periodo_selecionado == "Últimos 5 Anos":
            data_inicio = data_fim - pd.DateOffset(years=5)
        elif periodo_selecionado == "Todo o Período":
            data_inicio = df['data'].min()
        
        df_filtrado = df[(df['data'] >= data_inicio) & (df['data'] <= data_fim)]
        
        if df_filtrado.empty:
            st.warning("Não há dados disponíveis para o período selecionado.")
            return
        
        # Gráfico de linha usando Plotly para o período filtrado
        st.subheader("Evolução de Preços no Período Selecionado")
        fig = px.line(df_filtrado, x='data', y='preco', title='', line_shape='linear')
        fig.update_layout(xaxis_title='Data', yaxis_title='Preço (USD)')
        st.plotly_chart(fig)
        
        # Cálculo de métricas
        preco_atual = df_filtrado['preco'].iloc[-1]
        preco_inicio_periodo = df_filtrado['preco'].iloc[0]
        variacao_valor = preco_atual - preco_inicio_periodo
        variacao_percentual = (variacao_valor / preco_inicio_periodo * 100) if preco_inicio_periodo != 0 else 0
        
        col1, col2 = st.columns(2)
        col1.metric(label="Preço Atual", value=f"U$D {preco_atual:.2f}", delta=f"{variacao_percentual:.2f}%")
        col2.metric(label="Variação no Período", value=f"U$D {variacao_valor:.2f}")
        
        # Exibir últimos registros
        st.subheader("Últimos 10 Registros")
        st.dataframe(df_filtrado.tail(10).sort_values(by='data', ascending=False))

    with tab2:
        DATA_PROD_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/producao_petroleo.csv'))
        df_prod = pd.read_csv(DATA_PROD_FILE_PATH)
        df_prod['Producao'] = df_prod['Producao'].apply(clean_production_value)
        df_prod['Producao_milhoes_bpd'] = df_prod['Producao'] / Decimal('1000000')

        #Anos de 2000 a 2023
        anos_filtrados = [ano for ano in range(2000, 2024)]

        df_filtrado = df_prod[df_prod['Ano'].isin(anos_filtrados)]

        df_filtrado = df_filtrado.dropna(subset=['Producao_milhoes_bpd'])

        df_filtrado['Producao_milhoes_bpd'] = df_filtrado['Producao_milhoes_bpd'].astype(float)

        fig_2 = px.choropleth(df_filtrado,
                        locations='Pais',
                        locationmode='country names',
                        color='Producao_milhoes_bpd',
                        hover_name='Pais',
                        color_continuous_scale='YlOrRd',
                        animation_frame='Ano',
                        range_color=[0, df_filtrado['Producao_milhoes_bpd'].max() * 1.2],
                        title='Produção de Petróleo (milhões de barris/ano) por País - 2000 a 2023',
                        labels={'Producao_milhoes_bpd': 'Produção (milhões de barris/ano)'},
                        projection='natural earth')

        fig_2.update_layout(
            coloraxis_colorbar=dict(
                title="Produção",
                title_side="right"
            )
        )

        st.plotly_chart(fig_2)

        # Grafico de barras
        df_filtrado = df_prod[(df_prod['Ano'] >= 2000) & (df_prod['Ano'] <= 2023)]

        df_grouped = df_filtrado.groupby('Pais')['Producao_milhoes_bpd'].mean().reset_index()

        top_10 = df_grouped.sort_values('Producao_milhoes_bpd', ascending=False).head(10)

        fig_3 = px.bar(top_10, x='Pais', y='Producao_milhoes_bpd',
                    color_discrete_sequence=["green"],
                    labels={'Producao_milhoes_bbd': 'Produção média anual (milhões de barris/dia)'},
                    title='Top 10 Maiores Produtores de Petróleo (2000 a 2023) | Produção Média Anual (milhões de barris/dia)')
        
        st.plotly_chart(fig_3)