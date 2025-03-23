import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk load data dengan cache
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

# Mapping angka ke nama bulan
month_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
day_df["bulan"] = day_df["mnth"].map(month_mapping)

# Mapping angka ke kondisi cuaca
weather_mapping = {
    1: "Cerah", 2: "Mendung", 3: "Hujan"
}
day_df["cuaca"] = day_df["weathersit"].map(weather_mapping)

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk memilih visualisasi
dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")
    
    selected_month = st.selectbox("Pilih Bulan", day_df["bulan"].unique())
    selected_weather = st.selectbox("Pilih Cuaca", day_df["cuaca"].unique())
    
    filtered_data = day_df[(day_df["bulan"] == selected_month) & (day_df["cuaca"] == selected_weather)]
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='dteday', y='cnt', data=filtered_data, marker="o", color="blue")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45)
    plt.title(f'Tren Penyewaan Sepeda pada {selected_month} saat {selected_weather}')
    st.pyplot(plt)

elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")
    
    selected_hour = st.slider("Pilih Jam", min_value=0, max_value=23, value=12)
    filtered_hour_data = hour_df[hour_df["hr"] == selected_hour]
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x='workingday', y='cnt', data=filtered_hour_data, palette={0: 'orange', 1: 'blue'})
    plt.xticks(ticks=[0, 1], labels=["Akhir Pekan", "Hari Kerja"])
    plt.xlabel("Kategori Hari")
    plt.ylabel("Jumlah Penyewaan")
    plt.title(f'Jumlah Penyewaan Sepeda pada Jam {selected_hour}')
    st.pyplot(plt)

st.sidebar.markdown("💡 **Tip:** Pilih visualisasi dan filter untuk eksplorasi data lebih lanjut.")
