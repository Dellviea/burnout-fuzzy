# BurnSense

Aplikasi Streamlit untuk memprediksi tingkat burnout karyawan dengan logika fuzzy. Proyek kelompok ini membandingkan dua metode inferensi, Mamdani dan Sugeno, lalu menguji apakah keluaran fuzzy bisa membantu model Random Forest.

## Masalah yang diselesaikan

Burnout tidak punya batas yang tegas. Karyawan dengan skor kelelahan mental 6 dari 10 tidak bisa langsung disebut "lelah" atau "tidak lelah". Logika fuzzy cocok untuk kasus seperti ini karena setiap nilai bisa masuk ke beberapa kategori sekaligus dengan derajat keanggotaan yang berbeda, dan aturannya tetap bisa dibaca manusia.

## Cara kerjanya

```
5 input → fuzzifikasi → 20 aturan IF-THEN → defuzzifikasi → burn rate 0–1 → Low / Moderate / High / Severe
```

Inputnya skor kelelahan mental, alokasi sumber daya (jam kerja), level jabatan, ketersediaan WFH, dan tipe perusahaan. Fungsi keanggotaannya berbentuk segitiga dan trapesium, dan operator AND memakai min.

- **Mamdani:** keluaran tiap aturan berupa himpunan fuzzy, diagregasi dengan alpha-cut dan MAX, lalu didefuzzifikasi dengan centroid.
- **Sugeno:** keluaran tiap aturan berupa konstanta, lalu dirata-rata dengan bobot firing strength.

Hasil kedua metode juga dipakai sebagai fitur tambahan untuk Random Forest, lalu dibandingkan dengan Random Forest yang hanya memakai fitur mentah.

Implementasi fuzzy-nya ditulis sendiri dengan NumPy, tanpa library fuzzy. Analisis lengkapnya ada di [notebook](notebook/burnout_fuzzy.ipynb).

## Hasilnya

Dievaluasi pada 2.000 sampel dari dataset Kaggle *Are Your Employees Burning Out?*

| Model | MAE | RMSE | Waktu |
|---|---|---|---|
| Fuzzy Mamdani | 0,1184 | 0,1440 | 1,51 s |
| Fuzzy Sugeno | 0,1175 | 0,1429 | 0,16 s |
| Random Forest | 0,0527 | 0,0705 | 0,21 s |
| Random Forest + fitur fuzzy | 0,0526 | 0,0709 | 0,19 s |

Akurasi Sugeno sedikit lebih baik dan 9 kali lebih cepat dari Mamdani, karena tidak perlu menghitung centroid. Random Forest jauh lebih akurat dari keduanya, tetapi tambahan fitur fuzzy hampir tidak mengubah hasilnya. Kelebihan fuzzy ada di aturannya yang bisa dijelaskan, bukan di akurasinya.

## Kredit

Dataset [Are Your Employees Burning Out?](https://www.kaggle.com/datasets/blurredmachine/are-your-employees-burning-out) dari Kaggle. Dibuat dengan Streamlit, NumPy, pandas, Matplotlib, dan scikit-learn.
