# Technology Capacity Gap and Volcanic Disaster Risk Dashboard

## Description

A Streamlit-based dashboard supporting undergraduate thesis research on the relationship between technology capacity and volcanic disaster risk across 55 countries. Analysis uses OLS regression with NRI (Network Readiness Index) as the independent variable and WRI (World Risk Index) as the dependent variable.

---

## Features

- Profile and rankings of 55 volcanic countries
- Capacity-risk quadrant mapping
- OLS regression and Pearson correlation (NRI vs WRI)
- Head-to-head comparison: Indonesia vs developed nations
- Analysis by disaster management phase (mitigation, preparedness, response, recovery)
- Interactive map and volcano drill-down
- Full dataset download (CSV)
- Bilingual interface: Bahasa Indonesia / English

---

## How to Run

**Requirements:** Python 3.9+

```bash
# Clone repository
git clone https://github.com/ferrelganendra/Volcanic-Risk-Analysis.git
cd Volcanic-Risk-Analysis

# Install dependencies
pip install streamlit pandas numpy plotly scipy

# Run dashboard
streamlit run app.py
```

Dashboard accessible at `http://localhost:8501`.

---

## Repository Structure

```
├── app.py                  # Main dashboard source code
├── Master Dataset.xlsx     # Raw dataset (75 volcanic countries)
└── README.md
```

`app.py` reads data from `Master Dataset.xlsx` — both files must be in the same directory.  
Data sources: NRI 2024, World Risk Report 2024, GII 2024, World Bank GDP, INFORM Risk, GVP Smithsonian.

---

## Research Findings

| Indicator | Value |
|-----------|-------|
| Regression equation | Y = 69.0140 − 0.8489X |
| Coefficient of determination (R²) | 0.307 |
| Correlation coefficient (r) | −0.55 |
| Indonesia NRI | 53.84 |
| Indonesia WRI | 41.13 |
| Indonesia residual | +27.70 |

---

## License

Created for academic purposes. Commercial use is not permitted without the author's consent.

---
---

# Dashboard Kesenjangan Kapasitas Teknologi dan Risiko Bencana Vulkanik

## Deskripsi

Dashboard berbasis Streamlit untuk mendukung penelitian skripsi mengenai hubungan antara kapasitas teknologi dan risiko bencana vulkanik di 55 negara. Analisis menggunakan regresi OLS dengan NRI (Network Readiness Index) sebagai variabel independen dan WRI (World Risk Index) sebagai variabel dependen.

---

## Fitur Utama

- Profil dan peringkat 55 negara vulkanik
- Pemetaan kuadran kapasitas-risiko
- Regresi OLS dan korelasi Pearson (NRI vs WRI)
- Perbandingan Indonesia dengan negara-negara maju
- Analisis per fase penanggulangan bencana (mitigasi, kesiapsiagaan, respons, pemulihan)
- Peta interaktif dan drill-down gunung berapi
- Unduh dataset lengkap (CSV)
- Antarmuka bilingual: Bahasa Indonesia / English

---

## Cara Menjalankan

**Prasyarat:** Python 3.9+

```bash
# Clone repositori
git clone https://github.com/ferrelganendra/Volcanic-Risk-Analysis.git
cd Volcanic-Risk-Analysis

# Install dependensi
pip install streamlit pandas numpy plotly scipy

# Jalankan dashboard
streamlit run app.py
```

Dashboard dapat diakses di `http://localhost:8501`.

---

## Struktur Repositori

```
├── app.py                  # Source code utama dashboard
├── Master Dataset.xlsx     # Dataset mentah (75 negara vulkanik)
└── README.md
```

`app.py` membaca data dari `Master Dataset.xlsx` — pastikan kedua file berada di direktori yang sama.  
Sumber data: NRI 2024, World Risk Report 2024, GII 2024, World Bank GDP, INFORM Risk, GVP Smithsonian.

---

## Hasil Penelitian

| Indikator | Nilai |
|-----------|-------|
| Persamaan regresi | Y = 69.0140 − 0.8489X |
| Koefisien determinasi (R²) | 0.307 |
| Koefisien korelasi (r) | −0.55 |
| NRI Indonesia | 53.84 |
| WRI Indonesia | 41.13 |
| Residual Indonesia | +27.70 |

---

## Lisensi

Dibuat untuk keperluan akademik. Penggunaan komersial tidak diizinkan tanpa persetujuan penulis.
