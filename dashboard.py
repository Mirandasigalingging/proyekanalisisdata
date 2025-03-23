import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat data (cache untuk efisiensi)
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

# Load dataset
day_df, hour_df = load_data()

# Judul utama
st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Pilihan Analisis di Sidebar
dataset_choice = st.sidebar.radio("Pilih Visualisasi", ["Tren Bulanan (Cuaca)", "Pola Per Jam (Hari Kerja vs Akhir Pekan)"])

# --- ANALISIS TREN BULANAN ---
if dataset_choice == "Tren Bulanan (Cuaca)":
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

    # Menambahkan filter interaktif
    selected_month = st.selectbox("Pilih Bulan", sorted(day_df["mnth"].unique()))
    selected_weather = st.selectbox("Pilih Kondisi Cuaca", sorted(day_df["weathersit"].unique()))

    # Filter dataset berdasarkan pilihan pengguna
    filtered_day_df = day_df[(day_df["mnth"] == selected_month) & (day_df["weathersit"] == selected_weather)]

    # Visualisasi
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=filtered_day_df, palette={1: 'blue', 2: 'gray', 3: 'red'})

    plt.title('Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    # Mengubah legenda ke bahasa yang lebih mudah dipahami
    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}
    handles, labels = plt.gca().get_legend_handles_labels()
    labels = [weather_labels[int(label)] for label in labels]
    plt.legend(handles, labels, title='Kondisi Cuaca')

    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write(f"""
    - Penyewaan sepeda meningkat saat cuaca **{weather_labels[selected_weather]}**.
    - Pada bulan {selected_month}, terdapat tren penyewaan tertentu berdasarkan kondisi cuaca.
    - Cuaca memainkan peran besar dalam jumlah penyewaan sepeda.
    """)

# --- ANALISIS POLA PER JAM ---
elif dataset_choice == "Pola Per Jam (Hari Kerja vs Akhir Pekan)":
    st.subheader("⏰ Pola Penggunaan Sepeda Per Jam (Hari Kerja vs Akhir Pekan)")

    # Menambahkan filter rentang jam dengan slider
    selected_hours = st.slider("Pilih Rentang Jam", min_value=0, max_value=23, value=(6, 18))

    # Menambahkan checkbox untuk memilih hari kerja atau akhir pekan
    workingday_option = st.checkbox("Tampilkan Hari Kerja", value=True)
    weekend_option = st.checkbox("Tampilkan Akhir Pekan", value=True)

    # Filter dataset berdasarkan pilihan pengguna
    filtered_hour_df = hour_df[
        ((hour_df["workingday"] == 1) & workingday_option) |
        ((hour_df["workingday"] == 0) & weekend_option)
    ]
    
    filtered_hour_df = filtered_hour_df[
        (filtered_hour_df["hr"] >= selected_hours[0]) & (filtered_hour_df["hr"] <= selected_hours[1])
    ]

    # Visualisasi
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=filtered_hour_df, palette={0: 'orange', 1: 'blue'})

    # Ubah label legend
    legend_labels = ['Akhir Pekan', 'Hari Kerja']
    for t, l in zip(ax.legend_.texts, legend_labels):
        t.set_text(l)

    plt.title('Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write(f"""
    - Pada **hari kerja**, ada dua puncak penyewaan: **pagi & sore hari** (kemungkinan besar terkait perjalanan kerja/sekolah).
    - Pada **akhir pekan**, puncak penyewaan terjadi lebih **siang**, menunjukkan penggunaan lebih banyak untuk rekreasi.
    - Tren penggunaan sepeda dalam rentang jam **{selected_hours[0]} - {selected_hours[1]}** dapat membantu memahami pola aktivitas pengguna.
    """)

st.sidebar.markdown("💡 **Tip:** Gunakan filter di atas untuk mengeksplorasi data lebih dalam.")
