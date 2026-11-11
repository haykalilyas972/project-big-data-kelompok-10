import requests
import json
import hashlib
import time

from pathlib import Path
from datetime import datetime, timezone, timedelta


# ==========================================
# 1. PENGATURAN AKUISISI DATA
# ==========================================

START_YEAR = 2015
END_YEAR = 2024

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/"

PER_PAGE = 20000
MAX_RETRIES = 3
TIMEOUT = (30, 180)

INDICATORS = {
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",
    "GDP_per_Capita": "NY.GDP.PCAP.CD",
    "Unemployment": "SL.UEM.TOTL.ZS",
    "Internet_Users": "IT.NET.USER.ZS",
    "Population": "SP.POP.TOTL",
    "FDI": "BX.KLT.DINV.WD.GD.ZS"
}


# Lokasi folder proyek
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw" / "world_bank_wdi"

RAW_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. FUNGSI CHECKSUM SHA-256
# ==========================================

def calculate_checksum(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================
# 3. FUNGSI REQUEST DENGAN RETRY
# ==========================================

def request_api(url, params):

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=TIMEOUT,
                headers={
                    "User-Agent": "Group10-BigData-Project/1.0"
                }
            )

            response.raise_for_status()

            return response

        except requests.exceptions.RequestException as error:

            print(
                f"  Percobaan {attempt}/{MAX_RETRIES} gagal: {error}"
            )

            if attempt == MAX_RETRIES:
                raise

            wait_time = 5 * attempt

            print(f"  Mencoba kembali dalam {wait_time} detik...")

            time.sleep(wait_time)


# ==========================================
# 4. FUNGSI PENGAMBILAN DATA
# ==========================================

def acquire_indicator(indicator_name, indicator_code):

    print("\n====================================")
    print(f"Mengambil data: {indicator_name}")
    print(f"Kode indikator: {indicator_code}")
    print("====================================")

    page = 1
    total_pages = 1

    file_records = []
    total_records = 0

    indicator_url = BASE_URL + indicator_code

    while page <= total_pages:

        params = {
            "date": f"{START_YEAR}:{END_YEAR}",
            "format": "json",
            "per_page": PER_PAGE,
            "page": page
        }

        # Mengirim request ke World Bank API
        response = request_api(
            indicator_url,
            params
        )

        # Memeriksa respons JSON
        try:
            result = response.json()

        except ValueError:
            raise ValueError(
                f"Respons bukan JSON yang valid: {indicator_name}"
            )

        if not isinstance(result, list) or len(result) < 2:
            raise ValueError(
                f"Format respons API tidak sesuai: {indicator_name}"
            )

        metadata = result[0]
        records = result[1] or []

        if not isinstance(metadata, dict):
            raise ValueError(
                f"Metadata API tidak valid: {indicator_name}"
            )

        if not isinstance(records, list):
            raise ValueError(
                f"Data indikator tidak valid: {indicator_name}"
            )

        # Mendapatkan jumlah halaman dari API
        total_pages = int(metadata.get("pages", 1))

        # Menyimpan respons JSON asli
        file_name = (
            f"{indicator_code}_page_{page}.json"
        )

        file_path = RAW_FOLDER / file_name

        with open(file_path, "wb") as file:
            file.write(response.content)

        # Menghitung checksum file
        checksum = calculate_checksum(file_path)

        # Mencatat informasi file
        file_records.append({

            "file_name": file_name,
            "page": page,
            "records": len(records),
            "file_size_bytes": file_path.stat().st_size,
            "sha256": checksum

        })

        total_records += len(records)

        print(f"  Halaman: {page}/{total_pages}")
        print(f"  Jumlah data: {len(records)}")
        print(f"  File: {file_name}")

        page += 1

    print(f"\nBerhasil mengambil {indicator_name}")
    print(f"Total observasi: {total_records}")

    return {

        "indicator_name": indicator_name,
        "indicator_code": indicator_code,
        "status": "success",
        "date_range": f"{START_YEAR}-{END_YEAR}",
        "total_records": total_records,
        "total_pages": total_pages,
        "files": file_records

    }


# ==========================================
# 5. PROSES AKUISISI SEMUA INDIKATOR
# ==========================================

def main():

    print("====================================")
    print("WORLD BANK WDI DATA ACQUISITION")
    print("GROUP 10 - BIG DATA")
    print("====================================")

    acquisition_results = []
    failed_indicators = []

    for name, code in INDICATORS.items():

        try:

            result = acquire_indicator(name, code)

            acquisition_results.append(result)

        except Exception as error:

            print(f"\nGAGAL mengambil {name}: {error}")

            failed_indicators.append({

                "indicator_name": name,
                "indicator_code": code,
                "status": "failed",
                "error": str(error)

            })

    # ======================================
    # 6. MENYIAPKAN MANIFEST AKUISISI
    # ======================================

    jakarta_time = datetime.now(
        timezone(timedelta(hours=7))
    ).isoformat()

    manifest = {

        "dataset": "World Development Indicators",
        "publisher": "World Bank",
        "api_base_url": BASE_URL,
        "access_date": jakarta_time,

        "parameters": {

            "start_year": START_YEAR,
            "end_year": END_YEAR,
            "country": "all",
            "format": "json",
            "per_page": PER_PAGE,
            "timeout_seconds": TIMEOUT[1],
            "max_retries": MAX_RETRIES

        },

        "acquisition_status": (
            "success" if not failed_indicators else "incomplete"
        ),

        "indicators": acquisition_results,
        "failed_indicators": failed_indicators

    }

    # Menyimpan manifest
    manifest_path = RAW_FOLDER / "acquisition_manifest.json"

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ======================================
    # 7. MENYIMPAN CHECKSUM
    # ======================================

    checksum_path = RAW_FOLDER / "checksums.sha256"

    with open(
        checksum_path,
        "w",
        encoding="utf-8"
    ) as file:

        for indicator in acquisition_results:

            for item in indicator["files"]:

                file.write(
                    f"{item['sha256']}  {item['file_name']}\n"
                )

    # ======================================
    # 8. RINGKASAN HASIL AKUISISI
    # ======================================

    print("\n====================================")
    print("RINGKASAN AKUISISI DATA")
    print("====================================")

    print(
        f"Indikator berhasil: {len(acquisition_results)}"
    )

    print(
        f"Indikator gagal: {len(failed_indicators)}"
    )

    if failed_indicators:

        print("\nIndikator yang gagal:")

        for item in failed_indicators:
            print(f"- {item['indicator_name']}")

        print("\nSTATUS: AKUISISI BELUM LENGKAP")

    else:

        print("\nSTATUS: SEMUA AKUISISI BERHASIL!")

    print("------------------------------------")
    print(f"Lokasi data: {RAW_FOLDER}")
    print(f"Manifest: {manifest_path}")
    print(f"Checksum: {checksum_path}")
    print("====================================")


# ==========================================
# 9. MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":

    main()