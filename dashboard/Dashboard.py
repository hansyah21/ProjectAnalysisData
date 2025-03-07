import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load dataset
df_day = pd.read_csv('data/day.csv')
df_hour = pd.read_csv('data/hour.csv')

# Konversi kolom tanggal ke format datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Streamlit Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Pilihan Visualisasi
st.sidebar.header("Pilih Visualisasi")
option = st.sidebar.selectbox("Pilih Grafik", [
    "Distribusi Penyewaan Sepeda", "Pola Berdasarkan Cuaca", "Tren Harian & Bulanan", "RFM Analysis", "Clustering"
])
                              
# Sidebar untuk filtering interaktif
st.sidebar.header("Filter Data")
season_options = ['Semua Musim'] + list(df_day['season'].unique())
weather_options = ['Semua Cuaca'] + list(df_day['weathersit'].unique())

season_filter = st.sidebar.selectbox("Pilih Musim:", season_options, key="season_select")
weather_filter = st.sidebar.selectbox("Pilih Cuaca:", weather_options, key="weather_select")

# Filtering berdasarkan rentang tanggal
min_date = df_day['dteday'].min().date()
max_date = df_day['dteday'].max().date()
start_date = st.sidebar.date_input("Pilih Tanggal Awal:", min_date, key="start_date_picker")
end_date = st.sidebar.date_input("Pilih Tanggal Akhir:", max_date, key="end_date_picker")

# Validasi input tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Konversi start_date & end_date ke datetime agar cocok dengan df_day
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter Data
df_filtered = df_day[(df_day['dteday'] >= start_date) & (df_day['dteday'] <= end_date)]
if season_filter != 'Semua Musim':
    df_filtered = df_filtered[df_filtered['season'] == season_filter]
if weather_filter != 'Semua Cuaca':
    df_filtered = df_filtered[df_filtered['weathersit'] == weather_filter]

# Pastikan df_filtered tidak kosong sebelum visualisasi
if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    # Menampilkan dataset yang sudah difilter
    st.header("Dataset Setelah Filtering")
    st.write(df_filtered.head())

if option == "Distribusi Penyewaan Sepeda":
    st.subheader("Distribusi Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df_filtered['cnt'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title("Distribusi Jumlah Penyewaan Sepeda (Harian)")
    ax.set_xlabel("Jumlah Penyewaan Sepeda")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

elif option == "Pola Berdasarkan Cuaca":
    st.subheader("Pengaruh Cuaca, Suhu, dan Kelembaban terhadap Penyewaan Sepeda")

    # Debugging: Cek jumlah data setelah filter
    st.write("Jumlah data setelah filter:", df_filtered.shape)

    if df_filtered.empty:
        st.warning("❌ Tidak ada data yang sesuai dengan filter. Coba ubah filter musim/cuaca.")
    else:
        # Konversi 'weathersit' ke kategori string
        df_filtered['weathersit'] = df_filtered['weathersit'].astype(str)

        # Debugging: Cek nilai unik dalam kolom weathersit
        st.write("✅ Nilai unik dalam kolom weathersit:", df_filtered['weathersit'].unique())

        # Tambahkan dropdown interaktif untuk memilih cuaca dengan key unik
        weathersit_options = ['Semua Cuaca'] + sorted(df_filtered['weathersit'].unique())
        selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", weathersit_options, key="weather_dropdown_unique")

        # Debugging: Cek apakah dropdown memberikan output yang benar
        st.write("✅ Cuaca yang dipilih:", selected_weather)

        # Filter berdasarkan dropdown cuaca
        if selected_weather != "Semua Cuaca":
            df_filtered = df_filtered[df_filtered['weathersit'] == selected_weather]

        # Debugging: Cek apakah dataset kosong setelah filter cuaca
        st.write("Jumlah data setelah filter cuaca:", df_filtered.shape)

        if df_filtered.empty:
            st.warning("❌ Tidak ada data setelah filter cuaca. Coba ubah pilihan dropdown.")
        else:
            # Debugging: Cek apakah kolom cnt memiliki NaN
            st.write("Jumlah NaN dalam kolom cnt:", df_filtered['cnt'].isnull().sum())

            # Hapus NaN jika ada
            df_filtered = df_filtered.dropna(subset=['cnt'])

            # Pastikan kategori cuaca memiliki urutan yang benar
            cuaca_order = ['1', '2', '3', '4']

            # 📊 Visualisasi hubungan cuaca dengan jumlah penyewaan sepeda
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(x='weathersit', y='cnt', data=df_filtered, hue='weathersit', palette='viridis', legend=False, ax=ax, order=cuaca_order)
            ax.set_title("Pola Penyewaan Berdasarkan Kondisi Cuaca")
            ax.set_xlabel("Kondisi Cuaca (1=Cerah, 2=Berkabut, 3=Hujan, 4=Salju)")
            ax.set_ylabel("Jumlah Penyewaan Sepeda")
            st.pyplot(fig)

            # 📊 Visualisasi hubungan suhu dengan jumlah penyewaan sepeda
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.regplot(x='temp', y='cnt', data=df_filtered, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax)
            ax.set_title("Hubungan Suhu dan Jumlah Penyewaan Sepeda")
            ax.set_xlabel("Suhu (Normalized)")
            ax.set_ylabel("Jumlah Penyewaan Sepeda")
            st.pyplot(fig)

            # 📊 Visualisasi hubungan kelembaban dengan jumlah penyewaan sepeda
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.regplot(x='hum', y='cnt', data=df_filtered, scatter_kws={'alpha':0.5}, line_kws={'color':'blue'}, ax=ax)
            ax.set_title("Hubungan Kelembaban dan Jumlah Penyewaan Sepeda")
            ax.set_xlabel("Kelembaban")
            ax.set_ylabel("Jumlah Penyewaan Sepeda")
            st.pyplot(fig)
            
elif option == "Tren Harian & Bulanan":
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Waktu")
    df_hour_numeric = df_hour.select_dtypes(include=['number'])
    df_hour_grouped = df_hour_numeric.groupby('hr').mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=df_hour_grouped, marker='o', color='purple', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    st.pyplot(fig)
    
    df_day_grouped = df_day.groupby('mnth').mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='mnth', y='cnt', data=df_day_grouped, marker='o', color='orange', ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Bulanan")
    st.pyplot(fig)

elif option == "RFM Analysis":
    st.subheader("RFM Analysis - Segmentasi Pengguna Sepeda")
    df_day['Recency'] = (pd.to_datetime(df_day['dteday']).max() - pd.to_datetime(df_day['dteday'])).dt.days
    df_rfm = df_day.groupby('weekday').agg({'Recency': 'min', 'cnt': ['count', 'sum']}).reset_index()
    df_rfm.columns = ['weekday', 'Recency', 'Frequency', 'Monetary']
    
    # Visualisasi RFM Analysis
    fig, ax = plt.subplots(figsize=(10,5))
    sns.heatmap(df_rfm[['Recency', 'Frequency', 'Monetary']].corr(), annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title("Heatmap Korelasi RFM Analysis")
    st.pyplot(fig)
    
    st.write("""
    **Insight RFM Analysis:**
    - Pengguna dengan frekuensi tinggi cenderung memiliki recency rendah.
    - Pengguna dengan monetary tinggi menunjukkan pola penggunaan yang lebih stabil.
    - Strategi bisnis: Program loyalitas untuk pengguna dengan frekuensi tinggi dapat meningkatkan retensi.
    """)
    
    st.write(df_rfm)

elif option == "Clustering":
    st.subheader("Clustering - Pola Penggunaan Sepeda")
    df_hour['time_category'] = pd.cut(df_hour['hr'], bins=[0, 6, 12, 18, 24], labels=['Malam', 'Pagi', 'Siang', 'Sore'])
    time_cluster = df_hour.groupby('time_category').agg({'cnt': 'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='time_category', y='cnt', data=time_cluster, palette='coolwarm', ax=ax)
    ax.set_title("Total Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")
    ax.set_xlabel("Waktu dalam Sehari")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)
    
    st.write("""
    **Insight Clustering:**
    - Penggunaan sepeda tertinggi terjadi pada pagi dan sore hari.
    - Jam malam menunjukkan penurunan drastis dalam jumlah penyewaan.
    - Strategi: Promosi diskon malam hari atau peningkatan layanan di jam sibuk.
    """)

st.sidebar.text("Dashboard by Raihansyah A.M.")
