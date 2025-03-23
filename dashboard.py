import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set tema seaborn
sns.set_theme(style="darkgrid")

# Judul Aplikasi
st.title("📊 Dashboard Analisis Cuaca dan Musim")

# Load dataset langsung dari repository
@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    return day, hour

day, hour = load_data()

# Konversi bulan ke angka
bulan_mapping = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
    "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
    "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}

day["bulan"] = day["mnth"].map(lambda x: list(bulan_mapping.values())[x-1])

def pertanyaan_bisnis():
    st.subheader("📌 Analisis Pertanyaan Bisnis")
    
    # Pertanyaan 1: Hubungan Cuaca dengan Jumlah Pengguna
    st.write("### 1. Bagaimana pengaruh cuaca terhadap jumlah pengguna?")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x="weathersit", y="cnt", data=day, ax=ax, palette="coolwarm")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)
    
    # Pertanyaan 2: Pola Jumlah Pengguna Berdasarkan Musim
    st.write("### 2. Bagaimana tren jumlah pengguna berdasarkan musim?")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="season", y="cnt", data=day, ax=ax, palette="viridis")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Pengguna")
    st.pyplot(fig)

pertanyaan_bisnis()

# Filter visualisasi berdasarkan bulan dan cuaca
st.subheader("📊 Visualisasi Berdasarkan Bulan dan Cuaca")
selected_bulan = st.selectbox("Pilih Bulan", list(bulan_mapping.keys()))
selected_bulan_num = bulan_mapping[selected_bulan]
filtered_data = day[day["bulan"] == selected_bulan_num]

# Pilihan cuaca
dict_cuaca = {1: "Cerah", 2: "Berawan", 3: "Hujan", 4: "Salju"}
filtered_data["weathersit"] = filtered_data["weathersit"].map(dict_cuaca)
selected_cuaca = st.selectbox("Pilih Cuaca", filtered_data["weathersit"].unique())
filtered_data = filtered_data[filtered_data["weathersit"] == selected_cuaca]

# Visualisasi
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="cnt", data=filtered_data, ax=ax, palette="magma")
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Musim")
st.pyplot(fig)
