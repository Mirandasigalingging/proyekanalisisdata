# Proyek Analisis Data: Penyewaan Sepeda

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis pola penyewaan sepeda berdasarkan berbagai faktor, seperti musim, cuaca, dan waktu penggunaan. Data yang digunakan berasal dari dataset **Bike Sharing Dataset**, yang mencatat jumlah penyewaan sepeda setiap hari dan setiap jam.

Analisis dilakukan menggunakan **Python** dengan bantuan **Pandas, Matplotlib, Seaborn**, dan **Streamlit** untuk visualisasi interaktif.

---

## **Proses Analisis Data**
Analisis data dilakukan menggunakan Google Colab (`notebook.ipynb`) dan melibatkan tahapan berikut:

1. **Pengumpulan Data**: Memuat dataset `day.csv` dan `hour.csv` ke dalam Pandas DataFrame.
2. **Evaluasi Data**: Menilai kualitas data, termasuk identifikasi nilai yang hilang dan korelasi antar variabel.
3. **Pembersihan Data**: Menghapus kolom yang tidak relevan dan memastikan format data sesuai untuk analisis.
4. **Eksplorasi Data (EDA)**: Menganalisis pola dan tren dalam data, termasuk:
   - Heatmap korelasi untuk melihat hubungan antar variabel.
   - Boxplot untuk melihat distribusi penyewaan berdasarkan musim dan kondisi cuaca.
   - Teknik binning untuk mengelompokkan penyewaan sepeda ke dalam kategori **rendah, sedang, dan tinggi**.
   - Manual grouping berdasarkan musim untuk memahami pola penyewaan di berbagai musim.
5. **Visualisasi Data**: Membuat representasi visual menggunakan **Matplotlib** dan **Seaborn** untuk mengkomunikasikan temuan analisis.

---

## **Pertanyaan Penelitian**
Proyek ini dirancang untuk memahami pola penyewaan sepeda dan faktor-faktor yang mempengaruhinya, dengan menjawab pertanyaan berikut:

1️ **Bagaimana tren penggunaan sepeda setiap bulan dalam setahun terakhir, dan faktor apa yang paling memengaruhi peningkatannya?**  
   - Apakah cuaca berperan dalam perubahan pola penggunaan sepeda?  
   - Bagaimana tren penyewaan berubah dari bulan ke bulan?  

2️ **Pada jam berapa penggunaan sepeda paling tinggi dalam satu minggu terakhir, dan bagaimana pola perbedaannya antara hari kerja dan akhir pekan?**  
   - Apakah terdapat perbedaan pola penggunaan antara weekday dan weekend?  
   - Kapan jam sibuk utama penyewaan sepeda terjadi?  

---

## **Dashboard Streamlit**
Dashboard Streamlit (`dashboard.py`) menyajikan hasil analisis data secara **interaktif**. Pengguna dapat:

- **Melihat tren penyewaan bulanan berdasarkan kondisi cuaca** dengan filter bulan (**Januari - Desember** atau **seluruh tahun**) dan cuaca (**Cerah, Mendung, Hujan**).  
- **Menjelajahi pola penyewaan per jam** dengan perbandingan antara hari kerja dan akhir pekan.

### **Cara Menjalankan Dashboard**
1. **Pastikan telah menginstal dependensi yang diperlukan:**  
   ```bash
   pip install -r requirements.txt
   ```
2. **Jalankan dashboard Streamlit:**  
   ```bash
   streamlit run dashboard.py
   ```

Jika ingin menjalankan secara **lokal**, pastikan Anda berada dalam direktori proyek sebelum menjalankan perintah di atas.

---

## **Struktur Folder Submission**
```
submission
├───dashboard
│   ├───day.csv
│   ├───hour.csv
│   ├───dashboard.py
├───data
│   ├───day.csv
│   ├───hour.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

- **dashboard/** → Berisi kode **dashboard.py** dan dataset yang digunakan.
- **data/** → Menyimpan dataset mentah dalam format CSV.
- **notebook.ipynb** → Berisi analisis dan eksplorasi data menggunakan Google Colab.
- **README.md** → Berkas ini, berisi panduan lengkap proyek.
- **requirements.txt** → Daftar pustaka Python yang diperlukan untuk menjalankan analisis.
- **url.txt** → Berisi tautan ke **Streamlit Cloud** jika dashboard telah dideploy.

---

## **Kesimpulan Utama**
### 🔹 **1️ Tren Penyewaan Sepeda Berdasarkan Cuaca**
✔ Penyewaan sepeda meningkat saat cuaca **cerah** dan menurun saat **hujan**.  
✔ Puncak penyewaan terjadi di pertengahan tahun, kemungkinan karena **musim liburan atau musim panas**.  
✔ Faktor cuaca sangat memengaruhi pola penggunaan sepeda.  

### 🔹 **2️ Pola Penyewaan Sepeda Per Jam**
✔ Pada **hari kerja**, ada dua puncak penyewaan: **pagi dan sore hari**, terkait perjalanan kerja/sekolah.  
✔ Pada **akhir pekan**, penyewaan meningkat lebih **siang**, menunjukkan penggunaan untuk rekreasi.


