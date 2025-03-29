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

# --- Sidebar untuk Pilihan Visualisasi, Bulan, dan Cuaca ---
st.sidebar.header("📊 Pengaturan Visualisasi")

dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

if dataset_choice == "Tren Bulanan (Cuaca)":
    st.sidebar.subheader("📅 Filter Tren Bulanan")

    # Mapping bulan dan cuaca
    month_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan"}

    day_df["mnth_name"] = day_df["mnth"].map(month_map)
    day_df["cuaca"] = day_df["weathersit"].map(weather_map)

    # Sidebar filter untuk bulan dan cuaca
    bulan_options = ["Semua Bulan"] + list(month_map.values())
    selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)

    cuaca_options = ["Semua Cuaca"] + list(weather_map.values())
    selected_cuaca = st.sidebar.selectbox("Pilih Cuaca", cuaca_options)

    # Filter data berdasarkan pilihan
    filtered_data = day_df.copy()
    if selected_bulan != "Semua Bulan":
        filtered_data = filtered_data[filtered_data["mnth_name"] == selected_bulan]
    if selected_cuaca != "Semua Cuaca":
        filtered_data = filtered_data[filtered_data["cuaca"] == selected_cuaca]

    # --- VISUALISASI 1: Tren Bulanan ---
    st.subheader("📊 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    plt.figure(figsize=(10, 5))

    if selected_bulan == "Semua Bulan":
        # Menampilkan tren penyewaan tiap bulan berdasarkan cuaca
        palette = {1: 'blue', 2: 'gray', 3: 'red'}
        sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=filtered_data, palette=palette)

        plt.title('Tren Penggunaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Penyewaan')
        plt.xticks(ticks=[2, 4, 6, 8, 10, 12], labels=["2", "4", "6", "8", "10", "12"])  # Hanya menampilkan angka genap

        # Tambahkan garis puncak penyewaan
        max_month = day_df.loc[day_df['cnt'].idxmax(), 'mnth']
        max_rentals = day_df['cnt'].max()
        plt.axvline(x=max_month, linestyle='--', color='black', alpha=0.6)
        plt.text(max_month, max_rentals, f'Puncak Penyewaan\nBulan {max_month}',
                 verticalalignment='bottom', horizontalalignment='right',
                 fontsize=10, color='black')

        # Legenda cuaca
        weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
        handles, labels = plt.gca().get_legend_handles_labels()
        labels = [weather_labels[int(label)] for label in labels]
        plt.legend(handles, labels, title='Kondisi Cuaca')

    else:
        # Menampilkan tren harian dalam satu bulan yang dipilih
        plt.xticks(rotation=45)
        palette = {"Cerah": 'blue', "Mendung": 'gray', "Hujan": 'red'}
        sns.lineplot(x='dteday', y='cnt', hue='cuaca', data=filtered_data, palette=palette)

        plt.xlabel(f'Hari dalam {selected_bulan}')
        plt.ylabel('Jumlah Penyewaan')
        plt.title(f'Tren Penyewaan Sepeda pada {selected_bulan}')

    st.pyplot(plt)

    # --- Kesimpulan Tren Bulanan ---
    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan sepeda lebih tinggi saat cuaca **cerah** dan menurun saat **hujan**.
    - Tren bulanan menunjukkan penyewaan tertinggi di bulan tertentu, yang bisa berkaitan dengan musim atau liburan.
    - Jika memilih bulan tertentu, pola harian menunjukkan bagaimana cuaca mempengaruhi jumlah penyewaan.
    """)

elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    plt.figure(figsize=(12, 6))

    # Visualisasi dengan format seperti di Google Colab
    ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette={0: 'orange', 1: 'blue'})

    # Ubah legenda sesuai dengan label yang benar
    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title("Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    plt.xticks(range(0, 24, 2))

    st.pyplot(plt)

    # --- Kesimpulan Pola Per Jam ---
    st.subheader("📌 Kesimpulan")
    st.write("""
    - **Hari kerja**: Penyewaan sepeda menunjukkan dua puncak, yaitu di **pagi dan sore hari**. Ini kemungkinan terkait perjalanan kerja/sekolah.
    - **Akhir pekan**: Penyewaan lebih merata sepanjang hari, dengan puncaknya terjadi **di siang hari** karena lebih banyak aktivitas rekreasi.
    """)

# --- Footer ---
st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
