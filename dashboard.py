import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    plt.figure(figsize=(10, 5))
    palette = {1: 'blue', 2: 'gray', 3: 'red'}
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=day_df, palette=palette)

    plt.title('Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
    handles, labels = plt.gca().get_legend_handles_labels()
    labels = [weather_labels[int(label)] for label in labels]
    plt.legend(handles, labels, title='Kondisi Cuaca')

    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan sepeda meningkat saat cuaca **cerah** dan menurun ketika **hujan**.
    - Bulan dengan penyewaan tertinggi kemungkinan terjadi di musim liburan atau musim panas.
    - Kondisi cuaca sangat berpengaruh terhadap jumlah penyewaan.
    """)

elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette={0: 'orange', 1: 'blue'})

    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title('Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Pada **hari kerja**, ada dua puncak penyewaan: **pagi & sore hari** (kemungkinan besar terkait perjalanan kerja/sekolah).
    - Pada **akhir pekan**, puncak penyewaan terjadi lebih **siang**, menunjukkan penggunaan lebih banyak untuk rekreasi.
    """)

st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
