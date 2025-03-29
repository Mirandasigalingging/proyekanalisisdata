import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df_hour = pd.read_csv("hour.csv")
    df_day = pd.read_csv("day.csv")

    # Konversi ke datetime
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])

    # Tambahkan kolom bulan & cuaca
    df_hour['month'] = df_hour['dteday'].dt.month
    df_day['month'] = df_day['dteday'].dt.month

    df_hour['weather'] = df_hour['weathersit'].map({1: "Cerah", 2: "Mendung", 3: "Hujan"})
    df_day['weather'] = df_day['weathersit'].map({1: "Cerah", 2: "Mendung", 3: "Hujan"})

    # Gabungkan dataset berdasarkan tanggal
    df_merged = pd.merge(df_hour, df_day, on="dteday", suffixes=("_hour", "_day"))

    return df_merged

# Load Data
df = load_data()

# Mapping nama bulan
bulan_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Sidebar Interaktif
st.sidebar.title("Filter Data 🚴")
bulan_selected = st.sidebar.selectbox("Pilih Bulan:", ["Semua Bulan"] + list(bulan_mapping.values()))
cuaca_selected = st.sidebar.selectbox("Pilih Kondisi Cuaca:", ["Semua Cuaca", "Cerah", "Mendung", "Hujan"])

# Filtering Data
with st.spinner("Sedang memproses data..."):
    if bulan_selected != "Semua Bulan":
        bulan_num = list(bulan_mapping.keys())[list(bulan_mapping.values()).index(bulan_selected)]
        df = df[df["month_hour"] == bulan_num]

    if cuaca_selected != "Semua Cuaca":
        df = df[df["weather_hour"] == cuaca_selected]

    # Jika data kosong setelah difilter
    if df.empty:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
    else:
        # Tampilkan Data
        st.subheader("📊 Data Penyewaan Sepeda")
        st.dataframe(df.head())

        # Visualisasi Tren Penyewaan
        st.subheader("📈 Tren Penyewaan Sepeda")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="dteday", y="cnt_hour", data=df, ax=ax)
        ax.set_title("Tren Penyewaan Sepeda")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Penyewa")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Kesimpulan
        max_hari = df.loc[df["cnt_hour"].idxmax()]
        min_hari = df.loc[df["cnt_hour"].idxmin()]

        st.subheader("📌 Kesimpulan")
        st.write(f"📈 **Hari dengan penyewaan tertinggi:** {max_hari['dteday'].date()} ({max_hari['cnt_hour']} penyewa)")
        st.write(f"📉 **Hari dengan penyewaan terendah:** {min_hari['dteday'].date()} ({min_hari['cnt_hour']} penyewa)")
