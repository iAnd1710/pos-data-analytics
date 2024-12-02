# utils.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from statsmodels.tsa.statespace.sarimax import SARIMAX
import streamlit as st

def show_predictions(data, forecast_steps=30):
    """
    Função para realizar previsões futuras e visualizar os resultados.
    
    Parâmetros:
    - data (pd.DataFrame): DataFrame contendo os dados históricos com índice de datas.
    - forecast_steps (int): Número de dias futuros a prever.
    """
    
    # -------------------
    # Carregamento dos Modelos
    # -------------------
    MODEL_SARIMA_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sarima_model.pkl'))
    MODEL_XGB_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xgb_model.joblib'))
    SCALER_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scaler.joblib'))
    XGB_FEATURES_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xgb_features.pkl'))
    
    try:
        # Carregar o modelo SARIMA
        with open(MODEL_SARIMA_FILE_PATH, 'rb') as f:
            results_sarima = pickle.load(f)
    except FileNotFoundError:
        st.error("O arquivo 'sarima_model.pkl' não foi encontrado. Certifique-se de que o modelo SARIMA foi treinado e salvo corretamente.")
        return
    except Exception as e:
        st.error(f"Erro ao carregar o modelo SARIMA: {e}")
        return
    
    try:
        # Carregar o modelo XGBoost, scaler e feature names
        model_xgb = joblib.load(MODEL_XGB_FILE_PATH)
        scaler = joblib.load(SCALER_FILE_PATH)
        with open(XGB_FEATURES_FILE_PATH, 'rb') as f:
            feature_names = pickle.load(f)
    except FileNotFoundError as e:
        st.error(f"Arquivo não encontrado: {e}")
        return
    except Exception as e:
        st.error(f"Erro ao carregar os arquivos do XGBoost: {e}")
        return
    
    # -------------------
    # Previsão com SARIMA
    # -------------------
    # Calcular a última data no índice do DataFrame
    try:
        last_date = data.index[-1]
        if pd.isnull(last_date):
            raise ValueError("O índice do DataFrame não contém uma última data válida.")
    except IndexError:
        st.error("O DataFrame está vazio. Não é possível calcular a última data.")
        return
    
    # Gerar as datas futuras
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    
    # Fazer a previsão SARIMA
    forecast_sarima = results_sarima.forecast(steps=forecast_steps)
    forecast_sarima = pd.Series(forecast_sarima.values, index=future_dates)
    
    # -------------------
    # Previsão com XGBoost (Previsão Recursiva)
    # -------------------
    forecast_xgb = []
    last_lags = data['Price'][-30:].values.tolist()
    
    # Verificar se as features estão alinhadas
    expected_features = [f'lag_{i}' for i in range(1, 31)]
    if feature_names != expected_features:
        st.error(f"As features salvas não correspondem às esperadas: {feature_names} vs. {expected_features}")
        return
    
    for _ in range(forecast_steps):
        # Criar o DataFrame com as lag features
        input_features = np.array(last_lags[-30:]).reshape(1, -1)
        
        # Validar se o tamanho de input_features corresponde ao tamanho de feature_names
        if len(feature_names) != input_features.shape[1]:
            st.error(f"Desalinhamento entre número de features ({len(feature_names)}) e shape de input_features ({input_features.shape[1]}).")
            return
    
        input_df = pd.DataFrame(input_features, columns=feature_names)
        
        # Escalar as features
        input_scaled = scaler.transform(input_df)
        
        # Fazer a previsão
        pred = model_xgb.predict(input_scaled)[0]
        
        # Adicionar a previsão à lista
        forecast_xgb.append(pred)
        
        # Atualizar as lag features com a nova previsão
        last_lags.append(pred)
    
    forecast_xgb = pd.Series(forecast_xgb, index=future_dates)
    
    # -------------------
    # Visualização das Previsões
    # -------------------
    
    fig_future = go.Figure()

    last_180_days = data.iloc[-180:]
    
    # Dados históricos
    fig_future.add_trace(go.Scatter(
        x=last_180_days.index,
        y=last_180_days['Price'],
        mode='lines',
        name='Dados Históricos',
        line=dict(color='blue')
    ))
    
    # Previsão SARIMA
    '''fig_future.add_trace(go.Scatter(
        x=forecast_sarima.index,
        y=forecast_sarima.values,
        mode='lines',
        name='Previsão SARIMA',
        line=dict(color='orange')
    ))
    '''
    
    # Previsão XGBoost
    fig_future.add_trace(go.Scatter(
        x=forecast_xgb.index,
        y=forecast_xgb.values,
        mode='lines',
        name='Previsão XGBoost',
        line=dict(color='red')
    ))
    
    fig_future.update_layout(
        title='Previsões de Preço do Petróleo Brent para Datas Futuras',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        template='plotly_white',
        legend=dict(x=1, y=1, bgcolor='rgba(0,0,0,0)')
    )
    
    st.plotly_chart(fig_future, use_container_width=True)
    
    # -------------------
    # Tabela de Previsões Futuras
    # -------------------
    st.subheader('📊 Tabela de Previsões Futuras')
    
    forecast_df = pd.DataFrame({
        'Data': future_dates,
        'Previsão SARIMA': forecast_sarima.values,
        'Previsão XGBoost': forecast_xgb.values
    })
    forecast_df.set_index('Data', inplace=True)
    st.dataframe(forecast_df.style.format({
        "Previsão SARIMA": "{:.2f}",
        "Previsão XGBoost": "{:.2f}"
    }))
