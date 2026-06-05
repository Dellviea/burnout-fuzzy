import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from app.utils import C, page_header
from fuzzy.membership import get_mf_curves

COLORS = {
    'LOW':      C['pink_light'],
    'MEDIUM':   C['pink'],
    'HIGH':     C['pink_darker'],
    'JUNIOR':   C['pink_light'],
    'MID':      C['pink'],
    'SENIOR':   C['pink_darker'],
    'MODERATE': C['pink_med'],
    'SEVERE':   C['pink_darker'],
}


def _mf_chart(ax, curves, var_key, labels):
    cv = curves[var_key]
    for lbl in labels:
        ax.plot(cv['x'], cv[lbl], color=COLORS.get(lbl, C['pink']),
                linewidth=2.5, label=lbl.capitalize())
    ax.set_xlabel(cv['xlabel'], fontsize=11, color=C['gray_dark'])
    ax.set_ylabel('Derajat Keanggotaan', fontsize=11, color=C['gray_dark'])
    ax.set_ylim(-0.05, 1.2)
    ax.legend(fontsize=10, framealpha=0.5, loc='upper right',
              edgecolor=C['gray_light'])
    ax.tick_params(labelsize=10, colors=C['gray'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(C['gray_light'])
    ax.spines['bottom'].set_color(C['gray_light'])
    ax.grid(axis='y', color=C['gray_light'], linewidth=0.5, alpha=0.6)


def render():
    page_header("Membership Function",
                "Fungsi keanggotaan setiap variabel, Trapezoid &amp; Triangle · implementasi from scratch")

    curves = get_mf_curves()

    plots = [
        ('fatigue',     'Mental Fatigue Score (0–10)',  ['LOW','MEDIUM','HIGH']),
        ('resource',    'Resource Allocation (1–10)',   ['LOW','MEDIUM','HIGH']),
        ('designation', 'Designation Level (0–5)',      ['JUNIOR','MID','SENIOR']),
        ('output',      'Output Burn Rate (0–1)',       ['LOW','MODERATE','HIGH','SEVERE']),
    ]

    c1, c2 = st.columns(2)
    for i, (var_key, title, labels) in enumerate(plots):
        with (c1 if i % 2 == 0 else c2):
            fig, ax = plt.subplots(figsize=(5, 3.2))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            _mf_chart(ax, curves, var_key, labels)
            plt.tight_layout(pad=0.8)

            st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:14px 14px 0 14px;margin-bottom:4px'>
  <div style='font-size:13px;font-weight:700;color:{C['black']};margin-bottom:10px'>
    {title}</div>""", unsafe_allow_html=True)
            st.pyplot(fig, use_container_width=True)
            plt.close()
            st.markdown("</div>", unsafe_allow_html=True)

    # Tabel parameter -------------------------------------------
    st.markdown(f"""
<div style='background:{C['pink_bg']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-top:8px'>
  <div style='font-size:14px;font-weight:700;color:{C['black']};margin-bottom:4px'>
    Parameter Fungsi Keanggotaan</div>
  <div style='font-size:12px;color:{C['gray']};margin-bottom:14px'>
    Detail parameter setiap fungsi keanggotaan</div>
  <div style='background:{C['white']};border-radius:8px;overflow:hidden;
  border:0.5px solid {C['pink_light']}'>
  <table style='width:100%;font-size:13px;border-collapse:collapse'>
    <tr style='background:{C['pink_soft']}'>
      <th style='text-align:left;padding:10px 12px;color:{C['pink_dark']};
      font-size:11px;text-transform:uppercase;letter-spacing:0.5px;width:22%'>Variabel</th>
      <th style='text-align:left;padding:10px 12px;color:{C['pink_dark']};
      font-size:11px;text-transform:uppercase;letter-spacing:0.5px'>Label</th>
      <th style='text-align:left;padding:10px 12px;color:{C['pink_dark']};
      font-size:11px;text-transform:uppercase;letter-spacing:0.5px'>Tipe</th>
      <th style='text-align:left;padding:10px 12px;color:{C['pink_dark']};
      font-size:11px;text-transform:uppercase;letter-spacing:0.5px'>Parameter</th>
    </tr>
    {_prow('Mental Fatigue','LOW',    'Trapezoid','[0, 0, 2, 4]')}
    {_prow('',             'MEDIUM', 'Triangle', '[3, 5, 7]')}
    {_prow('',             'HIGH',   'Trapezoid','[6, 8, 10, 10]', alt=True)}
    {_prow('Resource Alloc.','LOW',  'Trapezoid','[1, 1, 3, 5]')}
    {_prow('',             'MEDIUM', 'Triangle', '[4, 5.5, 7]')}
    {_prow('',             'HIGH',   'Trapezoid','[6, 8, 10, 10]', alt=True)}
    {_prow('Designation',  'JUNIOR', 'Trapezoid','[0, 0, 1.5, 2.5]')}
    {_prow('',             'MID',    'Triangle', '[2, 3, 4]')}
    {_prow('',             'SENIOR', 'Trapezoid','[3.5, 4.5, 5, 5]', alt=True)}
    {_prow('Burn Rate',    'LOW',      'Trapezoid','[0, 0, 0.20, 0.35]')}
    {_prow('',             'MODERATE','Triangle', '[0.25, 0.45, 0.60]')}
    {_prow('',             'HIGH',    'Triangle', '[0.50, 0.65, 0.80]', alt=True)}
    {_prow('',             'SEVERE',  'Trapezoid','[0.70, 0.85, 1.0, 1.0]', last=True)}
  </table>
  </div>
</div>""", unsafe_allow_html=True)


def _prow(var, lbl, tipe, param, alt=False, last=False):
    bg  = C['white'] if not alt else '#FFF8FA'
    bdr = '' if last else f"border-bottom:0.5px solid {C['gray_light']};"
    return (f"<tr style='background:{bg}'>"
            f"<td style='padding:9px 12px;{bdr};color:{C['black']};font-weight:500'>{var}</td>"
            f"<td style='padding:9px 12px;{bdr};font-weight:700;color:{C['pink_dark']}'>{lbl}</td>"
            f"<td style='padding:9px 12px;{bdr};color:{C['gray']}'>{tipe}</td>"
            f"<td style='padding:9px 12px;{bdr};font-family:monospace;font-size:12px;color:{C['black']}'>{param}</td></tr>")
