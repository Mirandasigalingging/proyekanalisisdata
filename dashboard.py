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

    # Pemetaan nama bulan dan kondisi cuaca
    month_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    weather_map = {1: "Cerah", 2: "Mendung", 3: "Hujan"}

    day_df["mnth_name"] = day_df["mnth"].map(month_map)
    day_df["cuaca"] = day_df["weathersit"].map(weather_map)

    # Sidebar filter
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

    # Visualisasi tren penyewaan sepeda
    plt.figure(figsize=(10, 5))

    if selected_bulan == "Semua Bulan":
        # Warna sesuai pemetaan cuaca
        palette = {1: 'blue', 2: 'gray', 3: 'red'}
        sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=filtered_data, palette=palette)

        plt.xlabel('Bulan')
        plt.xticks(ticks=list(month_map.keys()), labels=list(month_map.values()))  # Format bulan
    else:
        # Jika memilih satu bulan, tampilkan tren harian
        plt.xticks(rotation=45)
        palette = {"Cerah": 'blue', "Mendung": 'gray', "Hujan": 'red'}
        sns.lineplot(x='dteday', y='cnt', hue='cuaca', data=filtered_data, palette=palette)

        plt.xlabel(f'Hari dalam {selected_bulan}')

    plt.ylabel('Jumlah Penyewaan')
    plt.title(f'Tren Penyewaan Sepeda pada {selected_bulan}' if selected_bulan != "Semua Bulan" else 'Tren Penyewaan Sepeda Tiap Bulan')

    # Memperbaiki legenda agar lebih jelas
    handles, labels = plt.gca().get_legend_handles_labels()
    if selected_bulan == "Semua Bulan":
        labels = [weather_map[int(label)] for label in labels]  # Ubah angka jadi label
    plt.legend(handles, labels, title='Kondisi Cuaca')

    st.pyplot(plt)

    # Menyesuaikan kesimpulan agar lebih deskriptif
    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan sepeda **lebih tinggi saat cuaca cerah** dan **menurun saat hujan**.
    - Tren bulanan menunjukkan bahwa musim panas atau masa liburan **cenderung meningkatkan jumlah penyewaan**.
    - Jika memilih satu bulan tertentu, pola harian memperlihatkan bahwa kondisi cuaca sangat memengaruhi jumlah penyewaan sepeda setiap harinya.
    """)

elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette={0: 'orange', 1: 'blue'})

    # Menyesuaikan label legenda agar lebih jelas
    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title('Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

    # Menyederhanakan kesimpulan agar lebih jelas
    st.subheader("📌 Kesimpulan")
    st.write("""
    - **Hari kerja**: Pola penyewaan membentuk **dua puncak utama** (pagi dan sore hari), kemungkinan besar terkait jam perjalanan kerja atau sekolah.
    - **Akhir pekan**: Puncak penyewaan lebih **terpusat di siang hari**, menandakan penggunaan sepeda lebih bersifat rekreasi.
    """)

st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
