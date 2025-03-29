import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Simulasi Data (Gantilah dengan data aslinya)
data = {
    'mnth': list(range(1, 13)) * 3,  # 12 bulan dikalikan 3 jenis cuaca
    'cnt': [1000 + i*300 for i in range(12)] * 3,  # Contoh jumlah penyewaan
    'weathersit': [1] * 12 + [2] * 12 + [3] * 12  # 1: Cerah, 2: Mendung, 3: Hujan
}
day_df = pd.DataFrame(data)

# Warna untuk setiap kondisi cuaca
palette = {1: 'blue', 2: 'gray', 3: 'red'}
weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan'}

# ==== 1. Visualisasi Tren Penyewaan Tiap Bulan ====
plt.figure(figsize=(10, 5))
sns.lineplot(x='mnth', y='cnt', hue='weathersit', data=day_df, palette=palette)

plt.title('Tren Penyewaan Sepeda Tiap Bulan Berdasarkan Kondisi Cuaca')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')

# Ganti angka bulan menjadi nama bulan
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
plt.xticks(ticks=range(1, 13), labels=bulan_labels)

# Ganti label legenda dengan teks cuaca
handles, labels = plt.gca().get_legend_handles_labels()
labels = [weather_labels[int(label)] for label in labels]
plt.legend(handles, labels, title='Kondisi Cuaca')

# Tambahkan garis dan label untuk bulan dengan penyewaan tertinggi
max_month = day_df.loc[day_df['cnt'].idxmax(), 'mnth']
max_rentals = day_df['cnt'].max()
plt.axvline(x=max_month, linestyle='--', color='black', alpha=0.6)
plt.text(max_month, max_rentals, f'Puncak Penyewaan\nBulan {bulan_labels[max_month-1]}',
         verticalalignment='bottom', horizontalalignment='right',
         fontsize=10, color='black')

plt.show()

# ==== 2. Visualisasi Tren Penyewaan di Bulan Tertentu (Januari) ====
# Simulasi data harian untuk Januari
data_jan = {
    'day': list(range(1, 32)),  # Hari dalam Januari
    'cnt': [1000 + i*50 for i in range(31)],  # Contoh jumlah penyewaan
    'weathersit': [1 if i % 3 == 0 else 2 if i % 3 == 1 else 3 for i in range(31)]  # Kondisi cuaca
}
df_jan = pd.DataFrame(data_jan)

plt.figure(figsize=(10, 5))
sns.lineplot(x='day', y='cnt', hue='weathersit', data=df_jan, palette=palette)

plt.title('Tren Penyewaan Sepeda di Bulan Januari')
plt.xlabel('Hari dalam Januari')
plt.ylabel('Jumlah Penyewaan')

# Ganti label legenda dengan teks cuaca
handles, labels = plt.gca().get_legend_handles_labels()
labels = [weather_labels[int(label)] for label in labels]
plt.legend(handles, labels, title='Kondisi Cuaca')

# Rotasi sumbu x agar lebih rapi
plt.xticks(rotation=45)

plt.show()
