import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from fuzzy.mamdani import mamdani_predict
from fuzzy.sugeno  import sugeno_predict
from app.utils import C, LEVEL, page_header, level_color, recommendations


def render(fatigue, resource, designation, wfh, company):
    page_header("Prediksi", "Atur input di sidebar, lalu klik Jalankan Prediksi")

    # -------- Tombol -------------------------------------------
    cb, ch = st.columns([1, 3])
    with cb:
        run = st.button("Jalankan Prediksi")
    with ch:
        st.markdown(
            f"<p style='font-size:13px;color:{C['gray']};padding-top:10px;margin:0'>"
            "Input sudah diatur? Klik untuk menjalankan Mamdani &amp; Sugeno sekaligus</p>",
            unsafe_allow_html=True)

    if run:
        st.session_state['ran'] = True
    if not st.session_state.get('ran', False):
        return

    with st.spinner("Menjalankan fuzzy inference..."):
        m = mamdani_predict(fatigue, resource, designation, wfh, company)
        s = sugeno_predict(fatigue, resource, designation, wfh, company)

    # -------- 4 KPI -------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Mamdani",    f"{m['burn_rate']:.3f}")
    with k2: st.metric("Sugeno",     f"{s['burn_rate']:.3f}")
    with k3: st.metric("Selisih",    f"{abs(m['burn_rate']-s['burn_rate']):.3f}")
    with k4: st.metric("Rule Aktif", f"{len(m['fired_rules'])} / 20")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # -------- Hasil Mamdani & Sugeno -------------------------------------------
    c1, c2 = st.columns(2)
    for col, res, tag, clr, bdr in [
        (c1, m, "MAMDANI", C['pink'],      C['pink_light']),
        (c2, s, "SUGENO",  C['blue_dark'], C['blue_light']),
    ]:
        bg, fg, acc = level_color(res['level'])
        method = "Defuzzifikasi centroid" if tag == "MAMDANI" else "Defuzzifikasi weighted average"
        with col:
            st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {bdr};
border-radius:10px;padding:16px;margin-bottom:12px'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'>
    <span style='font-size:11px;font-weight:700;color:{clr};
    text-transform:uppercase;letter-spacing:1px'>{tag}</span>
    <span style='background:{bg};color:{fg};border:0.5px solid {acc};
    padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700'>{res['level']}</span>
  </div>
  <div style='font-size:32px;font-weight:800;color:{C['black']};
  margin-bottom:4px;letter-spacing:-1px'>{res['burn_rate']:.3f}</div>
  <div style='font-size:11px;color:{C['gray']};margin-bottom:10px'>
    {method} · {res['runtime']*1000:.2f} ms</div>
  <div style='font-size:12px;font-weight:500;margin-bottom:6px'>
    Burn rate: {res['burn_rate']*100:.1f}%</div>
  <div style='height:6px;background:{C['gray_light']};border-radius:3px;overflow:hidden'>
    <div style='height:100%;width:{res['burn_rate']*100:.1f}%;
    background:{clr};border-radius:3px'></div>
  </div>
</div>""", unsafe_allow_html=True)

    # -------- Burnout Meter -------------------------------------------
    bm1, bm2 = st.columns(2)

    with bm1, st.container(border=True):
        st.markdown(f"<div style='font-size:14px;font-weight:700;color:{C['black']}'>Burnout Meter</div>",
                    unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 3.1), subplot_kw=dict(aspect='equal'))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        segs = [(0.00, 0.30, 'LOW'), (0.30, 0.55, 'MODERATE'),
                (0.55, 0.75, 'HIGH'), (0.75, 1.00, 'SEVERE')]
        for lo, hi, lvl in segs:
            ax.add_patch(mpatches.Wedge((.5, 0), .42, 180 - hi*180, 180 - lo*180,
                         width=.13, facecolor=LEVEL[lvl], edgecolor='white', linewidth=2))
            # label di tengah tiap segmen, tepat di luar arc
            a = np.radians(180 - (lo + hi) / 2 * 180)
            ax.text(.5 + .5*np.cos(a), .5*np.sin(a), {'MODERATE': 'MOD', 'SEVERE': 'SEV'}.get(lvl, lvl),
                    ha='center', va='center', fontsize=9, fontweight='bold', color=LEVEL[lvl])

        ang = np.radians(180 - m['burn_rate']*180)
        ax.annotate('', xy=(.5 + .3*np.cos(ang), .3*np.sin(ang)), xytext=(.5, 0),
                    arrowprops=dict(arrowstyle='-|>', color=C['black'], lw=2.5, mutation_scale=16))
        ax.plot(.5, 0, 'o', color=C['black'], markersize=8, zorder=5)

        # nilai di bawah poros jarum, tidak tertimpa jarum
        ax.text(.5, -.1, f"{m['burn_rate']:.3f}", ha='center', va='center',
                fontsize=17, fontweight='bold', color=C['black'])
        ax.text(.5, -.2, f"Mamdani · {m['level']}", ha='center', va='center',
                fontsize=9, color=C['gray'])

        ax.set_xlim(-.05, 1.05)
        ax.set_ylim(-.26, .56)
        ax.axis('off')
        plt.tight_layout(pad=0)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with bm2:
        bg_l, fg_l, acc_l = level_color(m['level'])
        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;height:100%'>
  <div style='font-size:14px;font-weight:700;color:{C['black']};margin-bottom:14px'>
    Perbandingan Burn Rate</div>

  <div style='margin-bottom:10px'>
    <div style='display:flex;justify-content:space-between;margin-bottom:5px'>
      <span style='font-size:13px;font-weight:600;color:{C['black']}'>Mamdani</span>
      <span style='font-size:13px;font-weight:700;color:{C['pink']}'>{m['burn_rate']*100:.0f}%</span>
    </div>
    <div style='height:10px;background:{C['gray_light']};border-radius:5px;overflow:hidden'>
      <div style='height:100%;width:{m['burn_rate']*100:.1f}%;
      background:{C['pink']};border-radius:5px'></div>
    </div>
  </div>

  <div style='margin-bottom:18px'>
    <div style='display:flex;justify-content:space-between;margin-bottom:5px'>
      <span style='font-size:13px;font-weight:600;color:{C['black']}'>Sugeno</span>
      <span style='font-size:13px;font-weight:700;color:{C['blue_dark']}'>{s['burn_rate']*100:.0f}%</span>
    </div>
    <div style='height:10px;background:{C['gray_light']};border-radius:5px;overflow:hidden'>
      <div style='height:100%;width:{s['burn_rate']*100:.1f}%;
      background:{C['blue']};border-radius:5px'></div>
    </div>
  </div>

  <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>
    <div style='background:{bg_l};border:0.5px solid {acc_l};
    border-radius:8px;padding:12px;text-align:center'>
      <div style='font-size:10px;color:{fg_l};text-transform:uppercase;
      letter-spacing:0.5px;margin-bottom:4px;font-weight:600'>Status</div>
      <div style='font-size:17px;font-weight:800;color:{fg_l}'>{m['level']}</div>
    </div>
    <div style='background:{C['bg']};border-radius:8px;padding:12px;text-align:center'>
      <div style='font-size:10px;color:{C['gray']};text-transform:uppercase;
      letter-spacing:0.5px;margin-bottom:4px;font-weight:600'>Selisih</div>
      <div style='font-size:17px;font-weight:800;color:{C['black']}'>{abs(m['burn_rate']-s['burn_rate']):.3f}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # -------- Rule Aktif + Rekomendasi -------------------------------------------
    r1, r2 = st.columns(2)

    with r1:
        rules_html = ""
        for rule in m['fired_rules'][:5]:
            conds = ""
            for j, (var, lbl) in enumerate(rule['conditions']):
                if j > 0:
                    conds += f"<span style='font-size:11px;color:{C['gray']};margin:0 4px'>AND</span>"
                conds += (f"<span style='background:{C['bg']};border:0.5px solid #ddd;"
                          f"border-radius:4px;padding:2px 8px;font-size:11px;"
                          f"font-weight:600;color:{C['black']}'>{lbl}</span>")
            out_clr = level_color(rule['output'])[1]
            rules_html += f"""
<div style='background:{C['bg']};border-radius:8px;padding:10px 12px;margin-bottom:8px'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
    <span style='font-size:12px;color:{C['gray']};font-weight:500'>
      Rule {rule['rule_idx']}</span>
    <span style='background:{C['pink_bg']};color:{C['pink_dark']};
    border:0.5px solid {C['pink_light']};border-radius:4px;
    padding:2px 8px;font-size:11px;font-weight:700'>α = {rule['firing_strength']:.2f}</span>
  </div>
  <div style='font-size:12px;color:{C['black']};line-height:2'>
    {conds}
    <span style='font-size:11px;color:{C['gray']};margin:0 4px'>→</span>
    <span style='color:{out_clr};font-weight:700;font-size:12px'>{rule['output']}</span>
  </div>
</div>"""

        st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:14px;font-weight:700;color:{C['black']};margin-bottom:4px'>
    Rule Aktif</div>
  <div style='font-size:12px;color:{C['gray']};margin-bottom:12px'>
    {len(m['fired_rules'])} dari 20 rule terpicu</div>
  {rules_html}
</div>""", unsafe_allow_html=True)

    with r2:
        recs = recommendations(m['level'])
        bg_r, fg_r, acc_r = level_color(m['level'])
        recs_html = "".join([
            f"<div style='display:flex;gap:10px;align-items:flex-start;"
            f"background:{C['white']};border:0.5px solid {C['pink_light']};"
            f"border-radius:8px;padding:10px 12px;margin-bottom:8px'>"
            f"<div style='width:6px;height:6px;border-radius:50%;background:{C['pink']};"
            f"flex-shrink:0;margin-top:5px'></div>"
            f"<span style='font-size:13px;color:{C['black']};line-height:1.5'>{r}</span></div>"
            for r in recs])
        st.markdown(f"""
<div style='background:{C['pink_bg']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px'>
  <div style='font-size:14px;font-weight:700;color:{C['black']};margin-bottom:4px'>
    Rekomendasi</div>
  <div style='font-size:12px;color:{C['gray']};margin-bottom:12px'>
    Level burnout: <b style='color:{C['pink_dark']}'>{m['level']}</b></div>
  {recs_html}
</div>""", unsafe_allow_html=True)
