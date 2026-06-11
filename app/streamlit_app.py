import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.utils      import inject_css
from app.sidebar    import render_sidebar
from app.components import home, predict, membership, evaluasi

st.set_page_config(
    page_title="BurnSense AI",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

fatigue, resource, designation, wfh, company = render_sidebar()

tab1, tab2, tab3, tab4 = st.tabs([
    "Home",
    "Prediksi",
    "Membership Function",
    "Evaluasi",
])

with tab1: home.render()
with tab2: predict.render(fatigue, resource, designation, wfh, company)
with tab3: membership.render()
with tab4: evaluasi.render()
