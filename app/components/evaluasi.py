import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from app.utils import C, page_header, load_data, compute_metrics, section_header
from fuzzy.mamdani import mamdani_batch
from fuzzy.sugeno  import sugeno_batch


def render():
    page_header("Evaluasi",
                "Perbandingan MAE, MSE, RMSE, dan waktu komputasi Mamdani vs Sugeno")

    df = load_data()

    run_eval = st.button("Jalankan Evaluasi (2.000 data sampel)")

    if run_eval:
        # waktu = total 2.000 data (1 data terlalu cepat, bisa terbaca 0.0s)
        with st.spinner("Mengevaluasi Mamdani..."):
            t0 = time.perf_counter()
            act_m, pred_m = mamdani_batch(df, sample_size=2000)
            rt_m = round(time.perf_counter() - t0, 3)
        with st.spinner("Mengevaluasi Sugeno..."):
            t0 = time.perf_counter()
            act_s, pred_s = sugeno_batch(df, sample_size=2000)
            rt_s = round(time.perf_counter() - t0, 3)
        mae_m, mse_m, rmse_m = compute_metrics(act_m, pred_m)
        mae_s, mse_s, rmse_s = compute_metrics(act_s, pred_s)
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
    acc_win = "Mamdani" if rmse_m <= rmse_s else "Sugeno"
    spd_win = "Mamdani" if rt_m   <= rt_s   else "Sugeno"
    if acc_win == spd_win:
        kesimpulan = (f"<b>{acc_win}</b> unggul di akurasi (RMSE {min(rmse_m,rmse_s):.4f}) "
                      f"sekaligus kecepatan, sehingga <b>{acc_win} lebih direkomendasikan</b>.")
    else:
        kesimpulan = (f"Terdapat trade-off: <b>{acc_win}</b> lebih akurat, <b>{spd_win}</b> lebih cepat. "
                      f"Untuk prediksi yang mengutamakan presisi, <b>{acc_win} lebih direkomendasikan</b>.")

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
    {_erow('MAE',             f'{mae_m:.4f}',  f'{mae_s:.4f}',  _w(mae_m,mae_s))}
    {_erow('MSE',             f'{mse_m:.4f}',  f'{mse_s:.4f}',  _w(mse_m,mse_s))}
    {_erow('RMSE',            f'{rmse_m:.4f}', f'{rmse_s:.4f}', _w(rmse_m,rmse_s))}
    {_erow('Waktu (2.000 data)', f'{rt_m}s', f'{rt_s}s', _w(rt_m,rt_s,lower=True), last=True)}
  </table>
</div>""", unsafe_allow_html=True)

    # --- 3 chart dengan legend -------------------------------------------
    cc1, cc2, cc3 = st.columns(3)
    for col, title, vm, vs, fmt in [
        (cc1,'MAE',                 mae_m,  mae_s,  '{:.4f}'),
        (cc2,'RMSE',                rmse_m, rmse_s, '{:.4f}'),
        (cc3,'Waktu Komputasi (s)', rt_m,   rt_s,   '{:.3f}s'),
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
                        fmt.format(val), ha='center', va='bottom',
                        fontsize=9.5, fontweight='bold', color=C['black'])

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
        Mamdani — Centroid</div>
      <div style='font-size:13px;color:{C['gray']};line-height:1.7'>
        MAE {mae_m:.4f} · RMSE {rmse_m:.4f}. Output berupa himpunan fuzzy yang didefuzzifikasi
        centroid, lebih interpretable namun butuh integrasi numerik.
      </div>
    </div>
    <div style='background:{C['white']};border:0.5px solid {C['blue_light']};
    border-radius:8px;padding:14px'>
      <div style='font-size:13px;font-weight:700;color:{C['blue_dark']};margin-bottom:8px'>
        Sugeno — Weighted Average</div>
      <div style='font-size:13px;color:{C['gray']};line-height:1.7'>
        MAE {mae_s:.4f} · RMSE {rmse_s:.4f}. Waktu komputasi {speedup}× dibanding Mamdani,
        karena weighted average tidak memerlukan integrasi numerik.
      </div>
    </div>
  </div>
  <div style='background:{C['white']};border:0.5px solid {C['pink_light']};
  border-radius:8px;padding:14px;font-size:13px;color:{C['black']};line-height:1.7'>
    <b>Kesimpulan:</b> {kesimpulan}
  </div>
</div>""", unsafe_allow_html=True)
