import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from fuzzy.membership import fuzzify_all
from app.utils import C


def render_sidebar():
    """
    Render sidebar. Return: (fatigue, resource, designation, wfh_enc, company_enc)
    """
    # Logo
    st.sidebar.markdown(f"""
<div style='padding:4px 0 14px 0;border-bottom:1.5px solid {C['pink_light']};margin-bottom:14px'>
  <div style='display:flex;align-items:center;gap:8px'>
    <div style='width:9px;height:9px;border-radius:50%;background:{C['pink']};flex-shrink:0'></div>
    <div style='font-size:15px;font-weight:700;color:{C['pink_darker']}'>BurnSense</div>
  </div>
  <div style='font-size:11px;color:{C['gray']};margin-top:2px;padding-left:17px'>Burnout Prediction System</div>
</div>
""", unsafe_allow_html=True)

    # -------- Input Karyawan -------------------------------------------
    st.sidebar.markdown(f"<div style='font-size:10px;color:{C['gray']};letter-spacing:0.7px;text-transform:uppercase;font-weight:600;margin-bottom:6px'>Input Karyawan</div>", unsafe_allow_html=True)

    fatigue     = st.sidebar.slider("Mental Fatigue Score", 0.0, 10.0, 7.0, 0.1)
    resource    = st.sidebar.slider("Resource Allocation",  1.0, 10.0, 8.0, 0.1)
    designation = st.sidebar.slider("Designation Level",    0,   5,    4,   1)

    st.sidebar.markdown(f"<div style='font-size:10px;color:{C['gray']};letter-spacing:0.7px;text-transform:uppercase;font-weight:600;margin-top:8px;margin-bottom:4px'>WFH Setup</div>", unsafe_allow_html=True)
    wfh = st.sidebar.selectbox("WFH Setup", ["No", "Yes"], label_visibility="collapsed")

    st.sidebar.markdown(f"<div style='font-size:10px;color:{C['gray']};letter-spacing:0.7px;text-transform:uppercase;font-weight:600;margin-top:6px;margin-bottom:4px'>Company Type</div>", unsafe_allow_html=True)
    company = st.sidebar.selectbox("Company Type", ["Product", "Service"], label_visibility="collapsed")

    wfh_enc     = 1 if wfh     == "Yes"     else 0
    company_enc = 1 if company == "Product" else 0

    # -------- Status Fuzzy realtime -------------------------------------------
    fuzz    = fuzzify_all(fatigue, resource, designation, wfh_enc, company_enc)
    fat_dom = max(fuzz['fatigue'],  key=fuzz['fatigue'].get)
    res_dom = max(fuzz['resource'], key=fuzz['resource'].get)
    des_dom = max(fuzz['desig'],    key=fuzz['desig'].get)
    fat_val = fuzz['fatigue'][fat_dom]
    res_val = fuzz['resource'][res_dom]

    st.sidebar.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:8px;padding:10px;margin-top:12px'>
  <div style='font-size:10px;color:{C['gray']};letter-spacing:0.7px;text-transform:uppercase;
  font-weight:600;margin-bottom:8px'>Status Fuzzy</div>
  <div style='display:grid;grid-template-columns:auto auto 1fr;row-gap:5px;font-size:11px;line-height:1.5'>
    <span style='color:{C['gray']}'>Fatigue</span>
    <span style='color:{C['gray']};padding:0 5px'>:</span>
    <span><b style='color:{C['pink_dark']}'>{fat_dom}</b>
          <span style='color:{C['gray']};font-size:10px'> ({fat_val:.2f})</span></span>
    <span style='color:{C['gray']}'>Workload</span>
    <span style='color:{C['gray']};padding:0 5px'>:</span>
    <span><b style='color:{C['pink_dark']}'>{res_dom}</b>
          <span style='color:{C['gray']};font-size:10px'> ({res_val:.2f})</span></span>
    <span style='color:{C['gray']}'>Level</span>
    <span style='color:{C['gray']};padding:0 5px'>:</span>
    <span><b style='color:{C['pink_dark']}'>{des_dom}</b></span>
    <span style='color:{C['gray']}'>WFH</span>
    <span style='color:{C['gray']};padding:0 5px'>:</span>
    <span><b style='color:{C['pink_dark']}'>{'YES' if wfh_enc else 'NO'}</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

    return fatigue, resource, designation, wfh_enc, company_enc
