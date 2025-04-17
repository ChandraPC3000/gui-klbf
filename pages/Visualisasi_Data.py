import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from predict import (
    load_model, predict_dataframe, get_data_train, get_data_test, forecast_future
)

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide")
st.title("Visualisasi Prediksi Saham KLBF.JK")
st.write("Pilih jenis visualisasi yang ingin ditampilkan.")

# --- Opsi Visualisasi ---
visualization_options = [
    "1. XGBoost-Default - Test",
    "2. XGBoost-PSO - Test",
    "3. XGBoost-GridSearchCV - Test",
    "4. Semua Model - Test"
]

selected_option = st.sidebar.selectbox("Pilih Jenis Visualisasi", visualization_options)

use_custom_csv = st.sidebar.checkbox("Gunakan File CSV Upload")
uploaded_csv = None
df_uploaded = None
if use_custom_csv:
    uploaded_csv = st.sidebar.file_uploader("Upload CSV: Date, Close, High, Low, Open, Volume", type="csv")
    if uploaded_csv is not None:
        try:
            df_uploaded_raw = pd.read_csv(uploaded_csv)
            required_cols = {"Date", "Open", "High", "Low", "Close"}
            if required_cols.issubset(df_uploaded_raw.columns):
                df_uploaded = pd.DataFrame({
                    "Date": pd.to_datetime(df_uploaded_raw["Date"]),
                    "Open": df_uploaded_raw["Open"],
                    "High": df_uploaded_raw["High"],
                    "Low": df_uploaded_raw["Low"],
                    "Close": df_uploaded_raw["Close"],
                    "Next_Day_Close": df_uploaded_raw["Close"]  # Asumsi: target = Close
                })
                st.success("✅ File CSV berhasil dimuat dan disesuaikan.")
            else:
                st.warning("❌ File tidak memiliki semua kolom yang dibutuhkan: Date, Close, High, Low, Open")
                df_uploaded = None
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file: {e}")
            df_uploaded = None

# --- Fungsi Visualisasi ---
def plot_comparison(df, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["Date"], df["Actual"], label="Harga Aktual", marker='o', color="blue")
    ax.plot(df["Date"], df["Predicted"], label="Harga Prediksi", marker='x', color="orange")
    ax.set_title(title)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga Penutupan")
    ax.legend()
    st.pyplot(fig)
    st.dataframe(df)

def run_visualization(selected_option):
    model_map = {
        "Default": "Model XGBoost Default",
        "PSO": "Model XGBoost PSO",
        "Grid": "Model XGBoost GridSearchCV"
    }

    # Load data sesuai opsi
    if df_uploaded is not None:
        df = df_uploaded.copy()
    elif "Test" in selected_option:
        df = get_data_test()
    else:
        df = None

    # Visualisasi per model
    for key in model_map:
        if key in selected_option:
            model = load_model(model_map[key])
            df["Predicted"] = predict_dataframe(model, df)

            # Visualisasi untuk Data Test
            df_test_ = pd.DataFrame({
                "Date": df["Date"],
                "Actual": df["Next_Day_Close"],
                "Predicted": df["Predicted"]
            })
            plot_comparison(df_test_, f"{model_map[key]} - Test")
            return  # Hentikan setelah visualisasi model yang dipilih

    # Visualisasi Semua Model - Test
    if "Semua Model" in selected_option:
        df_dict = {}
        for label, name in model_map.items():
            model = load_model(name)
            df["Predicted"] = predict_dataframe(model, df)
            df_dict[label] = pd.DataFrame({
                "Date": df["Date"],
                "Actual": df["Next_Day_Close"],
                "Predicted": df["Predicted"]
            })
        plot_comparison(df_dict, f"Perbandingan Semua Model - Test")

run_visualization(selected_option)
