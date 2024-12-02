import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime
'''def show_history():
    st.title("🕰️ Histórico")
    st.markdown("Eventos históricos que influenciaram os preços do petróleo.")
    
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
    
    # Gráfico com eventos históricos
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['preco'],
        mode='lines',
        name='Preço do Petróleo',
        line=dict(color='blue')
    ))
    
    # Eventos históricos
    eventos = {
        '2008-09-15': 'Crise Financeira Global',
        '2011-03-01': 'Primavera Árabe',
        '2014-11-20': 'Queda de Preços da OPEP',
        '2016-01-04': 'Acordo de Corte da OPEP',
        '2020-03-06': 'Pandemia de COVID-19',
        '2022-02-24': 'Conflito Rússia-Ucrânia',
        '2023-02-01': 'Tensões no Oriente Médio'
    }
    
    for data_str, descricao in eventos.items():
        data_evento = pd.to_datetime(data_str)
        # Encontrar o preço mais próximo da data do evento
        df_evento = df.loc[df['data'] == data_evento]
        if not df_evento.empty:
            preco_evento = df_evento['preco'].values[0]
            fig.add_trace(go.Scatter(
                x=[data_evento],
                y=[preco_evento],
                mode='markers+text',
                name=descricao,
                text=[descricao],
                textposition='top center',
                marker=dict(size=10, color='red')
            ))
    
    fig.update_layout(
        title='Preço Histórico do Petróleo com Eventos Importantes',
        xaxis_title='Data',
        yaxis_title='Preço (USD)'
    )
    
    st.plotly_chart(fig)
    
    # Descrição dos eventos
    st.subheader("Descrição dos Eventos")
    for data_str, descricao in eventos.items():
        st.markdown(f"**{data_str}** - {descricao}")
'''

def show_history():
    st.title("🕰️ Histórico de Preços do Petróleo Brent")
    
    # Obtendo dados de exemplo
    df_brent_oil = pd.read_excel('data/petroleo.xlsx')
    
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