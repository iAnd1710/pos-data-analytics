import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

def calculate_RSI(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    RS = gain / loss
    return 100 - (100 / (1 + RS))

def calculate_MACD(series, short_period=12, long_period=26, signal_period=9):
    short_ema = series.ewm(span=short_period, adjust=False).mean()
    long_ema = series.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_EMA(series, span=20):
    return series.ewm(span=span, adjust=False).mean()

def calculate_ADX(df, window=14):
    high = df['preco']
    low = df['preco']
    close = df['preco']
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = tr.rolling(window).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/window).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1/window).mean() / atr))
    
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = dx.rolling(window=window).mean()
    return adx

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