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

# Custom CSV Upload
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
            
            if "Train" in selected_option:
                df_ = pd.DataFrame({
                    "Date": df["Date"],
                    "Actual": df["Next_Day_Close"],
                    "Predicted": df["Predicted"]
                })
                plot_comparison(df_, f"{model_map[key]} - Train")

            elif "Test" in selected_option:
                df_test = get_data_test()
                df_test["Predicted"] = predict_dataframe(model, df_test)
                df_test_ = pd.DataFrame({
                    "Date": df_test["Date"],
                    "Actual": df_test["Next_Day_Close"],
                    "Predicted": df_test["Predicted"]
                })
                plot_comparison(df_test_, f"{model_map[key]} - Test")
                
            elif "All" in selected_option:
                df_all = pd.concat([get_data_train(), get_data_test()])
                df_all["Predicted"] = predict_dataframe(model, df_all)
                df_all_ = pd.DataFrame({
                    "Date": df_all["Date"],
                    "Actual": df_all["Next_Day_Close"],
                    "Predicted": df_all["Predicted"]
                })
                plot_comparison(df_all_, f"{model_map[key]} - All")
            
            return  # Hentikan setelah visualisasi model yang dipilih

    # Forecasting Masa Depan
    if "Forecasting" in selected_option or "ke Depan" in selected_option:
        model_name = st.selectbox("Pilih Model untuk Forecasting", list(model_map.values()))
        model = load_model(model_name)

        # Slider untuk custom periode prediksi
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
