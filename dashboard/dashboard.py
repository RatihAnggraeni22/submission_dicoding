import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

sns.set(style='dark')

# Load dataset
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")


# Define min and max dates
min_date = pd.to_datetime("2011-01-01")
max_date = pd.to_datetime("2012-12-31")

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

def filter_day_by_date(day_df, start_date, end_date):
    """Menyaring DataFrame hari berdasarkan tanggal mulai dan tanggal akhir."""
    return day_df.query(f'dteday >= "{start_date}" and dteday <= "{end_date}"')


# Menyaring DataFrame berdasarkan tanggal yang dipilih
main_df_day = filter_day_by_date(day_df, start_date, end_date)
main_df_hour = filter_day_by_date(hour_df, start_date, end_date)

# Agregasi Data
day_df_count_2011 = filter_day_by_date(main_df_day, "2011-01-01", "2012-12-31")

# Mengubah kolom tanggal menjadi tipe datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Asumsi: kolom 'month' adalah kategorikal, ubah menjadi numerik
hour_df['month'] = pd.to_numeric(hour_df['month'], errors='coerce')

# Menentukan bulan terakhir
bulan_terakhir = hour_df['month'].max()
tahun_terakhir = hour_df['year'].max()

# Memfilter data berdasarkan bulan terakhir
data_bulan_terakhir = hour_df[(hour_df['year'] == tahun_terakhir) & (hour_df['month'] == bulan_terakhir)]

# Cek kolom yang ada
print(data_bulan_terakhir.columns)

# Memastikan ada kolom yang diperlukan
if 'count' not in data_bulan_terakhir.columns or 'workingday' not in data_bulan_terakhir.columns:
    print("Kolom 'count' atau 'workingday' tidak ditemukan dalam DataFrame.")
else:
    # Membuat kolom 'weekend' untuk menandai akhir pekan (dalam hal ini Sabtu = 6 dan Minggu = 0)
    data_bulan_terakhir['weekend'] = data_bulan_terakhir['workingday'].isin([6, 0])

    # Menghitung total peminjaman pada akhir pekan dan hari kerja
    total_peminjaman_akhir_pekan = data_bulan_terakhir[data_bulan_terakhir['weekend']]['count'].sum()
    total_peminjaman_hari_kerja = data_bulan_terakhir[~data_bulan_terakhir['weekend']]['count'].sum()

    # Menghitung persentase peningkatan
    persentase_peningkatan = ((total_peminjaman_akhir_pekan - total_peminjaman_hari_kerja) / total_peminjaman_hari_kerja) * 100

    st.subheader("Berapa peningkatan jumlah peminjaman sepeda pada akhir pekan dibandingkan hari kerja dalam satu bulan terakhir?")

    # Menampilkan hasil

    # Visualisasi
    plt.figure(figsize=(8, 5))
    plt.bar(['Akhir Pekan', 'Hari Kerja'], [total_peminjaman_akhir_pekan, total_peminjaman_hari_kerja], color=['#FF7F7F', '#90CAF9'])
    plt.xlabel('Hari', fontsize=12)
    plt.ylabel('Jumlah Peminjaman', fontsize=12)
    plt.title('Perbandingan Jumlah Peminjaman Sepeda pada Bulan Terakhir', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tampilkan diagram di Streamlit
    st.pyplot(plt)

# Mengubah kolom tanggal menjadi tipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'], errors='coerce')  # Pastikan kolom dteday dalam format datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], errors='coerce')

# Cek jika konversi berhasil
if day_df['dteday'].isnull().any():
    st.error("Ada tanggal yang tidak valid di kolom 'dteday'. Silakan periksa data.")
else:
    st.subheader("Bagaimana tren jumlah peminjaman sepeda pada hari libur (holiday) dibandingkan dengan hari biasa dalam enam bulan terakhir?")

    # Menambahkan kolom 'weekday'
    day_df['weekday'] = day_df['dteday'].dt.weekday

    # Filter data untuk tahun 2011
    data_2011 = day_df[day_df['dteday'].dt.year == 2011]

    # Menghitung total peminjaman pada akhir pekan dan hari kerja
    peminjaman_akhir_pekan = data_2011[data_2011['weekday'].isin([5, 6])].groupby('dteday')['count'].sum()
    peminjaman_hari_kerja = data_2011[~data_2011['weekday'].isin([5, 6])].groupby('dteday')['count'].sum()

    # Plot tren jumlah peminjaman sepeda
    plt.figure(figsize=(14, 7))
    plt.plot(peminjaman_akhir_pekan.index, peminjaman_akhir_pekan.values, label='Akhir Pekan', color='r', marker='o')
    plt.plot(peminjaman_hari_kerja.index, peminjaman_hari_kerja.values, label='Hari Kerja', color='b', marker='o')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Jumlah Peminjaman Sepeda', fontsize=12)
    plt.title('Tren Jumlah Peminjaman Sepeda pada Akhir Pekan vs Hari Kerja (2011)', fontsize=14)
    plt.legend()
    plt.grid(True)

    # Tampilkan diagram di Streamlit
    st.pyplot(plt)