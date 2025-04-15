import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

# Konstanta nilai minimum dan maksimum
MIN_VALUE = 784.91
MAX_VALUE = 2271.54

# Path model dari CSV
MODELS_PATH = {
    "Model XGBoost Default": "models/xgboost_model_default_params.csv",
    "Model XGBoost GridSearchCV": "models/xgboost_model_gridsearchcv_params.csv", 
    "Model XGBoost PSO": "models/xgboost_pso_params.csv"
}

TRAIN_DATA_PATH = "models/train_data.csv"
TEST_DATA_PATH = "models/test_data.csv"

# --- Normalisasi & Invers ---
def custom_min_max_scaler(value, min_value=MIN_VALUE, max_value=MAX_VALUE):
    return 1 - ((value - min_value) / (max_value - min_value))

def inverse_scaler(scaled_value, min_value=MIN_VALUE, max_value=MAX_VALUE):
    return max_value - (scaled_value * (max_value - min_value))

# --- Load Model ---
def load_model(model_name):
    model_path = MODELS_PATH.get(model_name)
    if not model_path:
        raise ValueError("Model tidak ditemukan dalam daftar MODELS_PATH.")
    
    try:
        model_params = pd.read_csv(model_path)
        params_dict = model_params.set_index("Parameter")["Value"].to_dict()

        params_dict["max_depth"] = int(float(params_dict.get("max_depth", 6)))
        params_dict["n_estimators"] = int(float(params_dict.get("n_estimators", 100)))
        params_dict["min_child_weight"] = float(params_dict.get("min_child_weight", 1))
        params_dict["gamma"] = float(params_dict.get("gamma", 0))
        params_dict["reg_lambda"] = float(params_dict.get("reg_lambda", 1))
        params_dict["learning_rate"] = float(params_dict.get("learning_rate", 0.3))
        params_dict["subsample"] = float(params_dict.get("subsample", 1))
        params_dict["colsample_bytree"] = float(params_dict.get("colsample_bytree", 1))

        model = XGBRegressor(**params_dict)
        train_data = pd.read_csv(TRAIN_DATA_PATH)
        
        X_train = train_data[[ 
            "('Open', 'KLBF.JK')", 
            "('High', 'KLBF.JK')", 
            "('Low', 'KLBF.JK')", 
            "('Close', 'KLBF.JK')"
        ]]
        y_train = train_data['Next_Day_Close']
        X_train_normalized = X_train.applymap(custom_min_max_scaler)
        model.fit(X_train_normalized, y_train)
        return model
    except Exception as e:
        raise ValueError(f"❌ Terjadi kesalahan: {str(e)}")

# --- Prediksi Single Input ---
def predict(model, open_price, high_price, low_price, close_price):
    input_data = np.array([[
        custom_min_max_scaler(float(open_price)),
        custom_min_max_scaler(float(high_price)),
        custom_min_max_scaler(float(low_price)),
        custom_min_max_scaler(float(close_price))
    ]])
    prediction = model.predict(input_data)
    return prediction[0]

# --- Prediksi Batch (DataFrame) ---
def predict_dataframe(model, df):
    X = df[["Open", "High", "Low", "Close"]].copy()
    X_scaled = X.applymap(custom_min_max_scaler)  # ✅ fixed
    predictions = model.predict(X_scaled)
    return predictions

# --- Load Data Train ---
def get_data_train():
    df = pd.read_csv(TRAIN_DATA_PATH)
    return pd.DataFrame({
        "Date": pd.date_range(end="2024-12-01", periods=len(df)),  # placeholder
        "Open": df["('Open', 'KLBF.JK')"],
        "High": df["('High', 'KLBF.JK')"],
        "Low": df["('Low', 'KLBF.JK')"],
        "Close": df["('Close', 'KLBF.JK')"],
        "Next_Day_Close": df["Next_Day_Close"]
    })

# --- Load Data Test ---
def get_data_test():
    df = pd.read_csv(TEST_DATA_PATH)
    return pd.DataFrame({
        "Date": pd.date_range(start="2024-12-02", periods=len(df)),  # placeholder
        "Open": df["('Open', 'KLBF.JK')"],
        "High": df["('High', 'KLBF.JK')"],
        "Low": df["('Low', 'KLBF.JK')"],
        "Close": df["('Close', 'KLBF.JK')"],
        "Next_Day_Close": df["Next_Day_Close"]
    })

# --- Forecasting Ke Depan ---
def forecast_future(model, last_row, days=30):
    forecast_results = []
    current_input = last_row.copy()

    for i in range(days):
        input_scaled = np.array([[
            custom_min_max_scaler(current_input["Open"]),
            custom_min_max_scaler(current_input["High"]),
            custom_min_max_scaler(current_input["Low"]),
            custom_min_max_scaler(current_input["Close"])
        ]])
        prediction = model.predict(input_scaled)[0]

        next_day = {
            "Date": pd.to_datetime("2024-12-30") + pd.Timedelta(days=i),
            "Open": current_input["Open"],
            "High": current_input["High"],
            "Low": current_input["Low"],
            "Close": prediction
        }
        forecast_results.append(next_day)
        current_input["Close"] = prediction

    return pd.DataFrame(forecast_results)
