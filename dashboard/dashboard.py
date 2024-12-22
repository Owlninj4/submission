import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Tentukan base path
base_path = 'dashboard' if os.path.exists('dashboard') else '.'

# Load datasets
hour_df = pd.read_csv(f'{base_path}/hour.csv')
day_df = pd.read_csv(f'{base_path}/day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])   
# Set up Streamlit layout

st.sidebar.header("Filter Data")
rentang_tanggal = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df['dteday'].min(), day_df['dteday'].max()])
musim_terpilih = st.sidebar.multiselect(
    "Pilih Musim", 
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)
cuaca_terpilih = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca", 
    options=day_df['weathersit'].unique(),
    default=day_df['weathersit'].unique()
)

# Filter data
data_terfilter = day_df[
    (day_df['dteday'] >= pd.Timestamp(rentang_tanggal[0])) &
    (day_df['dteday'] <= pd.Timestamp(rentang_tanggal[1])) &
    (day_df['season'].isin(musim_terpilih)) &
    (day_df['weathersit'].isin(cuaca_terpilih))
]

# Judul Dashboard
st.title("Dashboard Data Penyewaan Sepeda")
st.write("Dashboard ini memberikan wawasan tentang pola penyewaan sepeda berdasarkan data historis.")

# Analisis Pertanyaan Bisnis
st.header("1. Analisis Segmentasi Pelanggan")
data_segmentasi = data_terfilter[['casual', 'registered']].sum()
st.bar_chart(data_segmentasi, use_container_width=True)
st.write("**Kesimpulan:** Pelanggan terdaftar berkontribusi lebih besar dibandingkan pelanggan kasual dalam total penyewaan sepeda.")

st.header("2. Strategi Retensi Pelanggan")
rata_rata_penyewaan = data_terfilter.groupby(['workingday'])['cnt'].mean().reset_index()
rata_rata_penyewaan['workingday'] = rata_rata_penyewaan['workingday'].replace({0: 'Hari Libur', 1: 'Hari Kerja'})
rata_rata_penyewaan = rata_rata_penyewaan.rename(columns={'workingday': 'Jenis Hari', 'cnt': 'Rata-rata Penyewaan'})
st.bar_chart(rata_rata_penyewaan.set_index('Jenis Hari'), use_container_width=True)
st.write("**Kesimpulan:** Hari kerja menunjukkan jumlah penyewaan yang lebih tinggi, mengindikasikan penggunaan sepeda untuk keperluan komuter.")

st.header("3. Optimasi Pemasaran")
plt.figure(figsize=(10, 5))
sns.boxplot(x='season', y='cnt', data=data_terfilter)
st.pyplot(plt.gcf())
st.write("**Kesimpulan:** Kampanye pemasaran dapat difokuskan pada musim panas dan musim gugur yang memiliki tingkat penyewaan lebih tinggi.")

st.header("4. Nilai Pelanggan Sepanjang Masa (Customer Lifetime Value - CLV)")
total_penyewaan = data_terfilter['cnt'].sum()
st.metric(label="Total Penyewaan (Data Terfilter)", value=total_penyewaan)
st.write("**Kesimpulan:** Total penyewaan dalam periode yang dipilih memberikan gambaran nilai pelanggan secara keseluruhan.")

# Fitur Interaktif Tambahan
st.sidebar.header("Eksplorasi Data Per Jam")
tampilkan_data_jam = st.sidebar.checkbox("Tampilkan Data Per Jam", value=False)
if tampilkan_data_jam:
    data_jam_terfilter = hour_df[
        (hour_df['season'].isin(musim_terpilih)) &
        (hour_df['weathersit'].isin(cuaca_terpilih))
    ]
    st.subheader("Distribusi Penyewaan Per Jam")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', data=data_jam_terfilter, estimator='mean')
    st.pyplot(plt.gcf())
