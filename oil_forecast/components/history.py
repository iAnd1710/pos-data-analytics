import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime\

def show_history():
    st.title("🕰️ Histórico de Preços do Petróleo Brent")
    
    # Obtendo dados de exemplo
    DATA_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/petroleo.xlsx'))

    df_brent_oil = pd.read_excel(DATA_FILE_PATH)
    
    # Criando o gráfico de linha para a série temporal
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_brent_oil['data'],
        y=df_brent_oil['preco'],
        mode='lines',
        line=dict(color='#E4292B'),
        name='Preço do Petróleo Brent'
    ))

    # Eventos históricos
    events = {
        '2003-03-20': 'Início da Guerra no Iraque',
        '2008-09-15': 'Crise Financeira Global',
        '2010-12-18': 'Primavera Árabe',
        '2014-11-20': 'OPEP não corta produção, preço cai',
        '2016-01-04': 'Acordo de Corte da OPEP',
        '2020-03-06': 'Pandemia de COVID-19',
        '2022-02-24': 'Invasão da Ucrânia pela Rússia'
    }

    # Adicionando eventos como marcadores numerados
    for i, (date, event) in enumerate(events.items(), 1):
        date = pd.to_datetime(date)
        if date not in df_brent_oil['data'].values:
            continue
        close_price = df_brent_oil.loc[df_brent_oil['data'] == date, 'preco'].values[0]
        offset_price = close_price + 5  # Elevar o marcador para melhor visibilidade

        # Linha tracejada conectando o marcador ao preço
        fig.add_trace(go.Scatter(
            x=[date, date],
            y=[close_price, offset_price],
            mode='lines',
            line=dict(color='gray', dash='dot'),
            showlegend=False
        ))

        # Adicionando o marcador numerado
        fig.add_trace(go.Scatter(
            x=[date],
            y=[offset_price],
            mode='markers+text',
            marker=dict(size=15, color='blue'),
            text=str(i),
            textposition='middle center',
            textfont=dict(color='white', size=12),
            showlegend=False
        ))

    # Configurando o layout do gráfico
    fig.update_layout(
        title='Preço Histórico do Petróleo Brent com Eventos Importantes',
        xaxis_title='Data',
        yaxis_title='Preço de Fechamento (USD)',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='date'
        )
    )

    # Mostrar o gráfico no Streamlit
    st.plotly_chart(fig)

    # Adicionar a legenda com descrição dos eventos
    st.subheader("Descrição dos Eventos")
    for i, (date, event) in enumerate(events.items(), 1):
        st.markdown(f"**{i}. {date}** - {event}")