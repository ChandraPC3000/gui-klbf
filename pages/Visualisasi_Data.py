# Modify the content of "Visualisasi_Data.py" to add test data visualization
modified_code = """
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from predict import load_model, predict
from datetime import datetime, timedelta

# Load daftar model
MODELS = ["Model XGBoost Default", "Model XGBoost GridSearchCV", "Model XGBoost PSO"]

# Halaman Visualisasi Grafik Prediksi
st.title("Visualisasi Grafik Prediksi Saham Kalbe Farma (KLBF)")
st.write("Halaman ini menampilkan visualisasi grafik prediksi harga saham berdasarkan model yang dipilih.")

# Dropdown untuk memilih model
selected_model_name = st.selectbox("Pilih Model Prediksi", MODELS)

# Load model berdasarkan pilihan
model = load_model(selected_model_name)

# Bagian input
st.sidebar.header("Input Data Prediksi")
input_method = st.sidebar.radio("Pilih Metode Input", ["Manual", "Upload CSV"])

if input_method == "Manual":
    # Input manual
    open_prices = st.sidebar.text_area("Harga Open (Pisahkan dengan koma)", "1530, 1540, 1550")
    high_prices = st.sidebar.text_area("Harga High (Pisahkan dengan koma)", "1545, 1555, 1565")
    low_prices = st.sidebar.text_area("Harga Low (Pisahkan dengan koma)", "1525, 1535, 1540")
    close_prices = st.sidebar.text_area("Harga Close (Pisahkan dengan koma)", "1535, 1545, 1555")
    
    # Convert the input data to pandas DataFrame
    open_prices = np.array([float(x) for x in open_prices.split(',')])
    high_prices = np.array([float(x) for x in high_prices.split(',')])
    low_prices = np.array([float(x) for x in low_prices.split(',')])
    close_prices = np.array([float(x) for x in close_prices.split(',')])
    
    data = pd.DataFrame({
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices
    })

elif input_method == "Upload CSV":
    # Upload CSV
    uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())

# Prediksi dan visualisasi
predictions = predict(model, data)

# Visualisasi Data Prediksi dan Test Data
st.subheader("Visualisasi Data Prediksi vs Data Asli (Test Data)")
if input_method == "Manual" or (input_method == "Upload CSV" and not uploaded_file.empty):
    st.write("Data Prediksi dan Data Asli:")
    
    # Assuming the test data and predicted data columns are available
    st.line_chart(data[['Open', 'Close']])
    st.line_chart(predictions)

# Correcting the file writing process by using an alternative method
file_path = os.path.join(pages_path, 'Visualisasi_Data.py')

# Writing the modified code to the file again
with open(file_path, 'w') as file:
    file.write(modified_code)

"Changes to Visualisasi_Data.py have been successfully applied!"
