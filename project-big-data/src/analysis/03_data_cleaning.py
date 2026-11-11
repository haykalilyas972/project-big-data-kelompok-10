import json
import pandas as pd

from pathlib import Path


# ==========================================
# 1. PENGATURAN FOLDER
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw" / "world_bank_wdi"
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)


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
# 3. MEMBACA DATA JSON
# ==========================================

def load_indicator(indicator_name, indicator_code):

    print(f"Membaca data: {indicator_name}")

    file_pattern = f"{indicator_code}_page_*.json"
    files = sorted(RAW_FOLDER.glob(file_pattern))

    if not files:
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_pattern}"
        )

    records = []

    for file_path in files:

        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)

        if not isinstance(content, list) or len(content) < 2:
            raise ValueError(
                f"Format JSON tidak sesuai: {file_path.name}"
            )

        records.extend(content[1] or [])

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError(
            f"Tidak ada data untuk {indicator_name}"
        )

    # Mengambil nama negara atau wilayah
    df["country"] = df["country"].apply(
        lambda x: x.get("value")
        if isinstance(x, dict)
        else x
    )

    # Membersihkan kode ISO3
    df["countryiso3code"] = (
        df["countryiso3code"]
        .astype("string")
        .str.strip()
        .str.upper()
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
    )

    # Menambahkan nama indikator
    df["indicator_name"] = indicator_name

    return df


# ==========================================
# 4. PROSES CLEANING DAN INTEGRATION
# ==========================================

def main():

    print("====================================")
    print("WORLD BANK WDI DATA CLEANING")
    print("====================================")

    datasets = []
    excluded_data = []
    cleaning_summary = []

    # --------------------------------------
    # Membaca dan memeriksa setiap indikator
    # --------------------------------------

    for name, code in INDICATORS.items():

        df = load_indicator(name, code)

        total_before = len(df)

        # Negara individual harus memiliki
        # kode ISO3 tepat tiga karakter

        valid_iso3 = (
            df["countryiso3code"].notna()
            & df["countryiso3code"].str.fullmatch(
                r"[A-Z]{3}",
                na=False
            )
        )

        # Memisahkan data negara individual
        # dan data agregat

        country_df = df[valid_iso3].copy()
        aggregate_df = df[~valid_iso3].copy()

        # Menyimpan data agregat yang dikeluarkan
        if not aggregate_df.empty:

            excluded_data.append(
                aggregate_df[
                    [
                        "country",
                        "countryiso3code",
                        "date",
                        "value",
                        "indicator_name"
                    ]
                ]
            )

        # Memastikan tidak ada duplikasi
        # pada data negara individual

        duplicate_count = country_df.duplicated(
            subset=["countryiso3code", "date"]
        ).sum()

        if duplicate_count > 0:
            raise ValueError(
                f"Ditemukan {duplicate_count} duplikasi "
                f"pada indikator {name}. "
                "Periksa kembali data sumber."
            )

        # Menyimpan kolom yang diperlukan
        country_df = country_df[
            [
                "country",
                "countryiso3code",
                "date",
                "value"
            ]
        ].copy()

        # Mengganti nama kolom value
        country_df = country_df.rename(
            columns={"value": name}
        )

        datasets.append(country_df)

        cleaning_summary.append({

            "indicator": name,
            "records_before": total_before,
            "individual_country_records": len(country_df),
            "excluded_aggregate_records": len(aggregate_df),
            "duplicate_records": int(duplicate_count)

        })

        print(
            f"{name}: {len(country_df)} record negara individual, "
            f"{len(aggregate_df)} record agregat dikeluarkan."
        )


    # ======================================
    # 5. MEMBANGUN DAFTAR NEGARA DAN TAHUN
    # ======================================

    print("\nMenggabungkan data negara dan tahun...")

    # Membuat daftar unik negara dan tahun
    # dari seluruh indikator

    key_datasets = []

    for df in datasets:

        key_datasets.append(
            df[
                [
                    "country",
                    "countryiso3code",
                    "date"
                ]
            ]
        )

    master_data = pd.concat(
        key_datasets,
        ignore_index=True
    )

    master_data = master_data.drop_duplicates(
        subset=["countryiso3code", "date"]
    )

    # ======================================
    # 6. MENGGABUNGKAN ENAM INDIKATOR
    # ======================================

    print("Mengintegrasikan enam indikator...")

    for df in datasets:

        indicator_column = [
            col for col in df.columns
            if col not in [
                "country",
                "countryiso3code",
                "date"
            ]
        ][0]

        master_data = master_data.merge(
            df[
                [
                    "countryiso3code",
                    "date",
                    indicator_column
                ]
            ],
            on=["countryiso3code", "date"],
            how="left",
            validate="one_to_one"
        )

    # Mengurutkan data
    master_data = master_data.sort_values(
        by=["country", "date"]
    ).reset_index(drop=True)

    # Mengatur urutan kolom
    final_columns = [
        "country",
        "countryiso3code",
        "date",
        "GDP_Growth",
        "GDP_per_Capita",
        "Unemployment",
        "Internet_Users",
        "Population",
        "FDI"
    ]

    master_data = master_data[final_columns]

    # ======================================
    # 7. MENYIMPAN DATA HASIL CLEANING
    # ======================================

    cleaned_path = (
        PROCESSED_FOLDER / "wdi_cleaned.csv"
    )

    master_data.to_csv(
        cleaned_path,
        index=False
    )

    print("\nData hasil cleaning berhasil disimpan.")


    # ======================================
    # 8. MEMERIKSA MISSING VALUES
    # ======================================

    print("Memeriksa missing values setelah penggabungan...")

    missing_summary = []

    for indicator in INDICATORS:

        missing_count = master_data[indicator].isna().sum()
        total_count = len(master_data)

        missing_summary.append({

            "indicator": indicator,
            "total_records": total_count,
            "missing_values": int(missing_count),
            "valid_values": int(total_count - missing_count),
            "missing_percentage": round(
                (missing_count / total_count) * 100, 2
            ) if total_count else 0

        })

    missing_df = pd.DataFrame(missing_summary)

    missing_df.to_csv(
        PROCESSED_FOLDER / "missing_values_after_cleaning.csv",
        index=False
    )


    # ======================================
    # 9. MEMBUAT DATASET LENGKAP
    # ======================================

    print("Membuat dataset dengan data lengkap...")

    indicator_columns = list(INDICATORS.keys())

    complete_data = master_data.dropna(
        subset=indicator_columns
    ).copy()

    complete_path = (
        PROCESSED_FOLDER / "wdi_complete.csv"
    )

    complete_data.to_csv(
        complete_path,
        index=False
    )


    # ======================================
    # 10. MENYIMPAN DATA AGREGAT TERPISAH
    # ======================================

    print("Menyimpan catatan data agregat...")

    if excluded_data:

        excluded_df = pd.concat(
            excluded_data,
            ignore_index=True
        )

    else:

        excluded_df = pd.DataFrame(
            columns=[
                "country",
                "countryiso3code",
                "date",
                "value",
                "indicator_name"
            ]
        )

    excluded_df.to_csv(
        PROCESSED_FOLDER / "excluded_aggregates.csv",
        index=False
    )


    # ======================================
    # 11. MENYIMPAN RINGKASAN CLEANING
    # ======================================

    summary_df = pd.DataFrame(cleaning_summary)

    summary_df.to_csv(
        PROCESSED_FOLDER / "cleaning_summary.csv",
        index=False
    )


    # ======================================
    # 12. MENAMPILKAN HASIL
    # ======================================

    print("\n====================================")
    print("HASIL DATA CLEANING")
    print("====================================")

    print(
        f"Total baris setelah cleaning: "
        f"{len(master_data)}"
    )

    print(
        f"Total baris data lengkap: "
        f"{len(complete_data)}"
    )

    print(
        f"Total data agregat yang dikeluarkan: "
        f"{len(excluded_df)}"
    )

    print("\nRINGKASAN MISSING VALUES:")
    print(missing_df.to_string(index=False))

    print("\nRINGKASAN CLEANING:")
    print(summary_df.to_string(index=False))

    print("\n====================================")
    print("DATA CLEANING BERHASIL")
    print("====================================")

    print(f"Lokasi hasil: {PROCESSED_FOLDER}")


# ==========================================
# 13. MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()