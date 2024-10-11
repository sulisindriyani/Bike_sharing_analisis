import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

@st.cache_data
def load_data():
    hour_df = pd.read_csv('./Bike-sharing-dataset/hour.csv')
    day_df = pd.read_csv('./Bike-sharing-dataset/day.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return hour_df, day_df

hour_df, day_df = load_data()

st.title(':bike: Bike Sharing Dashboard')

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

st.sidebar.header("Rentang Waktu")
start_date, end_date = st.sidebar.date_input(
    label='Rentang Tanggal',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
    key='date_range'
)

selected_hour = st.sidebar.selectbox(
    "Pilih Jam:",
    options=["All"] + sorted(hour_df['hr'].unique().tolist()),
    key='hour_filter'
)

# Filter data waktu
filtered_data = hour_df.copy()
filtered_data['dteday'] = pd.to_datetime(filtered_data['dteday'])

if start_date and end_date:
    filtered_data = filtered_data[
        (filtered_data['dteday'] >= pd.to_datetime(start_date)) & 
        (filtered_data['dteday'] <= pd.to_datetime(end_date))
    ]

if selected_hour != "All":
    filtered_data = filtered_data[filtered_data['hr'] == selected_hour]

st.subheader(f"Data Penyewaan untuk Jam: {selected_hour} dan Tanggal: {start_date} sampai {end_date}")
st.write(filtered_data)

# 2. Mengelompokkan dan menghitung total penyewaan per jam
# Data
data = {
    'instant': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'dteday': ['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04', '2011-01-05', 
               '2011-01-06', '2011-01-07', '2011-01-08', '2011-01-09', '2011-01-10'],
    'workingday': [0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
    'cnt': [10, 20, 30, 40, 50, 10, 20, 30, 40, 50]
}

# Membuat DataFrame dari data
df = pd.DataFrame(data)

# Mengelompokkan data berdasarkan workingday
grouped_df = df.groupby('workingday')['cnt'].sum().reset_index()

# Mengubah nilai workingday untuk label yang lebih baik
grouped_df['workingday'] = grouped_df['workingday'].replace({0: 'Hari Libur', 1: 'Hari Kerja'})

# Mengatur figure dan axes
plt.figure(figsize=(8, 6))

# Menggunakan seaborn untuk membuat barplot
sns.barplot(x='workingday', y='cnt', data=grouped_df, palette='viridis')

# Menambahkan judul dan label
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur', fontsize=15, fontweight='bold')
plt.xlabel('Jenis Hari', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)

# Menampilkan plot
plt.grid(axis='y')
plt.show()

# Analisis Data RFM
data = {
    'User Type': [0, 1, 2, 3, 4, 860, 871, 876, 885, 886],
    'Recency (Days)': [38, 0, 1, 0, 3, 97, 69, 68, 102, 110],
    'Frequency (Total Rentals)': [35, 294, 648, 1154, 1602, 967, 938, 1916, 976, 977],
    'Monetary (Total Time Rented)': [101, 1069, 2129, 3995, 5271, 16439, 15946, 32572, 16592, 17586]
}
df = pd.DataFrame(data)

st.title("Analisis Data RFM untuk Penyewaan Sepeda")
st.subheader("Analisis Deskriptif")
description = df.describe()
st.write(description)

# Visualisasi Data
st.subheader("Recency vs Frequency")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df.sort_values('Recency (Days)'), x='Recency (Days)', y='Frequency (Total Rentals)', marker='o', ax=ax)
ax.set_title('Recency vs Frequency')
ax.set_xlabel('Recency (Days)')
ax.set_ylabel('Frequency (Total Rentals)')
st.pyplot(fig)

st.subheader("Frequency vs Monetary")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df.sort_values('Frequency (Total Rentals)'), x='Frequency (Total Rentals)', y='Monetary (Total Time Rented)', marker='o', ax=ax2)
ax2.set_title('Frequency vs Monetary')
ax2.set_xlabel('Frequency (Total Rentals)')
ax2.set_ylabel('Monetary (Total Time Rented)')
st.pyplot(fig2)
