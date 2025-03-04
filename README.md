# ProjectAnalysisData
Dashboard Belajar Analisis Data dengan Python Laskar AI


# Setup Environment - Shell/Terminal
mkdir Project-Analysis-Data
cd Project-Analysis-Data
pipenv install
pipenv shell
pip install -r requirements.txt

# Dashboard Bike Sharing Analysis 🚴‍♂️

Dashboard ini dibuat dengan **Streamlit** untuk menganalisis data penyewaan sepeda.

## 📂 Struktur Proyek
Project-Analysis-Data/
├── dashboard/              
│   ├── dashboard.py          # Script utama untuk Streamlit
│   ├── requirements.txt      # Daftar pustaka yang digunakan
├── data/
│   ├── day.csv               # Dataset harian
│   ├── hour.csv              # Dataset per jam
├── notebook.ipynb  # Notebook Jupyter untuk analisis data
├── README.md                 # Dokumentasi proyek
├── url.txt                   # URL dashboard setelah deploy
└── .gitignore                # File untuk mengecualikan file tertentu dari Git

# Run Steamlit App
streamlit run dashboard.py





