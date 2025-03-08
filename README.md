# Analisis Data Penyewaan Sepeda (Harian & Per Jam)

Proyek ini bertujuan untuk menginvestigasi data penyewaan sepeda guna memahami pola penggunaan dan faktor-faktor yang mempengaruhinya. Data yang digunakan berasal dari Bike Sharing Dataset, yang mencakup informasi tentang penyewaan sepeda harian dan per jam.

## Dataset

Dataset yang digunakan dalam proyek ini adalah:

* `day.csv`: Data yang mencatat penyewaan sepeda setiap hari.
* `hour.csv`: Data yang mencatat penyewaan sepeda setiap jam.

Kedua dataset ini tersedia di direktori `data/`.

## Proses Analisis Data

Analisis data dilakukan menggunakan Google Colab (`notebook.ipynb`) dan melibatkan tahapan berikut:

1.  Pengumpulan Data: Memuat dataset ke dalam struktur data Pandas DataFrame.
2.  Evaluasi Data: Menilai kualitas data, termasuk identifikasi nilai yang hilang.
3.  Pembersihan Data: Memperbaiki inkonsistensi atau data yang tidak relevan.
4.  Eksplorasi Data: Menganalisis pola dan tren dalam data untuk menjawab pertanyaan bisnis.
5.  Visualisasi Data: Membuat representasi visual untuk mengkomunikasikan temuan analisis.

## Pertanyaan Penelitian

Proyek ini dirancang untuk menjawab pertanyaan-pertanyaan berikut:

Pertanyaan 1 : Bagaimana tren penggunaan sepeda setiap bulan dalam setahun terakhir, dan faktor apa yang paling memengaruhi peningkatannya?

Pertanyaan 2 : Pada jam berapa penggunaan sepeda paling tinggi dalam satu minggu terakhir, dan bagaimana pola perbedaannya antara hari kerja dan akhir pekan?

## Visualisasi Hasil

Visualisasi data dibuat menggunakan Matplotlib dan Seaborn, dan disajikan dalam dashboard interaktif yang dibuat dengan Streamlit.

## Dashboard Streamlit

Dashboard Streamlit (`dashboard.py`) menyajikan hasil analisis data secara interaktif. Pengguna dapat memilih antara dataset harian atau per jam untuk melihat visualisasi dan kesimpulan.

### Cara Menjalankan Dashboard

1.  Pastikan semua pustaka yang diperlukan telah terinstal. Anda dapat menginstal pustaka-pustaka ini menggunakan `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

2.  Jalankan aplikasi Streamlit:

    ```bash
    streamlit run dashboard.py
    ```

3.  Buka peramban web Anda dan kunjungi `http://localhost:8501`.

### Tautan Dashboard (Streamlit Cloud)

Dashboard telah di-deploy ke Streamlit Cloud, Anda dapat mengaksesnya melalui tautan berikut:

* [https://mirandasigalingging-proyekanalisisdata-dashboard-y4du0p.streamlit.app/](https://mirandasigalingging-proyekanalisisdata-dashboard-y4du0p.streamlit.app/)
