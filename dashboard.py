import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
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

# Mapping nama bulan
bulan_mapping = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Pilihan dropdown manual
print("Pilihan Bulan:")
print("0: Semua Bulan")
for k, v in bulan_mapping.items():
    print(f"{k}: {v}")

bulan_selected = int(input("Masukkan angka bulan yang dipilih: "))
cuaca_selected = input("Masukkan kondisi cuaca (Cerah/Mendung/Hujan/Semua Cuaca): ")

# Filter data
if bulan_selected != 0:
    df_merged = df_merged[df_merged["month_hour"] == bulan_selected]

if cuaca_selected.lower() != "semua cuaca":
    df_merged = df_merged[df_merged["weather_hour"].str.lower() == cuaca_selected.lower()]

# Tampilkan Data
print("\nData yang Ditampilkan:")
print(df_merged.head())

# Visualisasi Tren Jumlah Penyewa
plt.figure(figsize=(10, 5))
sns.lineplot(x="dteday", y="cnt_hour", data=df_merged)
plt.title("Tren Penyewaan Sepeda")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewa")
plt.xticks(rotation=45)
plt.show()

# Kesimpulan
if df_merged.empty:
    print("\n⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    max_hari = df_merged.loc[df_merged["cnt_hour"].idxmax()]
    min_hari = df_merged.loc[df_merged["cnt_hour"].idxmin()]
    
    print(f"\n📈 Hari dengan penyewaan tertinggi: {max_hari['dteday'].date()} ({max_hari['cnt_hour']} penyewa)")
    print(f"📉 Hari dengan penyewaan terendah: {min_hari['dteday'].date()} ({min_hari['cnt_hour']} penyewa)")
