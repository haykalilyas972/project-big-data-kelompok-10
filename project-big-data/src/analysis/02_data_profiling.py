import json
import pandas as pd

from pathlib import Path


# ==========================================
# 1. PENGATURAN FOLDER
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw" / "world_bank_wdi"
TABLE_FOLDER = PROJECT_ROOT / "results" / "tables"

TABLE_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. DAFTAR INDIKATOR
# ==========================================

INDICATORS = {
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",
    "GDP_per_Capita": "NY.GDP.PCAP.CD",
    "Unemployment": "SL.UEM.TOTL.ZS",
    "Internet_Users": "IT.NET.USER.ZS",
    "Population": "SP.POP.TOTL",
    "FDI": "BX.KLT.DINV.WD.GD.ZS"
}


# ==========================================
# 3. DATA DICTIONARY
# ==========================================

DATA_DICTIONARY = [
    {
        "variable": "country",
        "description": "Nama negara atau wilayah",
        "data_type": "String",
        "unit": "Nama",
        "role": "Key"
    },
    {
        "variable": "countryiso3code",
        "description": "Kode negara ISO 3166-1 alpha-3",
        "data_type": "String",
        "unit": "Kode",
        "role": "Key"
    },
    {
        "variable": "date",
        "description": "Tahun observasi",
        "data_type": "Integer",
        "unit": "Tahun",
        "role": "Key"
    },
    {
        "variable": "GDP_Growth",
        "description": "Pertumbuhan PDB tahunan",
        "data_type": "Numeric",
        "unit": "Persen (%)",
        "role": "Target"
    },
    {
        "variable": "GDP_per_Capita",
        "description": "PDB per kapita",
        "data_type": "Numeric",
        "unit": "US Dollar",
        "role": "Predictor"
    },
    {
        "variable": "Unemployment",
        "description": "Tingkat pengangguran total",
        "data_type": "Numeric",
        "unit": "Persen (%)",
        "role": "Predictor"
    },
    {
        "variable": "Internet_Users",
        "description": "Persentase penduduk pengguna internet",
        "data_type": "Numeric",
        "unit": "Persen (%)",
        "role": "Predictor"
    },
    {
        "variable": "Population",
        "description": "Jumlah penduduk",
        "data_type": "Numeric",
        "unit": "Orang",
        "role": "Predictor"
    },
    {
        "variable": "FDI",
        "description": "Investasi asing langsung bersih terhadap PDB",
        "data_type": "Numeric",
        "unit": "Persen (%)",
        "role": "Predictor"
    }
]


# ==========================================
# 4. MEMBACA DATA JSON
# ==========================================

def load_indicator(indicator_name, indicator_code):

    file_pattern = f"{indicator_code}_page_*.json"
    files = sorted(RAW_FOLDER.glob(file_pattern))

    if not files:
        raise FileNotFoundError(
            f"File tidak ditemukan untuk {indicator_name}: "
            f"{file_pattern}"
        )

    records = []

    for file_path in files:

        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)

        if not isinstance(content, list) or len(content) < 2:
            raise ValueError(
                f"Format JSON tidak sesuai: {file_path.name}"
            )

        page_records = content[1] or []
        records.extend(page_records)

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError(
            f"Tidak ada record untuk {indicator_name}"
        )

    # Mengambil nama negara atau wilayah
    df["country"] = df["country"].apply(
        lambda x: x.get("value")
        if isinstance(x, dict)
        else x
    )

    # Mengambil kode negara
    df["countryiso3code"] = df["countryiso3code"].replace(
        "", pd.NA
    )

    # Mengubah nilai indikator menjadi numerik
    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    # Mengubah tahun menjadi numerik
    df["date"] = pd.to_numeric(
        df["date"],
        errors="coerce"
    ).astype("Int64")

    # Menambahkan identitas indikator
    df["indicator_name"] = indicator_name
    df["indicator_code"] = indicator_code

    print(
        f"{indicator_name}: {len(df)} record berhasil dibaca."
    )

    return df


# ==========================================
# 5. PROSES UTAMA DATA PROFILING
# ==========================================

def main():

    print("====================================")
    print("WORLD BANK WDI DATA PROFILING")
    print("====================================")

    # --------------------------------------
    # Memuat semua indikator
    # --------------------------------------

    datasets = []

    for name, code in INDICATORS.items():

        df = load_indicator(name, code)
        datasets.append(df)

    all_data = pd.concat(
        datasets,
        ignore_index=True
    )

    print("\nSemua data berhasil dimuat.")
    print(f"Total record: {len(all_data)}")


    # ======================================
    # 6. PEMERIKSAAN MISSING VALUES
    # ======================================

    print("\nMemeriksa missing values...")

    missing_summary = []

    for name in INDICATORS:

        df = all_data[
            all_data["indicator_name"] == name
        ]

        missing_count = df["value"].isna().sum()
        total_count = len(df)

        missing_summary.append({

            "indicator": name,
            "total_records": total_count,
            "missing_values": int(missing_count),
            "valid_values": int(total_count - missing_count),
            "missing_percentage": round(
                (missing_count / total_count) * 100, 2
            ) if total_count else 0

        })

    missing_df = pd.DataFrame(missing_summary)

    missing_df.to_csv(
        TABLE_FOLDER / "missing_values.csv",
        index=False
    )


    # ======================================
    # 7. PEMERIKSAAN DUPLIKASI
    # ======================================

    print("Memeriksa duplikasi...")

    duplicate_summary = []
    duplicate_details = []

    for name in INDICATORS:

        df = all_data[
            all_data["indicator_name"] == name
        ].copy()

        # Menggunakan kode ISO3 jika tersedia.
        # Jika kosong, gunakan nama negara/wilayah.

        iso_code = df["countryiso3code"].astype("string").str.strip()

        df["country_key"] = iso_code.where(
            iso_code.notna() & iso_code.ne(""),
            df["country"].astype("string").str.strip()
        )

        # Mencari duplikasi berdasarkan identitas dan tahun

        duplicates = df[
            df.duplicated(
                subset=["country_key", "date"],
                keep=False
            )
        ].copy()

        duplicate_summary.append({

            "indicator": name,
            "duplicate_records": int(len(duplicates)),
            "duplicate_keys": int(
                duplicates[
                    ["country_key", "date"]
                ].drop_duplicates().shape[0]
            )

        })

        if not duplicates.empty:
            duplicate_details.append(duplicates)

    duplicate_df = pd.DataFrame(duplicate_summary)

    duplicate_df.to_csv(
        TABLE_FOLDER / "duplicate_summary.csv",
        index=False
    )

    if duplicate_details:

        duplicate_output = pd.concat(
            duplicate_details,
            ignore_index=True
        )

    else:

        duplicate_output = pd.DataFrame(
            columns=all_data.columns.tolist() + ["country_key"]
        )

    duplicate_output.to_csv(
        TABLE_FOLDER / "duplicate_records.csv",
        index=False
    )


    # ======================================
    # 8. STATISTIK DESKRIPTIF
    # ======================================

    print("Menghitung statistik deskriptif...")

    descriptive_summary = []

    for name in INDICATORS:

        df = all_data[
            all_data["indicator_name"] == name
        ]

        values = df["value"].dropna()

        descriptive_summary.append({

            "indicator": name,
            "count": int(values.count()),
            "mean": values.mean(),
            "median": values.median(),
            "std": values.std(),
            "min": values.min(),
            "max": values.max(),
            "q1": values.quantile(0.25),
            "q3": values.quantile(0.75)

        })

    descriptive_df = pd.DataFrame(descriptive_summary)

    descriptive_df.to_csv(
        TABLE_FOLDER / "descriptive_statistics.csv",
        index=False
    )


    # ======================================
    # 9. IDENTIFIKASI KANDIDAT OUTLIER
    # ======================================

    print("Mengidentifikasi kandidat outlier...")

    outlier_results = []

    for name in INDICATORS:

        df = all_data[
            all_data["indicator_name"] == name
        ].copy()

        values = df["value"].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = df[
            (df["value"] < lower_bound) |
            (df["value"] > upper_bound)
        ].copy()

        for _, row in outliers.iterrows():

            outlier_results.append({

                "indicator": name,
                "country": row["country"],
                "country_code": row["countryiso3code"],
                "year": row["date"],
                "value": row["value"],
                "lower_bound": lower_bound,
                "upper_bound": upper_bound

            })

    outlier_df = pd.DataFrame(outlier_results)

    outlier_df.to_csv(
        TABLE_FOLDER / "potential_outliers.csv",
        index=False
    )


    # ======================================
    # 10. PEMERIKSAAN TIPE DATA
    # ======================================

    print("Memeriksa tipe data...")

    dtype_df = pd.DataFrame({

        "column": all_data.columns,
        "data_type": all_data.dtypes.astype(str)

    })

    dtype_df.to_csv(
        TABLE_FOLDER / "data_types.csv",
        index=False
    )


    # ======================================
    # 11. MENYIMPAN DATA DICTIONARY
    # ======================================

    print("Menyimpan data dictionary...")

    dictionary_df = pd.DataFrame(DATA_DICTIONARY)

    dictionary_df.to_csv(
        TABLE_FOLDER / "data_dictionary.csv",
        index=False
    )


    # ======================================
    # 12. MENAMPILKAN RINGKASAN
    # ======================================

    print("\n====================================")
    print("HASIL DATA PROFILING")
    print("====================================")

    print("\nMISSING VALUES:")
    print(missing_df.to_string(index=False))

    print("\nDUPLIKASI:")
    print(duplicate_df.to_string(index=False))

    print("\nSTATISTIK DESKRIPTIF:")
    print(descriptive_df.to_string(index=False))

    print("\nJumlah kandidat outlier:")
    print(len(outlier_df))

    print("\n====================================")
    print("DATA PROFILING SELESAI")
    print("====================================")

    print(f"Hasil tersimpan di: {TABLE_FOLDER}")


# ==========================================
# 13. MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()