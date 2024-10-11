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

# 1. Mengelompokkan dan menghitung total penyewaan per jam
popular_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()

# Mengubah kolom jam menjadi format waktu
popular_hour['hr_formatted'] = popular_hour['hr'].astype(str).str.zfill(2) + ':00'

st.title("Penyewaan Sepeda Berdasarkan jam")
# Plot line chart
fig1, ax1 = plt.subplots()
sns.lineplot(data=popular_hour, x='hr_formatted', y='cnt', ax=ax1, marker='o', color=sns.color_palette("Blues", n_colors=3)[2])
ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Jam')
ax1.set_xlabel('Jam')
ax1.set_ylabel('Jumlah Penyewaan')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig1)


# 2. penyewaan di hari libur dan hari kerja
day_df['category'] = day_df['weekday'].apply(lambda x: 'Hari Kerja' if x < 5 else 'Hari Libur')

# Hitung rata-rata penyewaan berdasarkan kategori
avg_rentals = day_df.groupby('category')['cnt'].mean().reset_index()

st.title("penyewaan sepeda di hari kerja dan hari libur")
# Visualisasi
plt.figure(figsize=(10, 6))
sns.barplot(data=avg_rentals, x='category', y='cnt')
plt.title('Perbandingan Rata-rata Penyewaan Sepeda: Hari Kerja vs Hari Libur')
plt.xlabel('Kategori')
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
plt.grid(True)
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
