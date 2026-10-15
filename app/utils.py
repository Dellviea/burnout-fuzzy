import os
import numpy as np
import pandas as pd
import streamlit as st

C = {
    'pink':        '#BF3B69',   # >=4.5:1 di atas putih (WCAG AA)
    'pink_dark':   '#993556',
    'pink_darker': '#72243E',
    'pink_light':  '#F4C0D1',
    'pink_med':    '#ED93B1',
    'pink_bg':     '#FFF0F5',
    'pink_soft':   '#FBEAF0',
    'blue':        '#2B6CB0',
    'blue_dark':   '#185FA5',
    'blue_bg':     '#E6F1FB',
    'blue_light':  '#B5D4F4',
    'gray':        '#666666',   # >=4.5:1 di atas putih & pink_bg
    'gray_dark':   '#444444',
    'gray_light':  '#EEEEEE',
    'bg':          '#F7F7F7',
    'white':       '#FFFFFF',
    'black':       '#111111',
    'green':       '#27500A',
    'green_bg':    '#EAF3DE',
}

# Warna semantik per level burnout, dipakai di badge, meter, dan grafik MF output
LEVEL = {
    'LOW':      '#2E7D32',
    'MODERATE': '#E07B00',
    'HIGH':     '#D81B60',
    'SEVERE':   '#7A1340',
}

def inject_css():
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
.stApp {{ background: {C['white']}; }}

/* ── Sembunyikan semua chrome Streamlit ── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"],
button[data-testid="stBaseButton-header"],
button[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu, footer {{ display: none !important; visibility: hidden !important; }}

/* ── Sidebar — fixed, tidak bisa collapse ── */
[data-testid="stSidebar"] {{
    background: {C['pink_bg']} !important;
    border-right: 1.5px solid {C['pink_light']} !important;
    min-width: 240px !important;
    max-width: 240px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}
[data-testid="stSidebar"] > div > div {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}
[data-testid="stSidebar"] > div > div > div {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}
[data-testid="stSidebar"] section,
[data-testid="stSidebar"] section > div {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}
[data-testid="stSidebar"] label {{
    color: {C['black']} !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}}
[data-testid="stSidebarCollapseButton"] {{
    display: none !important;
}}

/* ── Block container ── */
.block-container,
[data-testid="stMainBlockContainer"] {{
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}}

/* ── Tabs — sticky + full width + bold + no emoji ── */
.stTabs [role="tablist"] {{
    position: sticky !important;
    top: 0 !important;
    z-index: 9999 !important;
    background: {C['white']} !important;
    border-bottom: 2px solid {C['pink_light']} !important;
    gap: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    display: flex !important;
    box-shadow: 0 2px 6px rgba(212,83,126,0.07) !important;
}}
.stTabs [role="tab"] {{
    flex: 1 1 0 !important;
    color: {C['gray']} !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 14px 4px !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    background: transparent !important;
    margin-bottom: -2px !important;
    text-align: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    transition: all 0.15s !important;
    min-width: 0 !important;
}}
.stTabs div:has(> [role="tablist"]) {{ width: 100% !important; }}
.stTabs [role="tab"] p {{
    font-size: inherit !important;
    font-weight: inherit !important;
    color: inherit !important;
}}
.stTabs [role="tab"]:hover {{
    color: {C['pink']} !important;
    background: {C['pink_bg']} !important;
}}
.stTabs [aria-selected="true"] {{
    color: {C['pink_dark']} !important;
    background: {C['pink_bg']} !important;
    border-bottom: 3px solid {C['pink']} !important;
    font-weight: 800 !important;
}}
.stTabs [role="tabpanel"] {{
    padding-top: 20px !important;
}}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"],
.stTabs .react-aria-SelectionIndicator {{
    display: none !important;
}}
/* Garis full width via pseudo element */
.stTabs [role="tablist"]::after {{
    content: '' !important;
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 2px !important;
    background: {C['pink_light']} !important;
    z-index: -1 !important;
}}

/* ── Metric ── */
[data-testid="stMetric"] {{
    background: {C['white']} !important;
    border: 1px solid {C['pink_light']} !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}}
[data-testid="stMetric"] label, [data-testid="stMetricLabel"] p {{
    color: {C['pink_dark']} !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}}
[data-testid="stMetricValue"] {{
    color: {C['black']} !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}}
[data-testid="stMetricDelta"] {{ display: none !important; }}

/* ── Button utama (Jalankan Prediksi & Evaluasi) ── */
.stButton > button {{
    background: {C['pink']} !important;
    color: {C['white']} !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 10px 28px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    box-shadow: 0 2px 8px rgba(212,83,126,0.25) !important;
    transition: background 0.15s !important;
}}
.stButton > button:hover {{
    background: {C['pink_dark']} !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] [role="slider"] {{
    background: {C['pink']} !important;
    border-color: {C['pink']} !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    border-color: {C['pink_light']} !important;
    border-radius: 8px !important;
    background: {C['white']} !important;
    font-size: 13px !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {C['pink_light']}; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)


def level_color(level):
    return {
        'LOW':      ('#E8F5E9', '#1B5E20', LEVEL['LOW']),
        'MODERATE': ('#FFF8E1', '#B34700', LEVEL['MODERATE']),
        'HIGH':     ('#FCE4EC', '#AD1457', LEVEL['HIGH']),
        'SEVERE':   (C['pink_soft'], LEVEL['SEVERE'], LEVEL['SEVERE']),
    }.get(level, (C['pink_bg'], C['pink_dark'], C['pink']))


def recommendations(level):
    return {
        'LOW': [
            "Pertahankan keseimbangan kerja dan istirahat",
            "Jaga kualitas tidur yang cukup",
            "Lanjutkan kebiasaan kerja yang sehat",
        ],
        'MODERATE': [
            "Atur jadwal istirahat lebih teratur",
            "Pertimbangkan untuk bicara dengan atasan",
            "Batasi lembur yang tidak perlu",
            "Lakukan aktivitas relaksasi rutin",
        ],
        'HIGH': [
            "Ambil jeda istirahat rutin setiap hari",
            "Pertimbangkan opsi kerja dari rumah (WFH)",
            "Kurangi beban kerja bersama atasan",
            "Konsultasi ke HR atau supervisor",
            "Prioritaskan tidur 7–8 jam per malam",
        ],
        'SEVERE': [
            "Ambil cuti untuk pemulihan segera",
            "Konsultasi ke profesional kesehatan mental",
            "Komunikasikan kondisi ke HR untuk redistribusi kerja",
            "Hindari lembur saat ini",
            "Minta dukungan dari keluarga atau orang terdekat",
        ],
    }.get(level, [])


def compute_metrics(actual, pred):
    mae  = float(np.mean(np.abs(actual - pred)))
    mse  = float(np.mean((actual - pred) ** 2))
    rmse = float(np.sqrt(mse))
    return round(mae, 4), round(mse, 4), round(rmse, 4)


@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, 'data', 'train.csv')
    df   = pd.read_csv(path)
    df   = df.drop(columns=['Employee ID', 'Date of Joining', 'Gender'], errors='ignore')
    df['WFH_encoded']     = df['WFH Setup Available'].map({'Yes': 1, 'No': 0})
    df['Company_encoded'] = df['Company Type'].map({'Product': 1, 'Service': 0})
    df   = df.dropna(subset=['Burn Rate'])   # target tidak boleh diimputasi (ground truth)
    for col in ['Mental Fatigue Score', 'Resource Allocation']:
        df[col] = df[col].fillna(df[col].median())
    return df


def page_header(title, subtitle):
    st.markdown(f"""
<div style='padding:4px 0 16px 0;margin-bottom:20px;
border-bottom:2px solid {C['pink_light']}'>
  <h1 style='font-size:26px;font-weight:800;color:{C['black']};
  margin:0 0 6px 0;letter-spacing:-0.5px;line-height:1.2'>{title}</h1>
  <p style='font-size:13px;color:{C['gray']};margin:0;font-weight:400'>{subtitle}</p>
</div>""", unsafe_allow_html=True)


def section_header(title, subtitle=""):
    sub = f"<div style='font-size:12px;color:{C['gray']};margin-top:3px'>{subtitle}</div>" if subtitle else ""
    return f"""<div style='margin-bottom:14px'>
  <div style='font-size:17px;font-weight:700;color:{C['black']}'>{title}</div>
  {sub}
</div>"""
