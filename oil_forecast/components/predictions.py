# pages/predictions.py
import streamlit as st
from utils.utils import show_predictions
import pandas as pd

def show_predictions_page():
    st.header("🔮 Previsões para Datas Futuras")
    
    # Carregamento e tratamento dos dados
    @st.cache_data
    def load_data(file_path):
        # Carregar os dados do arquivo Excel
        data = pd.read_excel(file_path)
        
        # Verificar se a coluna 'data' existe
        if 'data' not in data.columns:
            st.error("A coluna 'data' não foi encontrada no arquivo. Verifique os dados de entrada.")
            st.stop()
    
        # Converter a coluna 'data' para datetime com tratamento de erros
        data['Date'] = pd.to_datetime(data['data'], errors='coerce')
    
        # Verificar se há valores inválidos na coluna 'Date'
        invalid_dates = data['Date'].isnull().sum()
        #if invalid_dates > 0:
        #    st.warning(f"Existem {invalid_dates} valores inválidos na coluna 'data'. Eles serão removidos.")
    
        # Remover linhas com valores nulos na coluna 'Date'
        data = data.dropna(subset=['Date'])
    
        # Verificar se a coluna 'preco' existe
        if 'preco' not in data.columns:
            st.error("A coluna 'preco' não foi encontrada no arquivo. Verifique os dados de entrada.")
            st.stop()
    
        # Renomear e configurar a coluna 'Date' como índice
        data['Price'] = data['preco']
        data.set_index('Date', inplace=True)
        data.sort_index(inplace=True)
    
        # Verificar se o DataFrame está vazio após o tratamento
        if data.empty:
            st.error("O DataFrame está vazio após remover valores inválidos. Verifique os dados de entrada.")
            st.stop()
    
        return data
    
    data = load_data('./data/petroleo.xlsx')
    
    # Definir o número de dias futuros a prever
    forecast_steps = st.slider('Selecione o número de dias para prever', min_value=1, max_value=30, value=30)
    
    # Chamar a função show_predictions
    show_predictions(data, forecast_steps)
