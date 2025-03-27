import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk load dataset
@st.cache_data
def load_data():
    df_hour = pd.read_csv("hour.csv")  
    df_day = pd.read_csv("day.csv")  

    # Konversi ke datetime
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])

    # Tambahkan kolom bulan & kondisi cuaca
    df_hour['month'] = df_hour['dteday'].dt.month
    df_day['month'] = df_day['dteday'].dt.month

    df_hour['weather'] = df_hour['weathersit'].map({1: "Cerah", 2: "Mendung", 3: "Hujan"})
    df_day['weather'] = df_day['weathersit'].map({1: "Cerah", 2: "Mendung", 3: "Hujan"})

    # Gabungkan kedua dataset (berdasarkan tanggal)
    df_merged = pd.merge(df_hour, df_day, on="dteday", suffixes=("_hour", "_day"))
    
    return df_merged

# Load data
data = load_data()

# Mapping nama bulan
bulan_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Sidebar filter
st.sidebar.header("Filter Data")
bulan_selected = st.sidebar.selectbox("Pilih Bulan:", ["Semua Bulan"] + list(bulan_mapping.values()))
cuaca_selected = st.sidebar.selectbox("Pilih Kondisi Cuaca:", ["Semua Cuaca", "Cerah", "Mendung", "Hujan"])

# Filter data berdasarkan pilihan
if bulan_selected != "Semua Bulan":
    bulan_num = [k for k, v in bulan_mapping.items() if v == bulan_selected][0]
    data = data[data["month_hour"] == bulan_num]

if cuaca_selected != "Semua Cuaca":
    data = data[data["weather_hour"] == cuaca_selected]

# Tampilkan Data
st.write("## Data yang Ditampilkan")
st.dataframe(data)

# Visualisasi Tren Jumlah Penyewa
st.write("## Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="dteday", y="cnt_hour", data=data, ax=ax)
ax.set_title("Tren Penyewaan Sepeda")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Kesimpulan
st.write("## Kesimpulan")
if data.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    max_hari = data.loc[data["cnt_hour"].idxmax()]
    min_hari = data.loc[data["cnt_hour"].idxmin()]
    
    st.success(f"📈 Hari dengan penyewaan tertinggi: **{max_hari['dteday'].date()}** ({max_hari['cnt_hour']} penyewa)")
    st.error(f"📉 Hari dengan penyewaan terendah: **{min_hari['dteday'].date()}** ({min_hari['cnt_hour']} penyewa)")
