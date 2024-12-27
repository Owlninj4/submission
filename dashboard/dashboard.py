import streamlit as st
import pandas as pd
import os

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

    # Tampilkan ringkasan data
    st.header("Ringkasan Data Penyewaan Sepeda")
    musim_label = "Semua Musim" if selected_season == 0 else seasons[selected_season]
    st.write(f"Data disaring berdasarkan musim: **{musim_label}** dan rentang tanggal: **{start_date} hingga {end_date}**")
    st.write(filtered_data[['dteday', 'season', 'cnt']])

    # Visualisasi pola penyewaan sepeda
    st.header("Visualisasi Penyewaan Sepeda")
    st.line_chart(filtered_data.set_index('dteday')['cnt'])

    # Visualisasi penyewaan berdasarkan musim dan cuaca
    st.header("Penyewaan Berdasarkan Musim dan Cuaca")
    rentals_by_season = day_data.groupby('season')['cnt'].mean()
    rentals_by_weather = day_data.groupby('weathersit')['cnt'].mean()

    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    st.bar_chart(rentals_by_season.rename(index=seasons))

    weathers = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
    st.bar_chart(rentals_by_weather.rename(index=weathers))

    # Kesimpulan pertama
    st.write("Berdasarkan analisis EDA, faktor utama yang memengaruhi pola penyewaan sepeda adalah waktu dalam sehari (jam) dan kondisi cuaca. Penyewaan sepeda cenderung tinggi pada jam-jam sibuk (pagi dan sore) dan pada cuaca cerah. Musim juga memainkan peran, di mana musim Fall dan Summer menunjukkan tingkat penyewaan yang lebih tinggi.")

    # Analisis waktu terbaik untuk meningkatkan ketersediaan sepeda
    st.header("Analisis Waktu Terbaik")
    avg_rentals_by_hour = hour_data.groupby('hr')['cnt'].mean()
    st.write("Rata-rata penyewaan sepeda berdasarkan jam:")
    st.bar_chart(avg_rentals_by_hour)

    # Kesimpulan kedua
    st.write("Waktu terbaik untuk meningkatkan ketersediaan sepeda adalah pada jam-jam sibuk (pagi dan sore), terutama pada musim Summer dan Fall, yang menunjukkan permintaan yang lebih tinggi. Penyewaan sepeda lebih tinggi di musim-musim tersebut, dan saat cuaca cerah, sehingga meningkatkan ketersediaan sepeda pada jam-jam ini dapat membantu mengoptimalkan operasional.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
