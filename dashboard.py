import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mapping angka ke nama bulan
month_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Mapping angka ke kondisi cuaca
weather_mapping = {
    1: "Cerah",
    2: "Mendung",
    3: "Hujan"
}

# Streamlit UI
st.title("📊 Analisis Penyewaan Sepeda")

# Dropdown Pilih Bulan
selected_month = st.selectbox("Pilih Bulan", ["Semua Bulan"] + list(month_mapping.values()))

# Dropdown Pilih Cuaca
selected_weather = st.selectbox("Pilih Kondisi Cuaca", ["Semua Cuaca"] + list(weather_mapping.values()))

# --- VISUALISASI 1: Tren Penyewaan Berdasarkan Cuaca ---
st.subheader("🚴‍♂️ Tren Penyewaan Sepeda Berdasarkan Cuaca")

plt.figure(figsize=(10, 5))
palette = {1: 'blue', 2: 'gray', 3: 'red'}
weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}

# Filtering data sesuai pilihan pengguna
filtered_day_df = day_df.copy()
if selected_month != "Semua Bulan":
    selected_month_num = list(month_mapping.keys())[list(month_mapping.values()).index(selected_month)]
    filtered_day_df = filtered_day_df[filtered_day_df['mnth'] == selected_month_num]

if selected_weather != "Semua Cuaca":
    selected_weather_num = list(weather_mapping.keys())[list(weather_mapping.values()).index(selected_weather)]
    filtered_day_df = filtered_day_df[filtered_day_df['weathersit'] == selected_weather_num]

if selected_month == "Semua Bulan":
    # Semua bulan → Tampilkan bulan genap
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=filtered_day_df, palette=palette)
    plt.xticks([2, 4, 6, 8, 10, 12], ['2', '4', '6', '8', '10', '12'])
    plt.xlabel("Bulan")
else:
    # Satu bulan → Tampilkan tanggal (tanpa format YYYY-MM-DD)
    filtered_day_df['day'] = pd.to_datetime(filtered_day_df['dteday']).dt.day
    sns.lineplot(x='day', y='cnt', hue='weathersit', data=filtered_day_df, palette=palette)
    plt.xticks(range(1, 32, 5))
    plt.xlabel("Hari dalam Bulan")

plt.ylabel("Jumlah Penyewaan")
plt.title(f"📅 Tren Penyewaan Sepeda di {selected_month} ({selected_weather})")

# Tambah legenda
handles, labels = plt.gca().get_legend_handles_labels()
labels = [weather_labels[int(label)] for label in labels]
plt.legend(handles, labels, title="Kondisi Cuaca")

# Garis vertikal untuk puncak penyewaan
if not filtered_day_df.empty:
    max_idx = filtered_day_df['cnt'].idxmax()
    peak_x = filtered_day_df.loc[max_idx, 'mnth' if selected_month == "Semua Bulan" else 'day']
    peak_y = filtered_day_df['cnt'].max()
    plt.axvline(x=peak_x, linestyle='--', color='black', alpha=0.6)
    plt.text(peak_x, peak_y, f'📌 Puncak\n({peak_x})', verticalalignment='bottom', horizontalalignment='right')

st.pyplot(plt)

# --- VISUALISASI 2: Tren Penyewaan Hari Kerja vs Akhir Pekan ---
st.subheader("🗓️ Tren Penyewaan Sepeda di Hari Kerja vs Akhir Pekan")

plt.figure(figsize=(12, 6))

# Visualisasi dengan format seperti di Google Colab
ax = sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette={0: 'orange', 1: 'blue'})

# Ubah legenda sesuai dengan label yang benar
legend_labels = ['Akhir Pekan', 'Hari Kerja']
for t, l in zip(ax.legend_.texts, legend_labels):
    t.set_text(l)

plt.title("Pola Penggunaan Sepeda per Jam antara Hari Kerja dan Akhir Pekan")
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(range(0, 24, 2))

st.pyplot(plt)

# --- KESIMPULAN ---
st.subheader("📌 Kesimpulan")
if selected_month == "Semua Bulan":
    peak_month = month_mapping[filtered_day_df.loc[filtered_day_df['cnt'].idxmax(), 'mnth']]
    st.markdown(f"""
    - Puncak penyewaan sepeda terjadi di bulan **{peak_month}**.
    - Faktor cuaca memengaruhi pola penyewaan, terutama saat cerah.
    - Tren penyewaan **lebih tinggi di hari kerja saat jam sibuk** (pagi & sore).
    """)
else:
    peak_day = filtered_day_df.loc[filtered_day_df['cnt'].idxmax(), 'day']
    st.markdown(f"""
    - Di bulan **{selected_month}**, puncak penyewaan terjadi pada tanggal **{peak_day}**.
    - Penyewaan sepeda lebih tinggi saat cuaca cerah dibanding hujan.
    - Hari kerja memiliki pola penyewaan **lebih tinggi di pagi dan sore hari** dibanding akhir pekan.
    """)

st.success("✅ Analisis selesai! Gunakan filter untuk eksplorasi lebih lanjut.")
