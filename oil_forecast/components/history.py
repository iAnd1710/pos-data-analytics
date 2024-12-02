import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

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
        '1990-01-03': 'Guerra do Golfo',
        '1999-01-04': 'Corte na produção',
        '2003-03-20': 'Início da Guerra no Iraque',
        '2008-07-01': 'Crise Financeira Global',
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
    event_descriptions = {
        '1990-01-03': 'Guerra do Golfo: A invasão do Kuwait pelo Iraque elevou o preço do petróleo em 229%, alcançando US$ 41,90. A guerra visava o controle da produção, e o Iraque incendiou campos de petróleo na derrota.',
        '1999-01-04': 'Corte na produção: O preço aumentou 100,3% devido à crise nos Tigres Asiáticos, cortes de produção pela Opep e recuperação econômica global.',
        '2003-03-20': 'Início da Guerra no Iraque: A guerra começou em 2003 com a invasão liderada pelos EUA no Iraque. Aumentou a instabilidade no Oriente Médio.',
        '2008-07-01': 'Crise Financeira Global: Em julho de 2008, o petróleo alcançou US$ 147 por barril, impulsionado por alta demanda e tensões geopolíticas. Com a crise financeira global, os preços caíram drasticamente no final do ano. A Opep respondeu com cortes na produção, e estímulos econômicos globais impulsionaram uma recuperação de 56,66% entre fevereiro e junho de 2009.',
        '2010-12-18': 'Primavera Árabe: Uma série de protestos e revoltas no mundo árabe afetou a produção e os preços do petróleo.',
        '2014-11-20': 'OPEP não corta produção, preço cai: A decisão da OPEP de não cortar a produção levou a uma queda significativa nos preços do petróleo.',
        '2016-01-04': 'Acordo de Corte da OPEP: A OPEP e outros produtores concordaram em cortar a produção para estabilizar os preços.',
        '2020-03-06': 'Pandemia de COVID-19: Queda de 54,25% no preço devido à baixa demanda global. Com cortes de produção e estoques, houve rápida recuperação, com alta de 103,75% entre maio e agosto.',
        '2022-02-24': 'Invasão da Ucrânia pela Rússia: A invasão russa na Ucrânia causou preocupações com o fornecimento de energia e aumentou os preços do petróleo. A guerra causou alta de 58,13% entre dezembro de 2021 e maio de 2022, com aumento total de 111,3% em dois anos.'
    }

    for i, (date, event) in enumerate(events.items(), 1):
        formatted_date = pd.to_datetime(date).strftime('%d/%m/%Y')
        st.markdown(f"**{i}. {formatted_date}** - {event_descriptions[date]}")

if __name__ == "__main__":
    show_history()
