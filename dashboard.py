import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat data dengan cache agar tidak memuat ulang setiap kali aplikasi dijalankan
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")  # Dataset harian penyewaan sepeda
    hour_df = pd.read_csv("hour.csv")  # Dataset per jam penyewaan sepeda
    return day_df, hour_df

day_df, hour_df = load_data()

# Judul utama dashboard
st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk memilih jenis visualisasi
dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

# Visualisasi tren bulanan berdasarkan cuaca
if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    # Mapping untuk nama bulan dan kondisi cuaca agar lebih mudah dipahami
    month_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan"}

    # Tambahkan kolom nama bulan dan kondisi cuaca ke dataset
    day_df["mnth_name"] = day_df["mnth"].map(month_map)
    day_df["cuaca"] = day_df["weathersit"].map(weather_map)

    # Sidebar untuk memilih bulan dan kondisi cuaca
    bulan_options = ["Semua Bulan"] + list(month_map.values())
    selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)

    cuaca_options = ["Semua Cuaca"] + list(weather_map.values())
    selected_cuaca = st.sidebar.selectbox("Pilih Cuaca", cuaca_options)

    # Filter data berdasarkan pilihan pengguna
    filtered_data = day_df.copy()
    if selected_bulan != "Semua Bulan":
        filtered_data = filtered_data[filtered_data["mnth_name"] == selected_bulan]
    if selected_cuaca != "Semua Cuaca":
        filtered_data = filtered_data[filtered_data["cuaca"] == selected_cuaca]

    # Buat visualisasi data
    plt.figure(figsize=(10, 5))

    if selected_bulan == "Semua Bulan":
        # Menampilkan tren penyewaan sepanjang tahun
        palette = {1: 'blue', 2: 'gray', 3: 'red'}
        sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=filtered_data, palette=palette)

        plt.xlabel('Bulan')
        plt.xticks(ticks=list(month_map.keys()), labels=list(month_map.values()))  # Format nama bulan
    else:
        # Jika hanya satu bulan dipilih, tampilkan tren harian
        plt.xticks(rotation=45)
        palette = {"Cerah": 'blue', "Mendung": 'gray', "Hujan": 'red'}
        sns.lineplot(x='dteday', y='cnt', hue='cuaca', data=filtered_data, palette=palette)

        plt.xlabel(f'Hari dalam {selected_bulan}')

    plt.ylabel('Jumlah Penyewaan')
    plt.title(f'Tren Penyewaan Sepeda pada {selected_bulan}' if selected_bulan != "Semua Bulan" else 'Tren Penyewaan Sepeda Tiap Bulan')

    # Perbaikan legenda agar lebih informatif
    handles, labels = plt.gca().get_legend_handles_labels()
    if selected_bulan == "Semua Bulan":
        labels = [weather_map[int(label)] for label in labels]  # Ubah angka jadi deskripsi cuaca
    plt.legend(handles, labels, title='Kondisi Cuaca')

    st.pyplot(plt)

    # Kesimpulan dari analisis tren bulanan
    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan sepeda cenderung meningkat saat cuaca **cerah** dan menurun ketika **hujan**.
    - Secara bulanan, kemungkinan ada peningkatan di musim panas atau saat liburan.
    - Jika memilih bulan tertentu, tren harian dapat menunjukkan dampak cuaca pada penyewaan harian.
    """)

# Visualisasi pola penyewaan per jam berdasarkan hari kerja dan akhir pekan
elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette={0: 'orange', 1: 'blue'})

    # Ubah label legenda agar lebih mudah dipahami
    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title('Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

    # Kesimpulan dari analisis pola per jam
    st.subheader("📌 Kesimpulan")
    st.write("""
    - Pada **hari kerja**, terdapat dua puncak penggunaan: **pagi & sore hari**, kemungkinan besar karena perjalanan kerja/sekolah.
    - Pada **akhir pekan**, puncak penggunaan terjadi lebih **siang**, yang menunjukkan penggunaan untuk rekreasi.
    """)

# Catatan tambahan di sidebar
st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
