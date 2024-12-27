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

# Memuat data
try:
    day_data, hour_data = load_data()
    st.sidebar.header("Pengaturan Filter")

    # Filter berdasarkan musim
    seasons = {0: "Semua Musim", 1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    selected_season = st.sidebar.selectbox("Pilih Musim:", options=list(seasons.keys()), format_func=lambda x: seasons[x])

    # Filter berdasarkan rentang tanggal
    start_date = st.sidebar.date_input("Tanggal Mulai:", value=day_data['dteday'].min())
    end_date = st.sidebar.date_input("Tanggal Akhir:", value=day_data['dteday'].max())

    # Filter data berdasarkan input pengguna
    if selected_season == 0:
        filtered_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & (day_data['dteday'] <= pd.to_datetime(end_date))]
    else:
        filtered_data = day_data[(day_data['season'] == selected_season) & (day_data['dteday'] >= pd.to_datetime(start_date)) & (day_data['dteday'] <= pd.to_datetime(end_date))]

    # Visualisasi penyewaan berdasarkan musim dan cuaca
    st.header("Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
    weather_season_data = day_data.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weather_season_data, x='season', y='cnt', hue='weathersit', palette='Set2', ax=ax_weather)
    ax_weather.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca", fontsize=14)
    ax_weather.set_xlabel("Musim", fontsize=12)
    ax_weather.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax_weather.legend(title="Kondisi Cuaca")
    st.pyplot(fig_weather)

    # Visualisasi penyewaan per jam dalam setiap musim
    st.header("Penyewaan Sepeda per Jam dalam Setiap Musim")
    hourly_season_data = hour_data.groupby(['season', 'hr'])['cnt'].mean().reset_index()
    fig_hourly, ax_hourly = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_season_data, x='hr', y='cnt', hue='season', palette='coolwarm', ax=ax_hourly)
    ax_hourly.set_title("Penyewaan Sepeda per Jam Berdasarkan Musim", fontsize=14)
    ax_hourly.set_xlabel("Jam", fontsize=12)
    ax_hourly.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax_hourly.legend([seasons[s] for s in hourly_season_data['season'].unique()], title="Musim")
    st.pyplot(fig_hourly)

    # Kesimpulan pertama
    st.write("Analisis ini menunjukkan pola penyewaan sepeda berdasarkan musim dan waktu dalam sehari. Ini membantu kita mengidentifikasi jam-jam sibuk yang berbeda di musim-musim tertentu, memberikan wawasan mengenai kapan pelanggan lebih cenderung menyewa sepeda. Penyewaan sepeda cenderung tinggi pada jam-jam sibuk (pagi dan sore) dan pada cuaca cerah. Musim juga memainkan peran, di mana musim Fall dan Summer menunjukkan tingkat penyewaan yang lebih tinggi.")

    # Analisis waktu terbaik untuk meningkatkan ketersediaan sepeda
    st.header("Analisis Waktu Terbaik")
    avg_rentals_by_hour = hour_data.groupby('hr')['cnt'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_rentals_by_hour, x='hr', y='cnt', palette='viridis', ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
    ax2.set_xlabel("Jam", fontsize=12)
    ax2.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig2)

    # Kesimpulan kedua
    st.write("Berdasarkan analisis EDA, faktor utama yang memengaruhi pola penyewaan sepeda adalah waktu dalam sehari (jam) dan kondisi cuaca. Penyewaan sepeda cenderung tinggi pada jam-jam sibuk (pagi dan sore) dan pada cuaca cerah. Musim juga memainkan peran, di mana musim Fall dan Summer menunjukkan tingkat penyewaan yang lebih tinggi.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
