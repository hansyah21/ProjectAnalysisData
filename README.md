# ProjectAnalysisData
Dashboard Belajar Analisis Data dengan Python Laskar AI

# Setup Enviroment
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
pip install --upgrade pandas seaborn

# Setup Environment - Shell/Terminal
mkdir Project-Analysis-Data
cd Project-Analysis-Data
pipenv install
pipenv shell
pip install -r requirements.txt
pip install --upgrade pandas seaborn

# Dashboard Bike Sharing Analysis 🚴‍♂️
Dashboard ini dibuat dengan **Streamlit** untuk menganalisis data penyewaan sepeda.

git add .
git commit -m "Fix missing graphs in weather analysis"
git push origin main

# Run Steamlit App
streamlit run Dashboard.py


