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

    plt.figure(figsize=(10, 5))

    if selected_bulan == "Semua Bulan" and selected_cuaca == "Semua Cuaca":
        # **Visualisasi sesuai Google Colab**
        palette = {1: 'blue', 2: 'gray', 3: 'red'}
        sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=day_df, palette=palette)

        plt.title('Tren Penggunaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Penyewaan')
        plt.xticks(ticks=list(month_map.keys()), labels=list(month_map.values()))  # Format bulan

        # Menampilkan puncak penyewaan
        max_month = day_df.loc[day_df['cnt'].idxmax(), 'mnth']
        max_rentals = day_df['cnt'].max()
        plt.axvline(x=max_month, linestyle='--', color='black', alpha=0.6)
        plt.text(max_month, max_rentals, f'Puncak Penyewaan\nBulan {month_map[max_month]}',
                 verticalalignment='bottom', horizontalalignment='right',
                 fontsize=10, color='black')

        # Menyesuaikan legenda
        handles, labels = plt.gca().get_legend_handles_labels()
        labels = [weather_map[int(label)] for label in labels]
        plt.legend(handles, labels, title='Kondisi Cuaca')

    else:
        # **Jika memilih bulan tertentu, tampilkan tren harian dengan format tanggal lebih rapi**
        palette = {"Cerah": 'blue', "Mendung": 'gray', "Hujan": 'red'}
        filtered_data['day'] = filtered_data['dteday'].str[-2:]  # Hanya ambil tanggal tanpa tahun

        sns.lineplot(x='day', y='cnt', hue='cuaca', data=filtered_data, palette=palette)

        plt.title(f'Tren Penyewaan Sepeda di {selected_bulan}')
        plt.xlabel(f'Hari dalam {selected_bulan}')
        plt.ylabel('Jumlah Penyewaan')
        plt.xticks(rotation=45)  # Mencegah tulisan tanggal bertabrakan

        # Menyesuaikan legenda
        plt.legend(title='Kondisi Cuaca')

    st.pyplot(plt)

    # **Kesimpulan**
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

    # **Kesimpulan**
    st.subheader("📌 Kesimpulan")
    st.write("""
    - **Hari kerja**: Pola penyewaan membentuk **dua puncak utama** (pagi dan sore hari), kemungkinan besar terkait jam perjalanan kerja atau sekolah.
    - **Akhir pekan**: Puncak penyewaan lebih **terpusat di siang hari**, menandakan penggunaan sepeda lebih bersifat rekreasi.
    """)

st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
