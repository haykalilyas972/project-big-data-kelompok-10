# Analisis Faktor-Faktor yang Berhubungan dengan Pertumbuhan Ekonomi Negara

## Deskripsi Proyek

Proyek ini merupakan proyek akhir mata kuliah **Pengantar Big Data** yang bertujuan untuk menganalisis hubungan antara berbagai indikator pembangunan dengan pertumbuhan ekonomi negara.

Dataset yang digunakan adalah **World Development Indicators (WDI)** yang diterbitkan oleh **World Bank**. Dataset ini menyediakan berbagai indikator ekonomi, sosial, pendidikan, kesehatan, lingkungan, perdagangan, dan pembangunan dari berbagai negara dan wilayah.

Dalam proyek ini, analisis difokuskan pada pertumbuhan ekonomi serta hubungannya dengan beberapa indikator pembangunan seperti GDP per capita, tingkat pengangguran, penggunaan internet, pendidikan, populasi, investasi asing, dan perdagangan.

---

## Tujuan Penelitian

Penelitian ini bertujuan untuk:

1. Menganalisis perkembangan pertumbuhan ekonomi negara berdasarkan data World Development Indicators.
2. Menganalisis hubungan antara GDP per capita dengan pertumbuhan ekonomi.
3. Menganalisis hubungan antara tingkat pengangguran dengan pertumbuhan ekonomi.
4. Menganalisis hubungan antara penggunaan internet dan indikator pendidikan dengan pertumbuhan ekonomi.
5. Membangun model untuk mengetahui kemampuan beberapa indikator pembangunan dalam menjelaskan pertumbuhan ekonomi.
6. Mengelompokkan negara berdasarkan karakteristik indikator pembangunan yang dimiliki.

---

## Pertanyaan Analitik

Pertanyaan analitik yang digunakan dalam penelitian ini adalah:

1. Bagaimana perkembangan pertumbuhan ekonomi negara selama periode penelitian?
2. Negara mana yang memiliki pertumbuhan ekonomi relatif tinggi dan rendah?
3. Apakah GDP per capita memiliki hubungan dengan pertumbuhan ekonomi?
4. Apakah tingkat pengangguran memiliki hubungan dengan pertumbuhan ekonomi?
5. Apakah penggunaan internet dan pendidikan memiliki hubungan dengan pertumbuhan ekonomi?
6. Seberapa baik indikator pembangunan dapat menjelaskan variasi pertumbuhan ekonomi?
7. Apakah negara-negara dapat dikelompokkan berdasarkan karakteristik ekonominya?

---

## Dataset

### World Development Indicators (WDI)

**Penerbit:** World Bank

**Nama Dataset:** World Development Indicators

**Periode Data:** 1960–2025

**Periodicitas:** Tahunan

**Cakupan:** Lebih dari 200 negara dan wilayah

**Jumlah Indikator:** Lebih dari 1.500 indikator

**Lisensi Dataset:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**Tanggal Akses:** 6 September 2026

**Sumber Dataset:**

https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators

Dataset WDI digunakan sebagai sumber utama untuk analisis pada proyek ini.

---

## Variabel Utama

Variabel yang direncanakan digunakan dalam penelitian meliputi:

| Variabel                  | Keterangan                                    |
| ------------------------- | --------------------------------------------- |
| GDP Growth                | Pertumbuhan GDP tahunan                       |
| GDP per Capita            | GDP per kapita                                |
| Unemployment              | Tingkat pengangguran                          |
| Internet Users            | Persentase penduduk yang menggunakan internet |
| Education                 | Indikator pendidikan                          |
| Population                | Jumlah penduduk                               |
| Foreign Direct Investment | Investasi langsung asing                      |
| Trade                     | Indikator perdagangan                         |

### Variabel Target

Variabel target utama dalam penelitian ini adalah:

**GDP Growth (Annual %)**

Kode indikator World Bank:

`NY.GDP.MKTP.KD.ZG`

Variabel tersebut digunakan untuk merepresentasikan pertumbuhan ekonomi suatu negara.

---

## Unit Analisis

Unit analisis penelitian adalah:

**Negara/wilayah pada setiap tahun pengamatan.**

Setiap observasi merupakan kombinasi antara suatu negara/wilayah dan tahun tertentu.

Contoh:

```text
Indonesia - 2020
Indonesia - 2021
Malaysia - 2020
Malaysia - 2021
```

---

## Metodologi

Tahapan analisis yang digunakan dalam proyek ini meliputi:

1. Pengumpulan data
2. Data cleaning
3. Data preprocessing
4. Exploratory Data Analysis (EDA)
5. Analisis statistik deskriptif
6. Visualisasi data
7. Analisis korelasi
8. Regresi linear
9. K-Means clustering
10. Evaluasi model
11. Interpretasi hasil
12. Dokumentasi dan pelaporan

---

## Analisis Deskriptif

Analisis deskriptif digunakan untuk memahami karakteristik dasar dataset.

Statistik yang digunakan meliputi:

* Mean
* Median
* Minimum
* Maksimum
* Standar deviasi
* Kuartil
* Jumlah observasi
* Jumlah missing value

---

## Visualisasi

Visualisasi yang direncanakan meliputi:

* Line chart untuk melihat perkembangan pertumbuhan ekonomi dari waktu ke waktu.
* Bar chart untuk membandingkan pertumbuhan ekonomi antarnegara.
* Scatter plot untuk melihat hubungan antarvariabel.
* Heatmap untuk melihat korelasi antarvariabel.
* Boxplot untuk melihat distribusi dan outlier.
* Visualisasi hasil clustering untuk melihat kelompok negara berdasarkan karakteristik indikator pembangunan.

---

## Metode Analisis Lanjutan

### Korelasi

Analisis korelasi digunakan untuk mengetahui arah dan kekuatan hubungan antara pertumbuhan ekonomi dengan indikator pembangunan lainnya.

### Regresi Linear

Regresi linear digunakan untuk mengetahui hubungan beberapa indikator pembangunan terhadap GDP Growth.

Model yang direncanakan:

```text
GDP Growth =
β0 + β1(GDP per Capita)
+ β2(Unemployment)
+ β3(Internet Users)
+ β4(Education)
+ ε
```

### K-Means Clustering

K-Means digunakan untuk mengelompokkan negara berdasarkan kemiripan karakteristik indikator pembangunan.

Sebelum proses clustering, data akan melalui proses standardisasi agar perbedaan skala antarvariabel tidak memengaruhi hasil pengelompokan secara berlebihan.

---

## Evaluasi Model

Untuk model regresi, metrik evaluasi yang digunakan adalah:

* **Mean Absolute Error (MAE)**
* **Root Mean Squared Error (RMSE)**
* **R-Squared (R²)**

Untuk evaluasi clustering digunakan:

* **Silhouette Score**

Sebagai baseline model prediksi digunakan **Mean Baseline**, yaitu menggunakan nilai rata-rata GDP Growth dari data training sebagai prediksi.

---

## Potensi Bias dan Keterbatasan

Beberapa potensi bias dan keterbatasan dataset yang perlu diperhatikan antara lain:

1. Kualitas dan kelengkapan data dapat berbeda antarnegara.
2. Beberapa indikator memiliki missing value pada negara atau tahun tertentu.
3. Metode pengumpulan data dapat berbeda antarnegara.
4. Dataset dapat mengalami pembaruan atau revisi.
5. Outlier pada indikator tertentu dapat memengaruhi hasil analisis.
6. Hubungan statistik antarvariabel tidak secara otomatis menunjukkan hubungan sebab-akibat.

Oleh karena itu, hasil analisis akan diinterpretasikan secara hati-hati dan disertai dokumentasi mengenai proses preprocessing yang dilakukan.

---

## Struktur Direktori

```text
project-big-data/
│
├── README.md
├── LICENSE
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── milestones/
│       └── tugas-1/
│           ├── proposal.pdf
│           └── data-card.md
│
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   ├── 02-data-cleaning.ipynb
│   └── 03-analysis.ipynb
│
├── src/
│   ├── data_collection/
│   ├── preprocessing/
│   ├── analysis/
│   └── visualization/
│
└── results/
    ├── figures/
    └── tables/
```

---

## Dokumentasi Tugas

Dokumentasi setiap milestone proyek disimpan pada direktori:

```text
docs/milestones/
```

Untuk Tugas 1:

```text
docs/milestones/tugas-1/
```

File yang disimpan meliputi:

```text
proposal.pdf
data-card.md
```

---

## Anggota Kelompok

| No. | Nama             |      NIM      | Peran                 |
| --- | ---------------- | ------------- | --------------------- |
| 1   |   Haykal Ilyas   | 2410631250012 | Project Coordinator   |
| 2   |   Haykal Ilyas   | 2410631250012 | Data Collection       |
| 3   |   Haykal Ilyas   | 2410631250012 | Data Cleaning         |
| 4   | M hanif abdillah | 2410631250099 | Data Analysis         |
| 5   | M hanif abdillah | 2410631250099 | Visualization         |
| 6   | M hanif abdillah | 2410631250099 | Modeling & Evaluation |


---

## Pembagian Tugas

Pembagian tugas kelompok dilakukan berdasarkan beberapa bagian utama proyek:

* Project Coordinator: koordinasi proyek dan dokumentasi.
* Data Collection: pengumpulan dan dokumentasi dataset.
* Data Cleaning: preprocessing dan penanganan missing value.
* Data Analysis: analisis statistik dan korelasi.
* Visualization: pembuatan visualisasi.
* Modeling & Evaluation: pemodelan, evaluasi, dan interpretasi hasil.

Pembagian tugas dapat disesuaikan berdasarkan kebutuhan dan kontribusi aktual masing-masing anggota.

---

## Lisensi

Kode dan program yang dikembangkan dalam proyek ini menggunakan **MIT License**.

Dataset **World Development Indicators (WDI)** merupakan data dari World Bank dan penggunaannya mengikuti ketentuan lisensi serta atribusi yang berlaku pada dataset tersebut.

Untuk informasi lebih lanjut mengenai dataset:

https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators

---

## Sumber

World Bank. *World Development Indicators.*

World Bank Data Catalog:

https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators

---

## Milestone

### Tugas 1 — Fondasi Penelitian dan Persetujuan Dataset

Status: **In Progress**

Dokumen Tugas 1:

```text
docs/milestones/tugas-1/
├── proposal.pdf
└── data-card.md
```

Release/Tag:

```text
tugas-1
```

---

## Catatan Reproduksibilitas

Dataset yang digunakan dalam penelitian dapat diperbarui oleh penerbit. Oleh karena itu, penelitian mencatat tanggal akses dataset untuk menjaga keterlacakan sumber data.

**Tanggal akses dataset:** 6 September 2026

Setiap perubahan penting terhadap kode, data preprocessing, analisis, dan dokumentasi akan dicatat melalui commit pada repository GitHub.
