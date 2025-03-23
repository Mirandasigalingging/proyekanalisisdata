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
    
    # Filter berdasarkan bulan
    month_mapping = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
    selected_month = st.selectbox("Pilih Bulan", list(month_mapping.values()))
    selected_month_num = list(month_mapping.keys())[list(month_mapping.values()).index(selected_month)]
    
    filtered_data = day_df[day_df['mnth'] == selected_month_num]
    
    # Filter berdasarkan cuaca
    weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
    selected_weather = st.selectbox("Pilih Cuaca", list(weather_mapping.values()))
    selected_weather_num = list(weather_mapping.keys())[list(weather_mapping.values()).index(selected_weather)]
    
    filtered_data = filtered_data[filtered_data['weathersit'] == selected_weather_num]
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=day_df, palette={1: 'blue', 2: 'gray', 3: 'red'})
    plt.title('Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')
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
