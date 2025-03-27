import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    return day_df

day_df = load_data()

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk interaksi pengguna
st.sidebar.header("📊 Pengaturan Visualisasi")
selected_view = st.sidebar.radio("Pilih Visualisasi:", 
                                 ["Tren Penyewaan Bulanan", "Faktor yang Mempengaruhi Penyewaan"])

### 📌 VISUALISASI 1: Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca ###
if selected_view == "Tren Penyewaan Bulanan":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")
    
    plt.figure(figsize=(10, 5))
    palette = {1: 'blue', 2: 'gray', 3: 'red'}

    sns.lineplot(
        x='mnth', y='cnt', hue='weathersit', 
        data=day_df, palette=palette, linewidth=2, ci=80
    )

    # Garis vertikal untuk puncak penyewaan
    plt.axvline(x=9, color='black', linestyle="dashed", alpha=0.7)
    plt.text(9, day_df["cnt"].max(), "Puncak Penyewaan\nBulan 9", ha='center', fontsize=10)

    # Label dan judul
    plt.title('Tren Penggunaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    # Legenda sesuai label
    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
    handles, labels = plt.gca().get_legend_handles_labels()
    labels = [weather_labels[int(label)] for label in labels]
    plt.legend(handles, labels, title='Kondisi Cuaca')

    st.pyplot(plt)

### 📌 VISUALISASI 2: Faktor yang Mempengaruhi Penyewaan Sepeda ###
elif selected_view == "Faktor yang Mempengaruhi Penyewaan":
    st.subheader("🔍 Faktor yang Mempengaruhi Penyewaan Sepeda")
    
    # Opsi pemilihan faktor
    faktor = st.selectbox("Pilih Faktor:", ["temp", "hum", "windspeed"])

    # Visualisasi hubungan faktor terhadap jumlah penyewaan
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=day_df[faktor], y=day_df['cnt'], alpha=0.5)
    plt.xlabel(faktor.capitalize())
    plt.ylabel("Jumlah Penyewaan")
    plt.title(f"Hubungan antara {faktor.capitalize()} dan Penyewaan Sepeda")
    
    st.pyplot(plt)

# Kesimpulan Umum
st.subheader("📌 Kesimpulan")
st.write("""
- Penyewaan sepeda meningkat saat cuaca **cerah** dan menurun ketika **hujan**.
- Puncak penyewaan terjadi pada **bulan 9**.
- Faktor **temperatur** dan **kelembaban** berpengaruh terhadap jumlah penyewaan.
""")
