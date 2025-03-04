import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

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

elif option == "Tren Harian & Bulanan":
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=df_hour.groupby('hr').mean().reset_index(), marker='o', color='purple', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='mnth', y='cnt', data=df_day.groupby('mnth').mean().reset_index(), marker='o', color='orange', ax=ax)
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

