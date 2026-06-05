import numpy as np
import time
from sklearn.ensemble        import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics         import mean_absolute_error, mean_squared_error

from fuzzy.mamdani import mamdani_predict
from fuzzy.sugeno  import sugeno_predict

RAW_FEATURES   = ['Mental Fatigue Score', 'Resource Allocation',
                   'Designation', 'WFH_encoded', 'Company_encoded']
FUZZY_FEATURES = RAW_FEATURES + ['fuzzy_mamdani', 'fuzzy_sugeno']
TARGET         = 'Burn Rate'


def generate_fuzzy_features(df, sample_size=2000):
    """Tambah kolom fuzzy_mamdani & fuzzy_sugeno ke dataframe."""
    sample = df.sample(n=min(sample_size, len(df)), random_state=42).copy()
    sample = sample.dropna(subset=[TARGET])
    m_preds, s_preds = [], []
    for _, row in sample.iterrows():
        m = mamdani_predict(row['Mental Fatigue Score'], row['Resource Allocation'],
                            row['Designation'], row['WFH_encoded'], row['Company_encoded'])
        s = sugeno_predict(row['Mental Fatigue Score'], row['Resource Allocation'],
                           row['Designation'], row['WFH_encoded'], row['Company_encoded'])
        m_preds.append(m['burn_rate'])
        s_preds.append(s['burn_rate'])
    sample['fuzzy_mamdani'] = m_preds
    sample['fuzzy_sugeno']  = s_preds
    return sample


def train_and_evaluate(df_with_fuzzy):
    """Bandingkan RF tanpa fuzzy vs RF + fuzzy features."""
    df = df_with_fuzzy.dropna(subset=[TARGET] + RAW_FEATURES)
    X_raw,   y = df[RAW_FEATURES].values,   df[TARGET].values
    X_fuzzy, _ = df[FUZZY_FEATURES].values, df[TARGET].values

    X_r_tr, X_r_te, y_tr, y_te = train_test_split(X_raw,   y, test_size=0.2, random_state=42)
    X_f_tr, X_f_te, _,   _    = train_test_split(X_fuzzy, y, test_size=0.2, random_state=42)

    results = {}
    for tag, X_tr, X_te, label in [
        ('rf_raw',   X_r_tr, X_r_te, 'RF (tanpa fuzzy)'),
        ('rf_fuzzy', X_f_tr, X_f_te, 'RF + Fuzzy Features'),
    ]:
        t0   = time.time()
        rf   = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(X_tr, y_tr)
        pred = rf.predict(X_te)
        results[tag] = {
            'model':   rf,
            'mae':     round(mean_absolute_error(y_te, pred), 4),
            'mse':     round(mean_squared_error(y_te, pred), 4),
            'rmse':    round(np.sqrt(mean_squared_error(y_te, pred)), 4),
            'runtime': round(time.time() - t0, 3),
            'label':   label,
        }
    return results


def predict_with_rf(rf_model, fatigue, resource, designation, wfh, company_type,
                    use_fuzzy=True):
    features = [fatigue, resource, designation, wfh, company_type]
    if use_fuzzy:
        m = mamdani_predict(fatigue, resource, designation, wfh, company_type)
        s = sugeno_predict(fatigue, resource, designation, wfh, company_type)
        features += [m['burn_rate'], s['burn_rate']]
    return float(rf_model.predict([features])[0])
