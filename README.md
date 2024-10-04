## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas matplotlib seaborn jupyter streamlit
```

## Setup Environment - Shell/Terminal
```
mkdir proyek-analisis-data
cd proyek-analisis-data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard.py
```