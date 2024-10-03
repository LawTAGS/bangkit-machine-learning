import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file = './Bike-sharing-dataset/hour.csv'
df = pd.read_csv(file)

st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.markdown(
    """
    - **Nama:** Bryan Guok
    - **Email:** m002b4ky0877@bangkit.academy
    - **ID Dicoding:** bryanguok
    """
)

st.header("Pertanyaan Bisnis")
st.write(
    """
    - Kapan waktu (jam) puncak penggunaan Bike Sharing?
    - Berapa perbandingan jumlah pengguna Bike Sharing yang sudah terdaftar terhadap jumlah pengguna kasual?
    """
)

st.header("Import Packages dan Libraries")
st.code(
    """
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    """, language='python'
)

st.header("Data Wrangling")
st.subheader("Gathering Data")
st.code(
    """
    file = './Bike-sharing-dataset/hour.csv'
    df = pd.read_csv(file)
    """
)
st.markdown(
    """
    **Insight:**
    - Pengambilan data menggunakan data Bike Sharing tahun 2011-2012 dalam format csv yang mengandung jam karena data diharapkan dapat menjawab pertanyaan mengenai kapan jam Bike Sharing paling sering digunakan.
    - Data yang digunakan juga mengandung langsung nilai atau banyaknya pengguna *casual* dan pengguna yang sudah terdaftar pada Bike Sharing ini.
    - Data-data lain yang dikumpulkan yang belum tentu terpakai akan diabaikan, misalnya temperatur, kecepatan angin, dan lain sebagainya yang tidak menjawab pertanyaan bisnis.
    """
)

st.subheader("Assessing Data")
st.code(
    """
    df_null = df.isnull().sum()
    df_null

    df_duplicate = df.duplicated().sum()
    df_duplicate
    """
)
st.markdown(
    """
    **Insight:**
    - Data diidentifikasi terlebih dahulu apakah terdapat data yang kosong sehingga datanya tidak dapat digunakan.
    - Data kemudian dicari apakah ada data yang tidak sengaja terduplikasi.
    - Value dari data yang invalid seharusnya dicek melalui *regex*, namun dalam kasus data ini *regex* tidak dapat digunakan secara langsung karena *regex* memfilter data *invalid* apabila jenis ketidaksahihan data diketahui.
    - Pengecekan *outlier* juga tidak dilakukan, karena data yang akan digunakan adalah data waktu (frekuensi terhadap waktu) yang selalu dapat diisi dari 0 hingga 24, dan jumlah pengguna baik yang *casual* maupun *registered* yang digunakan untuk menghitung jumlah diskrit kehadiran pengguna pada saat itu, sehingga analisis data *outlier* tidak diperlukan.
    """
)

st.subheader("Cleaning Data")
st.markdown(
    """
    **Insight:**
    - Data yang diambilkan disimpulkan tidak bermasalah pada tahap asesmen data, sehingga pembersihan data tidak dilakukan.
    """
)

st.header("Exploratory Data Analysis (EDA)")
st.code(
    """
    print("Dataset Overview:")
    print(df.info())

    print("Descriptive Statistics:")
    print(df.describe(include='all'))

    df_nodate = df
    df_nodate.drop(columns=['dteday'])

    print("Correlation Analysis:")
    correlation_matrix = df_nodate.drop(columns=['dteday']).corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

    print("Data Grouping:")
    result = df.groupby(by='mnth').agg({
        'hr': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    result.columns = ['Month', 'Total_Hours', 'Casual', 'Registered']

    print(result)
    """
)
st.markdown(
    """
    **Insight:**
    - Digunakan df.info() untuk memperlihatkan informasi mengenai tipe data dan kosong atau tidaknya data tiap kolom.
    - Digunakan df.describe() untuk memperlihatkan statistika deskriptif tiap kolom data.
    - Dibuat visualisasi korelasi antar kolom pada data dengan mengabaikan data pada kolom ['dteday'] yang nilainya bukan nilai numerik.
    - Data dikelompokkan berdasarkan bulannya untuk diperlihatkan jumlah waktu dan banyaknya pengguna.
    """
)

st.header("Visualization and Explanatory Analysis")
st.subheader("Kapan waktu (jam) puncak pengunaan Bike Sharing?")
st.code(
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(df['hr'], bins=24)
    plt.title('Distribution of Bike Sharing Usage Frequency per Hour')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    plt.show()
    """
)
st.write("Berikut grafik distribusi jumlah pengguna tiap jamnya:")

plt.figure(figsize=(12, 6))
sns.histplot(df['hr'], bins=24)
plt.title('Distribution of Bike Sharing Usage Frequency per Hour')
plt.xlabel('Hour')
plt.ylabel('Frequency')
st.pyplot(plt)

st.subheader("Berapa perbandingan jumlah pengguna kasual terhadap pengguna yang terdafatar?")
st.code(
    """
    casual_yr1 = []
    registered_yr1 = []
    casual_yr2 = []
    registered_yr2 = []

    df_unique_month = df['mnth'].unique()

    for i in df_unique_month:
        df_month_filter = df[df['mnth'] == i]

        df_year_0 = df_month_filter[df_month_filter['yr'] == 0]
        df_year_1 = df_month_filter[df_month_filter['yr'] == 1]

        if not df_year_0.empty:
            casual_yr1.append(df_year_0['casual'].sum())
            registered_yr1.append(df_year_0['registered'].sum())

        if not df_year_1.empty:
            casual_yr2.append(df_year_1['casual'].sum())
            registered_yr2.append(df_year_1['registered'].sum())

    data_yr1 = pd.DataFrame({
        'Month': df_unique_month,
        'Casual': casual_yr1,
        'Registered': registered_yr1
    })

    data_yr2 = pd.DataFrame({
        'Month': df_unique_month,
        'Casual': casual_yr2,
        'Registered': registered_yr2
    })

    data_yr1_melted = pd.melt(data_yr1, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')
    data_yr2_melted = pd.melt(data_yr2, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Month', y='User_Count', hue='User_Type',
                data=data_yr1_melted, palette=['blue', 'orange'],
                errorbar=None, dodge=True)
    plt.title('Distribution of Users Type per Month (Year 1)')
    plt.xlabel('Month')
    plt.ylabel('Total Users')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Month', y='User_Count', hue='User_Type',
                data=data_yr2_melted, palette=['blue', 'orange'],
                errorbar=None, dodge=True)
    plt.title('Distribution of Users Type per Month (Year 2)')
    plt.xlabel('Month')
    plt.ylabel('Total Users')
    plt.legend()
    plt.show()
    """
)

casual_yr1 = []
registered_yr1 = []
casual_yr2 = []
registered_yr2 = []

df_unique_month = df['mnth'].unique()

for i in df_unique_month:
    df_month_filter = df[df['mnth'] == i]

    df_year_0 = df_month_filter[df_month_filter['yr'] == 0]
    df_year_1 = df_month_filter[df_month_filter['yr'] == 1]

    if not df_year_0.empty:
        casual_yr1.append(df_year_0['casual'].sum())
        registered_yr1.append(df_year_0['registered'].sum())

    if not df_year_1.empty:
        casual_yr2.append(df_year_1['casual'].sum())
        registered_yr2.append(df_year_1['registered'].sum())

data_yr1 = pd.DataFrame({
    'Month': df_unique_month,
    'Casual': casual_yr1,
    'Registered': registered_yr1
})

data_yr2 = pd.DataFrame({
    'Month': df_unique_month,
    'Casual': casual_yr2,
    'Registered': registered_yr2
})

data_yr1_melted = pd.melt(data_yr1, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')
data_yr2_melted = pd.melt(data_yr2, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')

st.write("Berikut grafik distribusi jumlah pengguna kasual dan terdaftar per bulan tahun 2011")

plt.figure(figsize=(12, 6))
sns.barplot(x='Month', y='User_Count', hue='User_Type',
            data=data_yr1_melted, palette=['blue', 'orange'],
            errorbar=None, dodge=True)
plt.title('Distribution of Users Type per Month (Year 1)')
plt.xlabel('Month')
plt.ylabel('Total Users')
plt.legend()
st.pyplot(plt)

st.write("Berikut grafik distribusi jumlah pengguna kasual dan terdaftar per bulan tahun 2012")

plt.figure(figsize=(12, 6))
sns.barplot(x='Month', y='User_Count', hue='User_Type',
            data=data_yr2_melted, palette=['blue', 'orange'],
            errorbar=None, dodge=True)
plt.title('Distribution of Users Type per Month (Year 2)')
plt.xlabel('Month')
plt.ylabel('Total Users')
plt.legend()
st.pyplot(plt)

st.markdown(
    """
    **Insight:**
    - Dapat dilihat dari visualisasi data pertama yang dibuat adalah distribusi banyaknya penggunaan Bike Sharing per jamnya, data divisualisasikan melalui histogram agar dapat terlihat secara langsung frekuensinya tiap satuan jam. Visualisasi ini menjawab pertanyaan pertama mengenai waktu puncak penggunaan Bike Sharing, yaitu sekitar pukul 13.00 hingga pukul 17.00, meskipun dari histogram tidak terlihat langsung jumlah pastinya, namun terdapat perbedaan ketinggian yang sangat kecil terhadap jam-jam lainnya.
    - Visualisasi data kedua merepresentasikan perbandingan jumlah pengguna Bike Sharing yang kasual vs. yang sudah terdaftar per bulan untuk masing-masing tahun. Visualisasi menggunakan bar plot agar dapat terlihat perbandingan frekuensi yang pengguna kasual terhadap pengguna yang terdaftar. Visualisasi ini telah menjawab secara langsung perbandingan jumlah pengguna.
    - Data diharapkan dapat digunakan untuk meningkatkan jumlah pengguna, misalnya dengan memberikan diskon pada jam puncak, atau promosi free trial untuk pendaftar akun baru, dan lain sebagainya.
    """
)

st.header("Conclusion")
st.markdown(
    """
    - Waktu puncak penggunaan Bike Sharing adalah sekitar pukul 13.00 hingga 17.00 dengan jumlah pengguna mencapai lebih dari 700 pengguna.
    - Perbandingan jumlah pengguna kasual terhadap pengguna yang terdaftar pada tahun pertama mencapai selisih terbanyak pada bulan ke-6 tahun pertama yaitu, dan pada bulan ke-9 tahun kedua. Sedangkan selisih jumlah pengguna kasual terhadap pengguna yang sudah terdaftar dicapai pada bulan ke-1 baik pada tahun pertama maupun tahun kedua.
    """
)