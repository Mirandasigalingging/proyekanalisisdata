import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv") 
    return day_df

day_df = load_data()

st.title("🚴 Dashboard Analisis Penyewaan Sepeda")

# Sidebar menu
dataset_choice = st.sidebar.radio(
    "Pilih Visualisasi", 
    [
        "Binning Jumlah Penyewaan", 
        "Grouping Musiman"
    ]
)

# 1️⃣ **Binning Jumlah Penyewaan**
if dataset_choice == "Binning Jumlah Penyewaan":
    st.subheader("📊 Kategorisasi Penyewaan Sepeda (Binning)")

    # Binning jumlah penyewaan
    bins = [0, 3000, 5000, 7000]
    labels = ['Rendah', 'Sedang', 'Tinggi']
    day_df['Kategori_Penyewaan'] = pd.cut(day_df['cnt'], bins=bins, labels=labels)

    plt.figure(figsize=(8, 5))
    sns.countplot(x="Kategori_Penyewaan", data=day_df, palette="viridis")

    plt.title("Distribusi Kategori Penyewaan Sepeda")
    plt.xlabel("Kategori Penyewaan")
    plt.ylabel("Jumlah Hari")

    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Mayoritas hari memiliki penyewaan dalam kategori **sedang**.
    - Penyewaan **rendah dan tinggi lebih jarang terjadi** dibandingkan kategori sedang.
    """)

# 2️⃣ **Grouping Musiman**
elif dataset_choice == "Grouping Musiman":
    st.subheader("🌦️ Pola Penyewaan Berdasarkan Musim (Manual Grouping)")

    # Fungsi manual grouping musim
    def season(month):
        if month in [12, 1, 2]:
            return 'Hujan'
        elif month in [3, 4, 5]:
            return 'Peralihan ke Kemarau'
        elif month in [6, 7, 8, 9]:
            return 'Kemarau'
        else:
            return 'Peralihan ke Hujan'

    day_df['Musim'] = day_df['mnth'].apply(season)

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Musim', y='cnt', data=day_df, palette="coolwarm")

    plt.title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan")

    st.pyplot(plt)

    st.subheader("📌 Kesimpulan")
    st.write("""
    - Penyewaan **lebih tinggi saat musim kemarau**.
    - Saat musim hujan, jumlah penyewaan **cenderung lebih rendah**.
    - Musim peralihan menunjukkan tren bervariasi.
    """)

st.sidebar.markdown("💡 **Tip:** Pilih visualisasi di sidebar untuk melihat analisisnya.")
