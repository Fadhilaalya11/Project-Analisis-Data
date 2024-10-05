# Proyek Analisis Data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menampilkan judul dan informasi
st.title("Proyek Analisis Data Bike Sharing")
st.write("Nama: [Fadhila Alya Syahfahlevi]")
st.write("Email: [m120b4kx1319@bangkit.academy]")
st.write("ID Dicoding: [m120b4kx1319]")

# Menentukan Pertanyaan Bisnis
st.header("Menentukan Pertanyaan Bisnis")
st.write("Bagaimana tren penggunaan bike-sharing pada hari kerja dibandingkan akhir pekan?")
st.write("Bagaimana Pengaruh cuaca Terhadap Jumlah Penggunaan Sepeda per Jam?")

# Data Wrangling
st.header("Data Wrangling")
st.subheader("Gathering Data")

# Mengatur path file
days_path = "C:/Users/fadhi/OneDrive - Telkom University/Dicoding/ProyekAnalisisData/day.csv"
hours_path = "C:/Users/fadhi/OneDrive - Telkom University/Dicoding/ProyekAnalisisData/hour.csv"

# Membaca data dari file CSV
days_df = pd.read_csv(days_path)
hours_df = pd.read_csv(hours_path)

# Menampilkan data hari dan jam
st.subheader("Table Days")
st.dataframe(days_df.head())

st.subheader("Table Hours")
st.dataframe(hours_df.head())

# Insight
st.write("**Insight:**")
st.write("Melalui perintah head() menampilkan data di days_df sebanyak 5 data.")
st.write("Melalui perintah head() menampilkan data di hours_df sebanyak 5 data.")

st.header("Assessing Data")
# Menilai tabel days_df
st.subheader("Menilai Tabel days_df")
st.write(days_df.info())
st.write(days_df.isna().sum())
st.write("Jumlah duplikasi: ", days_df.duplicated().sum())
st.write(days_df.describe())

# Menilai tabel hours_df
st.subheader("Menilai Tabel hours_df")
st.write(hours_df.info())
st.write(hours_df.isna().sum())
st.write("Jumlah duplikasi: ", hours_df.duplicated().sum())
st.write(hours_df.describe())

# Data Cleaning
st.header("Cleaning Data")
st.subheader("Memperbaiki Tipe data")
datetime_columns = ["dteday"]

# Mengubah tipe data di days_df
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
st.dataframe(days_df.dtypes)
st.write("**Insight:**")
st.write("- Sudah mengganti tipe data dteday di days_df menjadi tipe data datetime")
st.write(days_df.info())

# Mengubah tipe data di hours_df
for column in datetime_columns:
    hours_df[column] = pd.to_datetime(hours_df[column])
st.write("Tipe data pada hours_df setelah cleaning:")
st.dataframe(hours_df.dtypes)
st.write("**Insight:**")
st.write("- Sudah mengganti tipe data dteday di hours_df menjadi tipe data datetime")
st.write(hours_df.info())

# ## Exploratory Data Analysis (EDA)

st.header("Exploratory Data Analysis (EDA)")

### Explore days_df
st.write("Sample dari days_df:")
st.dataframe(days_df.sample(5))

st.write("Deskripsi days_df:")
st.write(days_df.describe(include="all"))

st.write("Apakah kolom instant unik?")
st.write(days_df.instant.is_unique)

# Group by workingday dan agregasi berdasarkan total penggunaan
workingday_usage = days_df.groupby('workingday').agg({'cnt':'sum'})
st.write("Total penggunaan berdasarkan hari kerja:")
st.write(workingday_usage)

# Group by weatherdit dan jam
hourly_weather_usage = hours_df.groupby(['weathersit', 'hr']).agg({'cnt':'mean'})
st.write("Rata-rata penggunaan berdasarkan kondisi cuaca dan jam:")
st.write(hourly_weather_usage)

# Mengelompokkan berdasarkan hari kerja dan menghitung total pengguna unik
unique_users_workingday = days_df.groupby(by="workingday").cnt.sum().sort_values(ascending=False)
st.write("Total pengguna unik berdasarkan hari kerja:")
st.write(unique_users_workingday)

# Mengelompokkan berdasarkan kondisi cuaca dan jam, menghitung total penggunaan unik
unique_users_weather = hours_df.groupby(by="weathersit").cnt.sum().sort_values(ascending=False)
st.write("Total penggunaan unik berdasarkan kondisi cuaca:")
st.write(unique_users_weather)

# Mengelompokkan berdasarkan musim dan menghitung pengguna terdaftar
season_registered = days_df.groupby(by="season").registered.sum().sort_values(ascending=False)
st.write("Total pengguna terdaftar berdasarkan musim:")
st.write(season_registered)

# Histogram dari total pengguna (cnt)
plt.figure(figsize=(10, 4))
days_df.cnt.hist(bins=30)
plt.title('Distribution of Total Bike Users per Day')
plt.xlabel('Total Users')
plt.ylabel('Frequency')
st.pyplot(plt)

# Histogram dari pengguna registered
plt.figure(figsize=(10, 4))
days_df.registered.hist(bins=30)
plt.title('Distribution of Registered Users per Day')
plt.xlabel('Registered Users')
plt.ylabel('Frequency')
st.pyplot(plt)

# Menambahkan kolom status ke dataset 'days_df'
active_users = hours_df['registered'].unique()
days_df['status'] = days_df['registered'].apply(lambda x: "Active" if x in active_users else "Non Active")

# Menampilkan sampel acak dari 5 baris
st.write("Sample dari days_df setelah menambahkan kolom status:")
st.dataframe(days_df.sample(5))

# Menggabungkan data days_df dan hours_df
days_hours_merged_df = pd.merge(
    left=hours_df,
    right=days_df,
    how="left",  # left join: semua data dari 'hour_data' dipertahankan
    left_on="dteday",  # Kolom kunci di tabel sebelah kiri (hour_data)
    right_on="dteday"  # Kolom kunci di tabel sebelah kanan (day_data)
)

# Melihat hasil penggabungan
st.write("Hasil penggabungan days_df dan hours_df:")
st.dataframe(days_hours_merged_df.head())

### Explore hours_df
st.write("Sample dari hours_df:")
st.dataframe(hours_df.sample(10))

st.write("Deskripsi hours_df:")
st.write(hours_df.describe(include="all"))

st.write("Mengelompokkan data berdasarkan season dan melakukan agregasi:")
season_agg = hours_df.groupby(by="season").agg({
    "hr": "nunique",       # Menghitung jumlah jam unik dalam setiap musim
    "cnt": "sum",           # Menjumlahkan total pengguna sepeda
    "temp": ["min", "max"]  # Mengambil suhu minimum dan maksimum
})
st.write(season_agg)

st.write("**Insight:**")
st.write("- EDA dilakukan dengan mengelompokan kolom working day dan jumlah pengguna dengan fungsi groupby untuk menjawab pertanyaan.")
st.write("- EDA juga dilakukan dengan mengelompokan kolom cuaca dan jumlah pengguna per jam dengan fungsi groupby untuk menjawab pertanyaan.")

st.header("Visualization & Explanatory Analysis")
st.subheader("Pertanyaan 1: Bagaimana Tren Penggunaan Bike-Sharing pada Hari Kerja Dibandingkan dengan Akhir Pekan?")
# Visualisasi Tren Penggunaan Bike-Sharing pada Hari Kerja vs. Akhir Pekan
workingday_usage = days_df.groupby('workingday')['cnt'].sum()
st.subheader("Total Bike Usage: Weekdays vs. Weekends")
st.bar_chart(workingday_usage)

st.subheader("Pertanyaan 2: Bagaimana Pengaruh Cuaca Terhadap Jumlah Penggunaan Sepeda per Jam?")
# Visualisasi Pengaruh Cuaca Terhadap Jumlah Penggunaan Sepeda per Jam
hourly_weather_usage = hours_df.groupby(['hr', 'weathersit'])['cnt'].mean().unstack()
st.subheader("Average Bike Usage per Hour by Weather Condition")
st.line_chart(hourly_weather_usage)

# Insight dan Kesimpulan
st.subheader("Insight")
st.write("Dari hasil visualisasi no 1, dapat diambil insight bahwa penggunaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan dengan akhir pekan. "
         "Hal ini bisa jadi disebabkan oleh banyaknya pengguna sepeda yang menggunakan transportasi tersebut untuk pergi ke sekolah ataupun bekerja ke kantor. "
         "Sedangkan pada akhir pekan, penggunaan sepeda lebih sedikit karena bisa jadi orang-orang menggunakan waktu akhir pekan mereka untuk berekreasi dengan keluarga atau teman.")

st.write("Dari hasil visualisasi no 2, dapat diambil insight bahwa kondisi cuaca memiliki dampak yang signifikan terhadap jumlah pengguna sepeda. "
         "Pengguna sepeda menurun drastis ketika cuaca buruk, seperti hujan atau kabut. Sebaliknya, pada cuaca yang cerah, penggunaan sepeda lebih tinggi. "
         "Variabel cuaca seperti suhu dan kelembaban juga berkontribusi besar terhadap jumlah pengguna.")

# Analisis Lanjutan (Opsional)
st.header("Analisis Lanjutan")

# Regresi Linier untuk memprediksi penggunaan sepeda
correlation_data = hours_df[['cnt', 'temp', 'hum', 'windspeed', 'weathersit']]

# Membuat heatmap untuk melihat korelasi antar variabel
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_data.corr(), annot=True)

plt.title('Correlation Between Bike Usage and Weather Variables')
st.pyplot(plt)  # Menggunakan Streamlit untuk menampilkan heatmap

# Insight dari analisis korelasi
st.write("Insight:")
st.write("- Suhu berpengaruh positif terhadap penggunaan sepeda; semakin tinggi suhu (tetapi masih dalam batas nyaman), semakin tinggi penggunaan sepeda. "
         "Namun, ketika suhu menjadi terlalu panas atau terlalu dingin, jumlah pengguna cenderung menurun. "
         "Kelembaban yang tinggi juga menurunkan jumlah pengguna sepeda, terutama ketika kelembaban di atas batas kenyamanan. "
         "Korelasi antar variabel (heatmap) menunjukkan bahwa suhu memiliki korelasi positif sedang dengan jumlah pengguna, "
         "sementara kelembaban dan kecepatan angin memiliki korelasi negatif terhadap penggunaan sepeda.")

# Conclusion
st.subheader("Conclusion")

st.write("Conclusion pertanyaan 1:** Pada hari kerja, penggunaan sepeda cenderung lebih tinggi dibandingkan akhir pekan (Temuan). "
         "Hal ini kemungkinan disebabkan oleh penggunaan sepeda yang dijadikan sebagai pilihan transportasi untuk pergi ke sekolah ataupun ke kantor. "
         "Sebaliknya di akhir pekan, sepertinya masyarakat lebih memilih kegiatan sosial dan berekreasi dengan keluarga (Analisis). "
         "Penyedia layanan bike-sharing dapat memanfaatkan temuan ini dengan meningkatkan jumlah sepeda dan ketersediaan layanan pada jam-jam sibuk di hari kerja, "
         "sementara juga mempertimbangkan strategi untuk menarik pengguna di akhir pekan, seperti promosi atau acara komunitas (Implikasi).")

st.write("Conclusion pertanyaan 2: Data menunjukkan bahwa penggunaan sepeda meningkat pada cuaca cerah dan hangat, "
         "sedangkan pada kondisi buruk (hujan, kabut) atau cuaca ekstrem (sangat panas atau sangat dingin), "
         "jumlah pengguna sepeda menurun drastis (Temuan). "
         "Keterkaitan ini mencerminkan kenyamanan dan preferensi pengguna sepeda yang cenderung memilih bersepeda dalam kondisi cuaca yang menyenangkan. "
         "Kelembaban yang tinggi dan suhu yang ekstrem juga mempengaruhi keputusan pengguna untuk bersepeda (Analisis). "
         "Untuk mengoptimalkan penggunaan sepeda, penyedia layanan dapat mempertimbangkan untuk menawarkan layanan yang lebih fleksibel berdasarkan cuaca, "
         "seperti penyewaan sepeda yang lebih terjangkau pada hari-hari dengan perkiraan cuaca baik atau menawarkan perlindungan tambahan saat cuaca buruk (Implikasi).")
