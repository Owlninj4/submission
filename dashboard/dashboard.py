import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat dataset
def load_data():
    # Tentukan base path
    base_path = 'dashboard' if os.path.exists('dashboard') else '.'

    # Memuat data
    day_data = pd.read_csv(f'{base_path}/day.csv')
    hour_data = pd.read_csv(f'{base_path}/hour.csv')
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])

    return day_data, hour_data

# Judul aplikasi
st.title("Dashboard Penyewaan Sepeda")

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_date = st.sidebar.date_input("Pilih Tanggal", pd.Timestamp("2011-01-01"))

# Memuat data
try:
    day_data, hour_data = load_data()

    # Filter data berdasarkan tanggal
    day_data_filtered = day_data[day_data['dteday'] == pd.Timestamp(selected_date)]

    # Visualisasi penyewaan berdasarkan musim dan cuaca
    st.header("Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
    weather_season_data = day_data.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    weather_labels = {1: "Clear", 2: "Few clouds", 3: "Partly cloudy"}
    fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weather_season_data, x='season', y='cnt', hue='weathersit', palette='Set2', ax=ax_weather)
    ax_weather.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca", fontsize=14)
    ax_weather.set_xlabel("Musim", fontsize=12)
    ax_weather.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    handles, labels = ax_weather.get_legend_handles_labels()
    ax_weather.legend(handles, [weather_labels[int(label)] for label in labels], title="Kondisi Cuaca")
    st.pyplot(fig_weather)

    # Visualisasi penyewaan per jam dalam setiap musim
    st.header("Penyewaan Sepeda per Jam dalam Setiap Musim")
    hourly_season_data = hour_data.groupby(['season', 'hr'])['cnt'].mean().reset_index()
    hourly_season_data['hr'] = hourly_season_data['hr'] + 1  # Shift jam dari 0-23 menjadi 1-24
    fig_hourly, ax_hourly = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_season_data, x='hr', y='cnt', hue='season', palette='coolwarm', ax=ax_hourly)
    ax_hourly.set_title("Penyewaan Sepeda per Jam Berdasarkan Musim", fontsize=14)
    ax_hourly.set_xlabel("Jam", fontsize=12)
    ax_hourly.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax_hourly.legend(["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"], title="Musim")
    st.pyplot(fig_hourly)

    # Kesimpulan pertama
    st.write("Analisis ini menunjukkan pola penyewaan sepeda berdasarkan musim dan waktu dalam sehari. Ini membantu kita mengidentifikasi jam-jam sibuk yang berbeda di musim-musim tertentu, memberikan wawasan mengenai kapan pelanggan lebih cenderung menyewa sepeda. Penyewaan sepeda cenderung tinggi pada jam-jam sibuk (pagi dan sore) dan pada cuaca cerah. Musim juga memainkan peran, di mana musim Fall dan Summer menunjukkan tingkat penyewaan yang lebih tinggi.")

    # Analisis waktu terbaik untuk meningkatkan ketersediaan sepeda
    st.header("Analisis Waktu Terbaik")
    avg_rentals_by_hour = hour_data.groupby('hr')['cnt'].mean().reset_index()
    avg_rentals_by_hour['hr'] = avg_rentals_by_hour['hr'] + 1  # Shift jam dari 0-23 menjadi 1-24
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_rentals_by_hour, x='hr', y='cnt', palette='viridis', ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
    ax2.set_xlabel("Jam", fontsize=12)
    ax2.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig2)

    # Kesimpulan kedua
    st.write("Grafik ini menunjukkan jam-jam puncak penyewaan sepeda yang biasanya terjadi pada pagi dan sore hari. Untuk meningkatkan ketersediaan sepeda, fokuslah ketersediaan pada jam-jam ini.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
