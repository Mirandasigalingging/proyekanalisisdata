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

st.title("🚴 Analisis Penyewaan Sepeda (Harian & Per Jam)")

dataset_choice = st.sidebar.radio("Pilih Dataset", ["Harian", "Per Jam"])

if dataset_choice == "Harian":
    st.subheader("📅 Tren Penyewaan Sepeda Harian")
    
    def season(month):
        if month in [12, 1, 2]: return 'Hujan'
        elif month in [3, 4, 5]: return 'Peralihan ke Kemarau'
        elif month in [6, 7, 8, 9]: return 'Kemarau'
        else: return 'Peralihan ke Hujan'

    day_df["Musim"] = day_df["mnth"].apply(season)

    fig, ax = plt.subplots()
    sns.boxplot(x="Musim", y="cnt", data=day_df, ax=ax, palette="Set2")
    st.pyplot(fig)

    st.subheader("📌 Kesimpulan Harian")
    st.write("""
    - Penyewaan sepeda lebih tinggi di **musim kemarau** dibanding musim hujan.
    - Tren harian menunjukkan peningkatan di bulan tertentu, menunjukkan pola musiman.
    """)

elif dataset_choice == "Per Jam":
    st.subheader("⏰ Pola Penyewaan Sepeda Per Jam")

    def time_of_day(hour):
        if 0 <= hour < 6: return "Dini Hari"
        elif 6 <= hour < 12: return "Pagi"
        elif 12 <= hour < 18: return "Siang"
        else: return "Malam"

    hour_df["Waktu"] = hour_df["hr"].apply(time_of_day)

    fig, ax = plt.subplots()
    sns.boxplot(x="Waktu", y="cnt", data=hour_df, ax=ax, palette="coolwarm")
    st.pyplot(fig)

    st.subheader("📌 Kesimpulan Per Jam")
    st.write("""
    - Penyewaan sepeda cenderung tinggi di **pagi & sore hari** (waktu kerja dan pulang kerja).
    - **Malam hari dan dini hari** memiliki jumlah penyewaan yang lebih rendah.
    """)

st.sidebar.markdown("💡 **Tip:** Pilih dataset di sidebar untuk melihat analisisnya.")