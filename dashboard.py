import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day_df = pd.read_csv("day.csv")

# Mapping angka ke nama bulan
month_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Streamlit UI
st.title("📊 Visualisasi Tren Penyewaan Sepeda Berdasarkan Cuaca")

# Dropdown Pilih Bulan
selected_month = st.selectbox("Pilih Bulan", ["Semua Bulan"] + list(month_mapping.values()))

# Plotting
plt.figure(figsize=(10, 5))
palette = {1: 'blue', 2: 'gray', 3: 'red'}
weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}

if selected_month == "Semua Bulan":
    # Visualisasi semua bulan
    sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=day_df, palette=palette)
    
    plt.title('📅 Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')

    # Ubah label x-axis → hanya tampilkan bulan genap (2,4,6,8,10,12)
    plt.xticks([2, 4, 6, 8, 10, 12], ['2', '4', '6', '8', '10', '12'])

    # Garis vertikal pada puncak penyewaan
    max_month = day_df.loc[day_df['cnt'].idxmax(), 'mnth']
    max_rentals = day_df['cnt'].max()
    plt.axvline(x=max_month, linestyle='--', color='black', alpha=0.6)
    plt.text(max_month, max_rentals, f'📌 Puncak Penyewaan\nBulan {max_month}',
             verticalalignment='bottom', horizontalalignment='right',
             fontsize=10, color='black')

    # 🔥 Kesimpulan untuk tren tahunan
    peak_month = month_mapping[max_month]
    st.markdown(f"""
    ### 📌 **Kesimpulan:**
    - Puncak penyewaan sepeda terjadi pada **{peak_month}**.
    - Kemungkinan faktor: cuaca yang lebih baik atau meningkatnya aktivitas luar ruangan.
    - Tren menunjukkan bahwa penggunaan sepeda lebih tinggi di bulan-bulan tertentu.
    """)
else:
    # Konversi nama bulan ke angka
    selected_month_num = list(month_mapping.keys())[list(month_mapping.values()).index(selected_month)]
    
    # Filter data untuk bulan yang dipilih
    filtered_df = day_df[day_df['mnth'] == selected_month_num]
    
    # Buat sumbu x lebih rapi (pakai hari dalam bulan, bukan format YYYY-MM-DD)
    filtered_df['day'] = pd.to_datetime(filtered_df['dteday']).dt.day
    
    sns.lineplot(x='day', y='cnt', hue='weathersit', data=filtered_df, palette=palette)
    
    plt.title(f'📆 Tren Penyewaan Sepeda di Bulan {selected_month}')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Penyewaan')
    
    # Atur label x-axis agar hanya menampilkan beberapa angka hari
    plt.xticks(range(1, 32, 5))

    # Hari dengan penyewaan terbanyak
    peak_day = filtered_df.loc[filtered_df['cnt'].idxmax(), 'day']
    max_rentals_day = filtered_df['cnt'].max()
    
    # 🔥 Kesimpulan untuk tren bulanan
    st.markdown(f"""
    ### 📌 **Kesimpulan:**
    - Puncak penyewaan di bulan **{selected_month}** terjadi pada tanggal **{peak_day}**.
    - Cuaca sangat mempengaruhi jumlah penyewaan, terutama pada hari-hari cerah.
    """)

# Tambah legenda
handles, labels = plt.gca().get_legend_handles_labels()
labels = [weather_labels[int(label)] for label in labels]
plt.legend(handles, labels, title='Kondisi Cuaca')

st.pyplot(plt)
