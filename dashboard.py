import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    return day_df

day_df = load_data()

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Cuaca")

# Filter data untuk semua bulan dan semua cuaca
plt.figure(figsize=(10, 5))
palette = {1: 'blue', 2: 'gray', 3: 'red'}

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
