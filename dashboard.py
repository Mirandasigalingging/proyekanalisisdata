import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

# Load dataset
day_df, hour_df = load_data()

# Judul Dashboard
st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Sidebar Pilihan Visualisasi
dataset_choice = st.sidebar.radio(
    "Pilih Visualisasi",
    ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"]
)

# **VISUALISASI 1: Tren Bulanan Berdasarkan Cuaca**
if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    # Warna untuk cuaca
    palette = {1: 'blue', 2: 'gray', 3: 'red'}

    # Plot Tren Penyewaan Sepeda
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        x='mnth', y='cnt', hue='weathersit',
        data=day_df, palette=palette, linewidth=2, ci=80
    )

    # Menambahkan garis vertikal pada puncak penyewaan (misalnya bulan 9)
    plt.axvline(x=9, color='black', linestyle="dashed", alpha=0.7)
    plt.text(9, day_df["cnt"].max(), "Puncak Penyewaan\nBulan 9", ha='center', fontsize=10)

    # Label dan judul
    plt.title('Tren Penggunaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    # Legenda sesuai label yang diinginkan
    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
    handles, labels = plt.gca().get_legend_handles_labels()
    labels = [weather_labels[int(label)] for label in labels]
    plt.legend(handles, labels, title='Kondisi Cuaca')

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan sepeda meningkat saat cuaca **cerah** dan menurun ketika **hujan**.
    - Puncak penyewaan terjadi pada **bulan 9**.
    - Tren penyewaan lebih tinggi selama musim hangat dan berkurang pada musim hujan.
    """)

# **VISUALISASI 2: Pola Per Jam Hari Kerja vs Akhir Pekan**
elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    # Visualisasi pola peminjaman sepeda per jam
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(
        x='hr', y='cnt', hue='workingday',
        data=hour_df, palette={0: 'orange', 1: 'blue'}
    )

    # Mengubah label legend
    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title('Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaan')

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Pada **hari kerja**, ada dua puncak penyewaan: **pagi & sore hari** (kemungkinan besar terkait perjalanan kerja/sekolah).
    - Pada **akhir pekan**, puncak penyewaan terjadi lebih **siang**, menunjukkan penggunaan lebih banyak untuk rekreasi.
    """)
