# Import library yang dibutuhkan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('your_dataset.csv')  # Sesuaikan dengan nama dataset

# Sidebar Filters
st.sidebar.header('Filter Data')
tahun_options = ['Semua'] + sorted(df['year'].unique().tolist())
cuaca_options = ['Semua'] + sorted(df['weathersit'].unique().tolist())

selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_options)
selected_cuaca = st.sidebar.selectbox("Pilih Cuaca", cuaca_options)

# Filter Data
filtered_df = df.copy()
if selected_tahun != "Semua":
    filtered_df = filtered_df[filtered_df['year'] == selected_tahun]
if selected_cuaca != "Semua":
    filtered_df = filtered_df[filtered_df['weathersit'] == selected_cuaca]

# Judul Dashboard
st.title("Analisis Data Penyewaan Sepeda")
st.write("Dashboard ini menyajikan hasil analisis data berdasarkan faktor cuaca dan tahun.")

# Visualisasi 1: Jumlah Penyewaan Sepeda per Bulan
st.subheader("Jumlah Penyewaan Sepeda per Bulan")
plt.figure(figsize=(10, 5))
sns.barplot(x='month', y='cnt', data=filtered_df, ci=None, palette='Blues')
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

# Visualisasi 2: Pengaruh Cuaca terhadap Penyewaan
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
plt.figure(figsize=(8, 5))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df, palette='Set2')
plt.xlabel("Cuaca")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

# Visualisasi 3: Tren Penyewaan Sepeda per Tahun
st.subheader("Tren Penyewaan Sepeda per Tahun")
plt.figure(figsize=(10, 5))
sns.lineplot(x='year', y='cnt', data=filtered_df, marker='o', color='red')
plt.xlabel("Tahun")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

st.write("**Catatan:** Data di atas dapat difilter berdasarkan tahun dan cuaca menggunakan panel di sebelah kiri.")
