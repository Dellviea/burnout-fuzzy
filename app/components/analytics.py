"""components/analytics.py — Tab Analisis Data"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from app.utils import C, page_header, load_data, section_header


def render():
    page_header("Analisis Data",
                "Distribusi dan statistik dataset 22.750 baris · Kaggle: Are Your Employees Burning Out?")
    df = load_data()

    # ── Statistik Deskriptif ──────────────────────────
    st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-bottom:14px'>
  {section_header('Statistik Deskriptif')}
  <table style='width:100%;font-size:13px;border-collapse:collapse'>
    <tr style='border-bottom:1.5px solid {C['pink_light']}'>
      {_th('Variabel', left=True)}{_th('Min')}{_th('Max')}{_th('Rata-rata')}{_th('Std. Dev')}
    </tr>
    {_stat_row(df,'Mental Fatigue Score')}
    {_stat_row(df,'Resource Allocation')}
    {_stat_row(df,'Designation')}
    {_stat_row(df,'Burn Rate', last=True)}
  </table>
</div>""", unsafe_allow_html=True)

    # ── 4 histogram ───────────────────────────────────
    chart_data = [
        ('Mental Fatigue Score','Distribusi Mental Fatigue Score','Nilai (0–10)'),
        ('Resource Allocation', 'Distribusi Resource Allocation', 'Nilai (1–10)'),
        ('Designation',         'Distribusi Designation Level',   'Level (0–5)'),
        ('Burn Rate',           'Distribusi Burn Rate',           'Burn Rate (0–1)'),
    ]
    c1, c2 = st.columns(2)
    for i, (col, title, xlabel) in enumerate(chart_data):
        with (c1 if i % 2 == 0 else c2):
            fig, ax = plt.subplots(figsize=(5, 3.2))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            n, bins, patches = ax.hist(df[col].dropna(), bins=12,
                                       edgecolor='white', linewidth=0.5)
            for j, patch in enumerate(patches):
                ratio = j / max(len(patches)-1, 1)
                r = int(0xF4 - (0xF4-0xD4)*ratio)
                g = int(0xC0 - (0xC0-0x53)*ratio)
                b = int(0xD1 - (0xD1-0x7E)*ratio)
                patch.set_facecolor(f'#{r:02x}{g:02x}{b:02x}')
            mean_v = df[col].mean()
            ax.axvline(mean_v, color=C['pink_dark'], linestyle='--',
                       linewidth=1.5, alpha=0.8)
            ymax = ax.get_ylim()[1]
            ax.text(mean_v + (bins[-1]-bins[0])*0.02, ymax*0.93,
                    f'μ={mean_v:.2f}', fontsize=9,
                    color=C['pink_dark'], fontweight='700')
            ax.set_xlabel(xlabel, fontsize=11, color=C['gray_dark'])
            ax.set_ylabel('Frekuensi', fontsize=11, color=C['gray_dark'])
            ax.tick_params(labelsize=10, colors=C['gray'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(C['gray_light'])
            ax.spines['bottom'].set_color(C['gray_light'])
            plt.tight_layout(pad=0.8)

            st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:14px 14px 0 14px;margin-bottom:4px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:10px'>
    {title}</div>""", unsafe_allow_html=True)
            st.pyplot(fig, use_container_width=True)
            plt.close()
            std_v = df[col].std()
            st.markdown(f"""
  <div style='font-size:12px;color:{C['gray']};padding:6px 0 10px 0'>
    Rata-rata {mean_v:.2f} &nbsp;·&nbsp; Std. dev {std_v:.2f}
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── Company Type & WFH ────────────────────────────
    c3, c4 = st.columns(2)
    with c3:
        vc    = df['Company Type'].value_counts()
        total = vc.sum()
        rows  = "".join([_hbar(k, round(v/total*100)) for k, v in vc.items()])
        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-bottom:12px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>
    Company Type</div>
  {rows}
  <div style='font-size:12px;color:{C['gray']};margin-top:8px'>
    Perusahaan jenis Service sedikit lebih dominan</div>
</div>""", unsafe_allow_html=True)

    with c4:
        vw    = df['WFH Setup Available'].value_counts()
        total = vw.sum()
        rows  = "".join([_hbar(k, round(v/total*100)) for k, v in vw.items()])
        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-bottom:12px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>
    WFH Setup Tersedia</div>
  {rows}
  <div style='font-size:12px;color:{C['gray']};margin-top:8px'>
    Distribusi hampir seimbang antara WFH dan non-WFH</div>
</div>""", unsafe_allow_html=True)

    # ── Missing Values ────────────────────────────────
    st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:15px;font-weight:700;color:{C['black']};margin-bottom:12px'>
    Missing Values (Setelah Preprocessing)</div>
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:10px'>
    {_mv('0%','Burn Rate')}
    {_mv('0%','Mental Fatigue')}
    {_mv('0%','Resource Alloc.')}
    {_mv('Median','Metode imputasi', info=True)}
  </div>
</div>""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────
def _th(t, left=False):
    align = "left" if left else "center"
    return (f"<th style='text-align:{align};padding:8px 0;color:{C['gray']};font-weight:600;"
            f"font-size:12px;text-transform:uppercase;letter-spacing:0.5px'>{t}</th>")

def _stat_row(df, col, last=False):
    bdr = '' if last else f"border-bottom:0.5px solid {C['gray_light']};"
    s   = df[col].describe()
    return (f"<tr>"
            f"<td style='padding:9px 0;{bdr};font-weight:500;text-align:left'>{col}</td>"
            f"<td style='padding:9px 0;{bdr};text-align:center;color:{C['gray_dark']}'>{s['min']:.1f}</td>"
            f"<td style='padding:9px 0;{bdr};text-align:center;color:{C['gray_dark']}'>{s['max']:.1f}</td>"
            f"<td style='padding:9px 0;{bdr};text-align:center;color:{C['gray_dark']}'>{s['mean']:.2f}</td>"
            f"<td style='padding:9px 0;{bdr};text-align:center;color:{C['gray_dark']}'>{s['std']:.2f}</td>"
            f"</tr>")

def _hbar(label, pct):
    return (f"<div style='margin-bottom:10px'>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:13px;color:{C['black']};font-weight:500'>{label}</span>"
            f"<span style='font-size:13px;font-weight:700;color:{C['pink_dark']}'>{pct}%</span></div>"
            f"<div style='height:10px;background:{C['gray_light']};border-radius:5px;overflow:hidden'>"
            f"<div style='height:100%;width:{pct}%;background:{C['pink']};border-radius:5px'></div>"
            f"</div></div>")

def _mv(val, lbl, info=False):
    clr  = C['green'] if val == '0%' else C['pink_dark']
    size = '14px' if info else '20px'
    return (f"<div style='background:{C['bg']};border-radius:8px;padding:12px;text-align:center'>"
            f"<div style='font-size:{size};font-weight:700;color:{clr};margin-bottom:4px'>{val}</div>"
            f"<div style='font-size:12px;color:{C['gray']}'>{lbl}</div></div>")
