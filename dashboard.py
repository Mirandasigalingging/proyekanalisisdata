import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data (gantilah dengan path dataset yang sesuai)
data = pd.read_csv('C:\Users\mirandabintangms_\Downloads\KULIAH\SEM 5\MBKM\submission\dashboard\day.csv')

# Pastikan kolom yang relevan ada
data['month'] = pd.to_datetime(data['date']).dt.strftime('%B')  # Ubah angka bulan ke nama

# Mapping cuaca dari angka ke kategori
weather_mapping = {
    1: 'Cerah',
    2: 'Mendung',
    3: 'Hujan'
}
data['weather'] = data['weather'].map(weather_mapping)

# Sidebar untuk memilih bulan dan cuaca
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", sorted(data['month'].unique()))
selected_weather = st.sidebar.selectbox("Pilih Cuaca", sorted(data['weather'].dropna().unique()))

# Filter data berdasarkan pilihan pengguna
filtered_data = data[(data['month'] == selected_month) & (data['weather'] == selected_weather)]

st.title(f"Visualisasi Data untuk {selected_month} - {selected_weather}")

# Visualisasi jumlah pengguna sepeda per jam
st.subheader("Penggunaan Sepeda Per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='hour', y='count', data=filtered_data, ax=ax, palette='coolwarm')
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Visualisasi pola penggunaan sepeda per musim
st.subheader("Pola Penggunaan Sepeda per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='season', y='count', data=data, palette='pastel')
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

st.write("Sumber data: Dataset penggunaan sepeda")
