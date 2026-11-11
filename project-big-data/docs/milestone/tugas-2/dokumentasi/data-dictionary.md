# DATA DICTIONARY
## World Development Indicators (WDI)

### 1. Informasi Dataset

| Keterangan | Informasi |
|---|---|
| Nama Dataset | World Development Indicators (WDI) |
| Sumber | World Bank |
| Periode Data | 2015–2024 |
| Frekuensi | Tahunan |
| Cakupan | Negara-negara individual |
| Jumlah Observasi | 2.610 baris |
| Jumlah Variabel Indikator | 6 indikator |
| Format Data | CSV dan JSON |
| Tujuan | Analisis faktor-faktor yang berhubungan dengan pertumbuhan ekonomi negara |

### 2. Daftar Variabel

| No. | Nama Variabel | Kode World Bank | Tipe Data | Satuan |
|---|---|---|---|---|
| 1 | GDP_Growth | NY.GDP.MKTP.KD.ZG | Float | Persen (%) |
| 2 | GDP_per_Capita | NY.GDP.PCAP.CD | Float | US Dollar (US$) |
| 3 | Unemployment | SL.UEM.TOTL.ZS | Float | Persen (%) |
| 4 | Internet_Users | IT.NET.USER.ZS | Float | Persen (%) |
| 5 | Population | SP.POP.TOTL | Integer/Numeric | Jiwa |
| 6 | FDI | BX.KLT.DINV.WD.GD.ZS | Float | Persen terhadap GDP (%) |

### 3. Penjelasan Variabel

1. **GDP_Growth**  
   Menunjukkan tingkat pertumbuhan ekonomi suatu negara berdasarkan perubahan GDP tahunan. Variabel ini digunakan sebagai target penelitian.

2. **GDP_per_Capita**  
   Menunjukkan nilai GDP per kapita dalam US Dollar, yang menggambarkan nilai output ekonomi rata-rata per penduduk.

3. **Unemployment**  
   Menunjukkan persentase pengangguran terhadap total angkatan kerja.

4. **Internet_Users**  
   Menunjukkan persentase penduduk yang menggunakan internet.

5. **Population**  
   Menunjukkan jumlah penduduk suatu negara.

6. **FDI**  
   Menunjukkan persentase investasi asing langsung bersih terhadap GDP suatu negara.

### 4. Kategori dan Target

- **Kategori:** Data ekonomi dan sosial negara.
- **Variabel target:** GDP_Growth.
- **Variabel lainnya:** GDP_per_Capita, Unemployment, Internet_Users, Population, dan FDI.

### 5. Kunci dan Grain Data

- **Primary Key (kunci identifikasi):** Kombinasi countryiso3code dan tahun.
- **countryiso3code:** Kode ISO tiga huruf yang mengidentifikasi negara.
- **Grain:** Satu baris data merepresentasikan satu negara pada satu tahun tertentu.
- **Frekuensi pencatatan:** Tahunan.

### 6. Missing Values

Berdasarkan hasil data cleaning, jumlah missing values adalah:

| Variabel | Missing Values | Persentase |
|---|---:|---:|
| GDP_Growth | 85 | 3,26% |
| GDP_per_Capita | 81 | 3,10% |
| Unemployment | 309 | 11,84% |
| Internet_Users | 446 | 17,09% |
| Population | 0 | 0,00% |
| FDI | 217 | 8,31% |

Missing values dipertahankan dalam dataset utama dan tidak diisi secara manual. Dataset tambahan `wdi_complete.csv` berisi observasi yang memiliki nilai lengkap pada seluruh enam indikator.

### 7. Keterangan Struktur Data

Dataset hasil cleaning terdiri dari 2.610 observasi negara individual untuk periode 2015–2024. Data agregat yang bukan merupakan negara individual dikeluarkan dari dataset utama. Penggabungan indikator dilakukan berdasarkan kode negara dan tahun untuk memastikan setiap observasi mewakili negara dan periode yang sama.