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
st.pyplot(plt)

# Analisis Data RFM
# Assuming you have your hour_df DataFrame already created
# Convert 'dteday' to datetime format
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Calculate the latest date in the dataset
latest_date = hour_df['dteday'].max()

# Calculate Recency in days
hour_df['Recency'] = (latest_date - hour_df['dteday']).dt.days

# Calculate Frequency by summing up counts of rentals
frequency = hour_df.groupby('registered')['cnt'].sum().reset_index()

# Calculate Monetary value based on counts and hours
hour_df['Monetary'] = hour_df['cnt'] * hour_df['hr']

# Create the RFM DataFrame
rfm = hour_df.groupby('registered').agg({
    'Recency': 'min',
    'cnt': 'sum',
    'Monetary': 'sum'
}).reset_index()

# Rename the columns for clarity
rfm.columns = ['User Type', 'Recency (Days)', 'Frequency (Total Rentals)', 'Monetary (Total Time Rented)']

# Set up the subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4"] * 5  # Keeping the same color for all bars

# Recency plot
sns.barplot(y="Recency (Days)", x="User Type", data=rfm.sort_values(by="Recency (Days)", ascending=True).head(5), palette=colors, ax=ax[0], hue="User Type", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (Days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)

# Frequency plot
sns.barplot(y="Frequency (Total Rentals)", x="User Type", data=rfm.sort_values(by="Frequency (Total Rentals)", ascending=False).head(5), palette=colors, ax=ax[1], hue="User Type", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

# Monetary plot
sns.barplot(y="Monetary (Total Time Rented)", x="User Type", data=rfm.sort_values(by="Monetary (Total Time Rented)", ascending=False).head(5), palette=colors, ax=ax[2], hue="User Type", legend=False)
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

# Overall title
plt.suptitle("Best Customers Based on RFM Parameters (User Type)", fontsize=20)
st.pyplot(fig)
