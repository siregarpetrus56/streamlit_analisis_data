# Submission Dicoding "Belajar Analisis Data dengan Python"

# Setup Environment - Anaconda

conda create --name main-ds python=3.10.10
conda activate main-ds
pip install -r requirements.txt

# Setup Environment - Shell/Terminal

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

# Run steamlit app

cd .\dashboard\
streamlit run dashboard.py