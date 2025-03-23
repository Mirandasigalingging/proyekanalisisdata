import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set tema seaborn
sns.set_theme(style="darkgrid")

# Judul Aplikasi
st.title("📊 Dashboard Analisis Cuaca dan Musim")

# Upload File CSV jika belum ada
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    # Baca data
    data = pd.read_csv(uploaded_file)

    # Pastikan kolom yang diperlukan ada
    required_columns = ["bulan", "musim", "cuaca", "jumlah_pengguna"]
    if not all(col in data.columns for col in required_columns):
        st.error("CSV harus memiliki kolom: bulan, musim, cuaca, jumlah_pengguna")
        st.stop()

    # Konversi nama bulan ke format yang benar
    bulan_mapping = {
        "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
        "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
        "September": 9, "Oktober": 10, "November": 11, "Desember": 12
    }
    
    # Pastikan data sesuai
    data["bulan"] = data["bulan"].map(bulan_mapping)

    # Pilihan bulan
    bulan_nama = list(bulan_mapping.keys())
    selected_bulan = st.selectbox("Pilih Bulan", bulan_nama)

    # Filter berdasarkan bulan
    selected_bulan_num = bulan_mapping[selected_bulan]
    filtered_data = data[data["bulan"] == selected_bulan_num]

    # Pilihan cuaca
    cuaca_options = filtered_data["cuaca"].unique()
    selected_cuaca = st.selectbox("Pilih Cuaca", cuaca_options)

    # Filter berdasarkan cuaca
    filtered_data = filtered_data[filtered_data["cuaca"] == selected_cuaca]

    # 📊 **Visualisasi Data**
    st.subheader(f"Jumlah Pengguna berdasarkan Musim - {selected_bulan}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="musim", y="jumlah_pengguna", data=filtered_data, ax=ax, palette="viridis")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_xlabel("Musim")
    st.pyplot(fig)

    # Visualisasi jumlah pengguna berdasarkan cuaca
    st.subheader(f"Jumlah Pengguna berdasarkan Cuaca - {selected_bulan}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="cuaca", y="jumlah_pengguna", data=filtered_data, ax=ax, palette="coolwarm")
    ax.set_ylabel("Jumlah Pengguna")
    ax.set_xlabel("Cuaca")
    st.pyplot(fig)

else:
    st.warning("Silakan unggah file CSV terlebih dahulu.")
