
# GUI-Python Untuk Memprediksi Harga Saham Menggunakan Model Extreme Gradient Boosting (XGBoost) Dengan Metode Optimasi PSO dan GridSearchCV

Proyek ini adalah aplikasi berbasis Python yang memanfaatkan **XGBoost** untuk memprediksi harga saham perusahaan menggunakan data historis. Aplikasi ini juga dilengkapi dengan optimasi parameter menggunakan metode **Particle Swarm Optimization (PSO)** dan **GridSearchCV** untuk meningkatkan akurasi prediksi.

Aplikasi ini dibangun menggunakan **Streamlit** untuk antarmuka pengguna grafis (GUI), yang memungkinkan pengguna untuk menginput data dan melihat hasil prediksi secara interaktif. Selain itu, aplikasi ini juga memungkinkan visualisasi grafik perbandingan antara harga saham aktual dan yang diprediksi.

## Fitur Utama
- **Pemilihan Model**: Pengguna dapat memilih salah satu dari tiga model prediksi, yaitu:
  - **XGBoost-Default**: Model dasar tanpa optimasi parameter.
  - **XGBoost-GridSearchCV**: Model dengan optimasi menggunakan GridSearchCV.
  - **XGBoost-PSO**: Model dengan optimasi menggunakan algoritma Particle Swarm Optimization.
  
- **Input Data**: Pengguna dapat menginput data secara manual atau mengunggah file CSV berisi data historis harga saham.
  
- **Prediksi Harga Saham**: Menghasilkan prediksi harga saham berdasarkan input data dengan model yang dipilih.
  
- **Visualisasi**: Menyediakan grafik interaktif yang membandingkan harga saham aktual dengan harga yang diprediksi.

- **Evaluasi Model**: Pengguna dapat mengevaluasi kinerja model menggunakan metrik seperti RMSE, MAPE, dan R-squared.

## Instalasi

### Prasyarat
Pastikan Anda sudah menginstal Python versi 3.x. Untuk menjalankan aplikasi ini, Anda perlu menginstal beberapa pustaka yang diperlukan, yang dapat Anda instal melalui **pip**.

### Langkah-langkah Instalasi

1. **Clone Repository**  
   Clone repositori ini ke komputer Anda:
   ```bash
   git clone https://github.com/username/repository-name.git
   ```

2. **Buat Virtual Environment (Opsional)**  
   Untuk menghindari konflik antara pustaka, disarankan untuk menggunakan virtual environment:
   ```bash
   python -m venv venv
   ```

3. **Aktifkan Virtual Environment**
   - Di Windows:
     ```bash
     venv\Scriptsctivate
     ```
   - Di macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instal Dependencies**  
   Setelah environment aktif, instal pustaka yang diperlukan dengan menjalankan:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi**  
   Setelah instalasi selesai, jalankan aplikasi Streamlit dengan perintah berikut:
   ```bash
   streamlit run app.py
   ```

6. **Akses Aplikasi**  
   Aplikasi akan berjalan di browser di alamat `http://localhost:8501`.

## Penggunaan

### Memilih Model
Setelah aplikasi berjalan, pengguna dapat memilih model prediksi yang diinginkan dari menu dropdown yang disediakan di halaman prediksi. Pilihan model termasuk:
- **XGBoost-Default**
- **XGBoost-GridSearchCV**
- **XGBoost-PSO**

### Menginput Data
Pengguna dapat memilih dua metode input data:
- **Input Manual**: Masukkan harga saham Open, High, Low, dan Close secara langsung.
- **Upload CSV**: Unggah file CSV yang berisi data historis harga saham. Pastikan file CSV memiliki kolom `Open`, `High`, `Low`, dan `Close`.

### Melihat Hasil Prediksi
Setelah menginput data, klik tombol **Predict** untuk melihat hasil prediksi harga saham berdasarkan model yang dipilih. Hasil prediksi akan ditampilkan di layar dan dapat diekspor dalam bentuk tabel atau file CSV.

### Visualisasi
Pengguna dapat melihat grafik interaktif yang membandingkan harga saham yang sebenarnya dengan hasil prediksi untuk periode tertentu.

### Evaluasi Model
Pengguna juga dapat mengevaluasi kinerja model dengan menguji model menggunakan data test dan melihat metrik evaluasi seperti RMSE dan MAPE.

## Struktur Proyek

```
/project-root
│
├── app.py                      # Aplikasi utama Streamlit
├── predict.py                  # Fungsi untuk memuat dan menjalankan model
├── requirements.txt            # Daftar pustaka yang dibutuhkan
├── models/                     # Folder untuk menyimpan model XGBoost
│   ├── xgboost_model_default_params.csv
│   ├── xgboost_gridsearchcv_params.csv
│   ├── xgboost_pso_params.csv
├── data/                       # Folder untuk data training dan testing
│   ├── train_data.csv
│   ├── test_data.csv
└── README.md                   # Dokumentasi proyek
```

## Pengembang

- **Chandra Putra Ciptaningtyas** - Pengembang Utama  
- **Dr. Triastuti Wuryandari, S.Si., M.Si.** - Dosen Pembimbing 1  
- **Miftahul Jannah, S.Si., M.Si.** - Dosen Pembimbing 2

## Lisensi
Proyek ini dilindungi oleh **Hak Cipta** dan tidak boleh disalin atau digunakan tanpa izin dari pengembang. Hak cipta ini melindungi aplikasi dan kode sumber yang telah dikembangkan.

## Referensi
- XGBoost: https://xgboost.readthedocs.io/
- Streamlit: https://streamlit.io/
- Particle Swarm Optimization: https://en.wikipedia.org/wiki/Particle_swarm_optimization
- GridSearchCV: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
