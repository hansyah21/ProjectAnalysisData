import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load dataset
df_day = pd.read_csv('data/day.csv')
df_hour = pd.read_csv('data/hour.csv')

# Streamlit Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Menampilkan informasi dataset
st.header("Informasi Dataset")
st.write("Dataset harian:")
st.write(df_day.head())
st.write("Dataset per jam:")
st.write(df_hour.head())

# Pilihan Visualisasi
st.sidebar.header("Pilih Visualisasi")
option = st.sidebar.selectbox("Pilih Grafik", [
    "Distribusi Penyewaan Sepeda", "Pola Berdasarkan Cuaca", "Tren Harian & Bulanan", "RFM Analysis", "Clustering"
])

if option == "Distribusi Penyewaan Sepeda":
    st.subheader("Distribusi Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df_day['cnt'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title("Distribusi Jumlah Penyewaan Sepeda (Harian)")
    ax.set_xlabel("Jumlah Penyewaan Sepeda")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

elif option == "Pola Berdasarkan Cuaca":
    st.subheader("Pengaruh Cuaca, Suhu, dan Kelembaban terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x='temp', y='cnt', data=df_day, color='red', ax=ax)
    ax.set_title("Hubungan Suhu dan Jumlah Penyewaan Sepeda")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x='hum', y='cnt', data=df_day, color='blue', ax=ax)
    ax.set_title("Hubungan Kelembaban dan Jumlah Penyewaan Sepeda")
    ax.set_xlabel("Kelembaban")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x='hum', y='cnt', data=df_day, color='green', ax=ax)
    ax.set_title("Hubungan cuaca dan Jumlah Penyewaan Sepeda")
    ax.set_xlabel("cuaca")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

elif option == "Tren Harian & Bulanan":
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(12, 5))
    df_hour_numeric = df_hour.select_dtypes(include=['number'])
    df_hour_grouped = df_hour_numeric.groupby('hr').mean().reset_index()
    sns.lineplot(x='hr', y='cnt', data=df_hour_grouped, marker='o', color='purple', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 5))
    df_day_numeric = df_day.select_dtypes(include=['number']) 
    df_day_grouped = df_day_numeric.groupby('mnth').mean().reset_index()
    sns.lineplot(x='mnth', y='cnt', data=df_day_grouped, marker='o', color='orange', ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Bulanan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid()
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

st.sidebar.text("Dashboard by Streamlit")
# Sidebar untuk filtering interaktif
st.sidebar.header("Filter Data")
season_filter = st.sidebar.selectbox("Pilih Musim:", df_day['season'].unique())
weather_filter = st.sidebar.selectbox("Pilih Cuaca:", df_day['weathersit'].unique())
# Pastikan kolom 'dteday' dalam format datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Konversi ke datetime.date agar kompatibel dengan Streamlit
min_date = df_day['dteday'].min().to_pydatetime().date()
max_date = df_day['dteday'].max().to_pydatetime().date()

# Input tanggal dengan default min dan max
start_date = st.sidebar.date_input("Pilih Tanggal Awal:", min_date)
end_date = st.sidebar.date_input("Pilih Tanggal Akhir:", max_date)

# Validasi input tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Filter data berdasarkan tanggal
df_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & 
                      (df_day['dteday'] <= pd.to_datetime(end_date)) & 
                      (df_day['season'] == season_filter) & 
                      (df_day['weathersit'] == weather_filter)]

start_date = st.sidebar.date_input("Pilih Tanggal Awal:", min_date, key="start_date_picker")
end_date = st.sidebar.date_input("Pilih Tanggal Akhir:", max_date, key="end_date_picker")


# Validasi input tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Filter data berdasarkan tanggal
df_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & 
                      (df_day['dteday'] <= pd.to_datetime(end_date)) & 
                      (df_day['season'] == season_filter) & 
                      (df_day['weathersit'] == weather_filter)]

# Pastikan pengguna tidak memilih rentang tanggal yang salah
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Filter data berdasarkan tanggal
df_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & 
                      (df_day['dteday'] <= pd.to_datetime(end_date)) & 
                      (df_day['season'] == season_filter) & 
                      (df_day['weathersit'] == weather_filter)]

# Filter Data
start_date, end_date = date_filter
df_filtered = df_day[(df_day['season'] == season_filter) & 
                      (df_day['weathersit'] == weather_filter) & 
                      (df_day['dteday'] >= start_date) & 
                      (df_day['dteday'] <= end_date)]

