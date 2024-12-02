import pandas as pd
import numpy as np
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib
import pickle

# -------------------
# Carregar os dados
# -------------------
data = pd.read_excel('data/petroleo.xlsx')

# Converter a coluna 'data' para datetime com tratamento de erros
data['Date'] = pd.to_datetime(data['data'], errors='coerce')
data['Price'] = data['preco']

# Configurar 'Date' como índice
data.set_index('Date', inplace=True)

# Ordenar os dados por data
data.sort_index(inplace=True)

# Preencher valores faltantes com forward fill
data = data.fillna(method='ffill')

# Dividir os dados em treinamento e teste
train = data.iloc[:-180]
test = data.iloc[-180:]

# -------------------
# Treinamento do SARIMA
# -------------------
print("Treinando o modelo SARIMA...")
smodel = pm.auto_arima(
    train['Price'],
    seasonal=True,
    m=12,  # Frequência sazonal (ajuste conforme necessário)
    trace=True,
    error_action='ignore',
    suppress_warnings=True
)
print(smodel.summary())

model_sarima = SARIMAX(
    train['Price'],
    order=smodel.order,
    seasonal_order=smodel.seasonal_order
)
results_sarima = model_sarima.fit()

# Salvar o modelo SARIMA
with open('sarima_model.pkl', 'wb') as f:
    pickle.dump(results_sarima, f)
print("Modelo SARIMA salvo como 'sarima_model.pkl'.")

# -------------------
# Treinamento do XGBoost
# -------------------
print("\nTreinando o modelo XGBoost...")
df = data.copy()

# Criação de features de defasagem (lag features)
for i in range(1, 31):
    df[f'lag_{i}'] = df['Price'].shift(i)

# Remover linhas com valores faltantes resultantes do lag
df = df.dropna()

# Selecionar apenas as lag features para treinamento
X = df[[f'lag_{i}' for i in range(1, 31)]]
y = df['Price']

# Salvar os nomes das features
feature_names = X.columns.tolist()
with open('xgb_features.pkl', 'wb') as f:
    pickle.dump(feature_names, f)
print(f"Nomes das features salvos: {feature_names}")

# Dividir em conjuntos de treinamento e teste
X_train = X.iloc[:-180]
X_test = X.iloc[-180:]
y_train = y.iloc[:-180]
y_test = y.iloc[-180:]

# Escalonar os dados
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar o modelo XGBoost
model_xgb = XGBRegressor(objective='reg:squarederror', n_estimators=500, random_state=42)
model_xgb.fit(X_train_scaled, y_train)
print("\nModelo XGBoost treinado.")

# Salvar o modelo XGBoost e o escalonador
joblib.dump(model_xgb, 'xgb_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
print("Modelo XGBoost salvo como 'xgb_model.joblib'.")
print("Scaler salvo como 'scaler.joblib'.")
