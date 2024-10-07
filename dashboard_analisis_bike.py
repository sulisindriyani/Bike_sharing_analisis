import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


# Fungsi untuk memuat data
@st.cache_data
def load_data():
    hour_df = pd.read_csv('C:\\Users\\smart user\\Videos\\Bike-sharing-dataset\\hour.csv') 
    day_df = pd.read_csv('C:\\Users\\smart user\\Videos\\Bike-sharing-dataset\\hour.csv')    
    return hour_df, day_df

hour_df, day_df = load_data()


# Dashboard title
st.title(':bike: Bike Sharing Dashboard')

# Sidebar filtering data
st.sidebar.header("Rentang Waktu")
selected_hour = st.sidebar.selectbox("Pilih Jam:", options=["All"] + sorted(hour_df['hr'].unique().tolist()), key='hour_filter')
selected_date = st.sidebar.selectbox("Pilih Tanggal:", options=["All"] + sorted(hour_df['dteday'].unique().tolist()), key='date_filter')

# Filter data
filtered_data = hour_df.copy()
if selected_hour != "All":
    filtered_data = filtered_data[filtered_data['hr'] == selected_hour]
if selected_date != "All":
    filtered_data = filtered_data[filtered_data['dteday'] == selected_date]

# 1. waktu paling banyak pelanggan peyewaan sepeda
st.header("penyewaan sepeda berdasarkan jam")
 # Mengelompokkan dan menghitung total penyewaan per jam
popular_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()

# Mengubah kolom jam menjadi format waktu (misalnya '00:00', '01:00', dll.)
popular_hour['hr_formatted'] = popular_hour['hr'].astype(str).str.zfill(2) + ':00'

# Plot line chart dengan format jam yang diubah
fig1, ax1 = plt.subplots()
sns.lineplot(data=popular_hour, x='hr_formatted', y='cnt', ax=ax1, marker='o', color=sns.color_palette("Blues", n_colors=3)[2])  # Menggunakan warna biru yang lebih gelap
ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Jam')
ax1.set_xlabel('Jam')
ax1.set_ylabel('Jumlah Penyewaan')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')  # Mengatur rotasi agar label tidak tumpang tindih
st.pyplot(fig1)


# Menampilkan data yang difilter
st.subheader(f"Data Penyewaan untuk Jam: {selected_hour} dan Tanggal: {selected_date}")
st.write(filtered_data)

# 2. Tren penyewaan sepeda berdasarkan hari kerja dan libur
day_df['day_name'] = day_df['weekday'].replace({
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
})

day_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
day_df['day_name'] = pd.Categorical(day_df['day_name'], categories=day_order, ordered=True)

st.header("Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur")
weekday_trend = day_df.groupby('day_name')['cnt'].sum().reset_index()

# Plot bar chart for rentals per weekday
fig3, ax3 = plt.subplots()
sns.barplot(data=weekday_trend, x='day_name', y='cnt', ax=ax3, order=day_order, palette="Blues")  # Menggunakan palet biru
ax3.set_title('Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur')
ax3.set_xlabel('Hari')
ax3.set_ylabel('Jumlah Penyewaan')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=30, ha='right')
st.pyplot(fig3)


# Data
data = {
    'User Type': [0, 1, 2, 3, 4, 860, 871, 876, 885, 886],
    'Recency (Days)': [38, 0, 1, 0, 3, 97, 69, 68, 102, 110],
    'Frequency (Total Rentals)': [35, 294, 648, 1154, 1602, 967, 938, 1916, 976, 977],
    'Monetary (Total Time Rented)': [101, 1069, 2129, 3995, 5271, 16439, 15946, 32572, 16592, 17586]
}

# Membuat DataFrame
df = pd.DataFrame(data)

# 1. Analisis Deskriptif
st.title("Analisis Data RFM untuk Penyewaan Sepeda")

st.subheader("1. Analisis Deskriptif")
description = df.describe()
st.write(description)

# 2. Visualisasi dengan Line Chart
st.subheader("2. Visualisasi Data")

# Grafik Garis untuk Frequency vs Recency
st.subheader("Recency vs Frequency")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df.sort_values('Recency (Days)'), x='Recency (Days)', y='Frequency (Total Rentals)', marker='o', ax=ax)
ax.set_title('Recency vs Frequency')
ax.set_xlabel('Recency (Days)')
ax.set_ylabel('Frequency (Total Rentals)')
st.pyplot(fig)

# Grafik Garis untuk Monetary vs Frequency
st.subheader("Frequency vs Monetary")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df.sort_values('Frequency (Total Rentals)'), x='Frequency (Total Rentals)', y='Monetary (Total Time Rented)', marker='o', ax=ax2)
ax2.set_title('Frequency vs Monetary')
ax2.set_xlabel('Frequency (Total Rentals)')
ax2.set_ylabel('Monetary (Total Time Rented)')
st.pyplot(fig2)
