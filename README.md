# Bike_sharing_analisis

Bike Sharing Dashboard adalah dashboard visualisasi data berbasis Streamlit yang menyediakan analisis mengenai penyewaan sepeda <br>
yang melakukan filter data berdasarkan jam dan tanggal, serta menampilkan visualisasi data berupa tabel dan grafik penyewaan sepeda.<br>
Dalam dashboard ini menampilkan visualisasi berdasarkan waktu paling populer dalam penyewaan sepeda<br>
Penyewaan Berdasarkan Hari Kerja dan Libur dan analisis lanjutan:<br>
yang berisi tentang Grafik Garis untuk Frequency vs Recency , Grafik Garis untuk Monetary vs Frequency<br>


# Fitur yang di tampilkan:
- Data Penyewaan untuk Jam : berisi detail penyewaan sepeda dengan keterangan jam dan tanggal
- Penyewaan Sepeda Berdasarkan Jam: Menampilkan waktu paling banyak pelanggan dalam penyewaan sepeda.
- Penyewaan sepeda di Hari Libur dan kerja: Menampilkan perbandingan jumlah penyewaan pada hari libur dan hari kerja.
- Analisis Lanjutan:
                    - menampilkan keterangan penyewaan sepeda dengan perbandingan hari, total rental dan total jam penewaan

# syarat sistem
1. pastikan memiliki library python yang dibutuhkan, jika belum bisa instal dengan perintah:
   pip install -r requirements.txt
2. jika sudah  library yang di butuhkan akan ada di dalam berkas requirements.txt

# Cara mnjalankan Aplikasi<br>
1. Unduh berkas<br>
2. buka Command Prompt <br>
2. Pastikan Streamlit Terpasang<br>
   pip install streamlit<br>
3. Navigasi ke Folder Proyek<br>
  "C:/Users/smart user/Videos/dashboard/dashboard/dashboard_analisis_bike.py" <br>
4. Jalankan Aplikasi Streamlit<br>
   streamlit run nama_file_anda.py<br>
misal: streamlit run "C:/Users/smart user/Videos/dashboard/dashboard/dashboard_analisis_bike.py"<br>
5. Setelah menjalankan perintah tersebut, Streamlit akan menampilkan tautan lokal tersebut<br>

#struktur berkas
1. dataset : berisi berkas bahan analisi
   ( datataset yang digunkan bike-sharing-dataset )
2. notrbook_analisis.ipynb ; berisi berkas olahan dari datase mulai dari Gathering Data sampai Explanatory Analysiss.
3. dashboard ; berisi kode untuk menjalankan  dashboard Streamlit (Dashboard).
4. requirements.txt: Berisi daftar library Python yang digunakan untuk menjalankan aplikasi.
5. url.txt : Berisi tautan untuk dashboard setelah di deploy
6. README.md: Berisi dokumentasi ini termasuk didalamnya cara menjalankan dashboard.

# Dataset<br>
yang di gunakan yaitu:<Br>
- hour.csv: Dataset yang berisi data penyewaan sepeda berdasarkan jam.<br>
- day.csv: Dataset yang berisi data penyewaan sepeda berdasarkan hari.<br>

