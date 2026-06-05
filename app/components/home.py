import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from app.utils import C, page_header


def render():
    page_header("Burnout Prediction System",
                "Sistem prediksi tingkat burnout karyawan, perbandingan metode Fuzzy Mamdani dan Sugeno")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>Dataset</div>
  {_row('Sumber',         'Are Your Employees Burning Out?')}
  {_row('Total data',     '22.750 baris')}
  {_row('Variabel input', '5 variabel')}
  {_row('Output',         'Burn Rate (0.0 – 1.0)')}
  {_row('Ground truth',   'MAE, MSE, RMSE', last=True)}
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>Sistem Fuzzy</div>
  {_row('Metode',              'Mamdani &amp; Sugeno')}
  {_row('Rule base',           '20 rules')}
  {_row('Membership function', 'Trapezoid &amp; Triangle')}
  {_row('Defuzzifikasi',       'Centroid / Weighted Average')}
  {_row('Operator AND',        'Minimum (min)', last=True)}
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>
    Variabel Input</div>
  <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:10px'>
    {_vcard('Mental Fatigue Score','Range: 0 – 10','Low / Medium / High')}
    {_vcard('Resource Allocation', 'Range: 1 – 10','Low / Medium / High')}
    {_vcard('Designation Level',   'Range: 0 – 5', 'Junior / Mid / Senior')}
  </div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>
    {_vcard('WFH Setup Available','Binary','Yes / No')}
    {_vcard('Company Type','Binary','Product / Service')}
  </div>
</div>""", unsafe_allow_html=True)


def _row(label, val, last=False):
    bdr = '' if last else f"border-bottom:0.5px solid {C['gray_light']};"
    return (f"<div style='display:flex;justify-content:space-between;"
            f"align-items:center;padding:8px 0;{bdr}'>"
            f"<span style='font-size:13px;color:{C['gray']}'>{label}</span>"
            f"<span style='font-size:13px;font-weight:500;color:{C['black']};text-align:right'>{val}</span>"
            f"</div>")

def _vcard(title, sub1, sub2):
    return (f"<div style='background:{C['pink_bg']};border:0.5px solid {C['pink_light']};"
            f"border-radius:8px;padding:12px;text-align:center'>"
            f"<div style='font-size:13px;font-weight:600;color:{C['black']};margin-bottom:4px'>{title}</div>"
            f"<div style='font-size:12px;color:{C['gray']}'>{sub1}</div>"
            f"<div style='font-size:12px;color:{C['gray']}'>{sub2}</div></div>")
