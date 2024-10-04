import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load dataset
day_df = pd.read_csv("dashboard/day_data.csv")
hour_df = pd.read_csv("dashboard/hour_data.csv")

# Convert date columns to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Modify 'workingday' column for readability

# Get min and max date for filtering
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Sidebar: Date range picker
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter day_df based on date selection
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Header
st.header("Bike Sharing Dataset Analysis")

st.subheader("Bike Rentals Weekdays and weekends)")
st.write(f"Peminjaman sepeda di weekday: nan, Peminjaman sepeda di weekend: 4191.5 nan")

# Barplot 1: Average Bike Rentals by Working Day
workingday = day_df.groupby(by="workingday").mean()

# Plot using matplotlib and seaborn
plt.figure(figsize=(10, 5))

# Menghitung rata-rata jumlah customer berdasarkan workingday
workingday_grouped = workingday.groupby('workingday')['cnt'].mean().reset_index()

# Membuat barplot
sns.barplot(
    y=workingday_grouped['cnt'], 
    x=workingday_grouped['workingday']
)
plt.title("Number of Customer by Workingday", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.show()

st.pyplot(plt)

# --- Second Analysis: Rush Hour Bike Rentals ---

# Filter hour_df for the last three months
last_three_months = hour_df[hour_df['dteday'] >= (hour_df['dteday'].max() - pd.DateOffset(months=3))]

# Determine rush hours (7-9 AM and 5-7 PM)
busy_hours = last_three_months[((last_three_months['hr'] >= 7) & (last_three_months['hr'] <= 9)) | 
((last_three_months['hr'] >= 17) & (last_three_months['hr'] <= 19))]

# Calculate average rentals during rush hours on weekdays
average_busy_rentals = busy_hours[busy_hours['weekday'].isin([0, 1, 2, 3, 4])]['cnt'].mean()

# Display average rush hour rentals
st.subheader("Average Bike Rentals During Rush Hours (Weekdays)")
st.write(f"Rata-rata peminjaman sepeda pada jam sibuk di hari kerja dalam tiga bulan terakhir: {average_busy_rentals:.2f}")

# Barplot 2: Average Rentals During Rush Hours by Hour
busy_hours_grouped = busy_hours[busy_hours['weekday'].isin([0, 1, 2, 3, 4])].groupby('hr')['cnt'].mean().reset_index()

# Plot rush hour rentals
plt.figure(figsize=(10, 5))
sns.barplot(
    x="hr", 
    y="cnt", 
    data=busy_hours_grouped, 
    palette=["#72BCD4" if 7 <= hr <= 9 or 17 <= hr <= 19 else "#D3D3D3" for hr in busy_hours_grouped['hr']]
)
plt.title("Average Bike Rentals During Rush Hours on Weekdays", fontsize=15)
plt.xlabel("Hour of Day", fontsize=12)
plt.ylabel("Average Rentals", fontsize=12)
plt.tick_params(axis='x', labelsize=12)
plt.tick_params(axis='y', labelsize=12)

# Display second plot in Streamlit
st.pyplot(plt)
