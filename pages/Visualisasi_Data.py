# Redefine updated Visualisasi_Data.py with CSV upload feature added
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
    "1. XGBoost-Default - Train",
    "2. XGBoost-Default - Test",
    "3. XGBoost-Default - All",
    "4. XGBoost-PSO - Train",
    "5. XGBoost-PSO - Test",
    "6. XGBoost-PSO - All",
    "7. XGBoost-GridSearchCV - Train",
    "8. XGBoost-GridSearchCV - Test",
    "9. XGBoost-GridSearchCV - All",
    "10. Semua Model - Train",
    "11. Semua Model - Test",
    "12. Semua Model - All",
    "13. Forecasting Harga Penutupan (mulai 30 Des 2024)",
    "14. Perbandingan Harga Aktual vs Prediksi ke Depan"
]

selected_option = st.sidebar.selectbox("Pilih Jenis Visualisasi", visualization_options)

use_custom_csv = st.sidebar.checkbox("Gunakan File CSV Upload")
uploaded_csv = None
df_uploaded = None
if use_custom_csv:
    uploaded_csv = st.sidebar.file_uploader("Upload CSV dengan kolom: Date, Open, High, Low, Close, Next_Day_Close", type="csv")
    if uploaded_csv is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_csv)
            required_cols = {"Date", "Open", "High", "Low", "Close", "Next_Day_Close"}
            if required_cols.issubset(df_uploaded.columns):
                df_uploaded["Date"] = pd.to_datetime(df_uploaded["Date"])
                st.success("✅ File CSV berhasil dimuat.")
            else:
                st.warning("❌ File tidak memiliki semua kolom yang dibutuhkan.")
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

def plot_multiple_models(df_dict, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    for label, df in df_dict.items():
        ax.plot(df["Date"], df["Predicted"], label=f"{label}", marker='x')
    ax.plot(list(df_dict.values())[0]["Date"], list(df_dict.values())[0]["Actual"], label="Harga Aktual", color='black')
    ax.set_title(title)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga Penutupan")
    ax.legend()
    st.pyplot(fig)

# --- Visualisasi Berdasarkan Pilihan ---
def run_visualization(selected_option):
    model_map = {
        "Default": "Model XGBoost Default",
        "PSO": "Model XGBoost PSO",
        "Grid": "Model XGBoost GridSearchCV"
    }

    # Load data sesuai opsi
    if df_uploaded is not None:
        df = df_uploaded.copy()
    elif "Train" in selected_option:
        df = get_data_train()
    elif "Test" in selected_option:
        df = get_data_test()
    elif "All" in selected_option:
        df = pd.concat([get_data_train(), get_data_test()])
    else:
        df = None

    # Visualisasi per model
    for key in model_map:
        if key in selected_option:
            model = load_model(model_map[key])
            df["Predicted"] = predict_dataframe(model, df)
            df_ = pd.DataFrame({
                "Date": df["Date"],
                "Actual": df["Next_Day_Close"],
                "Predicted": df["Predicted"]
            })
            plot_comparison(df_, f"{model_map[key]} - {selected_option.split('-')[-1].strip()}")
            return

    # Visualisasi semua model
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
        plot_multiple_models(df_dict, f"Perbandingan {selected_option}")

    # Forecasting Masa Depan
    if "Forecasting" in selected_option or "ke Depan" in selected_option:
        model_name = st.selectbox("Pilih Model untuk Forecasting", list(model_map.values()))
        model = load_model(model_name)
        days = st.slider("Jumlah Hari Prediksi ke Depan", min_value=7, max_value=180, value=30, step=1)

        all_data = get_data_train()
        last_known = all_data.iloc[-1][["Open", "High", "Low", "Close"]].to_dict()

        forecast_df = forecast_future(model, last_known, days)
        forecast_df["Predicted"] = forecast_df["Close"]

        if "ke Depan" in selected_option:
            df_test = get_data_test()
            merged = pd.merge(forecast_df, df_test[["Date", "Next_Day_Close"]], on="Date", how="left")
            merged = merged.rename(columns={"Next_Day_Close": "Actual"})
            plot_comparison(merged, f"Perbandingan Prediksi vs Aktual ke Depan ({model_name})")
        else:
            forecast_df["Actual"] = None
            plot_comparison(forecast_df, f"Forecasting {model_name} ({days} hari ke depan)")

run_visualization(selected_option)
