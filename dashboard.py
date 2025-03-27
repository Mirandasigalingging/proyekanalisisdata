import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    return day_df

day_df = load_data()

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    # Mapping bulan dan cuaca
    month_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
    palette = {1: 'blue', 2: 'gray', 3: 'red'}  # Warna untuk cuaca

    day_df["mnth_name"] = day_df["mnth"].map(month_map)
    day_df["cuaca"] = day_df["weathersit"].map(weather_map)

    # Pilihan filter
    bulan_options = ["Semua Bulan"] + list(month_map.values())
    selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)

    cuaca_options = ["Semua Cuaca"] + list(weather_map.values())
    selected_cuaca = st.sidebar.selectbox("Pilih Cuaca", cuaca_options)

    # Filter data
    filtered_data = day_df.copy()
    if selected_bulan != "Semua Bulan":
        filtered_data = filtered_data[filtered_data["mnth_name"] == selected_bulan]
    if selected_cuaca != "Semua Cuaca":
        filtered_data = filtered_data[filtered_data["cuaca"] == selected_cuaca]

    # Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        x='mnth', y='cnt', hue='weathersit', 
        data=filtered_data, palette=palette, linewidth=2, ci=80
    )

    # Menambahkan garis vertikal pada puncak penyewaan (misalnya bulan 9)
    plt.axvline(x=9, color='black', linestyle="dashed", alpha=0.7)
    plt.text(9, day_df["cnt"].max(), "Puncak Penyewaan\nBulan 9", ha='center', fontsize=10)

    # Label dan judul
    plt.title('Tren Penggunaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    # Legenda sesuai label cuaca
    handles, labels = plt
