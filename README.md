# BurnoutSense AI
Sistem prediksi tingkat burnout karyawan menggunakan Fuzzy Logic (Mamdani & Sugeno).

## Struktur Folder
```
burnout-fuzzy/
├── app/
│   ├── streamlit_app.py     ← entry point
│   ├── sidebar.py           ← komponen sidebar
│   ├── utils.py             ← warna, CSS, helpers
│   └── pages/
│       ├── home.py
│       ├── predict.py
│       ├── analytics.py
│       ├── membership.py
│       └── evaluasi.py
├── fuzzy/
│   ├── membership.py        ← MF trapezoid & triangle (from scratch)
│   ├── mamdani.py           ← Fuzzy Mamdani
│   └── sugeno.py            ← Fuzzy Sugeno
├── ml/
│   └── random_forest.py     ← Bonus: RF + Fuzzy Features
├── data/
│   └── train.csv
├── notebook/
│   └── burnout_fuzzy.ipynb
└── requirements.txt
```

## Cara Menjalankan
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Dataset
[Are Your Employees Burning Out?](https://www.kaggle.com/datasets/blurredmachine/are-your-employees-burning-out)
