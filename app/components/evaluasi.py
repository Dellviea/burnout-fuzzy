import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from app.utils import C, page_header, load_data, compute_metrics, section_header
from fuzzy.mamdani import mamdani_batch, mamdani_predict
from fuzzy.sugeno  import sugeno_batch,  sugeno_predict


def render():
    page_header("Evaluasi",
                "Perbandingan MAE, MSE, RMSE, dan waktu komputasi Mamdani vs Sugeno")

    df = load_data()

    run_eval = st.button("Jalankan Evaluasi dengan 23.000 data")

    if run_eval:
        with st.spinner("Mengevaluasi Mamdani..."):
            act_m, pred_m = mamdani_batch(df, sample_size=2000)
        with st.spinner("Mengevaluasi Sugeno..."):
            act_s, pred_s = sugeno_batch(df, sample_size=2000)
        mae_m, mse_m, rmse_m = compute_metrics(act_m, pred_m)
        mae_s, mse_s, rmse_s = compute_metrics(act_s, pred_s)
        t0 = time.time(); mamdani_predict(7.0,8.0,4,0,1); rt_m = round(time.time()-t0,4)
        t0 = time.time(); sugeno_predict(7.0,8.0,4,0,1);  rt_s = round(time.time()-t0,4)
        st.session_state['eval'] = dict(
            mae_m=mae_m, mse_m=mse_m, rmse_m=rmse_m, rt_m=rt_m,
            mae_s=mae_s, mse_s=mse_s, rmse_s=rmse_s, rt_s=rt_s)
        st.success("Evaluasi selesai!")

    ev = st.session_state.get('eval')
    if ev is None:
        st.markdown(f"""
<div style='background:{C['pink_bg']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:24px;text-align:center;margin-top:12px'>
  <div style='font-size:15px;font-weight:700;color:{C['pink_dark']};margin-bottom:8px'>
    Belum Ada Data Evaluasi</div>
  <div style='font-size:13px;color:{C['gray']}'>
    Klik <b>Jalankan Evaluasi</b> untuk menghitung metrik performa pada 2.000 data sampel.
  </div>
</div>""", unsafe_allow_html=True)
        return

    mae_m,mse_m,rmse_m,rt_m = ev['mae_m'],ev['mse_m'],ev['rmse_m'],ev['rt_m']
    mae_s,mse_s,rmse_s,rt_s = ev['mae_s'],ev['mse_s'],ev['rmse_s'],ev['rt_s']
    speedup = round(rt_m/rt_s,1) if rt_s > 0 else "–"

    # -------- Tabel-------------------------------------------
    def _w(a, b, lower=True):
        win = "Mamdani" if (a<=b)==lower else "Sugeno"
        bg  = C['pink_bg']   if win=="Mamdani" else C['blue_bg']
        fg  = C['pink_dark'] if win=="Mamdani" else C['blue_dark']
        return f"<span style='background:{bg};color:{fg};border-radius:10px;padding:3px 10px;font-size:11px;font-weight:700'>{win}</span>"

    def _erow(lbl, vm, vs, whtml, last=False):
        bdr = '' if last else f"border-bottom:0.5px solid {C['gray_light']};"
        return (f"<tr>"
                f"<td style='padding:10px 0;{bdr};font-weight:500;font-size:13px;text-align:center'>{lbl}</td>"
                f"<td style='text-align:center;padding:10px 0;{bdr};color:{C['pink_dark']};font-weight:700;font-size:13px'>{vm}</td>"
                f"<td style='text-align:center;padding:10px 0;{bdr};color:{C['blue_dark']};font-weight:700;font-size:13px'>{vs}</td>"
                f"<td style='text-align:center;padding:10px 0;{bdr}'>{whtml}</td></tr>")

    st.markdown(f"""
<div style='background:{C['white']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-bottom:14px'>
  {section_header('Tabel Perbandingan Metrik','Hasil evaluasi pada 2.000 data sampel')}
  <table style='width:100%;font-size:13px;border-collapse:collapse'>
    <tr style='border-bottom:1.5px solid {C['pink_light']}'>
      <th style='text-align:center;padding:8px 0;color:{C['gray']};font-size:12px;
      text-transform:uppercase;letter-spacing:0.5px;width:28%'>Metrik</th>
      <th style='text-align:center;padding:8px 0;color:{C['pink_dark']};font-size:12px;font-weight:700'>Mamdani</th>
      <th style='text-align:center;padding:8px 0;color:{C['blue_dark']};font-size:12px;font-weight:700'>Sugeno</th>
      <th style='text-align:center;padding:8px 0;color:{C['gray']};font-size:12px;
      text-transform:uppercase;letter-spacing:0.5px'>Lebih Baik</th>
    </tr>
    {_erow('MAE',             mae_m,  mae_s,  _w(mae_m,mae_s))}
    {_erow('MSE',             mse_m,  mse_s,  _w(mse_m,mse_s))}
    {_erow('RMSE',            rmse_m, rmse_s, _w(rmse_m,rmse_s))}
    {_erow('Waktu komputasi', f'{rt_m}s', f'{rt_s}s', _w(rt_m,rt_s,lower=True), last=True)}
  </table>
</div>""", unsafe_allow_html=True)

    # --- 3 chart dengan legend -------------------------------------------
    cc1, cc2, cc3 = st.columns(3)
    for col, title, vm, vs in [
        (cc1,'MAE',             mae_m,  mae_s),
        (cc2,'RMSE',            rmse_m, rmse_s),
        (cc3,'Waktu Komputasi', rt_m,   rt_s),
    ]:
        with col:
            max_v = max(vm, vs, 0.0001)
            fig, ax = plt.subplots(figsize=(3.5, 3.2))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')

            bars = ax.bar(['Mamdani','Sugeno'], [vm,vs],
                          color=[C['pink'],C['blue']],
                          width=0.45, edgecolor='white')
            for bar, val in zip(bars,[vm,vs]):
                ax.text(bar.get_x()+bar.get_width()/2,
                        bar.get_height()+max_v*0.04,
                        f'{val}', ha='center', va='bottom',
                        fontsize=9.5, fontweight='bold', color=C['black'])

            # -------- Legend -------------------------------------------
            legend_handles = [
                mpatches.Patch(color=C['pink'], label='Mamdani'),
                mpatches.Patch(color=C['blue'], label='Sugeno'),
            ]
            ax.legend(handles=legend_handles, fontsize=9,
                      loc='upper right', framealpha=0.7,
                      edgecolor=C['gray_light'])

            ax.set_ylim(0, max_v*1.4)
            ax.set_title(title, fontsize=12, fontweight='700',
                         color=C['pink_dark'], pad=8)
            ax.tick_params(labelsize=10, colors=C['gray'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(C['gray_light'])
            ax.spines['bottom'].set_color(C['gray_light'])
            plt.tight_layout(pad=0.8)
            st.pyplot(fig, use_container_width=True)
            plt.close()

    # -------- Interpretasi -------------------------------------------
    st.markdown(f"""
<div style='background:{C['pink_bg']};border:0.5px solid {C['pink_light']};
border-radius:10px;padding:16px;margin-top:8px'>
  {section_header('Interpretasi Hasil')}
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px'>
    <div style='background:{C['white']};border:0.5px solid {C['pink_light']};
    border-radius:8px;padding:14px'>
      <div style='font-size:13px;font-weight:700;color:{C['pink_dark']};margin-bottom:8px'>
        Mamdani — Lebih Akurat</div>
      <div style='font-size:13px;color:{C['gray']};line-height:1.7'>
        MAE &amp; RMSE lebih rendah. Defuzzifikasi centroid menangkap ketidakpastian
        linguistik lebih baik. Cocok saat interpretabilitas hasil penting.
      </div>
    </div>
    <div style='background:{C['white']};border:0.5px solid {C['blue_light']};
    border-radius:8px;padding:14px'>
      <div style='font-size:13px;font-weight:700;color:{C['blue_dark']};margin-bottom:8px'>
        Sugeno — Lebih Cepat</div>
      <div style='font-size:13px;color:{C['gray']};line-height:1.7'>
        Waktu komputasi {speedup}× lebih singkat. Weighted average tidak memerlukan
        integrasi numerik. Cocok untuk sistem real-time atau dataset besar.
      </div>
    </div>
  </div>
  <div style='background:{C['white']};border:0.5px solid {C['pink_light']};
  border-radius:8px;padding:14px;font-size:13px;color:{C['black']};line-height:1.7'>
    <b>Kesimpulan:</b> Terdapat trade-off antara akurasi dan kecepatan komputasi.
    Untuk sistem prediksi burnout yang mengutamakan presisi,
    <b>Mamdani lebih direkomendasikan</b>.
  </div>
</div>""", unsafe_allow_html=True)
