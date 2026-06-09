# =============================================================
# IMPORT LIBRARY
# re        → manipulasi teks (regex)
# streamlit → framework dashboard web interaktif
# pandas    → manipulasi data tabular (DataFrame)
# numpy     → komputasi numerik
# plotly    → visualisasi interaktif (grafik, peta)
# scipy     → statistik: regresi OLS (linregress) & korelasi Pearson
# =============================================================
import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress, pearsonr

# Konfigurasi halaman Streamlit: judul tab browser, ikon, dan layout lebar
st.set_page_config(
    page_title="Indonesia vs Dunia: Teknologi & Kesiapan Vulkanik",
    page_icon="🌋",
    layout="wide"
)

# ================================================================
# SISTEM TERJEMAHAN (Bilingual: Indonesia / English)
# _TRANS adalah dictionary berisi semua teks UI dalam dua bahasa.
# Fungsi T(key) digunakan di seluruh kode untuk mengambil teks
# sesuai bahasa yang sedang aktif (dipilih pengguna di sidebar).
# ================================================================
_TRANS = {
    "main_desc_id": {"id": "", "en": ""},
    "page_title":          {"id": "Indonesia vs Dunia: Teknologi & Kesiapan Vulkanik",       "en": "Indonesia vs World: Technology & Volcanic Disaster Readiness"},
    "sidebar_title":       {"id": "Dashboard Skripsi",                                        "en": "Research Dashboard"},
    "sidebar_subtitle":    {"id": "Teknologi & Kesiapan Bencana Gunung Berapi: Indonesia vs Dunia", "en": "Technology & Volcanic Disaster Readiness: Indonesia vs World"},
    "sidebar_flow":        {"id": "### 🗺️ Alur Analisis",                                     "en": "### 🗺️ Analysis Flow"},
    "sidebar_wri_legend":  {"id": "### 🎨 Kategori Risiko WRI",                               "en": "### 🎨 WRI Risk Categories"},
    "sidebar_wri_thresh":  {"id": "*Threshold resmi World Risk Report 2024*",                  "en": "*Official World Risk Report 2024 thresholds*"},
    "sidebar_wri_source":  {"id": "Sumber: World Risk Report 2024, Bündnis Entwicklung Hilft", "en": "Source: World Risk Report 2024, Bündnis Entwicklung Hilft"},
    "sidebar_wri_dir":     {"id": "⚠️ Semakin besar WRI Score = semakin tinggi risiko bencana",     "en": "⚠️ Higher WRI Score = higher disaster risk"},
    "sidebar_cap_dir":     {"id": "⚠️ Semakin kecil nilai Lack of Coping = semakin baik kapasitas penanggulangan", "en": "⚠️ Lower Lack of Coping value = better coping capacity"},
    "sidebar_cap_legend":  {"id": "### 🛡️ Kapasitas Penanggulangan (WRI)",                   "en": "### 🛡️ Coping Capacity (WRI)"},
    "sidebar_cap_thresh":  {"id": "*Berdasarkan Lack of Coping Capacities — World Risk Report 2024*", "en": "*Based on Lack of Coping Capacities — World Risk Report 2024*"},
    "sidebar_cap_desc":    {"id": "Threshold: 0–3.47 Sangat Tinggi | 3.48–10.01 Tinggi | 10.02–12.64 Sedang | 12.65–39.05 Rendah | >39.05 Sangat Rendah", "en": "Threshold: 0–3.47 Very High | 3.48–10.01 High | 10.02–12.64 Medium | 12.65–39.05 Low | >39.05 Very Low"},
    "sidebar_validity":    {"id": "### 📚 Validitas Indikator",                               "en": "### 📚 Indicator Validity"},
    "sidebar_sources":     {"id": "### 🔗 Sumber Data (2024)",                               "en": "### 🔗 Data Sources (2024)"},
    "sidebar_pembuat":     {"id": "**Pembuat:**",    "en": "**Publisher:**"},
    "sidebar_mengukur":    {"id": "**Mengukur:**",   "en": "**Measures:**"},
    "sidebar_validitas":   {"id": "**Validitas:**",  "en": "**Validity:**"},
    "tab1_sidebar": {"id": "**Tab 1** Profil & peringkat negara vulkanik",                                                          "en": "**Tab 1** Volcanic country profiles & rankings"},
    "tab2_sidebar": {"id": "**Tab 2** Di kuadran kapasitas-risiko mana posisi Indonesia? (Pemetaan Makro)",                         "en": "**Tab 2** Which capacity-risk quadrant is Indonesia in? (Macro Mapping)"},
    "tab3_sidebar": {"id": "**Tab 3** Apakah kapasitas teknologi berkorelasi dengan kemampuan penanggulangan? (Analisis Mikro)",    "en": "**Tab 3** Does technology capacity correlate with coping ability? (Micro/Regression Analysis)"},
    "tab4_sidebar": {"id": "**Tab 4** Seberapa besar gap teknologi Indonesia vs negara maju?",                                      "en": "**Tab 4** How large is Indonesia\'s technology gap vs advanced nations?"},
    "tab5_sidebar": {"id": "**Tab 5** Di fase penanggulangan mana Indonesia paling lemah?",                                        "en": "**Tab 5** Which disaster management phase is Indonesia weakest in?"},
    "tab6_sidebar": {"id": "**Tab 6** Beban vulkanik Indonesia vs dunia (drill-down gunung)",                                      "en": "**Tab 6** Indonesia\'s volcanic burden vs world (volcano drill-down)"},
    "tab7_sidebar": {"id": "**Tab 7** Data lengkap & unduh",                                                                       "en": "**Tab 7** Full dataset & download"},
    "wri_very_high": {"id": "Risiko Sangat Tinggi", "en": "Very High Risk"},
    "wri_high":      {"id": "Risiko Tinggi",        "en": "High Risk"},
    "wri_medium":    {"id": "Risiko Sedang",        "en": "Medium Risk"},
    "wri_low":       {"id": "Risiko Rendah",        "en": "Low Risk"},
    "wri_very_low":  {"id": "Risiko Sangat Rendah", "en": "Very Low Risk"},
    "wri_no_data":   {"id": "Data Tidak Tersedia",  "en": "Data Not Available"},
    "cap_very_high": {"id": "Kapasitas Sangat Tinggi", "en": "Very High Capacity"},
    "cap_high":      {"id": "Kapasitas Tinggi",        "en": "High Capacity"},
    "cap_medium":    {"id": "Kapasitas Sedang",        "en": "Medium Capacity"},
    "cap_low":       {"id": "Kapasitas Rendah",        "en": "Low Capacity"},
    "cap_very_low":  {"id": "Kapasitas Sangat Rendah", "en": "Very Low Capacity"},
    "quad_preventif": {"id": "Preventif — Teknologi Tinggi / Risiko Rendah", "en": "Preventive — High Technology / Low Risk"},
    "quad_reaktif":   {"id": "Reaktif — Teknologi Rendah / Risiko Tinggi",   "en": "Reactive — Low Technology / High Risk"},
    "quad_waspada":   {"id": "Waspada — Teknologi Tinggi / Risiko Tinggi",   "en": "Alert — High Technology / High Risk"},
    "quad_pasif":     {"id": "Pasif — Teknologi Rendah / Risiko Rendah",     "en": "Passive — Low Technology / Low Risk"},
    "ind_wri_desc":     {"id": "Risiko bencana komposit. Tinggi = lebih berisiko.",         "en": "Composite disaster risk. Higher = more at risk."},
    "ind_wri_valid":    {"id": "Diakui UNDRR Sendai Framework. 196 negara.",               "en": "Recognized by UNDRR Sendai Framework. 196 countries."},
    "ind_nri_desc":     {"id": "Kesiapan ekosistem teknologi & jaringan (0-100).",         "en": "Technology & network ecosystem readiness (0-100)."},
    "ind_nri_valid":    {"id": "Dikutip World Economic Forum. Peer-reviewed.",             "en": "Cited by World Economic Forum. Peer-reviewed."},
    "ind_gii_desc":     {"id": "Kapasitas inovasi: R&D, infrastruktur, SDM (0-100).",     "en": "Innovation capacity: R&D, infrastructure, human capital (0-100)."},
    "ind_gii_valid":    {"id": "Publikasi resmi WIPO/PBB. 132 negara.",                   "en": "Official WIPO/UN publication. 132 countries."},
    "ind_gdp_desc":     {"id": "Kekuatan ekonomi per orang. Proksi kapasitas investasi.", "en": "Economic strength per person. Proxy for investment capacity."},
    "ind_gdp_valid":    {"id": "Standar global semua lembaga internasional.",             "en": "Global standard across all international institutions."},
    "ind_inform_desc":  {"id": "Risiko krisis kemanusiaan. Tinggi = lebih rentan.",       "en": "Humanitarian crisis risk. Higher = more vulnerable."},
    "ind_inform_valid": {"id": "Digunakan EU & PBB untuk alokasi bantuan darurat.",       "en": "Used by EU & UN for emergency aid allocation."},
    "fase_mitigasi":      {"id": "Mitigasi",      "en": "Mitigation"},
    "fase_kesiapsiagaan": {"id": "Kesiapsiagaan", "en": "Preparedness"},
    "fase_respons":        {"id": "Respons",       "en": "Response"},
    "fase_pemulihan":      {"id": "Pemulihan",     "en": "Recovery"},
    "fase_mit_desc": {"id": "Kemampuan mengurangi risiko SEBELUM bencana melalui infrastruktur fisik, regulasi, dan program DRR.", "en": "Ability to reduce risk BEFORE a disaster through physical infrastructure, regulations, and DRR programs."},
    "fase_pre_desc": {"id": "Kapasitas sistem monitoring, jaringan komunikasi, dan teknologi peringatan dini.",                   "en": "Capacity of monitoring systems, communication networks, and early warning technology."},
    "fase_res_desc": {"id": "Kemampuan institusi merespons darurat — pengerahan sumber daya dan kapasitas penanggulangan.",        "en": "Institutional ability to respond to emergencies — resource deployment and coping capacity."},
    "fase_rec_desc": {"id": "Kapasitas pemulihan jangka panjang: ekonomi, inovasi, dan modal manusia.",                           "en": "Long-term recovery capacity: economy, innovation, and human capital."},
    "main_title":       {"id": "🌋 Indonesia vs Dunia: Teknologi & Kesiapan Bencana Gunung Berapi", "en": "🌋 Indonesia vs World: Technology & Volcanic Disaster Readiness"},
    "metric_sample":    {"id": "Negara Vulkanik (Sampel)",   "en": "Volcanic Countries (Sample)"},
    "metric_volcanoes": {"id": "Total Gunung Aktif",          "en": "Total Active Volcanoes"},
    "metric_eruptions": {"id": "Total Erupsi 1900-2025",      "en": "Total Eruptions 1900-2025"},
    "metric_wri_indo":  {"id": "World Risk Index Indonesia",  "en": "Indonesia World Risk Index"},
    "metric_eru_indo":  {"id": "Frekuensi Erupsi Indonesia",  "en": "Indonesia Eruption Frequency"},
    "metric_eru_delta": {"id": "Tertinggi di dunia",          "en": "Highest in the world"},
    "tab1_label":  {"id": "1️⃣  Profil Negara",            "en": "1️⃣  Country Profile"},
    "tab2_label":  {"id": "2️⃣  Analisis Kuadran",         "en": "2️⃣  Quadrant Analysis"},
    "tab3_label":  {"id": "3️⃣  Korelasi & Regresi",       "en": "3️⃣  Correlation & Regression"},
    "tab4_label":  {"id": "4️⃣  Head-to-Head Indonesia",   "en": "4️⃣  Head-to-Head Indonesia"},
    "tab5_label":  {"id": "5️⃣  Fase Bencana",             "en": "5️⃣  Disaster Phases"},
    "tab6_label":  {"id": "6️⃣  Peta & Drill-Down Gunung", "en": "6️⃣  Map & Volcano Drill-Down"},
    "tab7_label":  {"id": "7️⃣  Data Lengkap",             "en": "7️⃣  Full Dataset"},
    "t1_subheader":      {"id": "Profil & Peringkat Negara Vulkanik (Smithsonian GVP)",  "en": "Volcanic Country Profiles & Rankings (Smithsonian GVP)"},
    "t1_toggle_wri":     {"id": "Sub-komponen World Risk Index",                         "en": "World Risk Index sub-components"},
    "t1_toggle_nri":     {"id": "Sub-komponen Network Readiness Index",                  "en": "Network Readiness Index sub-components"},
    "t1_toggle_gii":     {"id": "Sub-komponen Global Innovation Index",                  "en": "Global Innovation Index sub-components"},
    "t1_toggle_inform":  {"id": "Sub-komponen INFORM Risk Index",                        "en": "INFORM Risk Index sub-components"},
    "t1_search":         {"id": "🔍 Cari negara:",                                       "en": "🔍 Search country:"},
    "t1_search_hint":    {"id": "contoh: Indonesia",                                     "en": "e.g.: Indonesia"},
    "t1_indicator_lbl":  {"id": "Indikator:",                                            "en": "Indicator:"},
    "t1_topn_lbl":       {"id": "Top N:",                                                "en": "Top N:"},
    "t1_dist_wri_title": {"id": "#### Distribusi Kategori Risiko WRI",                  "en": "#### WRI Risk Category Distribution"},
    "t1_dist_cap_title": {"id": "#### Distribusi Kapasitas Penanggulangan Bencana",     "en": "#### Disaster Coping Capacity Distribution"},
    "t1_see_list":       {"id": "📃 Lihat daftar negara per kategori",                  "en": "📃 View country list by category"},
    "t1_cap_no_data":    {"id": "Kolom Lack of Coping Capacities tidak tersedia.",      "en": "Lack of Coping Capacities column not available."},
    "t1_chart_title":    {"id": "#### Grafik Ringkas — Negara Vulkanik",                "en": "#### Quick Chart — Volcanic Countries"},
    "t2_subheader":      {"id": "Analisis Kuadran: Kapasitas Teknologi vs Risiko Bencana Vulkanik", "en": "Quadrant Analysis: Technology Capacity vs Volcanic Disaster Risk"},
    "t2_method_exp":     {"id": "📐 Metodologi Pembagian Kuadran — Basis Threshold",              "en": "📐 Quadrant Division Methodology — Threshold Basis"},
    "t2_var_y_label":    {"id": "**Variabel Y — Indikator Risiko**",                               "en": "**Variable Y — Risk Indicator**"},
    "t2_var_x_label":    {"id": "**Variabel X — Indikator Independen**",                           "en": "**Variable X — Independent Indicator**"},
    "t2_y_select":       {"id": "Pilih Indikator Risiko:",                                         "en": "Select Risk Indicator:"},
    "t2_x_select":       {"id": "Pilih Variabel X:",                                               "en": "Select Variable X:"},
    "t2_x_caption":      {"id": "💡 NRI/GII/GDP = kapasitas. Sub-indikator INFORM (DRR, Infrastructure, Institutional) juga kapasitas.", "en": "💡 NRI/GII/GDP = capacity. INFORM sub-indicators (DRR, Infrastructure, Institutional) are also capacity."},
    "t2_not_enough":     {"id": "Data tidak cukup.",                                               "en": "Insufficient data."},
    "t2_paradox_title":  {"id": "#### 🔍 Mengapa Indonesia Bisa di Kuadran Ini? — Paradoks Digital Divide", "en": "#### 🔍 Why Is Indonesia in This Quadrant? — Digital Divide Paradox"},
    "t2_gap_preventif":  {"id": "**Gap ke Kuadran Preventif:**",                                   "en": "**Gap to Preventive Quadrant:**"},
    "t2_stat_exp":       {"id": "📊 Statistik per Kuadran — Mean, Median, Min, Max",               "en": "📊 Statistics per Quadrant — Mean, Median, Min, Max"},
    "t2_stat_caption":   {"id": "Median X dan Y pada baris Preventif = target gap Indonesia ke kuadran Preventif.", "en": "Median X and Y for Preventive = Indonesia\'s target gap to the Preventive quadrant."},
    "t3_subheader":      {"id": "Korelasi & Regresi OLS + Heatmap Semua Variabel",     "en": "OLS Regression & Correlation + Full Variable Heatmap"},
    "t3_y_label":        {"id": "**Variabel Y — Indikator Penanggulangan (Dependen)**", "en": "**Variable Y — Coping Indicator (Dependent)**"},
    "t3_x_label":        {"id": "**Variabel X — Indikator Independen**",               "en": "**Variable X — Independent Indicator**"},
    "t3_y_select":       {"id": "Pilih Indikator:",                                    "en": "Select Indicator:"},
    "t3_x_caption":      {"id": "💡 NRI/GII/GDP = indikator kapasitas. Beberapa sub-indikator INFORM juga termasuk kapasitas.", "en": "💡 NRI/GII/GDP = capacity indicators. Some INFORM sub-indicators are also capacity."},
    "t3_corr":           {"id": "Korelasi (r)",         "en": "Correlation (r)"},
    "t3_r2":             {"id": "Determinasi (R²)",     "en": "Determination (R²)"},
    "t3_pval":           {"id": "P-Value",              "en": "P-Value"},
    "t3_slope":          {"id": "Slope (β)",            "en": "Slope (β)"},
    "t3_intercept":      {"id": "Intersep (α)",         "en": "Intercept (α)"},
    "t3_neg_corr":       {"id": "Negatif = terbalik ✅", "en": "Negative = inverse ✅"},
    "t3_pos_corr":       {"id": "Positif = searah",     "en": "Positive = direct"},
    "t3_sig":            {"id": "Signifikan (p<0.05)",  "en": "Significant (p<0.05)"},
    "t3_not_sig":        {"id": "Tidak Signifikan",     "en": "Not Significant"},
    "t3_heatmap_title":  {"id": "#### Heatmap Korelasi Semua Variabel",                "en": "#### Full Variable Correlation Heatmap"},
    "t3_heatmap_caption":{"id": "*** p<0.001 | ** p<0.01 | * p<0.05 | tanpa bintang = tidak signifikan", "en": "*** p<0.001 | ** p<0.01 | * p<0.05 | no star = not significant"},
    "t3_top5":           {"id": "##### 5 Korelasi Terkuat & Signifikan",               "en": "##### 5 Strongest Significant Correlations"},
    "t3_no_enough":      {"id": "Data tidak cukup untuk regresi.",                     "en": "Insufficient data for regression."},
    "t3_median_avg":     {"id": "#### Rata-rata berdasarkan median kapasitas",         "en": "#### Averages by Capacity Median Group"},
    "t3_neg_ideal":      {"id": "Negatif (ideal)", "en": "Negative (ideal)"},
    "t3_positive":       {"id": "Positif",         "en": "Positive"},
    "t3_strong":         {"id": "Kuat",            "en": "Strong"},
    "t3_moderate":       {"id": "Sedang",          "en": "Moderate"},
    "t3_weak":           {"id": "Lemah",           "en": "Weak"},
    "t4_subheader":      {"id": "Head-to-Head: Indonesia vs Negara Benchmark",                    "en": "Head-to-Head: Indonesia vs Benchmark Countries"},
    "t4_select_label":   {"id": "Pilih negara benchmark (dari kuadran Preventif):",               "en": "Select benchmark countries (from Preventive quadrant):"},
    "t4_recommend":      {"id": "**Rekomendasi:** Jepang, Selandia Baru, Islandia, Filipina",   "en": "**Recommended:** Japan, New Zealand, Iceland, Philippines"},
    "t4_radar_title":    {"id": "##### Radar Chart — Profil Multidimensi (6 Indikator Kunci)",   "en": "##### Radar Chart — Multi-Dimensional Profile (6 Key Indicators)"},
    "t4_bar_title":      {"id": "##### Nilai Aktual per Kategori Indikator",                      "en": "##### Actual Values by Indicator Category"},
    "t4_gap_title":      {"id": "##### Tabel Gap Analysis",                                       "en": "##### Gap Analysis Table"},
    "t4_cat_main":       {"id": "📊 Indeks Utama",   "en": "📊 Main Indices"},
    "t4_cat_nri":        {"id": "📡 NRI — Teknologi","en": "📡 NRI — Technology"},
    "t4_cat_gii":        {"id": "💡 GII — Inovasi",  "en": "💡 GII — Innovation"},
    "t4_cat_disaster":   {"id": "🚨 Kesiapan Bencana","en": "🚨 Disaster Readiness"},
    "t5_subheader":      {"id": "Ketangguhan per Fase: Mitigasi → Kesiapsiagaan → Respons → Pemulihan", "en": "Resilience by Phase: Mitigation → Preparedness → Response → Recovery"},
    "t5_select_label":   {"id": "Pilih negara pembanding:",                                          "en": "Select comparison countries:"},
    "t5_summary_title":  {"id": "#### Ringkasan: Profil Ketangguhan per Fase",                      "en": "#### Summary: Resilience Profile by Phase"},
    "t5_quad_title":     {"id": "#### 📊 Ringkasan Rata-rata per Fase Bencana: Kuadran Preventif vs Reaktif", "en": "#### 📊 Average per Disaster Phase: Preventive vs Reactive Quadrant"},
    "t5_no_data":        {"id": "Kolom tidak tersedia.",                                            "en": "Column not available."},
    "t5_no_nri_wri":     {"id": "Kolom NRI Score atau WRI Score tidak tersedia.",                   "en": "NRI Score or WRI Score column unavailable."},
    "t5_fase_sendai":    {"id": "Fase Sendai",   "en": "Sendai Phase"},
    "t5_acuan_sendai":   {"id": "Acuan Sendai",  "en": "Sendai Reference"},
    "t5_gap_col":        {"id": "Gap (Prev - Reak)", "en": "Gap (Prev - React)"},
    "t6_subheader":      {"id": "Peta & Drill-Down Aktivitas Vulkanik per Negara", "en": "Map & Per-Country Volcanic Activity Drill-Down"},
    "t6_select":         {"id": "Pilih Negara:",            "en": "Select Country:"},
    "t6_metric_volc":    {"id": "Jumlah Gunung",            "en": "No. of Volcanoes"},
    "t6_metric_freq":    {"id": "Frekuensi Erupsi 1900-2025","en": "Eruption Frequency 1900-2025"},
    "t6_metric_maxvei":  {"id": "Max VEI",                  "en": "Max VEI"},
    "t6_metric_wri":     {"id": "World Risk Index",         "en": "World Risk Index"},
    "t6_metric_cat":     {"id": "Kategori Risiko",          "en": "Risk Category"},
    "t6_emdat_header":   {"id": "**Dampak Historis — EM-DAT Volcanic Activity**", "en": "**Historical Impact — EM-DAT Volcanic Activity**"},
    "t6_emdat_deaths":   {"id": "Total Korban Jiwa",        "en": "Total Deaths"},
    "t6_emdat_affected": {"id": "Total Terdampak",          "en": "Total Affected"},
    "t6_emdat_events":   {"id": "Jumlah Kejadian",          "en": "Number of Events"},
    "t6_emdat_damage":   {"id": "Total Kerusakan",          "en": "Total Damage"},
    "t6_no_coord":       {"id": "Koordinat tidak tersedia.", "en": "Coordinates not available."},
    "t6_min_vei":        {"id": "Min VEI:",                 "en": "Min VEI:"},
    "t6_year_range":     {"id": "Tahun:",                   "en": "Year:"},
    "t6_no_history":     {"id": "Tidak ada data riwayat erupsi untuk negara ini.", "en": "No eruption history data for this country."},
    "t6_vei_expander":   {"id": "ℹ️ Apa itu VEI (Volcanic Explosivity Index)?",   "en": "ℹ️ What is VEI (Volcanic Explosivity Index)?"},
    "t7_search":         {"id": "Cari Negara:",  "en": "Search Country:"},
    "t7_search_hint":    {"id": "Indonesia",     "en": "Indonesia"},
    "t7_flow_title":     {"id": "#### Alur Seleksi Sampel",        "en": "#### Sample Selection Flow"},
    "t7_metric_pop":     {"id": "Populasi Awal (GVP)",             "en": "Initial Population (GVP)"},
    "t7_metric_excl":    {"id": "Setelah Eksklusi",                "en": "After Exclusion"},
    "t7_metric_sample":  {"id": "Sampel Analitik",                 "en": "Analytical Sample"},
    "t7_excl_delta":     {"id": "−2 (Antartika & Taiwan dieksklusi)", "en": "−2 (Antarctica & Taiwan excluded)"},
    "frek_erupsi_lbl":   {"id": "Frekuensi Erupsi",               "en": "Eruption Frequency"},
    "nilai_tinggi_buruk":{"id": "*(nilai tinggi = kapasitas buruk)*", "en": "*(high value = poor capacity)*"},
    "di_atas_median":    {"id": "Di atas median",                  "en": "Above median"},
    "di_bawah_median":   {"id": "Di bawah median",                 "en": "Below median"},
    "negara_sekuadran":  {"id": "Negara sekuadran",                "en": "Countries in same quadrant"},
    "kategori":          {"id": "Kategori",                        "en": "Category"},
    "jumlah_negara":     {"id": "Jumlah Negara",                   "en": "Number of Countries"},
    "indikator":         {"id": "Indikator",                       "en": "Indicator"},
    "nilai":             {"id": "Nilai",                           "en": "Value"},
    "negara_kol":        {"id": "Negara",                          "en": "Country"},

    # Tab 1 — extra hardcoded strings
    "t1_miss_wri_exp":   {"id": "{n} negara tidak memiliki data World Risk Index",   "en": "{n} countries have no World Risk Index data"},
    "t1_miss_wri_body":  {"id": "Ketiadaan data ini mencerminkan *digital divide* — negara yang tidak terdokumentasi cenderung adalah negara paling tertinggal.", "en": "Absence of data reflects *digital divide* — undocumented countries tend to be the most marginalized."},
    "t1_miss_list":      {"id": "**Daftar:**",                                       "en": "**List:**"},
    "t1_rank_caption":   {"id": "Menampilkan **{n}** negara. Klik nama kolom untuk mengurutkan. Kolom **Rank** = peringkat global (Rank 1 = nilai tertinggi). ⚠️ Untuk kolom **risiko** (WRI Score, INFORM RISK): Rank 1 = risiko TERTINGGI = paling berbahaya. Untuk kolom **kapasitas** (NRI, GII, GDP): Rank 1 = kapasitas TERTINGGI = paling baik. Baris merah muda = Indonesia. Kategori Risiko WRI berdasarkan threshold resmi World Risk Report 2024.",
                          "en": "Showing **{n}** countries. Click a column header to sort. **Rank** column = global ranking (Rank 1 = highest value). ⚠️ For **risk** columns (WRI Score, INFORM RISK): Rank 1 = HIGHEST risk = most dangerous. For **capacity** columns (NRI, GII, GDP): Rank 1 = HIGHEST capacity = best. Pink rows = Indonesia. WRI Risk Category based on official World Risk Report 2024 thresholds."},
    "t1_chart_yaxis":    {"id": "Jumlah Negara",                                    "en": "Number of Countries"},
    "t1_dist_cat_count": {"id": "{n} negara",                                       "en": "{n} countries"},

    # Tab 2 — extra hardcoded strings
    "t2_tab_desc":       {"id": "**Pertanyaan:** Di posisi mana Indonesia dalam peta kapasitas teknologi vs risiko bencana? Sumbu **X (Kapasitas)** mengukur kemampuan teknologi, inovasi, atau ekonomi suatu negara. Sumbu **Y (Risiko)** mengukur seberapa besar risiko bencana (semakin tinggi = semakin rentan). Garis batas = **nilai median** dari sampel negara vulkanik (pendekatan komparatif-relatif). ➡️ *Lanjut ke Tab 3 untuk analisis korelasi & regresi kapasitas vs kemampuan penanggulangan.*",
                          "en": "**Question:** Where does Indonesia stand on the technology capacity vs disaster risk map? The **X-axis (Capacity)** measures a country's technology, innovation, or economic capability. The **Y-axis (Risk)** measures disaster risk (higher = more vulnerable). Dividing lines = **median values** from the volcanic country sample (comparative-relative approach). ➡️ *Continue to Tab 3 for correlation & regression analysis of capacity vs coping ability.*"},
    "t2_quad_table":     {"id": "| Kuadran | Label | Kondisi |\n|---|---|---|\n| **Kapasitas Tinggi / Risiko Rendah** | 🟢 *Preventif* | Teknologi tinggi mampu menekan risiko |\n| **Kapasitas Tinggi / Risiko Tinggi** | 🟠 *Waspada* | Kapasitas ada, tapi beban vulkanik besar |\n| **Kapasitas Rendah / Risiko Tinggi** | 🔴 *Reaktif* | Minim kapasitas + berisiko tinggi = berbahaya |\n| **Kapasitas Rendah / Risiko Rendah** | 🔵 *Pasif* | Beban vulkanik kecil, tapi kapasitas rendah |",
                          "en": "| Quadrant | Label | Condition |\n|---|---|---|\n| **High Capacity / Low Risk** | 🟢 *Preventive* | High technology effectively reduces risk |\n| **High Capacity / High Risk** | 🟠 *Alert* | Capacity exists, but high volcanic burden |\n| **Low Capacity / High Risk** | 🔴 *Reactive* | Minimal capacity + high risk = dangerous |\n| **Low Capacity / Low Risk** | 🔵 *Passive* | Low volcanic burden, but low capacity |"},
    "t2_method_body":    {"id": "**Dasar Penentuan Batas Kuadran: Median Split (Pendekatan Komparatif-Relatif)**\n\nGaris batas pada grafik di bawah ditentukan berdasarkan **nilai median** dari masing-masing indikator yang dipilih, dihitung dari sampel negara vulkanik yang memiliki data lengkap. Artinya, kategori 'Kapasitas Tinggi' atau 'Risiko Rendah' bersifat **relatif terhadap negara vulkanik lainnya**, bukan berdasarkan nilai absolut resmi.\n\n**Mengapa median, bukan mean?**\n- Distribusi indikator seperti GDP per Kapita dan frekuensi erupsi cenderung *right-skewed* (beberapa negara bernilai ekstrem tinggi). Median lebih *robust* terhadap outlier dibanding mean.\n- Teknik median split untuk tipologi komparatif antarnegara lazim digunakan dalam studi pembangunan dan ekonomi komparatif (Porter, 1990; UNDP Human Development Reports).\n\n**Interpretasi yang tepat:** Posisi suatu negara di kuadran ini harus dibaca sebagai *'di atas atau di bawah rata-rata negara vulkanik'*, bukan sebagai penilaian absolut. Negara di kuadran 🔴 **Reaktif** berarti **di bawah median kapasitas DAN di atas median risiko** dibanding seluruh negara vulkanik dalam dataset.\n\n> ⚠️ **Catatan:** Batas kuadran akan bergeser jika indikator X atau Y diganti, karena median dihitung ulang dari negara yang memiliki data pada kedua indikator yang dipilih.",
                          "en": "**Quadrant Boundary Basis: Median Split (Comparative-Relative Approach)**\n\nThe dividing lines in the chart below are set based on the **median** of each selected indicator, calculated from the volcanic country sample that has complete data. Thus, 'High Capacity' or 'Low Risk' categories are **relative to other volcanic countries**, not absolute official values.\n\n**Why median instead of mean?**\n- Distributions of indicators like GDP per capita and eruption frequency tend to be *right-skewed* (some countries have extreme high values). Median is more *robust* to outliers than mean.\n- Median split for comparative country typologies is commonly used in development and comparative economics studies (Porter, 1990; UNDP Human Development Reports).\n\n**Correct interpretation:** A country's position in this quadrant should be read as *'above or below the average volcanic country'*, not as an absolute assessment. A country in the 🔴 **Reactive** quadrant means **below median capacity AND above median risk** compared to all volcanic countries in the dataset.\n\n> ⚠️ **Note:** Quadrant boundaries will shift when the X or Y indicator is changed, because the median is recalculated from countries that have data on both selected indicators."},
    "t2_analysis_cap":   {"id": "Analisis:",                                        "en": "Analysis:"},
    "t2_n_countries":    {"id": "negara",                                            "en": "countries"},
    "t2_scatter_title":  {"id": "Kuadran: {lx} vs {ly}  |  Garis batas = median negara vulkanik", "en": "Quadrant: {lx} vs {ly}  |  Dividing lines = volcanic country median"},
    "t2_country_quadrant":  {"id": "negara",   "en": "countries"},
    "t2_indo_pos":       {"id": "#### Posisi Indonesia:",                            "en": "#### Indonesia's Position:"},
    "t2_same_quad":      {"id": "**Negara sekuadran ({n}):**",                      "en": "**Same-quadrant countries ({n}):**"},
    "t2_paradox_body":   {"id": "💡 Indonesia memiliki **NRI/GII/GDP relatif tinggi** — indikator ekonomi & teknologi menunjukkan kapasitas yang baik. Namun **Lack of Coping Capacities = {lok}** ({kap}) dan frekuensi erupsi tertinggi dunia menunjukkan bahwa **pertumbuhan teknologi belum merata ke sektor penanggulangan bencana**. Inilah inti argumen *digital divide* dalam konteks vulkanik — kesenjangan antara kapasitas teknologi umum vs kesiapan bencana nyata.",
                          "en": "💡 Indonesia has a **relatively high NRI/GII/GDP** — economic & technology indicators show good capacity. However, **Lack of Coping Capacities = {lok}** ({kap}) and the world's highest eruption frequency show that **technology growth has not reached the disaster management sector**. This is the core of the *digital divide* argument in the volcanic context — the gap between general technology capacity and actual disaster readiness."},
    "t2_paradox_interp": {"id": "**Interpretasi Paradoks:**",                       "en": "**Paradox Interpretation:**"},
    "t2_stat_cap":       {"id": "Median X dan Y pada baris Preventif = target gap Indonesia ke kuadran Preventif.", "en": "Median X and Y for Preventive quadrant = Indonesia's target gap to the Preventive quadrant."},
    "t2_nri_label":      {"id": "NRI Score (Teknologi)",      "en": "NRI Score (Technology)"},
    "t2_gii_label":      {"id": "GII Score (Inovasi)",        "en": "GII Score (Innovation)"},
    "t2_gdp_label":      {"id": "GDP per Kapita",             "en": "GDP per Capita"},
    "t2_frek_label":     {"id": "Frekuensi Erupsi",          "en": "Eruption Frequency"},
    "t2_higher_cap":     {"id": "Tinggi = kapasitas buruk ⚠️","en": "High = poor capacity ⚠️"},
    "t2_world_highest":  {"id": "Tertinggi di dunia 🌋",      "en": "Highest in the world 🌋"},
    "t2_not_enough":     {"id": "Data tidak cukup.",           "en": "Insufficient data."},

    # Tab 3 — extra hardcoded strings
    "t3_tab_desc":       {"id": "**Pertanyaan:** Apakah negara dengan kapasitas teknologi dan inovasi lebih tinggi cenderung memiliki kemampuan penanggulangan bencana (*coping capacity*) yang lebih baik? Pilih kombinasi X (kapasitas teknologi) dan Y (indikator penanggulangan) untuk menguji hubungan ini. ➡️ *Lanjut ke Tab 4 untuk mengukur gap Indonesia vs negara di kuadran Preventif.*",
                          "en": "**Question:** Do countries with higher technology and innovation capacity tend to have better disaster coping ability (*coping capacity*)? Select an X (technology capacity) and Y (management indicator) combination to test this relationship. ➡️ *Continue to Tab 4 to measure Indonesia's gap vs countries in the Preventive quadrant.*"},
    "t3_x_select":       {"id": "Pilih Variabel X:",                               "en": "Select Variable X:"},
    "t3_x_caption2":     {"id": "💡 NRI/GII/GDP = indikator kapasitas. Beberapa sub-indikator INFORM (Infrastructure, DRR, Institutional) juga termasuk kapasitas. INFORM RISK/VULNERABILITY = indikator risiko — jika dipilih sebagai X, analisis menjadi risiko vs risiko.",
                          "en": "💡 NRI/GII/GDP = capacity indicators. Some INFORM sub-indicators (Infrastructure, DRR, Institutional) are also capacity. INFORM RISK/VULNERABILITY = risk indicators — if selected as X, the analysis becomes risk vs risk."},
    "t3_n_countries_data": {"id": "negara dengan data lengkap", "en": "countries with complete data"},
    "t3_sub_y":          {"id": "Sub-komponen indeks risiko/penanggulangan.",        "en": "Sub-component of risk/management index."},
    "t3_sub_x_risk":     {"id": "Sub-indikator risiko INFORM (nilai tinggi = lebih rentan).", "en": "INFORM risk sub-indicator (high value = more vulnerable)."},
    "t3_sub_x_cap":      {"id": "Sub-indikator kapasitas.",                         "en": "Capacity sub-indicator."},
    "t3_pct_var":        {"id": "{pct}% variansi dijelaskan",                       "en": "{pct}% variance explained"},
    "t3_ols_formula":    {"id": "**Persamaan Regresi OLS:** Y = {a} {sign} {b} X", "en": "**OLS Regression Equation:** Y = {a} {sign} {b} X"},
    "t3_scatter_label":  {"id": "Regresi OLS: {lx} → {ly}  (n={n} negara)",        "en": "OLS Regression: {lx} → {ly}  (n={n} countries)"},
    "t3_frek_label":     {"id": "Frekuensi Erupsi",                                 "en": "Eruption Frequency"},
    "t3_dot_color":      {"id": "Warna titik = frekuensi erupsi (kuning = sedikit, merah = banyak) | Garis putus-putus = trendline OLS (scipy)",
                          "en": "Dot color = eruption frequency (yellow = few, red = many) | Dashed line = OLS trendline (scipy)"},
    "t3_methodological_note": {"id": "📌 **Catatan Metodologis:** Analisis ini bersifat **asosiatif (korelasional)** dan tidak secara otomatis menyimpulkan hubungan kausalitas antara variabel yang dianalisis. Interpretasi harus dilakukan secara hati-hati, sesuai dengan standar pelaporan risiko global *(UNDRR Sendai Framework, IPCC AR6, Global Risk Report WEF)*. Korelasi yang ditemukan merupakan dasar untuk proposisi penelitian lebih lanjut, bukan klaim sebab-akibat definitif.",
                               "en": "📌 **Methodological Note:** This analysis is **associative (correlational)** and does not automatically imply causality between the analyzed variables. Interpretation must be done carefully, in line with global risk reporting standards *(UNDRR Sendai Framework, IPCC AR6, Global Risk Report WEF)*. Correlations found serve as a basis for further research propositions, not definitive causal claims."},
    "t3_interp_neg":     {"id": "negatif (terbalik)",   "en": "negative (inverse)"},
    "t3_interp_pos":     {"id": "positif (searah)",    "en": "positive (direct)"},
    "t3_interp_strong":  {"id": "kuat",                "en": "strong"},
    "t3_interp_moderate":{"id": "sedang",              "en": "moderate"},
    "t3_interp_weak":    {"id": "lemah",               "en": "weak"},
    "t3_interp_sig":     {"id": "signifikan (p<0.05)",  "en": "significant (p<0.05)"},
    "t3_interp_not_sig": {"id": "belum signifikan (p≥0.05)", "en": "not significant (p≥0.05)"},
    "t3_interp_full":    {"id": "**Interpretasi:** Hubungan **{strength} dan {direction}** (r={r}, R²={r2}, p={p}), **{sig}**. {lx} menjelaskan {pct}% variasi {ly}. *Kriteria kekuatan korelasi: |r|≥0.6 = kuat, 0.4–0.59 = sedang, <0.4 = lemah (Cohen, 1988; Evans, 1996).*",
                          "en": "**Interpretation:** **{strength} and {direction}** relationship (r={r}, R²={r2}, p={p}), **{sig}**. {lx} explains {pct}% of the variation in {ly}. *Correlation strength criteria: |r|≥0.6 = strong, 0.4–0.59 = moderate, <0.4 = weak (Cohen, 1988; Evans, 1996).*"},
    "t3_indo_pos":       {"id": "**Posisi Indonesia:** {lx} = {x_val} → prediksi {ly} = {pred}. Aktual = {actual} ({dir}{gap} dari prediksi).\n\n*{note}*",
                          "en": "**Indonesia's Position:** {lx} = {x_val} → predicted {ly} = {pred}. Actual = {actual} ({dir}{gap} from prediction).\n\n*{note}*"},
    "t3_gap_worse":      {"id": "lebih berisiko +",    "en": "more at risk +"},
    "t3_gap_better":     {"id": "lebih aman ",         "en": "less at risk "},
    "t3_gap_note_high":  {"id": "Faktor lain memperparah risiko Indonesia — beban vulkanik tertinggi dunia ({n} erupsi sejak 1900).",
                          "en": "Other factors worsen Indonesia's risk — world's highest volcanic burden ({n} eruptions since 1900)."},
    "t3_gap_note_low":   {"id": "Indonesia lebih baik dari prediksi model untuk kombinasi ini.", "en": "Indonesia performs better than the model's prediction for this combination."},
    "t3_median_caption": {"id": "Negara dibagi dua kelompok berdasarkan nilai median indikator kapasitas (X): 'Di atas median' vs 'Di bawah median'. Tabel menampilkan rata-rata tiap kelompok — jika kelompok kapasitas tinggi memiliki risiko rata-rata lebih rendah, ini memperkuat argumen korelasi negatif kapasitas–risiko.",
                          "en": "Countries are split into two groups based on the median value of the capacity indicator (X): 'Above median' vs 'Below median'. The table shows the average for each group — if the high-capacity group has a lower average risk, this supports the negative capacity–risk correlation argument."},
    "t3_above_median":   {"id": "Di atas median {lx}",  "en": "Above median {lx}"},
    "t3_below_median":   {"id": "Di bawah median {lx}", "en": "Below median {lx}"},
    "t3_heatmap_desc":   {"id": "Korelasi Pearson: variabel independen (X) — meliputi NRI, GII, GDP, dan sub-indikator INFORM — vs semua indikator risiko WRI (Y). **Merah tua** = negatif kuat (X tinggi → risiko rendah = ideal). **Biru tua** = positif. Bintang = tingkat signifikansi.",
                          "en": "Pearson correlation: independent variables (X) — including NRI, GII, GDP, and INFORM sub-indicators — vs all WRI risk indicators (Y). **Dark red** = strong negative (high X → low risk = ideal). **Dark blue** = positive. Stars = significance level."},
    "t3_heatmap_plot_title": {"id": "Heatmap Korelasi Pearson: Indikator Kapasitas vs Risiko", "en": "Pearson Correlation Heatmap: Capacity vs Risk Indicators"},
    "t3_top5_neg":       {"id": "Negatif (ideal)", "en": "Negative (ideal)"},
    "t3_top5_pos":       {"id": "Positif",          "en": "Positive"},
    "t3_top5_strong":    {"id": "Kuat",             "en": "Strong"},
    "t3_top5_moderate":  {"id": "Sedang",            "en": "Moderate"},
    "t3_top5_weak":      {"id": "Lemah",             "en": "Weak"},
    "t3_not_enough":     {"id": "Data tidak cukup untuk regresi.", "en": "Insufficient data for regression."},

    # Tab 4 — extra hardcoded strings
    "t4_tab_desc":       {"id": "**Pertanyaan:** Seberapa besar gap kapasitas teknologi dan kesiapan bencana vulkanik Indonesia dibanding negara-negara yang sudah siap (kuadran Preventif)? Pilih negara benchmark lalu bandingkan indikator per kategori. ➡️ *Lanjut ke Tab 5 untuk melihat di fase penanggulangan mana Indonesia paling lemah.*",
                          "en": "**Question:** How large is the gap in technology capacity and volcanic disaster readiness between Indonesia and prepared countries (Preventive quadrant)? Select benchmark countries and compare indicators by category. ➡️ *Continue to Tab 5 to see which disaster management phase Indonesia is weakest in.*"},
    "t4_select_min":     {"id": "Pilih minimal 1 negara benchmark.",               "en": "Select at least 1 benchmark country."},
    "t4_radar_caption":  {"id": "**Metodologi Radar:** Setiap indikator dinormalisasi ke skala 0–100% menggunakan min-max scaling berbasis seluruh negara vulkanik dalam dataset (bukan hanya negara yang ditampilkan). WRI Risk & INFORM Risk diinvert (100 − nilai) agar skor tinggi di radar selalu berarti lebih baik. Sumber data: WRI 2024, NRI 2024, GII 2024, World Bank, INFORM 2024.",
                          "en": "**Radar Methodology:** Each indicator is normalized to 0–100% using min-max scaling based on all volcanic countries in the dataset (not just displayed countries). WRI Risk & INFORM Risk are inverted (100 − value) so that higher radar scores always mean better performance. Data sources: WRI 2024, NRI 2024, GII 2024, World Bank, INFORM 2024."},
    "t4_radar_plot_title":{"id": "Radar: Kapasitas & Risiko Indonesia vs Benchmark (0% = terburuk, 100% = terbaik)", "en": "Radar: Indonesia's Capacity & Risk vs Benchmark (0% = worst, 100% = best)"},
    "t4_bar_y":          {"id": "Nilai",              "en": "Value"},
    "t4_gap_caption":    {"id": "**Cara membaca Gap:** Gap = Nilai Indonesia − Nilai Benchmark. 🔴 Gap positif untuk indikator **risiko** (WRI Score, INFORM RISK, Frekuensi Erupsi, Lack of Coping): Indonesia lebih buruk dari benchmark. 🟢 Gap positif untuk indikator **kapasitas** (NRI, GII, GDP): Indonesia lebih baik dari benchmark. Gap negatif = kebalikannya.",
                          "en": "**How to read Gap:** Gap = Indonesia Value − Benchmark Value. 🔴 Positive gap for **risk** indicators (WRI Score, INFORM RISK, Eruption Frequency, Lack of Coping): Indonesia is worse than benchmark. 🟢 Positive gap for **capacity** indicators (NRI, GII, GDP): Indonesia is better than benchmark. Negative gap = the opposite."},
    "t4_gdp_short":      {"id": "GDP/kapita",         "en": "GDP/capita"},

    # Tab 5 — extra hardcoded strings
    "t5_tab_desc":       {"id": "**Pertanyaan yang dijawab:** Di fase mana Indonesia paling lemah? Berdasarkan Sendai Framework UNDRR. ➡️ *Lanjut ke Tab 6 untuk melihat beban vulkanik sebagai konteksnya.*",
                          "en": "**Question answered:** Which phase is Indonesia weakest in? Based on the UNDRR Sendai Framework. ➡️ *Continue to Tab 6 to see the volcanic burden as context.*"},
    "t5_bar_y":          {"id": "Nilai",              "en": "Value"},
    "t5_bar_title":      {"id": "Indikator {fase}",   "en": "{fase} Indicators"},
    "t5_acuan_label":    {"id": "Acuan:",             "en": "Reference:"},
    "t5_insight":        {"id": "**Insight Indonesia — {fase}:** Indikator terlemah: **{col}** = {val}", "en": "**Indonesia Insight — {fase}:** Weakest indicator: **{col}** = {val}"},
    "t5_radar_title":    {"id": "Profil Ketangguhan per Fase — Indonesia vs Benchmark", "en": "Resilience Profile by Phase — Indonesia vs Benchmark"},
    "t5_radar_caption":  {"id": "**Metodologi Radar Ringkasan:** Nilai tiap fase = rata-rata indikator dalam fase tersebut. Indikator INFORM yang berskala **higher=worse** (DRR, Institutional, Communication, Physical Infrastructure, Lack of Coping Capacity, dll.) sudah **diinvert** sebelum dirata-rata, sehingga radar konsisten: **nilai lebih tinggi = lebih tangguh** di fase tersebut. Kemudian dinormalisasi min-max (0–100%) di antara negara yang dipilih — bersifat relatif, bukan absolut. Sumber arah indikator: INFORM Methodology 2024, JRC European Commission (semua output INFORM: higher score = higher risk/lack of capacity).",
                          "en": "**Summary Radar Methodology:** Value per phase = average of indicators within that phase. INFORM indicators scaled **higher=worse** (DRR, Institutional, Communication, Physical Infrastructure, Lack of Coping Capacity, etc.) are **inverted** before averaging, so the radar is consistent: **higher value = more resilient** in that phase. Then min-max normalized (0–100%) among selected countries — relative, not absolute. Indicator direction source: INFORM Methodology 2024, JRC European Commission (all INFORM outputs: higher score = higher risk/lack of capacity)."},
    "t5_quad_desc":      {"id": "Tabel ini membandingkan **rata-rata nilai ternormalisasi (0–1)** tiap fase Sendai antara negara-negara di kuadran **Preventif** (Teknologi Tinggi / Risiko Rendah) dan **Reaktif** (Teknologi Rendah / Risiko Tinggi), berdasarkan median split NRI Score vs WRI Score. Dihitung dari **sampel n={n} negara**. Nilai 1.0 = terbaik, 0.0 = terburuk.",
                          "en": "This table compares the **average normalized values (0–1)** per Sendai phase between countries in the **Preventive** (High Technology / Low Risk) and **Reactive** (Low Technology / High Risk) quadrants, based on NRI Score vs WRI Score median split. Calculated from **sample n={n} countries**. Value 1.0 = best, 0.0 = worst."},
    "t5_quad_table_cap": {"id": "**Cara membaca tabel:** Nilai 0.0–1.0 = hasil normalisasi min-max dari seluruh {n} negara sampel. Kolom INFORM yang berskala *higher = worse* (DRR, Institutional, Communication, dll.) sudah **diinvert** sebelum normalisasi sehingga **nilai lebih tinggi selalu berarti lebih tangguh**. Kuadran: NRI ≥ {med_nri} & WRI < {med_wri} → Preventif ({n_prev} negara); NRI < {med_nri} & WRI ≥ {med_wri} → Reaktif ({n_reak} negara).",
                          "en": "**How to read the table:** Values 0.0–1.0 = min-max normalization across all {n} sample countries. INFORM columns scaled *higher = worse* (DRR, Institutional, Communication, etc.) are **inverted** before normalization so **higher value always means more resilient**. Quadrant: NRI ≥ {med_nri} & WRI < {med_wri} → Preventive ({n_prev} countries); NRI < {med_nri} & WRI ≥ {med_wri} → Reactive ({n_reak} countries)."},
    "t5_insight_quad":   {"id": "**Insight:** Kesenjangan terbesar antara kuadran Preventif dan Reaktif terjadi pada fase **{fase}** dengan selisih rata-rata sebesar **{gap}** poin (skala 0–1). Ini mengindikasikan bahwa negara-negara dengan kapasitas teknologi tinggi memiliki keunggulan paling signifikan pada fase tersebut.",
                          "en": "**Insight:** The largest gap between Preventive and Reactive quadrants occurs in the **{fase}** phase with an average difference of **{gap}** points (scale 0–1). This indicates that countries with high technology capacity have the most significant advantage in this phase."},
    "t5_gap_bench_title": {"id": "📊 Gap Indonesia vs Benchmark per Fase (Skala 0–1)",           "en": "📊 Indonesia vs Benchmark Gap per Phase (Scale 0–1)"},
    "t5_gap_bench_col_fase":{"id": "Fase",                                                        "en": "Phase"},
    "t5_gap_bench_col_indo":{"id": "Skor Indonesia",                                              "en": "Indonesia Score"},
    "t5_gap_bench_col_avg": {"id": "Rata-rata Benchmark",                                        "en": "Benchmark Average"},
    "t5_gap_bench_col_gap": {"id": "Gap",                                                         "en": "Gap"},
    "t5_gap_bench_caption": {"id": "Radar chart di atas menunjukkan perbandingan visual relatif antara Indonesia dan negara benchmark yang dipilih. Tabel ini melengkapinya dengan angka gap yang lebih akurat: normalisasi dilakukan terhadap seluruh {n} negara sampel analitik (bukan hanya negara yang ditampilkan), sehingga skor Indonesia mencerminkan posisinya yang sesungguhnya di antara semua negara vulkanik — bukan sekadar relatif terhadap benchmark. Gap = rata-rata skor benchmark − skor Indonesia. 🔴 Gap positif = Indonesia tertinggal. 🟢 Gap negatif = Indonesia lebih baik.",
                              "en": "The radar chart above shows a relative visual comparison between Indonesia and the selected benchmark countries. This table complements it with more accurate gap figures: normalization is performed against all {n} analytical sample countries (not just displayed ones), so Indonesia's score reflects its true position among all volcanic countries — not merely relative to the benchmark. Gap = benchmark average score − Indonesia score. 🔴 Positive gap = Indonesia lags behind. 🟢 Negative gap = Indonesia performs better."},
    "t5_gap_bench_no_bench":{"id": "Pilih minimal satu negara benchmark untuk melihat tabel gap.", "en": "Select at least one benchmark country to view the gap table."},
    "t5_gap_bench_no_indo": {"id": "Data Indonesia tidak tersedia.",                              "en": "Indonesia data not available."},

    # Tab 6 — extra hardcoded strings
    "t6_tab_desc":       {"id": "**Pertanyaan yang dijawab:** Seberapa besar beban vulkanik tiap negara? Indonesia = **{erupsi} erupsi** sejak 1900 = frekuensi tertinggi dunia (Rank #{rank} dari {total} negara vulkanik). Ini menjelaskan mengapa gap di Tab 4 & 5 sangat krusial.",
                          "en": "**Question answered:** How heavy is each country's volcanic burden? Indonesia = **{erupsi} eruptions** since 1900 = world's highest frequency (Rank #{rank} of {total} volcanic countries). This explains why the gaps in Tab 4 & 5 are crucial."},
    "t6_emdat_caption":  {"id": "Sumber: EM-DAT — CRED, Université Catholique de Louvain. Cakupan data: kejadian bencana vulkanik yang tercatat sejak 1900. Negara dengan nilai 0 berarti tidak ada kejadian yang terdokumentasi di EM-DAT, bukan berarti tidak ada korban.",
                          "en": "Source: EM-DAT — CRED, Université Catholique de Louvain. Data coverage: volcanic disaster events recorded since 1900. Countries with value 0 mean no events documented in EM-DAT, not that there were no casualties."},
    "t6_emdat_damage":   {"id": "Total Kerusakan",    "en": "Total Damage"},
    "t6_damage_unit":    {"id": "ribu USD",           "en": "thousand USD"},
    "t6_map_title":      {"id": "🌋 {country} — Distribusi Gunung Berapi  |  Ukuran & warna = frekuensi erupsi", "en": "🌋 {country} — Volcano Distribution  |  Size & color = eruption frequency"},
    "t6_freq_erupsi":    {"id": "Freq. Erupsi",       "en": "Eruption Freq."},
    "t6_history_header": {"id": "#### Riwayat Erupsi {country} (1900–2025)", "en": "#### Eruption History of {country} (1900–2025)"},
    "t6_download_btn":   {"id": "⬇️ Download CSV Erupsi {country}",         "en": "⬇️ Download Eruption CSV for {country}"},
    "t6_tl_title":       {"id": "Timeline Erupsi — {country}",              "en": "Eruption Timeline — {country}"},
    "t6_vei_body":       {"id": "**VEI** adalah skala untuk mengukur besarnya letusan gunung berapi, dikembangkan oleh Newhall & Self (1982). Skala 0–8 bersifat **logaritmik** (setiap naik 1 = 10× lebih kuat).\n\n| VEI | Kategori | Contoh |\n|---|---|---|\n| 0–1 | Efusif / Sangat Kecil | Kilauea, Hawaii |\n| 2–3 | Kecil – Sedang | Sinabung 2010 |\n| 4 | Besar | Merapi 2010 |\n| 5 | Sangat Besar | Pinatubo 1991 |\n| 6 | Kolosal | Krakatau 1883 |\n| 7 | Super-kolosal | Tambora 1815 |\n| 8 | Mega-kolosal | Toba ~74.000 tahun lalu |\n\n*Sumber: Newhall & Self (1982), Smithsonian GVP*",
                          "en": "**VEI** (Volcanic Explosivity Index) is a scale to measure the magnitude of a volcanic eruption, developed by Newhall & Self (1982). The 0–8 scale is **logarithmic** (each step up = 10× stronger).\n\n| VEI | Category | Example |\n|---|---|---|\n| 0–1 | Effusive / Very Small | Kilauea, Hawaii |\n| 2–3 | Small – Moderate | Sinabung 2010 |\n| 4 | Large | Merapi 2010 |\n| 5 | Very Large | Pinatubo 1991 |\n| 6 | Colossal | Krakatau 1883 |\n| 7 | Super-Colossal | Tambora 1815 |\n| 8 | Mega-Colossal | Toba ~74,000 years ago |\n\n*Source: Newhall & Self (1982), Smithsonian GVP*"},

    # Tab 7 — extra hardcoded strings
    "t7_subheader":      {"id": "Dataset Master — Populasi {n} Negara Vulkanik",   "en": "Master Dataset — Population of {n} Volcanic Countries"},
    "t7_desc":           {"id": "Tabel ini menampilkan **populasi penuh {n_full} negara vulkanik** (setelah eksklusi Antartika & Taiwan dari 77 negara awal Smithsonian GVP). Dari populasi ini, **{n_sample} negara** memenuhi syarat kelengkapan data di 4 indikator utama model OLS (*listwise deletion*) dan menjadi **sampel analitik** penelitian. 🟠 **Baris oranye = {n_excl} negara yang dieksklusi** akibat data tidak lengkap (memiliki NaN di WRI Score, NRI Score, GDP per Kapita, atau INFORM RISK).",
                          "en": "This table shows the **full population of {n_full} volcanic countries** (after excluding Antarctica & Taiwan from the initial 77 Smithsonian GVP countries). From this population, **{n_sample} countries** meet the data completeness requirement for the 4 main OLS model indicators (*listwise deletion*) and form the **analytical sample**. 🟠 **Orange rows = {n_excl} excluded countries** due to incomplete data (missing WRI Score, NRI Score, GDP per Capita, or INFORM RISK)."},
    "t7_download_btn":   {"id": "⬇️ Download CSV ({n} Negara)",                  "en": "⬇️ Download CSV ({n} Countries)"},
    "t7_table_cap":      {"id": "Menampilkan **{n_show}** dari **{n_full}** negara (populasi). 🟠 Oranye = **{n_excl} negara dieksklusi** dari sampel analitik karena data tidak lengkap di ≥1 indikator utama OLS (WRI, NRI, GDP, INFORM). ✅ Putih = **{n_sample} negara sampel analitik** yang digunakan dalam analisis korelasi & kuadran.",
                          "en": "Showing **{n_show}** of **{n_full}** countries (population). 🟠 Orange = **{n_excl} excluded countries** from the analytical sample due to incomplete data in ≥1 main OLS indicators (WRI, NRI, GDP, INFORM). ✅ White = **{n_sample} analytical sample countries** used in correlation & quadrant analysis."},
    "t7_flow_pop_delta": {"id": "Smithsonian GVP — semua negara dengan gunung aktif", "en": "Smithsonian GVP — all countries with active volcanoes"},
    "t7_excl_listwise":  {"id": "−{n} (Listwise Deletion — data tidak lengkap)",   "en": "−{n} (Listwise Deletion — incomplete data)"},
    "t7_stat_header":    {"id": "#### Statistik Deskriptif (Sampel Analitik — {n} Negara)", "en": "#### Descriptive Statistics (Analytical Sample — {n} Countries)"},
    "t7_stat_caption":   {"id": "Statistik deskriptif di bawah dihitung dari {n} negara sampel analitik, bukan dari {n_full} negara populasi.",
                          "en": "Descriptive statistics below are calculated from {n} analytical sample countries, not from {n_full} population countries."},
    "t7_country_label":  {"id": "negara",              "en": "countries"},

    # Header
    "header_pop":        {"id": "Populasi",            "en": "Population"},
    "header_sample":     {"id": "Sampel Analitik",    "en": "Analytical Sample"},
    "header_eru":        {"id": "erupsi",              "en": "eruptions"},
    "header_gun":        {"id": "gunung aktif",        "en": "active volcanoes"},
    "header_nego_vulk":  {"id": "negara vulkanik",     "en": "volcanic countries"},
    "header_negara":     {"id": "negara",              "en": "countries"},
    "header_dari":       {"id": "dari",                "en": "of"},
    "header_metric1_val":{"id": "{n} dari {total}",   "en": "{n} of {total}"},
    "header_desc":       {"id": "{pop}: **{n_volk} negara vulkanik** (Smithsonian GVP) → {sample}: **{n_sample} negara** (Listwise Deletion) | **{n_eru} erupsi** (1900–2025) | **{n_gun} gunung aktif**",
                          "en": "{pop}: **{n_volk} volcanic countries** (Smithsonian GVP) → {sample}: **{n_sample} countries** (Listwise Deletion) | **{n_eru} eruptions** (1900–2025) | **{n_gun} active volcanoes**"},
    "metric_eru_unit":   {"id": "erupsi",              "en": "eruptions"},
    "t1_count_caption":  {"id": "Menampilkan",         "en": "Showing"},
}

def _lang():
    """Ambil kode bahasa aktif dari session state. Default: 'id' (Indonesia)."""
    return st.session_state.get("lang", "id")

def T(key, **kwargs):
    """
    Fungsi terjemahan utama.
    Mengambil teks dari _TRANS berdasarkan key dan bahasa aktif.
    kwargs digunakan untuk mengisi placeholder format string, misal: T('t7_desc', n=55).
    """
    lang = _lang()
    entry = _TRANS.get(key, {})
    text = entry.get(lang, entry.get("id", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    return text

# ================================================================
# KONSTANTA & KONFIGURASI GLOBAL
# EXCEL_FILE : nama file sumber data master (satu file Excel, banyak sheet)
# Fungsi _wri_kat_color, _quad_color, _kap_color, dll. dibangun
# secara dinamis agar label warna ikut berubah saat bahasa diganti.
# ================================================================
EXCEL_FILE = "Master Data Skripsi.xlsx"  # File Excel master berisi semua sheet data

# Kategori risiko resmi WRI (World Risk Report)
# WRI_KATEGORI_COLOR keys built dynamically so they follow language toggle
def _wri_kat_color():
    return {
        T("wri_very_high"): "#d62728",
        T("wri_high"):      "#ff7f0e",
        T("wri_medium"):    "#f5c542",
        T("wri_low"):       "#2ca02c",
        T("wri_very_low"):  "#1f77b4",
    }
WRI_KATEGORI_COLOR = _wri_kat_color()

def _quad_color():
    return {
        T("quad_preventif"): "#2ca02c",
        T("quad_reaktif"):   "#d62728",
        T("quad_waspada"):   "#ff7f0e",
        T("quad_pasif"):     "#1f77b4",
    }
QUAD_COLOR = _quad_color()

# Threshold resmi World Risk Report 2024 — Lack of Coping Capacities
def _kap_color():
    return {
        T("cap_very_high"): "#1f77b4",
        T("cap_high"):      "#2ca02c",
        T("cap_medium"):    "#f5c542",
        T("cap_low"):       "#ff7f0e",
        T("cap_very_low"):  "#d62728",
    }
KAPASITAS_COLOR = _kap_color()

def _indikator_info():
    return {
        "World Risk Index":        ("Bündnis Entwicklung Hilft, Jerman",    T("ind_wri_desc"),    T("ind_wri_valid")),
        "Network Readiness Index": ("Portulans Institute, Washington D.C.", T("ind_nri_desc"),    T("ind_nri_valid")),
        "Global Innovation Index": ("WIPO & Cornell University (PBB)",      T("ind_gii_desc"),    T("ind_gii_valid")),
        "GDP per Kapita":          ("World Bank",                            T("ind_gdp_desc"),    T("ind_gdp_valid")),
        "INFORM Risk Index":       ("European Commission JRC & OCHA PBB",   T("ind_inform_desc"), T("ind_inform_valid")),
    }
INDIKATOR_INFO = _indikator_info()

def _fase_bencana():
    return {
        T("fase_mitigasi"): {
            "icon": "🛡️",
            "deskripsi": T("fase_mit_desc"),
            "kolom": ["DRR", "Physical infrastructure", "INFORM - Infrastructure", "GII - Infrastructure"],
            "acuan": "Sendai Framework Priority 1: Understanding Disaster Risk"
        },
        T("fase_kesiapsiagaan"): {
            "icon": "📡",
            "deskripsi": T("fase_pre_desc"),
            "kolom": ["Communication", "Technology Pillar", "NRI Score", "People Pillar"],
            "acuan": "Sendai Framework Priority 4: Enhancing Disaster Preparedness"
        },
        T("fase_respons"): {
            "icon": "🚨",
            "deskripsi": T("fase_res_desc"),
            "kolom": ["Institutional", "LACK OF COPING CAPACITY", "Governance Pillar"],
            "acuan": "Sendai Framework Priority 2: Strengthening Disaster Risk Governance"
        },
        T("fase_pemulihan"): {
            "icon": "🔄",
            "deskripsi": T("fase_rec_desc"),
            "kolom": ["GDP Per Capita 2024", "Human capital and research", "GII Score", "Knowledge and technology outputs"],
            "acuan": "Sendai Framework Priority 3: Investing in DRR for Resilience"
        }
    }
FASE_BENCANA = _fase_bencana()

def _label_panjang():
    lang = _lang()
    return {
        "Jumlah_Gunung":                    "No. of Volcanoes" if lang=="en" else "Jumlah Gunung",
        "Frekuensi_Erupsi":                 "Eruption Frequency (1900-2025)" if lang=="en" else "Frekuensi Erupsi (1900-2025)",
        "Max_VEI":                          "Max VEI",
        "Avg_VEI":                          "Average VEI" if lang=="en" else "Rata-rata VEI",
        "GDP Per Capita 2024":              "GDP per Capita (USD)" if lang=="en" else "GDP per Kapita (USD)",
        "WRI Score":                        "World Risk Index",
        "NRI Score":                        "Network Readiness Index",
        "GII Score":                        "Global Innovation Index",
        "INFORM RISK":                      "INFORM Risk Index",
        "Exposure":                         "WRI — Exposure",
        "Vulnerability":                    "WRI — Vulnerability",
        "Susceptibility":                   "WRI — Susceptibility",
        "Lack of Coping Capacities":        "WRI — Lack of Coping Capacities",
        "Lack of Adaptive Capacities":      "WRI — Lack of Adaptive Capacities",
        "Technology Pillar":                "NRI — Technology Pillar",
        "People Pillar":                    "NRI — People Pillar",
        "Governance Pillar":                "NRI — Governance Pillar",
        "Impact Pillar":                    "NRI — Impact Pillar",
        "Institutions":                     "GII — Institutions",
        "Human capital and research":       "GII — Human Capital & Research",
        "GII - Infrastructure":             "GII — Infrastructure",
        "Market sophistication":            "GII — Market Sophistication",
        "Business sophistication":          "GII — Business Sophistication",
        "Knowledge and technology outputs": "GII — Knowledge & Technology Outputs",
        "Creative outputs":                 "GII — Creative Outputs",
        "LACK OF COPING CAPACITY":          "INFORM — Lack of Coping Capacity",
        "INFORM - Infrastructure":          "INFORM — Infrastructure",
        "Communication":                    "INFORM — Communication",
        "Physical infrastructure":          "INFORM — Physical Infrastructure",
        "DRR":                              "INFORM — DRR",
        "Institutional":                    "INFORM — Institutional",
        "VULNERABILITY":                    "INFORM — Vulnerability",
        "HAZARD & EXPOSURE":                "INFORM — Hazard & Exposure",
        "EMDAT_Total_Deaths":               "EM-DAT — Total Deaths" if lang=="en" else "EM-DAT — Total Korban Jiwa",
        "EMDAT_Total_Affected":             "EM-DAT — Total Affected" if lang=="en" else "EM-DAT — Total Terdampak",
        "EMDAT_Events":                     "EM-DAT — Number of Events" if lang=="en" else "EM-DAT — Jumlah Kejadian",
        "EMDAT_Total_Damage_USD":           "EM-DAT — Total Damage (thousand USD)" if lang=="en" else "EM-DAT — Total Kerusakan (ribu USD)",
    }
LABEL_PANJANG = _label_panjang()


# ================================================================
# LOAD & PREPROCESSING DATA
# Fungsi load_all_data() membaca semua sheet Excel, membersihkan
# nama negara (country name normalization), melakukan merge antar
# dataset, lalu mengembalikan:
#   master      → sampel analitik (setelah listwise deletion)
#   master_full → populasi penuh (sebelum listwise deletion)
#   df_jml      → jumlah gunung per negara
#   df_gun      → daftar gunung berapi (Smithsonian GVP)
#   df_hist     → riwayat erupsi per gunung
# Menggunakan @st.cache_data agar data hanya dimuat sekali (efisiensi).
# ================================================================
@st.cache_data
def load_all_data():
    xls = pd.ExcelFile(EXCEL_FILE)  # Buka file Excel sekali, baca banyak sheet dari sini

    # ── Sheet 1: Daftar gunung berapi (Smithsonian GVP) ──
    df_gun = pd.read_excel(xls, 'Data Daftar Gunung')
    # Volcano Number dikonversi ke string bulat (hapus desimal) agar bisa di-merge dengan df_hist
    df_gun['Volcano Number'] = df_gun['Volcano Number'].astype(str).str.split('.').str[0].str.strip()

    # ── Sheet 2: Riwayat erupsi (GVP Historical Eruptions) ──
    df_hist = pd.read_excel(xls, 'Data History Erupsi')
    df_hist['Volcano Number'] = df_hist['Volcano Number'].astype(str).str.strip()
    df_hist['Start Year'] = pd.to_numeric(df_hist['Start Year'], errors='coerce')  # Paksa numerik
    df_hist = df_hist[df_hist['Start Year'] >= 1900].copy()  # Filter: hanya erupsi sejak tahun 1900
    df_hist['VEI'] = pd.to_numeric(df_hist['VEI'], errors='coerce')  # VEI = Volcanic Explosivity Index

    # ── Sheet 3: Jumlah gunung per negara (agregasi dari GVP) ──
    df_jml = pd.read_excel(xls, 'Data Jumlah Negara Gunung Berap').rename(
        columns={'Jumlah Gunung Berapi': 'Jumlah_Gunung'})  # Rename agar konsisten

    # ── Normalisasi nama negara: perbaiki nama yang tidak standar di dataset GVP ──
    country_name_map = {
        'Russia': 'Russian Federation', 'South Korea': 'Republic of Korea',
        'Turkiye': 'Turkey', 'Burma (Myanmar)': 'Myanmar',
        'DR Congo': 'Democratic Republic of the Congo',
        'Union of the Comoros': 'Comoros', 'Cabo Verde': 'Cape Verde',
    }
    # Entri yang dieksklusi: lintas-batas (dua negara) & fitur bawah laut
    exclude_entries = {
        'Armenia-Azerbaijan', 'Chile-Argentina', 'Chile-Bolivia', 'China-North Korea',
        'Colombia-Ecuador', 'DR Congo-Rwanda', 'Eritrea-Djibouti', 'Ethiopia-Djibouti',
        'Ethiopia-Eritrea', 'Ethiopia-Eritrea-Djibouti', 'France - claimed by Vanuatu',
        'Guatemala-El Salvador', 'Japan - administered by Russia', 'Mexico-Guatemala',
        'Syria-Jordan-Saudi Arabia', 'Undersea Features', 'Antarctica'
    }
    # Terapkan normalisasi: entry eksklusif → None (akan di-drop saat merge)
    df_gun['Country_clean'] = df_gun['Country'].apply(
        lambda x: country_name_map.get(x, x) if x not in exclude_entries else None)

    # ── Agregasi statistik erupsi per negara dari riwayat erupsi 1900–2025 ──
    m_hist = df_hist.merge(
        df_gun[['Volcano Number', 'Country_clean']].dropna(subset=['Country_clean']),
        on='Volcano Number', how='left')  # Join riwayat erupsi dengan nama negara bersih
    stat = m_hist.groupby('Country_clean').agg(
        Frekuensi_Erupsi=('Start Year', 'count'),  # Hitung jumlah kejadian erupsi
        Max_VEI=('VEI', 'max'),                     # Maksimum VEI yang pernah tercatat
        Avg_VEI=('VEI', 'mean')                     # Rata-rata VEI
    ).reset_index().rename(columns={'Country_clean': 'Negara'})

    df_wri = pd.read_excel(xls, 'Data World Risk Index 2024')
    # Rename 'Infrastructure' di WRI sebelum merge agar tidak bentrok dengan GII/INFORM
    if 'Infrastructure' in df_wri.columns:
        df_wri = df_wri.rename(columns={'Infrastructure': 'WRI - Infrastructure'})
    df_nri = pd.read_excel(xls, 'Data Network Readiness Index 20')
    df_gii = pd.read_excel(xls, 'Data Global Innovation Index 20')
    # Rename kolom 'Infrastructure' di GII sebelum merge
    if 'Infrastructure' in df_gii.columns:
        df_gii = df_gii.rename(columns={'Infrastructure': 'GII - Infrastructure'})

    df_gdp = pd.read_excel(xls, 'Data GDP Per Capita 2024').rename(columns={'Country Name': 'Negara'})
    # Noise filter: exclude aggregate/regional rows — use exact or safe substrings only
    # Avoid filtering real countries (South Africa, Saudi Arabia, Syrian Arab Republic, etc.)
    noise_exact = {
        'World', 'Kosovo', 'Euro area', 'IBRD only', 'IDA only', 'IDA & IBRD total',
        'IDA blend', 'IDA total', 'Not classified',
    }
    noise_partial = [
        'income', ' Asia', 'Europe', 'America', 'Caribbean', 'Pacific',
        'dividend', 'Heavily', 'Least developed', 'small states',
        'Sub-Saharan', 'Middle East', 'Central Europe', 'South Asia',
        'East Asia', 'Latin America', 'OECD members', 'Post-demographic',
        'Pre-demographic', 'Late-demographic', 'Early-demographic',
        'Fragile and conflict', 'Heavily indebted',
    ]
    df_gdp = df_gdp[~df_gdp['Negara'].apply(
        lambda x: str(x).strip() in noise_exact or
                  any(n in str(x) for n in noise_partial))].copy()

    # Normalize GDP country names to match volcanic country list
    gdp_name_map = {
        'Cabo Verde':                        'Cape Verde',
        'Congo, Dem. Rep.':                  'Democratic Republic of the Congo',
        "Korea, Dem. People's Rep.":         "Dem. People's Republic of Korea",
        'Korea, Rep.':                       'Republic of Korea',
        'Iran, Islamic Rep.':                'Iran',
        'St. Kitts and Nevis':               'Saint Kitts and Nevis',
        'St. Lucia':                         'Saint Lucia',
        'St. Vincent and the Grenadines':    'Saint Vincent and the Grenadines',
        'Turkiye':                           'Turkey',
        'Viet Nam':                          'Vietnam',
        'Yemen, Rep.':                       'Yemen',
        'Syrian Arab Republic':              'Syrian Arab Republic',  # kept, noise fix above
        'South Africa':                      'South Africa',          # kept, noise fix above
        'Saudi Arabia':                      'Saudi Arabia',          # kept, noise fix above
    }
    df_gdp['Negara'] = df_gdp['Negara'].map(lambda x: gdp_name_map.get(str(x).strip(), str(x).strip()))

    df_inf = pd.read_excel(xls, 'Inform Risk Index 2024').rename(columns={'COUNTRY': 'Negara'})
    inform_name_map = {
        'Cabo Verde':               'Cape Verde',
        'Congo':                    'Democratic Republic of the Congo',
        'Korea DPR':                "Dem. People's Republic of Korea",
        'Korea Republic of':        'Republic of Korea',
        'Syria':                    'Syrian Arab Republic',
        'United States of America': 'United States',
        'Viet Nam':                 'Vietnam',
    }
    df_inf['Negara'] = df_inf['Negara'].map(lambda x: inform_name_map.get(str(x).strip(), str(x).strip()))
    # Rename Infrastructure di INFORM sebelum merge agar tidak bentrok dengan WRI/GII
    if 'Infrastructure' in df_inf.columns:
        df_inf = df_inf.rename(columns={'Infrastructure': 'INFORM - Infrastructure'})
    inform_wanted = ['Negara', 'INFORM RISK', 'LACK OF COPING CAPACITY', 'INFORM - Infrastructure',
                     'Communication', 'Physical infrastructure', 'DRR', 'Institutional',
                     'VULNERABILITY', 'HAZARD & EXPOSURE']
    inform_wanted = [c for c in inform_wanted if c in df_inf.columns]
    df_inf = df_inf[inform_wanted].copy()
    for c in df_inf.columns:
        if c != 'Negara':
            df_inf[c] = pd.to_numeric(df_inf[c].astype(str).str.replace(',', '.'), errors='coerce')

    # ── Fungsi helper: merge antar dataset menggunakan nama negara lowercase sebagai kunci ──
    # Tujuan: menghindari mismatch kapitalisasi (misal 'Indonesia' vs 'indonesia')
    def merge_neg(left, right):
        left = left.copy(); right = right.copy()
        left['_k'] = left['Negara'].str.lower().str.strip()   # Key kiri: lowercase nama negara
        right['_k'] = right['Negara'].str.lower().str.strip() # Key kanan: sama
        right = right.drop(columns=['Negara'], errors='ignore')
        return left.merge(right, on='_k', how='left').drop(columns=['_k'])  # Left join: semua negara kiri tetap ada

    # Eksklusi Antarctica dan Taiwan dari daftar negara vulkanik:
    # - Antarctica: 19 gunung di dataset GVP, tapi bukan subjek penelitian komparatif
    # - Taiwan: status politik disputed, tidak ada di WRI/NRI/GII/GDP/INFORM
    EXCLUDE_NEGARA = {'Antarctica', 'Taiwan'}
    master = df_jml[~df_jml['Negara'].isin(EXCLUDE_NEGARA)].copy()
    master = master.reset_index(drop=True)
    master = merge_neg(master, stat)
    master = merge_neg(master, df_wri)
    master = merge_neg(master, df_nri)
    master = merge_neg(master, df_gii)
    master = merge_neg(master, df_gdp[['Negara', 'GDP Per Capita 2024']])
    master = merge_neg(master, df_inf)

    # Load EM-DAT Volcano Activity
    df_emdat = pd.read_excel(xls, 'Em-Dat Volcano Activity')
    # Cari kolom 'Country' (case-insensitive) untuk robustness
    emdat_country_col = next((c for c in df_emdat.columns if c.strip().lower() == 'country'), 'Country')
    df_emdat = df_emdat.rename(columns={emdat_country_col: 'Country'})
    # Normalisasi nama negara EM-DAT agar match dengan master
    emdat_name_map = {
        'United States of America':           'United States',
        'Viet Nam':                           'Vietnam',
        'Cabo Verde':                         'Cape Verde',       # match Cape Verde di master
        'Bolivia (Plurinational State of)':   'Bolivia',          # match Bolivia di master
        'Congo, Dem. Rep.':                   'Democratic Republic of the Congo',
        'Korea, Rep.':                        'Republic of Korea',
        "Korea, Dem. People's Rep.":          "Dem. People's Republic of Korea",
        'Turkiye':                            'Turkey',
        'Syrian Arab Republic':               'Syrian Arab Republic',
        'Iran, Islamic Rep.':                 'Iran',
    }
    df_emdat['Country'] = df_emdat['Country'].map(
        lambda x: emdat_name_map.get(str(x).strip(), str(x).strip()))
    # Cek keberadaan kolom kerusakan (nama bisa bervariasi antar versi EM-DAT)
    damage_col = next(
        (c for c in df_emdat.columns if 'damage' in c.lower() and 'adjust' in c.lower()), None)
    agg_dict = {
        'EMDAT_Total_Deaths':    ('Total Deaths',   'sum'),
        'EMDAT_Total_Affected':  ('Total Affected', 'sum'),
        'EMDAT_Events':          ('DisNo.',          'count'),
    }
    if damage_col:
        agg_dict['EMDAT_Total_Damage_USD'] = (damage_col, 'sum')
    emdat_agg = df_emdat.groupby('Country').agg(**agg_dict).reset_index().rename(
        columns={'Country': 'Negara'})
    if 'EMDAT_Total_Damage_USD' not in emdat_agg.columns:
        emdat_agg['EMDAT_Total_Damage_USD'] = 0
    master = merge_neg(master, emdat_agg)
    for c in ['EMDAT_Total_Deaths', 'EMDAT_Total_Affected', 'EMDAT_Events', 'EMDAT_Total_Damage_USD']:
        if c in master.columns:
            master[c] = pd.to_numeric(master[c], errors='coerce').fillna(0).astype(int)

    # Setelah rename sebelum merge, kolom _x/_y tidak akan muncul lagi.
    # Guard ini untuk antisipasi sisa konflik nama yang mungkin masih ada.
    if 'Infrastructure_x' in master.columns:
        master = master.rename(columns={'Infrastructure_x': 'GII - Infrastructure'})
    if 'Infrastructure_y' in master.columns:
        master = master.rename(columns={'Infrastructure_y': 'INFORM - Infrastructure'})
    # Bersihkan kolom WRI - Infrastructure (sub-komponen WRI, tidak dipakai di visualisasi)
    # Tidak perlu dibuang, biarkan ada sebagai referensi

    # Filter: hanya negara yang BENAR-BENAR memiliki gunung berapi aktif (Jumlah_Gunung > 0)
    master = master[master['Jumlah_Gunung'] > 0].copy()
    master['Frekuensi_Erupsi'] = master['Frekuensi_Erupsi'].fillna(0).astype(int)  # Negara tanpa erupsi = 0
    master['Max_VEI'] = pd.to_numeric(master['Max_VEI'], errors='coerce')
    master['Avg_VEI'] = pd.to_numeric(master['Avg_VEI'], errors='coerce').round(2)

    # Konversi semua kolom (kecuali Negara) ke numerik untuk memastikan kompatibilitas statistik
    for c in master.columns:
        if c != 'Negara':
            master[c] = pd.to_numeric(master[c], errors='coerce')

    # Kategori risiko — stored as internal key matching _TRANS (language-neutral)
    # Threshold resmi World Risk Report 2024 (Tabel hlm. 10):
    # Very Low 0.00–1.84 | Low 1.85–3.20 | Medium 3.21–5.87 | High 5.88–12.88 | Very High 12.89–100
    def wri_kategori(v):
        if pd.isna(v): return "wri_no_data"
        if v > 12.88:  return "wri_very_high"
        if v >  5.87:  return "wri_high"
        if v >  3.20:  return "wri_medium"
        if v >  1.84:  return "wri_low"
        return                "wri_very_low"
    master['Kategori Risiko WRI'] = master['WRI Score'].apply(wri_kategori)

    # Kategori kapasitas — stored as internal key matching _TRANS (language-neutral)
    def kapasitas_bencana(v):
        if pd.isna(v):  return "data_no"
        if v <= 3.47:   return "cap_very_high"
        if v <= 10.01:  return "cap_high"
        if v <= 12.64:  return "cap_medium"
        if v <= 39.05:  return "cap_low"
        return                 "cap_very_low"
    master['Kategori Kapasitas'] = master['Lack of Coping Capacities'].apply(kapasitas_bencana)

    # Hitung kelengkapan data per negara sebagai persentase dari 5 kolom kunci
    key_cols = [c for c in ['WRI Score', 'NRI Score',
                             'GDP Per Capita 2024', 'INFORM RISK', 'Frekuensi_Erupsi']
                if c in master.columns]
    master['Kelengkapan_Data (%)'] = (
        master[key_cols].notna().sum(axis=1) / len(key_cols) * 100  # Proporsi kolom terisi
    ).round(0).astype(int)

    # ── LISTWISE DELETION GLOBAL (sinkron dengan metodologi skripsi — 4 variabel OLS) ──
    # Hanya negara yang memiliki data LENGKAP di keempat kolom ini yang
    # masuk sampel analitik. Metode ini disebut Listwise Deletion.
    # GII Score TIDAK masuk ANALYTIC_COLS karena tidak ada di persamaan OLS final (Tabel 4.2).
    # GII tetap di-merge dan tersedia untuk visualisasi, tapi tidak jadi syarat listwise.
    ANALYTIC_COLS = ['WRI Score', 'NRI Score', 'GDP Per Capita 2024', 'INFORM RISK']
    # Simpan salinan SEBELUM listwise deletion (populasi setelah
    # eksklusi Antartika & Taiwan) untuk keperluan Tab 7 (Master Data)
    master_full = master.copy()  # Populasi: 75 negara (sebelum hapus NaN)
    master = master.dropna(subset=ANALYTIC_COLS).copy()  # Sampel: negara dengan data lengkap
    # ────────────────────────────────────────────────────────────────────────

    return master, master_full, df_jml, df_gun, df_hist


try:
    # Panggil fungsi load_all_data dan simpan hasilnya ke variabel global
    master, master_full, df_jml, df_gun, df_hist = load_all_data()
except FileNotFoundError:
    # Jika file Excel tidak ditemukan, tampilkan error dan hentikan eksekusi
    st.error(f"File `{EXCEL_FILE}` tidak ditemukan. Pastikan ada di folder yang sama dengan app.py.")
    st.stop()

# Cek apakah 'Indonesia' ada di data — jika tidak (error data), INDO = None untuk mencegah crash
INDO = "Indonesia" if "Indonesia" in master['Negara'].values else None

# Rebuild language-dependent constants (called after lang toggle too)
def _rebuild_lang_constants():
    global WRI_KATEGORI_COLOR, QUAD_COLOR, KAPASITAS_COLOR, INDIKATOR_INFO, FASE_BENCANA, LABEL_PANJANG
    global WRI_KEY_TO_LABEL, CAP_KEY_TO_LABEL
    WRI_KATEGORI_COLOR = _wri_kat_color()
    QUAD_COLOR         = _quad_color()
    KAPASITAS_COLOR    = _kap_color()
    INDIKATOR_INFO     = _indikator_info()
    FASE_BENCANA       = _fase_bencana()
    LABEL_PANJANG      = _label_panjang()
    # Internal key → display label (changes with language)
    WRI_KEY_TO_LABEL = {
        "wri_very_high": T("wri_very_high"),
        "wri_high":      T("wri_high"),
        "wri_medium":    T("wri_medium"),
        "wri_low":       T("wri_low"),
        "wri_very_low":  T("wri_very_low"),
        "wri_no_data":   T("wri_no_data"),
    }
    CAP_KEY_TO_LABEL = {
        "cap_very_high": T("cap_very_high"),
        "cap_high":      T("cap_high"),
        "cap_medium":    T("cap_medium"),
        "cap_low":       T("cap_low"),
        "cap_very_low":  T("cap_very_low"),
        "data_no":       T("wri_no_data"),
    }

WRI_KEY_TO_LABEL: dict = {}
CAP_KEY_TO_LABEL: dict = {}
_rebuild_lang_constants()  # populate all language-dependent dicts on first load

WRI_COLS    = [c for c in ['WRI Score', 'Exposure', 'Vulnerability', 'Susceptibility',
                            'Lack of Coping Capacities', 'Lack of Adaptive Capacities',
                            'INFORM RISK'] if c in master.columns]
NRI_COLS    = [c for c in ['NRI Score', 'Technology Pillar', 'People Pillar',
                            'Governance Pillar', 'Impact Pillar'] if c in master.columns]
GII_COLS    = [c for c in ['GII Score', 'Institutions', 'Human capital and research',
                            'GII - Infrastructure', 'Market sophistication', 'Business sophistication',
                            'Knowledge and technology outputs', 'Creative outputs'] if c in master.columns]
INFORM_COLS = [c for c in ['INFORM RISK', 'LACK OF COPING CAPACITY', 'INFORM - Infrastructure',
                            'Communication', 'Physical infrastructure', 'DRR', 'Institutional',
                            'VULNERABILITY', 'HAZARD & EXPOSURE'] if c in master.columns]
VOL_COLS    = [c for c in ['Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI', 'Avg_VEI'] if c in master.columns]
ALL_X_COLS  = [c for c in dict.fromkeys(NRI_COLS + GII_COLS + ['GDP Per Capita 2024'] + INFORM_COLS)
               if c in master.columns and master[c].notna().sum() >= 5]

# Kolom numerik Tab 1 (dengan ranking)
RANK_COLS = [c for c in ['Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI',
                          'WRI Score', 'NRI Score', 'GII Score',
                          'GDP Per Capita 2024', 'INFORM RISK'] if c in master.columns]

# Sub-komponen
SUB_WRI    = [c for c in ['Exposure', 'Vulnerability', 'Susceptibility',
                           'Lack of Coping Capacities', 'Lack of Adaptive Capacities'] if c in master.columns]
SUB_NRI    = [c for c in ['Technology Pillar', 'People Pillar', 'Governance Pillar', 'Impact Pillar'] if c in master.columns]
SUB_GII    = [c for c in ['Institutions', 'Human capital and research', 'GII - Infrastructure',
                           'Market sophistication', 'Business sophistication',
                           'Knowledge and technology outputs', 'Creative outputs'] if c in master.columns]
SUB_INFORM = [c for c in ['LACK OF COPING CAPACITY', 'INFORM - Infrastructure', 'Communication',
                           'Physical infrastructure', 'DRR', 'Institutional',
                           'VULNERABILITY', 'HAZARD & EXPOSURE'] if c in master.columns]


def build_ranking_table(df, extra_cols=None):
    """
    Bangun tabel dengan kolom ranking di sebelah kiri tiap kolom numerik.
    Ranking 1 = nilai tertinggi untuk semua kolom.
    Format: Negara | Rank(Jumlah Gunung) | Jumlah Gunung | Rank(Frekuensi) | Frekuensi | ...
    """
    cols_to_rank = list(RANK_COLS)
    if extra_cols:
        cols_to_rank += [c for c in extra_cols if c in df.columns]

    result = df[['Negara', 'Kategori Risiko WRI']].copy()
    for col in cols_to_rank:
        if col not in df.columns:
            continue
        rank_col = f"Rank ({LABEL_PANJANG.get(col, col)[:20]})"
        result[rank_col] = df[col].rank(ascending=False, method='min', na_option='bottom').astype(int)
        result[LABEL_PANJANG.get(col, col)] = df[col].round(2)

    return result


# ================================================================
# SIDEBAR (Panel Kiri)
# Berisi: tombol ganti bahasa, ringkasan alur analisis,
# legenda kategori WRI & kapasitas, info validitas indikator,
# dan daftar sumber data resmi.
# ================================================================
with st.sidebar:
    # ── Inisialisasi bahasa default = Indonesia jika belum ada di session state ──
    if "lang" not in st.session_state:
        st.session_state["lang"] = "id"

    # ── Tombol ganti bahasa (Indonesia / English) — dua kolom sejajar ──
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        # Jika tombol Indonesia diklik: set lang='id', rebuild semua label, reload halaman
        if st.button("🇮🇩 Indonesia", use_container_width=True,
                     type="primary" if _lang()=="id" else "secondary"):
            st.session_state["lang"] = "id"
            _rebuild_lang_constants()  # Update semua dict label agar ikut bahasa baru
            st.rerun()                 # Reload halaman agar semua teks berubah
    with lang_col2:
        # Jika tombol English diklik: set lang='en', rebuild label, reload
        if st.button("🇬🇧 English", use_container_width=True,
                     type="primary" if _lang()=="en" else "secondary"):
            st.session_state["lang"] = "en"
            _rebuild_lang_constants()
            st.rerun()

    st.markdown("---")
    st.title(f"🌋 {T('sidebar_title')}")
    st.markdown(f"**{T('sidebar_subtitle')}**")
    st.markdown("---")

    # ── Ringkasan alur analisis: Tab 1 → Tab 2 → ... → Tab 7 ──
    st.markdown(T("sidebar_flow"))
    st.markdown(
        T("tab1_sidebar") + "\n\n" +
        T("tab2_sidebar") + "\n\n" +
        T("tab3_sidebar") + "\n\n" +
        T("tab4_sidebar") + "\n\n" +
        T("tab5_sidebar") + "\n\n" +
        T("tab6_sidebar") + "\n\n" +
        T("tab7_sidebar")
    )
    st.markdown("---")

    # ── Legenda Kategori Risiko WRI ──
    # Threshold resmi World Risk Report 2024 (hlm. 10)
    st.markdown(T("sidebar_wri_legend"))
    st.markdown(T("sidebar_wri_thresh"))
    st.caption(T("sidebar_wri_dir"))  # Catatan: nilai tinggi = risiko tinggi
    _wkc = _wri_kat_color()  # Dict: label kategori → kode warna hex
    _wri_sidebar_thresh = {
        T("wri_very_high"): "12.89–100.00",  # Sangat Tinggi
        T("wri_high"):      "5.88–12.88",    # Tinggi
        T("wri_medium"):    "3.21–5.87",     # Sedang
        T("wri_low"):       "1.85–3.20",     # Rendah
        T("wri_very_low"):  "0.00–1.84",     # Sangat Rendah
    }
    # Tampilkan tiap kategori dengan warna dan range threshold-nya
    for kat, col in _wkc.items():
        _th = _wri_sidebar_thresh.get(kat, "")
        st.markdown(f"<span style='color:{col}'>■</span> **{kat}** <small style='color:#888'>({_th})</small>", unsafe_allow_html=True)
    st.caption(T("sidebar_wri_source"))
    st.markdown("---")

    # ── Legenda Kapasitas Penanggulangan (dari WRI — Lack of Coping Capacities) ──
    # CATATAN: nilai RENDAH = kapasitas BAIK (skala terbalik dari WRI Score)
    st.markdown(T("sidebar_cap_legend"))
    st.markdown(T("sidebar_cap_thresh"))
    st.caption(T("sidebar_cap_dir"))  # Catatan: nilai kecil = kapasitas baik
    _kpc = _kap_color()  # Dict: label kapasitas → kode warna hex
    _cap_sidebar_thresh = {
        T("cap_very_high"): "0.00–3.47",     # Kapasitas Sangat Tinggi (terbaik)
        T("cap_high"):      "3.48–10.01",    # Kapasitas Tinggi
        T("cap_medium"):    "10.02–12.64",   # Kapasitas Sedang
        T("cap_low"):       "12.65–39.05",   # Kapasitas Rendah
        T("cap_very_low"):  "39.06–100.00",  # Kapasitas Sangat Rendah (terburuk)
    }
    for kat, col in _kpc.items():
        _th = _cap_sidebar_thresh.get(kat, "")
        st.markdown(f"<span style='color:{col}'>■</span> **{kat}** <small style='color:#888'>({_th})</small>", unsafe_allow_html=True)
    st.caption(T("sidebar_cap_desc"))
    st.markdown("---")

    # ── Info Validitas per Indikator (expander per indikator) ──
    st.markdown(T("sidebar_validity"))
    _ii = _indikator_info()  # Dict: nama indikator → (pembuat, deskripsi, validitas)
    for nama, (pembuat, ukur, valid) in _ii.items():
        with st.expander(f"**{nama}**"):  # Klik untuk buka detail tiap indikator
            st.markdown(f"{T('sidebar_pembuat')} {pembuat}\n\n{T('sidebar_mengukur')} {ukur}\n\n{T('sidebar_validitas')} {valid}")
    st.markdown("---")

    # ── Daftar Sumber Data Resmi (dengan hyperlink) ──
    st.markdown(T("sidebar_sources"))
    st.markdown(
        "- [World Risk Index](https://weltrisikobericht.de/en/)\n"
        "- [Network Readiness Index](https://networkreadinessindex.org/)\n"
        "- [Global Innovation Index](https://www.globalinnovationindex.org/)\n"
        "- [World Bank GDP](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)\n"
        "- [INFORM Risk Index](https://drmkc.jrc.ec.europa.eu/inform-index)\n"
        "- [Smithsonian GVP](https://volcano.si.edu/)\n"
        "- [EM-DAT — CRED](https://www.emdat.be/)"
    )


# ================================================================
# HEADER UTAMA
# Menampilkan judul besar, deskripsi singkat populasi & sampel,
# dan 5 metrik ringkasan (kartu angka kunci di bagian atas halaman).
# ================================================================
st.title(T("main_title"))  # Judul besar halaman dashboard

# Baris deskripsi singkat: populasi (GVP) → sampel analitik, total erupsi & gunung
st.markdown(
    T("header_desc",
      pop=T("header_pop"), sample=T("header_sample"),
      n_volk=len(df_jml),          # Jumlah negara vulkanik (populasi GVP)
      n_sample=len(master),        # Jumlah sampel analitik (setelah listwise deletion)
      n_eru=f"{int(master['Frekuensi_Erupsi'].sum()):,}",  # Total erupsi 1900–2025
      n_gun=f"{int(master['Jumlah_Gunung'].sum()):,}"      # Total gunung aktif
    )
)

# ── 5 Kartu Metrik Ringkasan di bagian atas halaman ──
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric(T("metric_sample"), T("header_metric1_val", n=len(master), total=len(df_jml)))  # Negara sampel/populasi
m2.metric(T("metric_volcanoes"), f"{int(master['Jumlah_Gunung'].sum()):,}")               # Total gunung aktif
m3.metric(T("metric_eruptions"), f"{int(master['Frekuensi_Erupsi'].sum()):,}")            # Total erupsi
if INDO:
    irow = master[master['Negara'] == INDO].iloc[0]  # Ambil baris data Indonesia
    # Hitung ranking WRI Indonesia di antara semua negara vulkanik
    rank_wri = int(master['WRI Score'].rank(ascending=False).loc[master['Negara'] == INDO].values[0]) if pd.notna(irow.get('WRI Score')) else None
    # Metrik WRI Score Indonesia + rankingnya (delta_color='inverse': merah = buruk)
    m4.metric(T("metric_wri_indo"), f"{irow['WRI Score']:.2f}" if pd.notna(irow.get('WRI Score')) else "N/A",
              delta=f"Rank {rank_wri}/{master['WRI Score'].notna().sum()} — {WRI_KEY_TO_LABEL.get(irow['Kategori Risiko WRI'], irow['Kategori Risiko WRI'])}" if rank_wri else None,
              delta_color="inverse")
    # Metrik frekuensi erupsi Indonesia (tertinggi dunia)
    m5.metric(T("metric_eru_indo"), f"{int(irow['Frekuensi_Erupsi'])} {T('metric_eru_unit')}",
              delta=T("metric_eru_delta"), delta_color="inverse")

st.markdown("---")


# ================================================================
# TABS — 7 TAB ANALISIS
# Tab 1: Profil & peringkat negara vulkanik
# Tab 2: Analisis kuadran kapasitas-risiko (Pemetaan Makro)
# Tab 3: Korelasi & regresi OLS (Analisis Mikro)
# Tab 4: Head-to-head Indonesia vs negara benchmark
# Tab 5: Ketangguhan per fase bencana (Sendai Framework)
# Tab 6: Peta & drill-down aktivitas vulkanik
# Tab 7: Data lengkap & unduh
# ================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    T("tab1_label"), T("tab2_label"), T("tab3_label"), T("tab4_label"),
    T("tab5_label"), T("tab6_label"), T("tab7_label"),
])


# ════════════════════════════════════
# TAB 1 — PROFIL NEGARA
# Menampilkan tabel ranking semua negara vulkanik dengan indikator
# utama (WRI, NRI, GII, GDP, INFORM), grafik bar top-N, serta
# distribusi kategori risiko WRI dan kapasitas penanggulangan.
# ════════════════════════════════════
with tab1:
    st.subheader(T("t1_subheader"))
    if _lang() == "id":
        st.markdown("**Pertanyaan:** Bagaimana posisi Indonesia dibanding negara vulkanik lain dari sisi risiko bencana, kapasitas teknologi, dan beban vulkanik?")
        _b1_id = f"- Tabel menampilkan **{len(master)} negara sampel analitik** — hasil *listwise deletion* dari {len(master_full)} negara vulkanik. Hanya negara dengan data lengkap di 4 indikator OLS utama yang diikutkan: **WRI Score, NRI Score, GDP per Kapita, INFORM Risk**."
        st.markdown(
            _b1_id + "\n"
            "- Tiap kolom numerik dilengkapi kolom **Rank** — Rank 1 = nilai tertinggi di antara semua negara vulkanik.\n"
            "- Kategori Risiko WRI menggunakan threshold resmi *World Risk Report 2024*.\n"
            "- Negara yang ditampilkan **hanya negara yang memiliki gunung berapi aktif** berdasarkan data Smithsonian GVP.\n\n"
            "➡️ *Lanjut ke Tab 2 untuk melihat peta posisi Indonesia dalam kuadran kapasitas–risiko vulkanik.*"
        )
    else:
        st.markdown("**Question:** How does Indonesia compare to other volcanic countries in terms of disaster risk, technology capacity, and volcanic burden?")
        _b1_en = f"- Table shows **{len(master)} analytical sample countries** — result of *listwise deletion* from {len(master_full)} volcanic countries. Only countries with complete data on all 4 main OLS indicators are included: **WRI Score, NRI Score, GDP per Capita, INFORM Risk**."
        st.markdown(
            _b1_en + "\n"
            "- Each numeric column includes a **Rank** column — Rank 1 = highest value among all volcanic countries.\n"
            "- WRI Risk Category uses official *World Risk Report 2024* thresholds.\n"
            "- **Only countries with active volcanoes** are shown, based on Smithsonian GVP data.\n\n"
            "➡️ *Continue to Tab 2 to see Indonesia's position on the capacity–risk quadrant map.*"
        )

    # ── Toggle tampilkan sub-komponen indeks di tabel ──
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1: show_sub_wri    = st.toggle(T("t1_toggle_wri"),    value=False)  # Sub-komponen WRI
    with col_t2: show_sub_nri    = st.toggle(T("t1_toggle_nri"),    value=False)  # Sub-komponen NRI
    with col_t3: show_sub_inform = st.toggle(T("t1_toggle_inform"), value=False)  # Sub-komponen INFORM

    # Kumpulkan kolom extra yang perlu ditampilkan berdasarkan toggle
    extra = []
    if show_sub_wri:    extra += SUB_WRI     # Tambah kolom Exposure, Vulnerability, dll.
    if show_sub_nri:    extra += SUB_NRI     # Tambah kolom Technology Pillar, People Pillar, dll.
    if show_sub_inform: extra += SUB_INFORM  # Tambah kolom DRR, Institutional, dll.

    # ── Filter pencarian negara ──
    srch1 = st.text_input(T("t1_search"), placeholder=T("t1_search_hint"), key="srch1")
    df_tbl = master.copy()  # Mulai dari sampel analitik penuh
    if srch1:  # Jika ada input pencarian, filter baris yang mengandung teks tersebut
        df_tbl = df_tbl[df_tbl['Negara'].str.contains(srch1, case=False, na=False)]

    # Bangun tabel ranking: tiap kolom numerik diberi kolom Rank di sebelah kirinya
    df_display = build_ranking_table(df_tbl, extra_cols=extra)

    # Fungsi highlight: warnai baris Indonesia dengan latar merah muda
    def highlight_indo(row):
        if row['Negara'] == INDO:
            return ['background-color: rgba(214,39,40,0.08); font-weight: 500'] * len(row)
        return [''] * len(row)

    # Tampilkan tabel interaktif dengan highlight Indonesia
    st.dataframe(
        df_display.style.apply(highlight_indo, axis=1),
        use_container_width=True,
        hide_index=True,
        height=450
    )
    st.caption(T("t1_rank_caption", n=len(df_tbl)))  # Catatan cara baca tabel

    # ── Peringatan: negara yang tidak memiliki data WRI Score ──
    n_miss = master['WRI Score'].isna().sum()  # Hitung negara tanpa data WRI
    if n_miss > 0:
        miss_names = sorted(master[master['WRI Score'].isna()]['Negara'].tolist())
        with st.expander(f"⚠️ {T('t1_miss_wri_exp', n=n_miss)}"):  # Daftar negara tanpa data
            st.markdown(
                f"{T('t1_miss_wri_body')}\n\n"
                f"{T('t1_miss_list')} {', '.join(miss_names)}"
            )

    # ── Grafik Bar: Top-N negara berdasarkan indikator pilihan ──
    st.markdown("---")
    st.markdown(T("t1_chart_title"))
    # Daftar indikator yang tersedia untuk dipilih di bar chart
    bar_opts = [c for c in ['WRI Score', 'Frekuensi_Erupsi', 'Jumlah_Gunung', 'NRI Score',
                             'GII Score', 'GDP Per Capita 2024', 'INFORM RISK', 'Max_VEI',
                             'EMDAT_Total_Deaths', 'EMDAT_Total_Affected',
                             'EMDAT_Events', 'EMDAT_Total_Damage_USD']
                if c in master.columns]
    bar_col1, bar_col2 = st.columns([3, 1])
    with bar_col1:
        # Dropdown pilih indikator (label panjang yang ramah pengguna)
        bar_sel = st.selectbox(T("t1_indicator_lbl"), bar_opts,
                               format_func=lambda x: LABEL_PANJANG.get(x, x), key="bar_sel")
    with bar_col2:
        # Slider pilih jumlah negara (Top N) — default 25
        n_top = st.slider(T("t1_topn_lbl"), min_value=10, max_value=len(master), value=25, step=5, key="n_top")

    # Ambil Top-N negara, urutkan descending, warna merah=Indonesia, biru=lainnya
    df_bar_top = master.dropna(subset=[bar_sel]).sort_values(bar_sel, ascending=False).head(n_top).copy()
    df_bar_top['_color'] = df_bar_top['Negara'].apply(lambda x: '#d62728' if x == INDO else '#4C72B0')

    # Buat bar chart horizontal (orientasi 'h') menggunakan Plotly Graph Objects
    fig_bar = go.Figure(go.Bar(
        x=df_bar_top[bar_sel], y=df_bar_top['Negara'], orientation='h',  # Horizontal bar
        marker_color=df_bar_top['_color'],                                 # Warna tiap bar
        hovertemplate='<b>%{y}</b><br>' + LABEL_PANJANG.get(bar_sel, bar_sel) + ': %{x:.2f}<extra></extra>'
    ))
    fig_bar.update_layout(
        title=f"Top {n_top} — {LABEL_PANJANG.get(bar_sel, bar_sel)}",
        yaxis=dict(autorange='reversed'),  # Nilai tertinggi tampil di atas
        plot_bgcolor="white",
        height=max(400, n_top * 22),       # Tinggi grafik adaptif
        margin=dict(l=0, r=20, t=50, b=10),
        xaxis_title=LABEL_PANJANG.get(bar_sel, bar_sel), yaxis_title=""
    )
    fig_bar.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
    # Jika Indonesia masuk Top-N, tambahkan label penanda ◀ Indonesia
    if INDO and INDO in df_bar_top['Negara'].values:
        iv = df_bar_top.loc[df_bar_top['Negara'] == INDO, bar_sel].values[0]
        fig_bar.add_annotation(x=iv, y=INDO, text=" ◀ Indonesia", showarrow=False,
                               font=dict(color="#d62728", size=11), xanchor="left", yanchor="middle")
    st.plotly_chart(fig_bar, use_container_width=True)


    # Distribusi Kategori Risiko WRI + Kapasitas Penanggulangan — side by side
    st.markdown("---")
    dc1, dc2 = st.columns(2)

    def chart_distribusi(data_col, key_to_label, color_map, title, caption_txt,
                         threshold_map=None, dir_note=None):
        """Helper: buat bar chart distribusi + expander daftar negara per kategori.
        data_col berisi internal key (misal 'wri_very_high'); key_to_label memetakan
        key → label terjemahan saat ini; color_map memetakan label → warna.
        threshold_map: dict internal_key → string threshold (opsional)."""
        # Internal keys yang berarti "tidak ada data"
        _no_data_keys = {"wri_no_data", "data_no"}
        master_valid = master[~master[data_col].isin(_no_data_keys)].copy()
        # Terjemahkan internal key ke label bahasa aktif
        master_valid = master_valid.copy()
        master_valid['_label'] = master_valid[data_col].map(key_to_label).fillna(master_valid[data_col])
        # Buat peta: label → internal key (untuk lookup threshold)
        label_to_key = {v: k for k, v in key_to_label.items()}
        n_valid = len(master_valid)
        dist = master_valid['_label'].value_counts().reset_index()
        dist.columns = ['Kategori', 'Jumlah']
        order = list(color_map.keys())
        dist['order'] = dist['Kategori'].map({k: i for i, k in enumerate(order)})
        dist = dist.dropna(subset=['order']).sort_values('order')
        # Ganti angka negara di title dengan n_valid
        title_fixed = re.sub(r'\d+ (Negara|Countries)', T('t1_dist_cat_count', n=n_valid), title)
        _yaxis_lbl = T("t1_chart_yaxis")
        fig = px.bar(dist, x='Kategori', y='Jumlah',
                     color='Kategori', color_discrete_map=color_map,
                     title=title_fixed, height=320)
        fig.update_layout(plot_bgcolor="white", showlegend=False,
                          xaxis_title="", yaxis_title=_yaxis_lbl)
        fig.update_xaxes(showgrid=False, tickangle=-15)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
        st.caption(caption_txt)
        st.plotly_chart(fig, use_container_width=True)
        # Daftar negara per kategori
        with st.expander(T("t1_see_list")):
            if dir_note:
                st.caption(dir_note)
            for kat in order:
                negara_list = sorted(master_valid[master_valid['_label'] == kat]['Negara'].dropna().tolist())
                if negara_list:
                    # Tampilkan threshold jika tersedia
                    _int_key = label_to_key.get(kat, "")
                    _thresh = threshold_map.get(_int_key, "") if threshold_map else ""
                    _thresh_str = f" — *{_thresh}*" if _thresh else ""
                    st.markdown(f"**{kat}**{_thresh_str} ({T('t1_dist_cat_count', n=len(negara_list))}):")
                    st.markdown(", ".join(negara_list))

    with dc1:
        st.markdown(T("t1_dist_wri_title"))
        n_wri = master['WRI Score'].notna().sum()
        _wri_dist_title = (f"Distribusi {n_wri} Negara Vulkanik — Kategori Risiko WRI"
                           if _lang() == "id" else
                           f"Distribution of {n_wri} Volcanic Countries — WRI Risk Category")
        _wri_dist_cap = ("Threshold WRI Score: Sangat Rendah (0.00–1.84) | Rendah (1.85–3.20) | Sedang (3.21–5.87) | Tinggi (5.88–12.88) | Sangat Tinggi (12.89–100.00)"
                         if _lang() == "id" else
                         "WRI Score Threshold: Very Low (0.00–1.84) | Low (1.85–3.20) | Medium (3.21–5.87) | High (5.88–12.88) | Very High (12.89–100.00)")
        _wri_thresh_map = {
            "wri_very_high": "WRI 12.89–100.00",
            "wri_high":      "WRI 5.88–12.88",
            "wri_medium":    "WRI 3.21–5.87",
            "wri_low":       "WRI 1.85–3.20",
            "wri_very_low":  "WRI 0.00–1.84",
        }
        _wri_dir_note = ("\u2191 Semakin besar WRI Score = semakin tinggi risiko bencana. Sumber threshold: World Risk Report 2024."
                         if _lang() == "id" else
                         "\u2191 Higher WRI Score = higher disaster risk. Threshold source: World Risk Report 2024.")
        chart_distribusi('Kategori Risiko WRI', WRI_KEY_TO_LABEL, WRI_KATEGORI_COLOR,
                         _wri_dist_title, _wri_dist_cap, threshold_map=_wri_thresh_map,
                         dir_note=_wri_dir_note)
        if INDO:
            indo_key = master.loc[master['Negara'] == INDO, 'Kategori Risiko WRI'].values[0]
            indo_kat = WRI_KEY_TO_LABEL.get(indo_key, indo_key)
            st.info(f"🇮🇩 Indonesia: **{indo_kat}** (WRI Score = {irow['WRI Score']:.2f})")

    with dc2:
        st.markdown(T("t1_dist_cap_title"))
        if 'Kategori Kapasitas' in master.columns:
            n_kap = master['Lack of Coping Capacities'].notna().sum()
            _cap_dist_title = (f"Distribusi {n_kap} Negara — Kapasitas Penanggulangan"
                               if _lang() == "id" else
                               f"Distribution of {n_kap} Countries — Coping Capacity")
            _cap_dist_cap = ("Threshold Lack of Coping Capacities (WRI): 0–3.47 | 3.48–10.01 | 10.02–12.64 | 12.65–39.05 | >39.05"
                             if _lang() == "id" else
                             "WRI Lack of Coping Capacities Threshold: 0–3.47 | 3.48–10.01 | 10.02–12.64 | 12.65–39.05 | >39.05")
            _cap_thresh_map = {
                "cap_very_high": "0.00–3.47",
                "cap_high":      "3.48–10.01",
                "cap_medium":    "10.02–12.64",
                "cap_low":       "12.65–39.05",
                "cap_very_low":  "39.06–100.00",
            }
            _cap_dir_note = ("\u2193 Nilai yang digunakan adalah Lack of Coping Capacities: semakin kecil nilainya = semakin baik kapasitas penanggulangan. Sumber threshold: World Risk Report 2024."
                             if _lang() == "id" else
                             "\u2193 The value used is Lack of Coping Capacities: lower value = better coping capacity. Threshold source: World Risk Report 2024.")
            chart_distribusi('Kategori Kapasitas', CAP_KEY_TO_LABEL, KAPASITAS_COLOR,
                             _cap_dist_title, _cap_dist_cap, threshold_map=_cap_thresh_map,
                             dir_note=_cap_dir_note)
            if INDO:
                indo_cap_key = master.loc[master['Negara'] == INDO, 'Kategori Kapasitas'].values[0]
                indo_kap = CAP_KEY_TO_LABEL.get(indo_cap_key, indo_cap_key)
                lok_val  = master.loc[master['Negara'] == INDO, 'Lack of Coping Capacities'].values[0]
                st.info(f"🇮🇩 Indonesia: **{indo_kap}** (Lack of Coping Capacities = {lok_val:.2f})")
        else:
            st.warning(T("t1_cap_no_data"))



# ════════════════════════════════════
# TAB 2 — ANALISIS KUADRAN (Pemetaan Makro)
# Scatter plot dengan garis batas median (median split).
# Setiap negara diklasifikasikan ke 4 kuadran:
#   Preventif (Kapasitas Tinggi/Risiko Rendah) — ideal
#   Reaktif   (Kapasitas Rendah/Risiko Tinggi) — berbahaya
#   Waspada   (Kapasitas Tinggi/Risiko Tinggi)
#   Pasif     (Kapasitas Rendah/Risiko Rendah)
# ════════════════════════════════════
with tab2:
    st.subheader(T("t2_subheader"))
    st.markdown(T("t2_tab_desc"))
    st.markdown(T("t2_quad_table"))

    with st.expander(T("t2_method_exp")):
        st.markdown(T("t2_method_body"))

    # Selector X & Y — di dalam Tab 2 (Kuadran)
    ca2, cb2 = st.columns(2)
    with ca2:
        st.markdown(T("t2_var_y_label"))
        # Default: WRI Score (Pemetaan Makro)
        _y2_default = WRI_COLS.index('WRI Score') if 'WRI Score' in WRI_COLS else 0
        label_y2 = st.selectbox(T("t2_y_select"), WRI_COLS, index=_y2_default, key="ly2")
    with cb2:
        st.markdown(T("t2_var_x_label"))
        st.caption(T("t2_x_caption"))
        _x2_default = ALL_X_COLS.index('NRI Score') if 'NRI Score' in ALL_X_COLS else 0
        label_x2 = st.selectbox(T("t2_x_select"), ALL_X_COLS, index=_x2_default, key="lx2")

    lx2 = LABEL_PANJANG.get(label_x2, label_x2)
    ly2 = LABEL_PANJANG.get(label_y2, label_y2)
    df_plot2 = master.dropna(subset=[label_x2, label_y2]).copy()
    st.caption(f"{T('t2_analysis_cap')} **{lx2}** → **{ly2}** | {len(df_plot2)} {T('t2_n_countries')}.")

    # Ambil nilai median X dan Y — dipakai sebagai batas pemisah kuadran (median split)
    if len(df_plot2) >= 5:
        mx2, my2 = df_plot2[label_x2].median(), df_plot2[label_y2].median()

        # Fungsi klasifikasi kuadran berdasarkan posisi relatif terhadap median
        # hx=True: negara di atas/sama median X (kapasitas tinggi)
        # hy=True: negara di atas/sama median Y (risiko tinggi)
        def kuadran(row):
            hx, hy = row[label_x2] >= mx2, row[label_y2] >= my2
            if hx and not hy:  return T("quad_preventif")  # Kapasitas Tinggi / Risiko Rendah
            if not hx and hy:  return T("quad_reaktif")    # Kapasitas Rendah / Risiko Tinggi
            if hx and hy:      return T("quad_waspada")    # Kapasitas Tinggi / Risiko Tinggi
            return                    T("quad_pasif")       # Kapasitas Rendah / Risiko Rendah

        # Terapkan fungsi kuadran ke setiap baris — hasilnya kolom 'Kuadran'
        df_plot2['Kuadran'] = df_plot2.apply(kuadran, axis=1)

        # Scatter plot: setiap titik = 1 negara, warna = kuadrannya
        fig2 = px.scatter(df_plot2, x=label_x2, y=label_y2,
                          color="Kuadran", color_discrete_map=QUAD_COLOR, hover_name="Negara",
                          hover_data={c: True for c in ['Jumlah_Gunung', 'Frekuensi_Erupsi',
                                                         'Max_VEI', 'Kategori Risiko WRI', 'Kuadran']
                                      if c in df_plot2.columns},
                          labels={label_x2: lx2, label_y2: ly2},
                          title=T("t2_scatter_title", lx=lx2, ly=ly2),
                          height=560)
        fig2.update_traces(marker=dict(size=12, line=dict(width=0.8, color='white')), opacity=0.88)
        fig2.update_layout(plot_bgcolor="#f9f9f9",
                           legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1))
        # Garis putus-putus horizontal = median Y (batas atas/bawah kuadran)
        fig2.add_hline(y=my2, line_dash="dash", line_color="#555", line_width=1.5,
                       annotation_text=f"Median {ly2[:25]}={my2:.1f}", annotation_position="top right",
                       annotation_font_color="black")
        # Garis putus-putus vertikal = median X (batas kiri/kanan kuadran)
        fig2.add_vline(x=mx2, line_dash="dash", line_color="#555", line_width=1.5,
                       annotation_text=f"Median {lx2[:25]}={mx2:.1f}", annotation_position="top left",
                       annotation_font_color="black")
        # Hitung rentang nilai untuk posisi label kuadran di sudut grafik
        xmn, xmx = df_plot2[label_x2].min(), df_plot2[label_x2].max()
        ymn, ymx = df_plot2[label_y2].min(), df_plot2[label_y2].max()
        dx, dy = xmx - xmn, ymx - ymn  # Lebar dan tinggi area plot
        _reaktif_lbl   = T("quad_reaktif").split(" — ")[0]
        _preventif_lbl = T("quad_preventif").split(" — ")[0]
        _waspada_lbl   = T("quad_waspada").split(" — ")[0]
        _pasif_lbl     = T("quad_pasif").split(" — ")[0]
        # Top-left: Reaktif (Low cap, High risk)
        fig2.add_annotation(x=xmn+dx*.04, y=ymx-dy*.04, showarrow=False, text=f"<b>{_reaktif_lbl.upper()}</b>",
                            font=dict(color="#d62728", size=11), bgcolor="rgba(214,39,40,0.07)", borderpad=4)
        # Bottom-right: Preventif (High cap, Low risk)
        fig2.add_annotation(x=xmx-dx*.04, y=ymn+dy*.04, showarrow=False, text=f"<b>{_preventif_lbl.upper()}</b>",
                            font=dict(color="#2ca02c", size=11), bgcolor="rgba(44,160,44,0.07)",
                            borderpad=4, xanchor="right")
        # Top-right: Waspada (High cap, High risk)
        fig2.add_annotation(x=xmx-dx*.04, y=ymx-dy*.04, showarrow=False, text=f"<b>{_waspada_lbl.upper()}</b>",
                            font=dict(color="#ff7f0e", size=11), bgcolor="rgba(255,127,14,0.07)",
                            borderpad=4, xanchor="right")
        # Bottom-left: Pasif (Low cap, Low risk)
        fig2.add_annotation(x=xmn+dx*.04, y=ymn+dy*.04, showarrow=False, text=f"<b>{_pasif_lbl.upper()}</b>",
                            font=dict(color="#1f77b4", size=11), bgcolor="rgba(31,119,180,0.07)", borderpad=4)
        if INDO:
            ip2 = df_plot2[df_plot2['Negara'] == INDO]
            if not ip2.empty:
                fig2.add_annotation(x=ip2[label_x2].values[0], y=ip2[label_y2].values[0],
                                    text="<b>INDONESIA</b>", showarrow=True, arrowhead=3,
                                    ax=-95, ay=70,
                                    bgcolor="#d62728", bordercolor="white", borderwidth=1.5,
                                    font=dict(color="white", size=12),
                                    arrowcolor="#d62728", arrowwidth=2.5, arrowsize=1.3)
        fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ddd', zeroline=False)
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ddd', zeroline=False)
        st.plotly_chart(fig2, use_container_width=True)

        dq = df_plot2['Kuadran'].value_counts().reset_index(); dq.columns = ['Kuadran', 'Jumlah']
        cq = st.columns(4)
        for i, row in dq.iterrows():
            cq[i % 4].metric(row['Kuadran'].split(' — ')[0], f"{row['Jumlah']} {T('t2_country_quadrant')}")

        # ── Statistik per Kuadran (untuk verifikasi angka skripsi) ──
        with st.expander(T("t2_stat_exp")):
            # Quadrant keys must match what kuadran() returns (i.e. T() values)
            _quad_keys = [
                T("quad_preventif"),
                T("quad_reaktif"),
                T("quad_waspada"),
                T("quad_pasif"),
            ]
            _quad_short_labels = [
                T("quad_preventif").split(" — ")[0],
                T("quad_reaktif").split(" — ")[0],
                T("quad_waspada").split(" — ")[0],
                T("quad_pasif").split(" — ")[0],
            ]
            rows_stat = []
            for quad_full, quad_label in zip(_quad_keys, _quad_short_labels):
                sub = df_plot2[df_plot2['Kuadran'] == quad_full]
                if sub.empty:
                    continue
                for col, col_label in [(label_x2, lx2), (label_y2, ly2)]:
                    rows_stat.append({
                        T("indikator"): col_label,
                        "Quadrant" if _lang()=="en" else "Kuadran": quad_label,
                        "N":          len(sub),
                        "Mean":       round(sub[col].mean(), 2),
                        "Median":     round(sub[col].median(), 2),
                        "Min":        round(sub[col].min(), 2),
                        "Max":        round(sub[col].max(), 2),
                        "Std Dev":    round(sub[col].std(), 2),
                    })
            if rows_stat:
                df_stat = pd.DataFrame(rows_stat)
                st.dataframe(df_stat, use_container_width=True, hide_index=True)
                st.caption(T("t2_stat_cap"))

        # ── Tabel keanggotaan kuadran ──────────────────────────────────────
        st.markdown("---")
        st.markdown("#### " + ("Keanggotaan Kuadran" if _lang() == "id" else "Quadrant Membership"))
        _kq_cols = [c for c in ['Negara', label_x2, label_y2, 'Kuadran'] if c in df_plot2.columns]
        st.dataframe(
            df_plot2[_kq_cols].sort_values('Kuadran').reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

        if INDO and INDO in df_plot2['Negara'].values:
            indo_kd2 = df_plot2.loc[df_plot2['Negara'] == INDO, 'Kuadran'].values[0]
            # indo_kd2 is already a T() value matching T("quad_..."), use it directly as display
            st.markdown("---")
            st.markdown(f"{T('t2_indo_pos')} **{indo_kd2}**")
            same2 = df_plot2[(df_plot2['Kuadran'] == indo_kd2) & (df_plot2['Negara'] != INDO)]['Negara'].tolist()
            prev2 = df_plot2[df_plot2['Kuadran'] == T("quad_preventif")]
            ca1, ca2b = st.columns(2)
            with ca1:
                st.markdown(f"{T('t2_same_quad', n=len(same2))} {', '.join(sorted(same2))}")
            with ca2b:
                if not prev2.empty:
                    ix2 = df_plot2.loc[df_plot2['Negara'] == INDO, label_x2].values[0]
                    iy2b = df_plot2.loc[df_plot2['Negara'] == INDO, label_y2].values[0]
                    tx2, ty2 = prev2[label_x2].median(), prev2[label_y2].median()
                    _prev_quad_lbl = T("quad_preventif").split(" — ")[0]
                    if _lang() == "id":
                        st.info(
                            f"**Gap ke Kuadran Preventif:**\n\n"
                            f"- {lx2}: {ix2:.1f} → naik **+{tx2-ix2:.1f}** (target: {tx2:.1f})\n"
                            f"- {ly2}: {iy2b:.1f} → turun **-{iy2b-ty2:.1f}** (target: {ty2:.1f})"
                        )
                    else:
                        st.info(
                            f"**Gap to {_prev_quad_lbl} Quadrant:**\n\n"
                            f"- {lx2}: {ix2:.1f} → increase **+{tx2-ix2:.1f}** (target: {tx2:.1f})\n"
                            f"- {ly2}: {iy2b:.1f} → decrease **-{iy2b-ty2:.1f}** (target: {ty2:.1f})"
                        )

            # Paradoks Indonesia — argumen utama digital divide
            st.markdown("---")
            st.markdown(T("t2_paradox_title"))
            irow2 = master[master['Negara'] == INDO].iloc[0]
            p1, p2, p3 = st.columns(3)
            with p1:
                nri_v = irow2.get('NRI Score')
                gii_v = irow2.get('GII Score')
                gdp_v = irow2.get('GDP Per Capita 2024')
                st.metric(T("t2_nri_label"), f"{nri_v:.1f}" if pd.notna(nri_v) else "N/A")
                st.metric(T("t2_gii_label"), f"{gii_v:.1f}" if pd.notna(gii_v) else "N/A")
                st.metric(T("t2_gdp_label"), f"${gdp_v:,.0f}" if pd.notna(gdp_v) else "N/A")
            with p2:
                lok_v  = irow2.get('Lack of Coping Capacities')
                wri_v  = irow2.get('WRI Score')
                eru_v  = irow2.get('Frekuensi_Erupsi')
                st.metric("Lack of Coping Cap. (WRI)", f"{lok_v:.1f}" if pd.notna(lok_v) else "N/A",
                          delta=T("t2_higher_cap"), delta_color="inverse")
                st.metric("WRI Score (Risk)" if _lang()=="en" else "WRI Score (Risiko)",
                          f"{wri_v:.2f}" if pd.notna(wri_v) else "N/A",
                          delta=f"{WRI_KEY_TO_LABEL.get(irow2['Kategori Risiko WRI'], irow2['Kategori Risiko WRI'])}", delta_color="inverse")
                st.metric(T("t2_frek_label"), f"{int(eru_v)} {T('metric_eru_unit')}" if pd.notna(eru_v) else "N/A",
                          delta=T("t2_world_highest"), delta_color="inverse")
            with p3:
                kap_v  = irow2.get('Kategori Kapasitas', 'N/A')
                st.markdown(T("t2_paradox_interp"))
                st.warning(T("t2_paradox_body", lok=f"{lok_v:.1f}" if pd.notna(lok_v) else "N/A", kap=kap_v))
    else:
        st.warning(T("t2_not_enough"))


# ════════════════════════════════════
# TAB 3 — KORELASI & REGRESI OLS (Analisis Mikro)
# Menguji hubungan antara indikator kapasitas teknologi (X)
# dan indikator penanggulangan bencana (Y) menggunakan:
#   - Pearson Correlation (r) → kekuatan & arah hubungan
#   - OLS Regression (scipy linregress) → persamaan prediksi
#   - Heatmap korelasi semua kombinasi variabel X–Y
# Posisi Indonesia ditandai & residualnya dihitung.
# ════════════════════════════════════
with tab3:
    st.subheader(T("t3_subheader"))
    st.markdown(T("t3_tab_desc"))

    # Selector X & Y — di dalam Tab 3 (Regresi)
    ca3, cb3 = st.columns(2)
    with ca3:
        st.markdown(T("t3_y_label"))
        # Default: Lack of Coping Capacities (Analisis Mikro/Regresi)
        _y3_default = WRI_COLS.index('Lack of Coping Capacities') if 'Lack of Coping Capacities' in WRI_COLS else 0
        label_y3 = st.selectbox(T("t3_y_select"), WRI_COLS, index=_y3_default, key="ly3")
    with cb3:
        st.markdown(T("t2_var_x_label"))
        st.caption(T("t3_x_caption2"))
        _x3_default = ALL_X_COLS.index('NRI Score') if 'NRI Score' in ALL_X_COLS else 0
        label_x3 = st.selectbox(T("t3_x_select"), ALL_X_COLS, index=_x3_default, key="lx3")

    lx3 = LABEL_PANJANG.get(label_x3, label_x3)
    ly3 = LABEL_PANJANG.get(label_y3, label_y3)
    df_plot3 = master.dropna(subset=[label_x3, label_y3]).copy()
    st.caption(f"{T('t2_analysis_cap')} **{lx3}** → **{ly3}** | {len(df_plot3)} {T('t3_n_countries_data')}.")

    # Info variabel
    ci1, ci2 = st.columns(2)
    with ci1:
        info_y3 = next(((p,u,v) for n,(p,u,v) in INDIKATOR_INFO.items() if any(k in label_y3 for k in n.split())), None)
        st.info(f"**Y = {ly3}**\n\n{T('t3_sub_y') if not info_y3 else info_y3[1]}")
    with ci2:
        info_x3 = next(((p,u,v) for n,(p,u,v) in INDIKATOR_INFO.items() if any(k in label_x3 for k in n.split())), None)
        _risk_inform3 = {'INFORM RISK', 'VULNERABILITY', 'HAZARD & EXPOSURE', 'LACK OF COPING CAPACITY'}
        _x3_desc = info_x3[1] if info_x3 else (
            T("t3_sub_x_risk") if label_x3 in _risk_inform3 else T("t3_sub_x_cap")
        )
        st.info(f"**X = {lx3}**\n\n{_x3_desc}")

    # Minimal 5 data agar regresi bermakna secara statistik
    if len(df_plot3) >= 5:
        # Regresi OLS menggunakan scipy.stats.linregress
        # Output: slope (β), intercept (α), r (korelasi Pearson), p_val, stderr
        slope3, intercept3, r3, p_val3, _ = linregress(df_plot3[label_x3], df_plot3[label_y3])
        r2_3 = r3 ** 2  # R² = koefisien determinasi (seberapa besar X menjelaskan variansi Y)

        # ── ANGKA KUNCI ──
        if label_x3 == 'NRI Score' and label_y3 == 'Lack of Coping Capacities':
            st.markdown("### 🔑 Angka Kunci Penelitian")
            st.caption("Empat angka ini adalah inti dari seluruh analisis — catat sebelum melanjutkan.")
            _k1, _k2, _k3, _k4 = st.columns(4)
            _k1.metric("Korelasi NRI vs LoCC", f"r = {r3:.2f}", delta="Hubungan negatif signifikan", delta_color="off")
            _k2.metric("Kekuatan Model OLS", f"R² = {r2_3:.3f}", delta=f"{r2_3*100:.1f}% variasi dijelaskan NRI", delta_color="off")

            if INDO and INDO in df_plot3['Negara'].values:
                _ip = df_plot3[df_plot3['Negara'] == INDO].iloc[0]
                _pred_key = slope3 * _ip[label_x3] + intercept3
                _resid_key = _ip[label_y3] - _pred_key
                _k3.metric("Residual Indonesia", f"+{_resid_key:.2f}", delta="Jauh di atas prediksi model", delta_color="inverse")
                _k4.metric("Aktual vs Prediksi Indonesia", f"{_ip[label_y3]:.2f} vs {_pred_key:.2f}", delta=f"Selisih {_resid_key:.2f} poin anomali", delta_color="inverse")
            st.markdown("---")

        # ── 5 Metrik Hasil Regresi OLS ──
        r3c1, r3c2, r3c3, r3c4, r3c5 = st.columns(5)
        r3c1.metric(T("t3_corr"), f"{r3:.3f}",         # r: korelasi Pearson
                    delta=T("t3_neg_corr") if r3 < 0 else T("t3_pos_corr"))  # Negatif=ideal
        r3c2.metric(T("t3_r2"), f"{r2_3:.3f}",          # R²: proporsi variansi yang dijelaskan
                    delta=T("t3_pct_var", pct=f"{r2_3*100:.1f}"))
        r3c3.metric(T("t3_pval"), f"{p_val3:.4f}",       # p-value: signifikansi statistik
                    delta=T("t3_sig") if p_val3 < 0.05 else T("t3_not_sig"),  # Signifikan jika p<0.05
                    delta_color="normal" if p_val3 < 0.05 else "inverse")
        r3c4.metric(T("t3_slope"), f"{slope3:.4f}")      # β (slope): perubahan Y per satuan X
        r3c5.metric(T("t3_intercept"), f"{intercept3:.4f}")  # α (intercept): nilai Y saat X=0

        # Tampilkan persamaan regresi OLS: Y = α ± βX
        st.success(T("t3_ols_formula", a=f"{intercept3:.4f}", sign='+' if slope3 >= 0 else '-', b=f"{abs(slope3):.4f}"))

        fig3 = px.scatter(
            df_plot3, x=label_x3, y=label_y3,
            color='Frekuensi_Erupsi', color_continuous_scale='Plasma',
            hover_name="Negara",
            hover_data={c: True for c in ['Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI', 'Kategori Risiko WRI']
                        if c in df_plot3.columns},
            labels={label_x3: lx3, label_y3: ly3, 'Frekuensi_Erupsi': T("t3_frek_label")},
            title=T("t3_scatter_label", lx=lx3, ly=ly3, n=len(df_plot3)),
            height=500
        )
        # Trendline manual berbasis scipy linregress (tidak membutuhkan statsmodels)
        x_range3 = np.linspace(df_plot3[label_x3].min(), df_plot3[label_x3].max(), 100)
        y_hat3   = slope3 * x_range3 + intercept3
        fig3.add_trace(go.Scatter(
            x=x_range3, y=y_hat3, mode='lines', name='OLS Trendline',
            line=dict(color='#333', width=2, dash='dash'), showlegend=True))
        fig3.update_traces(selector=dict(mode='markers'),
                           marker=dict(size=11, line=dict(width=0.8, color='white')), opacity=0.87)
        fig3.update_layout(plot_bgcolor="white",
                           coloraxis_colorbar=dict(title=T("t3_frek_label")))
        fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#eee', zeroline=False)
        fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee', zeroline=False)

        if INDO:
            ip3 = df_plot3[df_plot3['Negara'] == INDO]
            if not ip3.empty:
                fig3.add_annotation(x=ip3[label_x3].values[0], y=ip3[label_y3].values[0],
                                    text="<b>INDONESIA</b>", showarrow=True, arrowhead=3,
                                    ax=90, ay=-65,
                                    bgcolor="#d62728", bordercolor="white", borderwidth=1.5,
                                    font=dict(color="white", size=11),
                                    arrowcolor="#d62728", arrowwidth=2, arrowsize=1.2)
        st.plotly_chart(fig3, use_container_width=True)
        st.caption(T("t3_dot_color"))

        # ── DISCLAIMER AKADEMIK (Anti-Kritik) ──
        st.info(T("t3_methodological_note"))

        arah3 = T("t3_interp_neg") if r3 < 0 else T("t3_interp_pos")
        kuat3 = T("t3_interp_strong") if abs(r3) >= 0.6 else (T("t3_interp_moderate") if abs(r3) >= 0.4 else T("t3_interp_weak"))
        sig3  = T("t3_interp_sig") if p_val3 < 0.05 else T("t3_interp_not_sig")
        st.info(T("t3_interp_full", strength=kuat3, direction=arah3,
                  r=f"{r3:.3f}", r2=f"{r2_3:.3f}", p=f"{p_val3:.4f}",
                  sig=sig3, lx=lx3, pct=f"{r2_3*100:.1f}", ly=ly3))

        if INDO and INDO in df_plot3['Negara'].values:
            ip3r = df_plot3[df_plot3['Negara'] == INDO].iloc[0]
            pred3 = slope3 * ip3r[label_x3] + intercept3
            gap3  = ip3r[label_y3] - pred3
            _eru_indo3 = int(irow['Frekuensi_Erupsi']) if INDO else 0
            _gap_note3 = (
                T("t3_gap_note_high", n=f"{_eru_indo3:,}")
                if gap3 > 0 else
                T("t3_gap_note_low")
            )
            _dir3 = T("t3_gap_worse") if gap3 > 0 else T("t3_gap_better")
            st.warning(
                T("t3_indo_pos", lx=lx3, x_val=f"{ip3r[label_x3]:.2f}",
                  ly=ly3, pred=f"{pred3:.2f}",
                  actual=f"{ip3r[label_y3]:.2f}",
                  dir=_dir3, gap=f"{abs(gap3):.2f}", note=_gap_note3)
            )

        st.markdown(T("t3_median_avg"))
        st.caption(T("t3_median_caption"))
        med_x3 = df_plot3[label_x3].median()
        df_plot3['_kat'] = df_plot3[label_x3].apply(
            lambda v: T("t3_above_median", lx=lx3[:20]) if v >= med_x3 else T("t3_below_median", lx=lx3[:20]))
        show_avg3 = [c for c in [label_x3, label_y3, 'Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI']
                     if c in df_plot3.columns]
        summ3 = df_plot3.groupby('_kat')[show_avg3].mean().round(2).reset_index().rename(columns={'_kat': T("kategori")})
        summ3.columns = [T("kategori")] + [LABEL_PANJANG.get(c, c) for c in summ3.columns[1:]]
        st.dataframe(summ3, use_container_width=True, hide_index=True)

        # ── RESIDUAL CHART ──
        if label_x3 == 'NRI Score' and label_y3 == 'Lack of Coping Capacities':
            st.markdown("---")
            st.markdown("#### 📉 Residual per Negara: Selisih Aktual vs Prediksi Model OLS")
            st.caption("Residual = nilai aktual Lack of Coping Capacities dikurangi nilai prediksi model. "
                       "Positif = lebih buruk dari prediksi. Negatif = lebih baik dari prediksi.")

            df_resid = df_plot3[["Negara", label_x3, label_y3]].copy()
            df_resid["Prediksi"] = slope3 * df_resid[label_x3] + intercept3
            df_resid["Residual"] = df_resid[label_y3] - df_resid["Prediksi"]
            df_resid = df_resid.sort_values("Residual", ascending=False).reset_index(drop=True)

            colors = []
            for _, row in df_resid.iterrows():
                if row["Negara"] == INDO:
                    colors.append("#d62728")
                elif row["Residual"] < 0:
                    colors.append("#4393c3")
                else:
                    colors.append("#aaaaaa")

            fig_resid = go.Figure(go.Bar(
                x=df_resid["Negara"],
                y=df_resid["Residual"],
                marker_color=colors,
                customdata=df_resid[[label_x3, label_y3, "Prediksi", "Residual"]].values,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "NRI: %{customdata[0]:.2f}<br>"
                    "LoCC Aktual: %{customdata[1]:.2f}<br>"
                    "LoCC Prediksi: %{customdata[2]:.2f}<br>"
                    "Residual: <b>%{customdata[3]:+.2f}</b><extra></extra>"
                )
            ))
            fig_resid.update_layout(
                title="Residual OLS: Aktual − Prediksi (NRI → Lack of Coping Capacities)",
                xaxis_title="Negara",
                yaxis_title="Residual",
                plot_bgcolor="white",
                height=450,
                xaxis=dict(tickangle=-45, showticklabels=True),
                yaxis=dict(showgrid=True, gridcolor="#eee", zeroline=True,
                           zerolinecolor="#333", zerolinewidth=1.5),
                showlegend=False
            )

            if INDO and INDO in df_resid["Negara"].values:
                indo_resid_val = float(df_resid.loc[df_resid["Negara"] == INDO, "Residual"].values[0])
                sign = "+" if indo_resid_val >= 0 else ""
                fig_resid.add_annotation(
                    x=INDO, y=indo_resid_val,
                    text=f"<b>INDONESIA<br>{sign}{indo_resid_val:.2f}</b>",
                    showarrow=True, arrowhead=3,
                    ax=60, ay=-50,
                    bgcolor="#d62728", bordercolor="white", borderwidth=1.5,
                    font=dict(color="white", size=11),
                    arrowcolor="#d62728", arrowwidth=2, arrowsize=1.2
                )

            st.plotly_chart(fig_resid, use_container_width=True)

    else:
        st.warning(T("t3_not_enough"))

    # Heatmap
    st.markdown("---")
    st.markdown(T("t3_heatmap_title"))
    st.markdown(T("t3_heatmap_desc"))
    hmap_y = [c for c in WRI_COLS   if master[c].notna().sum() >= 10]
    hmap_x = [c for c in ALL_X_COLS if master[c].notna().sum() >= 10 and c not in hmap_y]
    if hmap_x and hmap_y:
        corr_m = pd.DataFrame(index=hmap_y, columns=hmap_x, dtype=float)
        pval_m = pd.DataFrame(index=hmap_y, columns=hmap_x, dtype=float)
        for yc in hmap_y:
            for xc in hmap_x:
                d = master[[xc, yc]].dropna()
                if xc == yc or len(d) < 5:
                    continue
                rv, pv = pearsonr(d[xc], d[yc])
                corr_m.loc[yc, xc] = round(rv, 3)
                pval_m.loc[yc, xc] = round(pv, 4)
        text_m = corr_m.copy().astype(str)
        for yc in hmap_y:
            for xc in hmap_x:
                cv = corr_m.loc[yc, xc]; pv = pval_m.loc[yc, xc]
                if pd.isna(cv): text_m.loc[yc, xc] = "N/A"
                else:
                    star = "***" if pv < 0.001 else ("**" if pv < 0.01 else ("*" if pv < 0.05 else ""))
                    text_m.loc[yc, xc] = f"{cv:.2f}{star}"
        # Transpose: kapasitas → Y axis (kiri, terbaca langsung)  |  risiko → X axis (bawah, 6 label pendek)
        fig_hm = px.imshow(corr_m.T.values.astype(float),
                           x=[LABEL_PANJANG.get(c, c) for c in hmap_y],
                           y=[LABEL_PANJANG.get(c, c) for c in hmap_x],
                           color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                           title=T("t3_heatmap_plot_title"),
                           height=max(500, len(hmap_x) * 32))
        fig_hm.update_traces(text=text_m.T.values, texttemplate="%{text}",
                             textfont=dict(size=8))
        fig_hm.update_layout(
            xaxis=dict(tickangle=-20, tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=9)),
            coloraxis_colorbar=dict(title="r", tickvals=[-1, -0.5, 0, 0.5, 1],
                                   thickness=12, len=0.5, x=1.01),
            margin=dict(l=0, r=50, t=60, b=120)
        )
        st.plotly_chart(fig_hm, use_container_width=True)
        st.caption(T("t3_heatmap_caption"))

        flat = []
        for yc in hmap_y:
            for xc in hmap_x:
                cv = corr_m.loc[yc, xc]; pv = pval_m.loc[yc, xc]
                if pd.notna(cv):
                    flat.append({'X': LABEL_PANJANG.get(xc, xc), 'Y': LABEL_PANJANG.get(yc, yc),
                                 'r': cv, 'p': pv, 'abs_r': abs(cv)})
        top5 = pd.DataFrame(flat).sort_values('abs_r', ascending=False)
        top5 = top5[top5['p'] < 0.05].head(5)
        if not top5.empty:
            st.markdown(T("t3_top5"))
            for _, row in top5.iterrows():
                aicon = T("t3_top5_neg") if row['r'] < 0 else T("t3_top5_pos")
                kstr  = T("t3_top5_strong") if abs(row['r']) >= 0.6 else (T("t3_top5_moderate") if abs(row['r']) >= 0.4 else T("t3_top5_weak"))
                st.markdown(f"- **{row['X']}** → **{row['Y']}**: r=`{row['r']:.3f}` ({aicon}, {kstr}) | p=`{row['p']:.4f}`")


# ════════════════════════════════════
# TAB 4 — HEAD-TO-HEAD INDONESIA VS BENCHMARK
# Membandingkan Indonesia dengan negara benchmark pilihan pengguna
# (umumnya negara kuadran Preventif: Jepang, Selandia Baru, dll.)
# menggunakan:
#   - Radar chart 6 dimensi (NRI, GII, GDP, WRI, DRR, INFORM)
#   - Bar chart per kategori indikator
#   - Tabel gap analysis (selisih nilai Indonesia vs benchmark)
# Radar dinormalisasi 0–100% (min-max scaling dari seluruh sampel).
# ════════════════════════════════════
with tab4:
    st.subheader(T("t4_subheader"))
    st.markdown(T("t4_tab_desc"))

    all_nc = sorted([n for n in master['Negara'].dropna().unique() if n != INDO])
    defs   = [n for n in ['Japan', 'New Zealand', 'Iceland'] if n in all_nc]
    cs1, cs2 = st.columns([3, 1])
    with cs1:
        pembanding = st.multiselect(T("t4_select_label"),
                                     options=all_nc, default=defs[:3], max_selections=5)
    with cs2:
        st.markdown(T("t4_recommend"))

    if not pembanding:
        st.info(T("t4_select_min"))
    else:
        target = ([INDO] if INDO else []) + pembanding
        df_cmp = master[master['Negara'].isin(target)].copy()
        CC = ["#d62728", "#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]

        # Radar — disederhanakan ke 6 dimensi kunci agar tidak tumpang tindih
        st.markdown(T("t4_radar_title"))
        rcols = [c for c in ['NRI Score', 'GII Score', 'GDP Per Capita 2024',
                              'WRI Score', 'DRR', 'INFORM RISK']
                 if c in df_cmp.columns and df_cmp[c].notna().sum() > 0]
        short_labels = {
            'NRI Score': 'NRI', 'GII Score': 'GII', 'GDP Per Capita 2024': T("t4_gdp_short"),
            'WRI Score': 'WRI Risk', 'DRR': 'DRR', 'INFORM RISK': 'INFORM Risk'
        }
        df_rad = df_cmp[['Negara'] + rcols].copy()
        for col in rcols:
            mn, mx2 = master[col].min(), master[col].max()
            df_rad[col] = ((df_rad[col] - mn) / (mx2 - mn) * 100) if mx2 > mn else 50.0
        for ic in ['WRI Score', 'INFORM RISK']:
            if ic in rcols: df_rad[ic] = 100 - df_rad[ic]
        theta = [short_labels.get(c, c) for c in rcols]
        fig_r = go.Figure()
        for i, (_, row) in enumerate(df_rad.iterrows()):
            vals = [row[c] if pd.notna(row[c]) else 0 for c in rcols]
            nm = str(row['Negara'])
            fig_r.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=theta + [theta[0]], fill='toself', name=nm,
                line=dict(color=CC[i % len(CC)], width=3 if nm == INDO else 1.8),
                fillcolor=CC[i % len(CC)], opacity=0.45 if nm == INDO else 0.2))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%", gridcolor="#ddd",
                                tickfont=dict(size=10)),
                angularaxis=dict(tickfont=dict(size=12))
            ),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
            title=T("t4_radar_plot_title"),
            height=480)
        st.plotly_chart(fig_r, use_container_width=True)
        st.caption(T("t4_radar_caption"))

        # Bar — dikelompokkan per kategori dalam sub-tab agar tidak tumpuk
        st.markdown("---")
        st.markdown(T("t4_bar_title"))
        cat_groups = {
            T("t4_cat_main"): [c for c in ['NRI Score', 'GII Score', 'GDP Per Capita 2024',
                                           'WRI Score', 'INFORM RISK'] if c in df_cmp.columns],
            T("t4_cat_nri"): [c for c in ['Technology Pillar', 'People Pillar',
                                               'Governance Pillar', 'Impact Pillar'] if c in df_cmp.columns],
            T("t4_cat_gii"): [c for c in ['Human capital and research', 'GII - Infrastructure',
                                            'Knowledge and technology outputs', 'Business sophistication']
                                    if c in df_cmp.columns],
            T("t4_cat_disaster"): [c for c in ['DRR', 'Communication', 'LACK OF COPING CAPACITY',
                                                'Physical infrastructure', 'Institutional']
                                    if c in df_cmp.columns],
        }
        cat_groups = {k: v for k, v in cat_groups.items() if v}
        bar_tabs4 = st.tabs(list(cat_groups.keys()))
        for bi, (cat_name, bcols) in enumerate(cat_groups.items()):
            with bar_tabs4[bi]:
                df_bar4 = df_cmp[['Negara'] + bcols].melt(
                    id_vars='Negara', var_name=T("indikator"), value_name=T("nilai"))
                df_bar4[T("indikator")] = df_bar4[T("indikator")].map(lambda x: LABEL_PANJANG.get(x, x))
                fig_b = px.bar(df_bar4, x=T("indikator"), y=T("nilai"), color='Negara',
                               barmode='group', color_discrete_sequence=CC, height=360)
                fig_b.update_layout(
                    plot_bgcolor="white", xaxis_title="", yaxis_title=T("t4_bar_y"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1))
                fig_b.update_xaxes(tickangle=-15, showgrid=False)
                fig_b.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
                st.plotly_chart(fig_b, use_container_width=True)

        # Gap table
        st.markdown("---")
        st.markdown(T("t4_gap_title"))
        gcols = [c for c in ['WRI Score', 'NRI Score', 'GII Score', 'GDP Per Capita 2024',
                              'Frekuensi_Erupsi', 'Max_VEI', 'INFORM RISK',
                              'LACK OF COPING CAPACITY', 'DRR', 'Communication',
                              'Exposure', 'Vulnerability', 'Lack of Coping Capacities']
                 if c in df_cmp.columns]
        if INDO:
            irow4 = df_cmp[df_cmp['Negara'] == INDO].iloc[0]
            grows = []
            for col in gcols:
                try: iv = float(irow4[col])
                except: iv = None
                row_d = {"Indikator": LABEL_PANJANG.get(col, col),
                         "Indonesia": round(iv, 2) if iv is not None else None}
                for nb in pembanding:
                    nbr = df_cmp[df_cmp['Negara'] == nb]
                    if nbr.empty:
                        row_d[nb] = None; row_d[f"Gap vs {nb[:8]}"] = None; continue
                    try:
                        nv = float(nbr.iloc[0][col])
                        row_d[nb] = round(nv, 2)
                        row_d[f"Gap vs {nb[:8]}"] = round(iv - nv, 2) if iv is not None else None
                    except:
                        row_d[nb] = None; row_d[f"Gap vs {nb[:8]}"] = None
                grows.append(row_d)

            if grows:
                df_gap = pd.DataFrame(grows)
                gap_cols_list = [c for c in df_gap.columns if c.startswith("Gap vs")]
                def cgap(v):
                    if not isinstance(v, (int, float)) or pd.isna(v): return ''
                    return 'color:#d62728;font-weight:bold' if v > 0 else 'color:#2ca02c;font-weight:bold'
                st.dataframe(df_gap.style.map(cgap, subset=gap_cols_list),
                             use_container_width=True, hide_index=True)
                st.caption(T("t4_gap_caption"))


# ════════════════════════════════════
# TAB 5 — KETANGGUHAN PER FASE BENCANA (Sendai Framework)
# Menganalisis posisi Indonesia di 4 fase penanggulangan bencana
# berdasarkan Sendai Framework UNDRR:
#   Mitigasi      → DRR, infrastruktur fisik
#   Kesiapsiagaan → komunikasi, teknologi, NRI
#   Respons       → institusi, Lack of Coping Capacity
#   Pemulihan     → GDP, GII, inovasi
# Kolom INFORM (higher=worse) di-invert sebelum rata-rata & normalisasi
# agar nilai radar lebih tinggi selalu berarti lebih tangguh.
# ════════════════════════════════════
with tab5:
    st.subheader(T("t5_subheader"))
    st.markdown(T("t5_tab_desc"))

    all_nf = sorted([n for n in master['Negara'].dropna().unique() if n != INDO])
    def_f  = [n for n in ['Japan', 'New Zealand', 'Iceland'] if n in all_nf]
    fase_bench = st.multiselect(T("t5_select_label"), options=all_nf,
                                 default=def_f[:3], max_selections=4, key="fb")
    fase_target = ([INDO] if INDO else []) + fase_bench
    df_fa = master[master['Negara'].isin(fase_target)].copy()
    CC5   = ["#d62728", "#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd"]

    fase_tabs = st.tabs([f"{v['icon']} {k}" for k, v in FASE_BENCANA.items()])
    for i, (fase_k, fase_v) in enumerate(FASE_BENCANA.items()):
        with fase_tabs[i]:
            st.markdown(f"**{fase_v['deskripsi']}**")
            st.caption(f"{T('t5_acuan_label')} *{fase_v['acuan']}*")
            fcols = [c for c in fase_v['kolom'] if c in master.columns and master[c].notna().sum() >= 5]
            if not fcols:
                st.warning(T("t5_no_data")); continue
            df_melt = df_fa[['Negara'] + fcols].melt(id_vars='Negara', var_name=T("indikator"), value_name=T("t5_bar_y")).dropna()
            df_melt[T("indikator")] = df_melt[T("indikator")].map(lambda x: LABEL_PANJANG.get(x, x))
            fig_f = px.bar(df_melt, x=T("indikator"), y=T("t5_bar_y"), color='Negara',
                           barmode='group', color_discrete_sequence=CC5,
                           title=T("t5_bar_title", fase=fase_k), height=360)
            fig_f.update_layout(plot_bgcolor="white", xaxis_title="", yaxis_title=T("t5_bar_y"),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig_f.update_xaxes(tickangle=-20, showgrid=False)
            fig_f.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
            st.plotly_chart(fig_f, use_container_width=True)

            trows = []
            for col in fcols:
                rd = {"Indikator": LABEL_PANJANG.get(col, col)}
                for nm in fase_target:
                    r5 = df_fa[df_fa['Negara'] == nm]
                    rd[nm] = round(r5[col].values[0], 2) if not r5.empty and pd.notna(r5[col].values[0]) else None
                if INDO and rd.get(INDO) is not None:
                    bvals = [rd[n] for n in fase_bench if rd.get(n) is not None]
                    if bvals:
                        gv = round(rd[INDO] - np.mean(bvals), 2)
                        # INFORM — semua sub-indikator Lack of Coping Capacity: nilai TINGGI = situasi LEBIH BURUK
                        # (DRR tinggi = kurangnya implementasi DRR; Institutional tinggi = lemahnya institusi, dst.)
                        # Sumber: INFORM Conceptual Model, JRC 2024 — seluruh output sudah dinormalisasi
                        # sehingga higher = higher risk secara konsisten.
                        risk_c = ['LACK OF COPING CAPACITY', 'INFORM RISK', 'INFORM - Infrastructure',
                                  'VULNERABILITY', 'HAZARD & EXPOSURE', 'DRR',
                                  'Institutional', 'Physical infrastructure', 'Communication']
                        rd['Gap vs Benchmark'] = (f"{'🔴 +' if gv > 0 else '🟢 '}{gv}" if col in risk_c
                                                   else f"{'🔴 ' if gv < 0 else '🟢 +'}{gv}")
                trows.append(rd)
            if trows:
                st.dataframe(pd.DataFrame(trows), use_container_width=True, hide_index=True)
            if INDO:
                ir = df_fa[df_fa['Negara'] == INDO]
                if not ir.empty:
                    # Kolom risiko: nilai TINGGI = buruk (cari max). Kolom kapasitas: nilai RENDAH = buruk (cari min).
                    # INFORM: semua sub-indikator (DRR, Institutional, Communication, Physical infrastructure)
                    # juga menggunakan skala higher=worse (sudah dinormalisasi INFORM).
                    # Sumber: INFORM Methodology 2024, JRC European Commission.
                    risk_cols_fase = {
                        'LACK OF COPING CAPACITY', 'INFORM RISK', 'VULNERABILITY',
                        'HAZARD & EXPOSURE', 'DRR', 'Institutional',
                        'Physical infrastructure', 'Communication', 'INFORM - Infrastructure'
                    }
                    vlist = [(c, ir[c].values[0]) for c in fcols if pd.notna(ir[c].values[0])]
                    if vlist:
                        # Untuk kolom risiko, konversi nilainya menjadi negatif agar min() = nilai terburuk
                        vlist_adj = [(c, -v if c in risk_cols_fase else v) for c, v in vlist]
                        worst_col, _ = min(vlist_adj, key=lambda x: x[1])
                        worst_val = dict(vlist)[worst_col]
                        st.info(
                            T("t5_insight", fase=fase_k,
                              col=LABEL_PANJANG.get(worst_col, worst_col),
                              val=f"{worst_val:.2f}")
                            + (" " + T("nilai_tinggi_buruk") if worst_col in risk_cols_fase else ".")
                        )

    st.markdown("---")
    st.markdown(T("t5_summary_title"))
    # Kolom INFORM yang higher=worse (seluruh output INFORM sudah dinormalisasi: tinggi = lebih rentan)
    # Kolom ini perlu diinvert (×-1) sebelum dirata-rata per fase agar radar konsisten:
    # nilai radar lebih tinggi = lebih tangguh di fase tersebut.
    INFORM_RISK_COLS = {
        'LACK OF COPING CAPACITY', 'INFORM RISK', 'VULNERABILITY',
        'HAZARD & EXPOSURE', 'DRR', 'Institutional',
        'Physical infrastructure', 'Communication', 'INFORM - Infrastructure'
    }
    sum_rows = []
    for nm in fase_target:
        rn = {'Negara': nm}
        for fk, fv in FASE_BENCANA.items():
            fc2 = [c for c in fv['kolom'] if c in master.columns]
            r5  = master[master['Negara'] == nm]
            vals_raw = []
            for c in fc2:
                if not r5.empty and pd.notna(r5[c].values[0]):
                    v = r5[c].values[0]
                    # Invert kolom INFORM (higher=worse) agar konsisten: lebih tinggi = lebih baik
                    if c in INFORM_RISK_COLS:
                        v = -v
                    vals_raw.append(v)
            rn[fk] = np.mean(vals_raw) if vals_raw else None
        sum_rows.append(rn)
    df_sum = pd.DataFrame(sum_rows)
    fkeys  = list(FASE_BENCANA.keys())
    df_nrm = df_sum.copy()
    for fk in fkeys:
        cv2 = pd.to_numeric(df_nrm[fk], errors='coerce')
        mn2, mx3 = cv2.min(), cv2.max()
        df_nrm[fk] = ((cv2 - mn2) / (mx3 - mn2) * 100).round(1) if mx3 > mn2 else 50.0
    fig_sum = go.Figure()
    for i, row in df_nrm.iterrows():
        nm = row['Negara']
        vals2 = [row.get(fk) or 0 for fk in fkeys]
        fig_sum.add_trace(go.Scatterpolar(
            r=vals2 + [vals2[0]], theta=fkeys + [fkeys[0]], fill='toself', name=nm,
            line=dict(color=CC5[i % len(CC5)], width=3 if nm == INDO else 1.8),
            fillcolor=CC5[i % len(CC5)], opacity=0.45 if nm == INDO else 0.2))
    fig_sum.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ddd")),
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        title=T("t5_radar_title"), height=420)
    st.plotly_chart(fig_sum, use_container_width=True)
    st.caption(T("t5_radar_caption"))

    # ── Tabel Gap Indonesia vs Benchmark per Fase (Skala 0–1) ───────────────
    # Normalisasi: min/max dari seluruh 55 negara sampel analitik (master),
    # identik dengan _process_column di section Kuadran di bawahnya.
    # INFORM (higher=worse) diinvert: (max - val) / (max - min).
    # Kapasitas (higher=better): (val - min) / (max - min).
    # Skor per fase = rata-rata skor ternormalisasi semua indikator dalam fase tersebut.
    st.markdown("---")
    st.markdown(f"#### {T('t5_gap_bench_title')}")
    if not fase_bench:
        st.info(T("t5_gap_bench_no_bench"))
    elif INDO is None:
        st.warning(T("t5_gap_bench_no_indo"))
    else:
        def _norm_val_global(col, val):
            """Normalisasi nilai tunggal ke 0–1 menggunakan global min/max dari master.
            Logika identik dengan _process_column (didefinisikan di section Kuadran)."""
            if col not in master.columns or pd.isna(val):
                return None
            col_min = master[col].min()
            col_max = master[col].max()
            if col_max == col_min:
                return 0.5
            if col in INFORM_RISK_COLS:  # INFORM: higher = worse → invert
                return (col_max - val) / (col_max - col_min)
            else:
                return (val - col_min) / (col_max - col_min)

        def _phase_score_global(negara, fase_key):
            """Hitung skor fase (0–1) untuk satu negara menggunakan normalisasi global."""
            fv   = FASE_BENCANA[fase_key]
            fc   = [c for c in fv['kolom'] if c in master.columns]
            row  = master[master['Negara'] == negara]
            if row.empty:
                return None
            nv_list = []
            for c in fc:
                raw = row[c].values[0]
                nv  = _norm_val_global(c, raw)
                if nv is not None:
                    nv_list.append(nv)
            return round(np.mean(nv_list), 3) if nv_list else None

        _gap_rows = []  # Kumpul satu baris per fase
        for fk in fkeys:
            _indo_score   = _phase_score_global(INDO, fk)      # Skor Indonesia di fase ini (0–1)
            _bench_scores = [s for bn in fase_bench
                             if (s := _phase_score_global(bn, fk)) is not None]
            _avg_bench    = round(np.mean(_bench_scores), 3) if _bench_scores else None  # Rata-rata benchmark

            if _indo_score is not None and _avg_bench is not None:
                _gap_val  = round(_avg_bench - _indo_score, 3)  # Gap = benchmark – Indonesia
                # Positif (🔴) = Indonesia tertinggal; Negatif (🟢) = Indonesia lebih baik
                _gap_prefix = '🔴 +' if _gap_val > 0 else ('🟢 ' if _gap_val < 0 else '')
                _gap_disp = f"{_gap_prefix}{_gap_val:+.3f}"
            else:
                _gap_val  = None
                _gap_disp = "—"

            _gap_rows.append({
                T("t5_gap_bench_col_fase"): f"{FASE_BENCANA[fk]['icon']} {fk}",
                T("t5_gap_bench_col_indo"): _indo_score,    # Skor Indonesia (0–1)
                T("t5_gap_bench_col_avg"):  _avg_bench,     # Rata-rata skor benchmark (0–1)
                T("t5_gap_bench_col_gap"):  _gap_disp,      # Gap dengan emoji warna
            })

        if _gap_rows:
            _gap_df       = pd.DataFrame(_gap_rows)
            _gap_col_name = T("t5_gap_bench_col_gap")

            def _style_gap_cell(val):
                if not isinstance(val, str): return ''
                if val.startswith('🔴'): return 'color:#d62728; font-weight:bold'
                if val.startswith('🟢'): return 'color:#2ca02c; font-weight:bold'
                return ''

            st.dataframe(
                _gap_df.style.map(_style_gap_cell, subset=[_gap_col_name]),
                use_container_width=True,
                hide_index=True
            )
            st.caption(T("t5_gap_bench_caption", n=len(master)))

    # ── Tabel Ringkasan per Kuadran (dengan Inversi + Normalisasi) ───────────
    st.markdown("---")
    st.markdown(T("t5_quad_title"))
    st.markdown(T("t5_quad_desc", n=len(master)))

    # Kolom INFORM: higher = worse → harus diinvert sebelum normalisasi
    INFORM_HIGHER_IS_WORSE = {
        'LACK OF COPING CAPACITY', 'INFORM RISK', 'VULNERABILITY',
        'HAZARD & EXPOSURE', 'DRR', 'Institutional',
        'Physical infrastructure', 'Communication', 'INFORM - Infrastructure'
    }

    def _process_column(col, values_series):
        """
        Normalisasi min-max (0–1) dari seluruh sampel master.
        Untuk kolom INFORM (higher=worse): diinvert dulu → normalized = (max - v) / (max - min).
        Untuk kolom lain (higher=better): normalized = (v - min) / (max - min).
        Mengembalikan Series ternormalisasi.
        """
        col_min = master[col].min()
        col_max = master[col].max()
        if col_max == col_min:
            return pd.Series([0.5] * len(values_series), index=values_series.index)
        if col in INFORM_HIGHER_IS_WORSE:
            return (col_max - values_series) / (col_max - col_min)
        else:
            return (values_series - col_min) / (col_max - col_min)

    _quad_cols_avail = all(c in master.columns for c in ['NRI Score', 'WRI Score'])
    if _quad_cols_avail:
        _df_quad = master.dropna(subset=['NRI Score', 'WRI Score']).copy()
        _med_nri  = _df_quad['NRI Score'].median()
        _med_wri  = _df_quad['WRI Score'].median()

        def _assign_quad(row):
            hi_cap  = row['NRI Score'] >= _med_nri
            hi_risk = row['WRI Score'] >= _med_wri
            if hi_cap and not hi_risk:  return "Preventif"
            if not hi_cap and hi_risk:  return "Reaktif"
            if hi_cap and hi_risk:      return "Waspada"
            return "Pasif"

        _df_quad['_Kuadran'] = _df_quad.apply(_assign_quad, axis=1)
        _n_prev = (_df_quad['_Kuadran'] == "Preventif").sum()
        _n_reak = (_df_quad['_Kuadran'] == "Reaktif").sum()

        # Normalisasi seluruh kolom terlebih dahulu (dari seluruh 55 negara master)
        _df_norm = _df_quad.copy()
        for fk, fv in FASE_BENCANA.items():
            for col in fv['kolom']:
                if col in _df_norm.columns:
                    _df_norm[col] = _process_column(col, _df_norm[col])

        _quad_rows = []
        for fk, fv in FASE_BENCANA.items():
            fc_avail = [c for c in fv['kolom'] if c in _df_norm.columns]
            if not fc_avail:
                continue

            _prev_df = _df_norm[_df_norm['_Kuadran'] == "Preventif"][fc_avail]
            _reak_df = _df_norm[_df_norm['_Kuadran'] == "Reaktif"][fc_avail]

            avg_prev = round(_prev_df.mean(axis=1).mean(), 3) if not _prev_df.empty else None
            avg_reak = round(_reak_df.mean(axis=1).mean(), 3) if not _reak_df.empty else None
            gap      = round(avg_prev - avg_reak, 3) if (avg_prev is not None and avg_reak is not None) else None

            # Setelah normalisasi + inversi, SEMUA kolom konsisten: lebih tinggi = lebih baik
            # Jadi gap positif selalu berarti Preventif lebih baik
            if gap is not None:
                gap_label = f"{'🟢 +' if gap > 0 else '🔴 '}{gap}"
            else:
                gap_label = "—"

            _prev_col_hdr = T("quad_preventif").split(" — ")[0] + f" (n={_n_prev})"
            _reak_col_hdr = T("quad_reaktif").split(" — ")[0] + f" (n={_n_reak})"
            _quad_rows.append({
                T("t5_fase_sendai"): f"{fv['icon']} {fk}",
                T("t5_acuan_sendai"): fv['acuan'].replace("Sendai Framework ", ""),
                _prev_col_hdr: avg_prev,
                _reak_col_hdr: avg_reak,
                T("t5_gap_col"): gap_label,
            })

        if _quad_rows:
            df_quad_tbl = pd.DataFrame(_quad_rows)

            def _style_quad(val):
                if not isinstance(val, str): return ''
                if val.startswith('🟢'): return 'color:#2ca02c; font-weight:bold'
                if val.startswith('🔴'): return 'color:#d62728; font-weight:bold'
                return ''

            def _style_prev(val):
                if not isinstance(val, (int, float)) or pd.isna(val): return ''
                return 'background-color: rgba(44,160,44,0.08)'

            def _style_reak(val):
                if not isinstance(val, (int, float)) or pd.isna(val): return ''
                return 'background-color: rgba(214,39,40,0.08)'

            prev_col = T("quad_preventif").split(" — ")[0] + f" (n={_n_prev})"
            reak_col = T("quad_reaktif").split(" — ")[0] + f" (n={_n_reak})"
            gap_col  = T("t5_gap_col")

            st.dataframe(
                df_quad_tbl.style
                    .map(_style_prev, subset=[prev_col])
                    .map(_style_reak, subset=[reak_col])
                    .map(_style_quad, subset=[gap_col]),
                use_container_width=True,
                hide_index=True
            )
            st.caption(
                T("t5_quad_table_cap",
                  n=len(master),
                  med_nri=f"{_med_nri:.1f}", med_wri=f"{_med_wri:.1f}",
                  n_prev=_n_prev, n_reak=_n_reak)
            )
            if _lang() == "id":
                st.info(
                    "**Mengapa hanya dua kuadran yang dibandingkan?** "
                    "Tabel ini hanya menampilkan kuadran **Preventif** (Teknologi Tinggi / Risiko Rendah) dan **Reaktif** (Teknologi Rendah / Risiko Tinggi) "
                    "karena penelitian bertujuan menguji apakah kapasitas teknologi tinggi berkorelasi dengan ketangguhan fase bencana yang lebih baik. "
                    "Perbandingan dua kutub ekstrem ini menghasilkan kontras paling kuat untuk menjawab pertanyaan tersebut. "
                    "Kuadran **Waspada** (Teknologi Tinggi / Risiko Tinggi) dan **Pasif** (Teknologi Rendah / Risiko Rendah) tidak diikutkan "
                    "karena kondisinya bersifat campuran dan kurang relevan terhadap argumen utama penelitian."
                )
            else:
                st.info(
                    "**Why only two quadrants are compared?** "
                    "This table only shows the **Preventive** (High Technology / Low Risk) and **Reactive** (Low Technology / High Risk) quadrants "
                    "because the research aims to test whether high technology capacity correlates with better disaster phase resilience. "
                    "Comparing these two extreme poles provides the strongest contrast to answer this question. "
                    "The **Alert** (High Technology / High Risk) and **Passive** (Low Technology / Low Risk) quadrants are excluded "
                    "because their conditions are mixed and less relevant to the main research argument."
                )

            # Insight otomatis berdasarkan gap terbesar
            _fase_key    = T("t5_fase_sendai")
            _gap_vals = [(r[_fase_key], r[reak_col], r[prev_col])
                         for r in _quad_rows
                         if isinstance(r[prev_col], (int, float))
                         and isinstance(r[reak_col], (int, float))]
            if _gap_vals:
                _biggest  = max(_gap_vals, key=lambda x: abs((x[2] or 0) - (x[1] or 0)))
                _gap_abs  = round(abs((_biggest[2] or 0) - (_biggest[1] or 0)), 3)
                st.info(T("t5_insight_quad", fase=_biggest[0], gap=f"{_gap_abs:.3f}"))
    else:
        st.warning(T("t5_no_nri_wri"))


# ════════════════════════════════════
# TAB 6 — PETA & DRILL-DOWN GUNUNG BERAPI
# Menampilkan peta interaktif distribusi gunung berapi per negara
# (dari Smithsonian GVP). Pengguna bisa memilih negara lalu melihat:
#   - Peta titik gunung (ukuran & warna = frekuensi erupsi)
#   - Metrik ringkasan (jumlah gunung, Max VEI, WRI, EM-DAT)
#   - Tabel & timeline riwayat erupsi 1900–2025
# Koordinat diambil dari df_gun; riwayat dari df_hist.
# ════════════════════════════════════
with tab6:
    st.subheader(T("t6_subheader"))
    _indo_erupsi = int(master.loc[master['Negara'] == INDO, 'Frekuensi_Erupsi'].values[0]) if INDO else 0
    _indo_rank_eru = int(master['Frekuensi_Erupsi'].rank(ascending=False).loc[master['Negara'] == INDO].values[0]) if INDO else 1
    st.markdown(T("t6_tab_desc", erupsi=f"{_indo_erupsi:,}", rank=_indo_rank_eru, total=len(master)))

    sel_list = sorted(master[master['Jumlah_Gunung'] > 0]['Negara'].unique().tolist())
    sel = st.selectbox(T("t6_select"), sel_list,
                       index=sel_list.index(INDO) if INDO and INDO in sel_list else 0)

    sr = master[master['Negara'] == sel]
    if not sr.empty:
        sr = sr.iloc[0]
        sm1, sm2, sm3, sm4, sm5 = st.columns(5)
        sm1.metric(T("t6_metric_volc"), int(sr['Jumlah_Gunung']))
        sm2.metric(T("t6_metric_freq"), int(sr['Frekuensi_Erupsi']))
        sm3.metric(T("t6_metric_maxvei"), f"{sr['Max_VEI']:.0f}" if pd.notna(sr['Max_VEI']) else "N/A")
        sm4.metric(T("t6_metric_wri"), f"{sr['WRI Score']:.2f}" if pd.notna(sr.get('WRI Score')) else "N/A")
        sm5.metric(T("t6_metric_cat"), WRI_KEY_TO_LABEL.get(sr['Kategori Risiko WRI'], sr['Kategori Risiko WRI']))

        # EM-DAT metrics row
        has_emdat = any(c in master.columns for c in ['EMDAT_Total_Deaths', 'EMDAT_Events'])
        if has_emdat:
            st.markdown(T("t6_emdat_header"))
            em1, em2, em3, em4 = st.columns(4)
            emdat_row = master[master['Negara'] == sel].iloc[0] if not master[master['Negara'] == sel].empty else None
            if emdat_row is not None:
                em1.metric(T("t6_emdat_deaths"),   f"{int(emdat_row.get('EMDAT_Total_Deaths', 0)):,}")
                em2.metric(T("t6_emdat_affected"), f"{int(emdat_row.get('EMDAT_Total_Affected', 0)):,}")
                em3.metric(T("t6_emdat_events"),   f"{int(emdat_row.get('EMDAT_Events', 0)):,}")
                dmg = emdat_row.get('EMDAT_Total_Damage_USD', 0)
                em4.metric(T("t6_emdat_damage"), f"${int(dmg):,} {T('t6_damage_unit')}" if dmg > 0 else "N/A")
            st.caption(T("t6_emdat_caption"))

    gn = df_gun[df_gun['Country_clean'] == sel].copy()

    def fix_coord(val, is_lat=True):
        s = str(val).strip(); lim = 90 if is_lat else 180
        if ',' in s:
            try:
                v = float(s.replace(',', '.')); return v if abs(v) <= lim else None
            except: return None
        if '.' in s:
            try:
                v = float(s); return v if abs(v) <= lim else None
            except: return None
        try:
            v = float(s)
            if abs(v) <= lim: return v
            v1 = v / 1000
            if abs(v1) <= lim: return v1
            v2 = v / 10000
            return v2 if abs(v2) <= lim else None
        except: return None

    if 'Latitude'  in gn.columns: gn['Latitude']  = gn['Latitude'].apply(lambda x: fix_coord(x, True))
    if 'Longitude' in gn.columns: gn['Longitude'] = gn['Longitude'].apply(lambda x: fix_coord(x, False))
    gn = gn.dropna(subset=['Latitude', 'Longitude'])

    cm1, cm2 = st.columns([3, 2])
    with cm1:
        if not gn.empty:
            gn['Volcano Number'] = gn['Volcano Number'].astype(str).str.split('.').str[0].str.strip()
            vg = df_hist.groupby('Volcano Number').agg(
                n_erupsi=('Start Year', 'count'), max_vei=('VEI', 'max')).reset_index()
            gn = gn.merge(vg, on='Volcano Number', how='left')
            gn['n_erupsi'] = gn['n_erupsi'].fillna(0).astype(int)
            gn['size_m']   = gn['n_erupsi'].clip(lower=1).apply(lambda x: min(x / 20 + 3, 10))
            fig_map = px.scatter_mapbox(
                gn, lat='Latitude', lon='Longitude', hover_name='Volcano Name',
                hover_data={c: True for c in ['Primary Volcano Type', 'Last Known Eruption',
                                               'Elevation (m)', 'n_erupsi', 'max_vei'] if c in gn.columns},
                size='size_m', color='n_erupsi', color_continuous_scale='Plasma',
                size_max=10, zoom=3, mapbox_style="carto-darkmatter",
                opacity=0.65,
                title=T("t6_map_title", country=sel))
            fig_map.update_layout(
                margin={"r": 0, "t": 45, "l": 0, "b": 0},
                coloraxis_colorbar=dict(title=T("t6_freq_erupsi"), thickness=12, len=0.6))
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning(T("t6_no_coord"))
    with cm2:
        if not gn.empty:
            sg = [c for c in ['Volcano Name', 'Primary Volcano Type', 'Last Known Eruption',
                               'Elevation (m)', 'n_erupsi', 'max_vei'] if c in gn.columns]
            st.dataframe(gn[sg].sort_values('n_erupsi', ascending=False).reset_index(drop=True),
                         use_container_width=True, hide_index=True, height=350)

    st.markdown("---")
    st.markdown(T("t6_history_header", country=sel))
    with st.expander(T("t6_vei_expander")):
        st.markdown(T("t6_vei_body"))
    gids = df_gun[df_gun['Country_clean'] == sel]['Volcano Number'].astype(str).str.split('.').str[0].str.strip().tolist()
    df_hs = df_hist[df_hist['Volcano Number'].isin(gids)].copy()
    if not df_hs.empty:
        f1, f2, f3 = st.columns(3)
        with f1: min_vei = st.slider(T("t6_min_vei"), 0, 7, 0, key="mv")
        with f2: yr_r    = st.slider(T("t6_year_range"), 1900, 2025, (1900, 2025), key="yr")
        with f3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(T("t6_download_btn", country=sel),
                               data=df_hs.to_csv(index=False).encode('utf-8'),
                               file_name=f"erupsi_{sel.lower().replace(' ', '_')}.csv",
                               mime="text/csv", use_container_width=True)
        df_hf = df_hs[(df_hs['Start Year'] >= yr_r[0]) & (df_hs['Start Year'] <= yr_r[1])].copy()
        if min_vei > 0: df_hf = df_hf[df_hf['VEI'] >= min_vei]
        sh = [c for c in ['Volcano Name', 'Start Year', 'VEI', 'Eruption Category'] if c in df_hf.columns]
        st.dataframe(df_hf[sh].sort_values('Start Year', ascending=False).reset_index(drop=True),
                     use_container_width=True, hide_index=True, height=260)
        if len(df_hf) > 0:
            tl = df_hf.groupby('Start Year').agg(Jml=('Start Year', 'count'), MaxVEI=('VEI', 'max')).reset_index()
            ft = px.bar(tl, x='Start Year', y='Jml', color='MaxVEI', color_continuous_scale='YlOrRd',
                        title=T("t6_tl_title", country=sel), height=260)
            ft.update_layout(plot_bgcolor="white", coloraxis_colorbar=dict(title="Max VEI"))
            ft.update_xaxes(showgrid=False)
            ft.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
            st.plotly_chart(ft, use_container_width=True)
    else:
        st.info(T("t6_no_history"))


# ════════════════════════════════════
# TAB 7 — DATA LENGKAP & UNDUH
# Menampilkan populasi penuh 75 negara vulkanik (master_full)
# sebelum listwise deletion, dengan highlight oranye untuk negara
# yang dieksklusi dari sampel analitik karena data tidak lengkap.
# Juga menampilkan alur seleksi sampel & statistik deskriptif.
# ════════════════════════════════════
with tab7:
    _n_excl7 = len(master_full) - len(master)  # Hitung jumlah negara yang dieksklusi
    st.subheader(T("t7_subheader", n=len(master_full)))
    st.markdown(T("t7_desc", n_full=len(master_full), n_sample=len(master), n_excl=_n_excl7))

    # Set nama negara yang MASUK sampel analitik (untuk highlight baris eksklusi)
    _negara_sampel = set(master['Negara'].tolist())

    c1t, c2t, c3t = st.columns([2, 1, 1])
    with c1t: srch7 = st.text_input(T("t7_search"), placeholder=T("t7_search_hint"), key="srch7")
    with c3t:
        st.markdown("<br>", unsafe_allow_html=True)
        # Tombol download seluruh data populasi (75 negara) sebagai CSV
        st.download_button(
            T("t7_download_btn", n=len(master_full)),
            data=master_full.to_csv(index=False).encode('utf-8'),
            file_name="master_vulkanik_populasi.csv",
            mime="text/csv",
            use_container_width=True
        )

    df_sh = master_full.copy()  # Tampilkan populasi penuh (bukan hanya sampel)
    if srch7:  # Filter pencarian negara jika ada input
        df_sh = df_sh[df_sh['Negara'].str.contains(srch7, case=False, na=False)]

    # Pilih kolom yang ditampilkan di tabel (hanya yang tersedia di dataset)
    scols7 = [c for c in ['Negara', 'Kategori Risiko WRI', 'Kelengkapan_Data (%)', 'WRI Score',
                           'NRI Score', 'GII Score', 'GDP Per Capita 2024',
                           'Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI',
                           'Exposure', 'Vulnerability', 'Lack of Coping Capacities',
                           'INFORM RISK', 'DRR', 'Communication'] if c in df_sh.columns]
    # Urutkan: negara dengan kelengkapan data terbanyak di atas
    df_srt7 = df_sh[scols7].sort_values('Kelengkapan_Data (%)', ascending=False, na_position='last').reset_index(drop=True)

    # Rename kolom ke label yang ramah pengguna (bahasa aktif)
    _special7 = {
        'Negara':              T("negara_kol"),
        'Kategori Risiko WRI': ("WRI Risk Category" if _lang()=="en" else "Kategori Risiko WRI"),
        'Kelengkapan_Data (%)': ("Data Completeness (%)" if _lang()=="en" else "Kelengkapan Data (%)"),
    }
    rename7 = {}
    for c in scols7:
        if c in _special7:
            rename7[c] = _special7[c]
        elif c in LABEL_PANJANG:
            rename7[c] = LABEL_PANJANG[c]
    df_srt7_display = df_srt7.rename(columns=rename7)

    def hi7(row):
        """Highlight oranye: negara yang TIDAK masuk sampel analitik (kena listwise deletion).
        Negara berwarna oranye = datanya tidak lengkap di ≥1 indikator OLS utama."""
        if row.get('Negara') is not None and row['Negara'] not in _negara_sampel:
            return ['background-color: #ffe0cc; color: #7a3a00;'] * len(row)
        return [''] * len(row)  # Putih = masuk sampel analitik

    # Tampilkan tabel dengan highlight oranye untuk negara yang dieksklusi
    st.dataframe(df_srt7_display.style.apply(hi7, axis=1), use_container_width=True, height=500)

    n_ekskl = len(master_full) - len(master)
    st.caption(T("t7_table_cap", n_show=len(df_sh), n_full=len(master_full),
                 n_excl=n_ekskl, n_sample=len(master)))

    # ── Alur Seleksi Sampel: GVP → Eksklusi → Listwise Deletion ──
    st.markdown("---")
    st.markdown(T("t7_flow_title"))
    col_alur1, col_alur2, col_alur3 = st.columns(3)
    col_alur1.metric(T("t7_metric_pop"), f"77 {T('t7_country_label')}",    # Populasi awal GVP
                     delta=T("t7_flow_pop_delta"))
    col_alur2.metric(T("t7_metric_excl"), f"{len(master_full)} {T('t7_country_label')}",  # Setelah eksklusi Antartika & Taiwan
                     delta=T("t7_excl_delta"), delta_color="inverse")
    col_alur3.metric(T("t7_metric_sample"), f"{len(master)} {T('t7_country_label')}",     # Sampel analitik final
                     delta=T("t7_excl_listwise", n=n_ekskl), delta_color="inverse")

    # ── Statistik Deskriptif Sampel Analitik ──
    st.markdown("---")
    st.markdown(T("t7_stat_header", n=len(master)))
    st.caption(T("t7_stat_caption", n=len(master), n_full=len(master_full)))
    # Pilih kolom numerik utama untuk dihitung statistiknya
    stc = [c for c in ['WRI Score', 'NRI Score', 'GII Score', 'GDP Per Capita 2024',
                        'Jumlah_Gunung', 'Frekuensi_Erupsi', 'Max_VEI',
                        'INFORM RISK', 'LACK OF COPING CAPACITY', 'DRR',
                        'Lack of Coping Capacities'] if c in master.columns]
    desc = master[stc].describe().round(2)  # .describe() = count, mean, std, min, 25%, 50%, 75%, max
    desc.columns = [LABEL_PANJANG.get(c, c) for c in desc.columns]  # Ganti header kolom ke label panjang
    st.dataframe(desc, use_container_width=True)

