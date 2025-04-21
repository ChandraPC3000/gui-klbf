import streamlit as st

# Styling for improved aesthetics
st.markdown("""
<style>
/* Global styling for all h2 elements */
h2 {
    font-weight: bold;  /* Ensure font is bold for all h2 elements */
    font-size: 28px;    /* Consistent font size for all h2 elements */
    color: #333;        /* Ensure consistent color */
}

/* Specific styling for "Get in Touch" and "Contact Me" */
.get-in-touch {
    font-size: 20px; /* Adjust size for 'Get in Touch' */
    color: #555;     /* Set a lighter color for 'Get in Touch' */
}

.contact-me {
    font-size: 36px; /* Larger font size for 'Contact Me' */
    font-weight: bold;
    color: #333;     /* Set a darker color for 'Contact Me' */
}

.center {
    text-align: center;
    font-weight: bold;
    font-size: 24px;
}

.subheader {
    text-align: center;
    font-size: 18px;
    color: #555;
}

.boxed-text {
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    background-color: #f9f9f9;
    margin: 20px 0;
    font-size: 16px;
    line-height: 1.6;
}

.instructions {
    background-color: #eef;
    padding: 10px;
    border-radius: 10px;
    line-height: 1.8;
}

a {
    text-decoration: none;
    font-size: 18px;
    font-family: 'Arial', sans-serif;
    font-weight: 600;
    color: #333;
}

a:hover {
    text-decoration: underline;
}

.contact-bar {
    display: flex;
    justify-content: center;
    gap: 40px;
    padding: 15px;
    background-color: #f0f0f0;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.contact-bar a {
    display: flex;
    align-items: center;
    gap: 8px;
}

.contact-bar a img {
    width: 28px;
    height: 28px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="center">GUI-Python Untuk Memprediksi Harga Saham Menggunakan Model Extreme Gradient Boosting (XGBoost) Dengan Metode Optimasi PSO dan GridSearchCV</h1>', unsafe_allow_html=True)

# Pengenalan GUI
st.markdown('<p class="subheader">Sistem ini dirancang untuk memprediksi harga penutupan saham perusahaan menggunakan model Extreme Gradient Boosting (XGBoost).</p>', unsafe_allow_html=True)

st.markdown("""
<div class='boxed-text'>
Sistem ini memungkinkan pengguna untuk melakukan prediksi harga penutupan saham berdasarkan berbagai parameter historis yang diperoleh dari dataset harga saham harian. Prediksi dilakukan menggunakan beberapa metode Machine Learning, yaitu:

- **XGBoost-Default** (model tanpa optimasi parameter)
- **XGBoost-GridSearchCV** (model dengan optimasi hyperparameter menggunakan GridSearchCV)
- **XGBoost-PSO** (model dengan optimasi hyperparameter menggunakan Particle Swarm Optimization)

Sistem ini memiliki antarmuka interaktif yang sederhana dan mudah digunakan untuk mendapatkan hasil prediksi secara real-time serta menampilkan visualisasi data dalam bentuk grafik interaktif.
</div>
""", unsafe_allow_html=True)

# Panduan Penggunaan
st.markdown("""
### Panduan Penggunaan
<div class='instructions'>
<b>1. Memilih Model</b><br>
Pengguna dapat memilih salah satu model yang tersedia di menu "Prediksi" untuk melakukan prediksi harga saham berdasarkan model yang dipilih.

<b>2. Menginput Data</b><br>
- **Input Manual:** Pengguna dapat memasukkan harga **Open, High, Low, dan Close** secara langsung melalui formulir input.
- **Upload CSV:** Alternatif lain adalah mengunggah file CSV yang berisi data harga saham untuk diprediksi secara otomatis.

<b>3. Menampilkan Hasil Prediksi</b><br>
Setelah input data dimasukkan, sistem akan melakukan perhitungan dan menampilkan prediksi harga saham di layar. Hasil prediksi ini ditampilkan dalam bentuk tabel dan dapat diunduh untuk analisis lebih lanjut.

<b>4. Visualisasi Data</b><br>
Pada menu **Visualisasi Data**, pengguna dapat melihat grafik interaktif yang membandingkan harga aktual dengan hasil prediksi dari model yang dipilih.
</div>
""", unsafe_allow_html=True)

# Get in Touch Section with improved layout and unique icons
st.markdown("""
<div class="center">
    <h2 class="get-in-touch">Get in Touch</h2>
    <h2 class="contact-me">Contact Me</h2>
    <div class="boxed-text">
        <div class="contact-bar">
             <!-- Gmail with Link (Fixing the mailto error) -->
            <a href="mailto:cputraciptaning@gmail.com" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gmail_icon_%282020%29.svg/1024px-Gmail_icon_%282020%29.svg.png" alt="Email"> Gmail
            </a>
            <!-- Instagram without Link -->
            <a href="https://www.instagram.com/ciptaning.chan/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram"> Instagram
            </a>
            <!-- LinkedIn with Link -->
            <a href="https://www.linkedin.com/in/chandra-putra-ciptaningtyas/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn"> LinkedIn
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
---
Copyright © 2025 Chandra Putra Ciptaningtyas. All Rights Reserved.
""")
