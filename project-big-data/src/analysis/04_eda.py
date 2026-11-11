import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. PENGATURAN FOLDER DAN DATA
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT_DIR / "data" / "processed" / "wdi_cleaned.csv"
TABLE_DIR = ROOT_DIR / "results" / "tables"
FIGURE_DIR = ROOT_DIR / "results" / "figures"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("WORLD BANK WDI - EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# Membaca dataset
df = pd.read_csv(INPUT_FILE)

# Memastikan tahun dan indikator berbentuk numerik
df["date"] = pd.to_numeric(df["date"], errors="coerce")

indicators = [
    "GDP_Growth",
    "GDP_per_Capita",
    "Unemployment",
    "Internet_Users",
    "Population",
    "FDI"
]

for column in indicators:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print(f"Jumlah observasi: {len(df)}")
print(f"Jumlah negara: {df['countryiso3code'].nunique()}")
print(f"Periode: {int(df['date'].min())}-{int(df['date'].max())}")


# ==========================================
# 2. STATISTIK DESKRIPTIF
# ==========================================

print("\n[1] Membuat statistik deskriptif...")

statistics = df[indicators].describe().T
statistics.to_csv(TABLE_DIR / "eda_descriptive_statistics.csv")

print(statistics)


# ==========================================
# 3. ANALISIS TREN GDP GROWTH PER TAHUN
# ==========================================

print("\n[2] Menganalisis tren GDP Growth...")

yearly_growth = (
    df.groupby("date")["GDP_Growth"]
    .agg(["count", "mean", "median", "min", "max"])
    .reset_index()
)

yearly_growth.to_csv(
    TABLE_DIR / "eda_gdp_growth_by_year.csv",
    index=False
)

plt.figure(figsize=(10, 6))
plt.plot(
    yearly_growth["date"],
    yearly_growth["mean"],
    marker="o",
    label="Rata-rata GDP Growth"
)
plt.plot(
    yearly_growth["date"],
    yearly_growth["median"],
    marker="s",
    linestyle="--",
    label="Median GDP Growth"
)

plt.title("Tren GDP Growth Negara Tahun 2015-2024")
plt.xlabel("Tahun")
plt.ylabel("GDP Growth (%)")
plt.xticks(yearly_growth["date"].dropna().astype(int))
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(FIGURE_DIR / "01_gdp_growth_trend.png", dpi=300)
plt.close()


# ==========================================
# 4. DISTRIBUSI GDP GROWTH
# ==========================================

print("\n[3] Menganalisis distribusi GDP Growth...")

growth_data = df["GDP_Growth"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(growth_data, bins=40, edgecolor="black")
plt.title("Distribusi GDP Growth Negara")
plt.xlabel("GDP Growth (%)")
plt.ylabel("Frekuensi")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "02_gdp_growth_distribution.png", dpi=300)
plt.close()


# ==========================================
# 5. KORELASI ANTARVARIABEL
# ==========================================

print("\n[4] Menghitung korelasi antarvariabel...")

correlation = df[indicators].corr(method="pearson")

correlation.to_csv(TABLE_DIR / "eda_correlation_matrix.csv")

plt.figure(figsize=(10, 8))
plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Koefisien Korelasi")

plt.xticks(
    range(len(indicators)),
    indicators,
    rotation=45,
    ha="right"
)
plt.yticks(range(len(indicators)), indicators)

for i in range(len(indicators)):
    for j in range(len(indicators)):
        value = correlation.iloc[i, j]
        if pd.notna(value):
            plt.text(
                j, i, f"{value:.2f}",
                ha="center",
                va="center",
                fontsize=8
            )

plt.title("Matriks Korelasi Antarvariabel")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "03_correlation_matrix.png", dpi=300)
plt.close()


# ==========================================
# 6. HUBUNGAN GDP GROWTH DENGAN PREDIKTOR
# ==========================================

print("\n[5] Membuat analisis hubungan antarvariabel...")

predictors = [
    "GDP_per_Capita",
    "Unemployment",
    "Internet_Users",
    "Population",
    "FDI"
]

correlation_with_target = (
    correlation["GDP_Growth"]
    .drop("GDP_Growth")
    .reset_index()
)

correlation_with_target.columns = [
    "predictor",
    "correlation_with_GDP_Growth"
]

correlation_with_target.to_csv(
    TABLE_DIR / "eda_correlation_with_target.csv",
    index=False
)

for i, predictor in enumerate(predictors, start=1):

    plot_data = df[["GDP_Growth", predictor]].dropna()

    plt.figure(figsize=(8, 6))
    plt.scatter(
        plot_data[predictor],
        plot_data["GDP_Growth"],
        alpha=0.35
    )

    plt.title(f"GDP Growth dan {predictor}")
    plt.xlabel(predictor)
    plt.ylabel("GDP Growth (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / f"0{i + 3}_gdp_growth_vs_{predictor}.png",
        dpi=300
    )
    plt.close()


# ==========================================
# 7. PERBANDINGAN RATA-RATA GDP GROWTH NEGARA
# ==========================================

print("\n[6] Membandingkan rata-rata GDP Growth negara...")

country_growth = (
    df.groupby(["country", "countryiso3code"])["GDP_Growth"]
    .agg(["count", "mean"])
    .reset_index()
)

# Menggunakan negara dengan minimal 5 tahun data GDP Growth
country_growth = country_growth[
    country_growth["count"] >= 5
].copy()

country_growth = country_growth.sort_values(
    "mean",
    ascending=False
)

country_growth.to_csv(
    TABLE_DIR / "eda_country_average_gdp_growth.csv",
    index=False
)

top_countries = country_growth.head(10)
bottom_countries = country_growth.tail(10).sort_values("mean")

plt.figure(figsize=(11, 7))
plt.barh(
    top_countries["country"],
    top_countries["mean"]
)
plt.title("10 Negara dengan Rata-rata GDP Growth Tertinggi")
plt.xlabel("Rata-rata GDP Growth (%)")
plt.ylabel("Negara")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "09_top_10_gdp_growth_countries.png", dpi=300)
plt.close()

plt.figure(figsize=(11, 7))
plt.barh(
    bottom_countries["country"],
    bottom_countries["mean"]
)
plt.title("10 Negara dengan Rata-rata GDP Growth Terendah")
plt.xlabel("Rata-rata GDP Growth (%)")
plt.ylabel("Negara")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "10_bottom_10_gdp_growth_countries.png", dpi=300)
plt.close()


# ==========================================
# 8. RINGKASAN HASIL EDA
# ==========================================

print("\n[7] Membuat ringkasan hasil EDA...")

summary = pd.DataFrame({
    "Informasi": [
        "Jumlah observasi",
        "Jumlah negara",
        "Tahun awal",
        "Tahun akhir",
        "Rata-rata GDP Growth",
        "Median GDP Growth",
        "GDP Growth tertinggi",
        "GDP Growth terendah",
        "Jumlah data GDP Growth tersedia"
    ],
    "Nilai": [
        len(df),
        df["countryiso3code"].nunique(),
        int(df["date"].min()),
        int(df["date"].max()),
        df["GDP_Growth"].mean(),
        df["GDP_Growth"].median(),
        df["GDP_Growth"].max(),
        df["GDP_Growth"].min(),
        df["GDP_Growth"].count()
    ]
})

summary.to_csv(
    TABLE_DIR / "eda_summary.csv",
    index=False
)

print(summary.to_string(index=False))

print("\n" + "=" * 50)
print("EDA BERHASIL DISELESAIKAN!")
print("=" * 50)
print(f"Hasil tabel disimpan di: {TABLE_DIR}")
print(f"Hasil grafik disimpan di: {FIGURE_DIR}")