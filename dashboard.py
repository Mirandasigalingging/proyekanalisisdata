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
    
    bulan_mapping = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    bulan_options = ["1 TAHUN"] + list(bulan_mapping.values())
    selected_bulan = st.sidebar.selectbox("Pilih Bulan", bulan_options)
    
    cuaca_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
    cuaca_options = [cuaca_mapping[key] for key in day_df["weathersit"].unique()]
    selected_cuaca = st.sidebar.selectbox("Pilih Cuaca", cuaca_options)
    
    cuaca_reverse_mapping = {v: k for k, v in cuaca_mapping.items()}
    selected_cuaca_value = cuaca_reverse_mapping[selected_cuaca]
    
    if selected_bulan == "1 TAHUN":
        filtered_data = day_df[day_df["weathersit"] == selected_cuaca_value]
    else:
        selected_bulan_value = [k for k, v in bulan_mapping.items() if v == selected_bulan][0]
        filtered_data = day_df[(day_df["mnth"] == selected_bulan_value) & (day_df["weathersit"] == selected_cuaca_value)]
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='mnth', y='cnt', data=filtered_data, color='blue', marker='o')
    
    plt.title('Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')
    plt.xticks(ticks=list(bulan_mapping.keys()), labels=list(bulan_mapping.values()))
    
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
