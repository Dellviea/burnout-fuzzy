import numpy as np
import time
from fuzzy.membership import fuzzify_all, mf_output


# --- Rule base 20 rules ---

RULES = [
    # Severe
    {'conditions': [('fatigue','HIGH'),   ('resource','HIGH')],                      'output': 'SEVERE'},
    {'conditions': [('fatigue','HIGH'),   ('wfh','NO')],                             'output': 'SEVERE'},
    {'conditions': [('desig','SENIOR'),   ('fatigue','HIGH'),  ('resource','HIGH')], 'output': 'SEVERE'},
    {'conditions': [('company','PRODUCT'),('fatigue','HIGH'),  ('resource','HIGH')], 'output': 'SEVERE'},
    # High
    {'conditions': [('fatigue','HIGH'),   ('resource','MEDIUM')],                    'output': 'HIGH'},
    {'conditions': [('fatigue','MEDIUM'), ('resource','HIGH')],                      'output': 'HIGH'},
    {'conditions': [('wfh','NO'),         ('resource','HIGH')],                      'output': 'HIGH'},
    {'conditions': [('desig','SENIOR'),   ('resource','HIGH')],                      'output': 'HIGH'},
    {'conditions': [('desig','JUNIOR'),   ('fatigue','HIGH')],                       'output': 'HIGH'},
    {'conditions': [('fatigue','MEDIUM'), ('wfh','NO'),        ('resource','HIGH')], 'output': 'HIGH'},
    # Moderate
    {'conditions': [('fatigue','MEDIUM'), ('resource','MEDIUM')],                    'output': 'MODERATE'},
    {'conditions': [('fatigue','HIGH'),   ('resource','LOW')],                       'output': 'MODERATE'},
    {'conditions': [('desig','MID'),      ('fatigue','MEDIUM')],                     'output': 'MODERATE'},
    {'conditions': [('fatigue','MEDIUM'), ('resource','MEDIUM'),('wfh','NO')],       'output': 'MODERATE'},
    # Low
    {'conditions': [('fatigue','LOW'),    ('wfh','YES')],                            'output': 'LOW'},
    {'conditions': [('fatigue','LOW'),    ('resource','LOW')],                       'output': 'LOW'},
    {'conditions': [('desig','JUNIOR'),   ('fatigue','LOW')],                        'output': 'LOW'},
    {'conditions': [('fatigue','LOW'),    ('resource','MEDIUM'),('wfh','YES')],      'output': 'LOW'},
    {'conditions': [('fatigue','MEDIUM'), ('resource','LOW'),  ('wfh','YES')],       'output': 'LOW'},
    {'conditions': [('wfh','YES'),        ('fatigue','LOW'),   ('resource','LOW')],  'output': 'LOW'},
]


def evaluate_rules(fuzz):
    """Evaluasi rule, AND = min."""
    fired = []
    for i, rule in enumerate(RULES):
        fs = min(fuzz[var][lbl] for var, lbl in rule['conditions'])
        if fs > 0:
            fired.append({
                'rule_idx':        i + 1,
                'conditions':      rule['conditions'],
                'output':          rule['output'],
                'firing_strength': round(fs, 4)
            })
    return fired


def aggregate(fired_rules, x_values):
    """Agregasi alpha-cut + MAX."""
    agg = np.zeros(len(x_values))
    for rule in fired_rules:
        alpha, label = rule['firing_strength'], rule['output']
        for j, x in enumerate(x_values):
            agg[j] = max(agg[j], min(alpha, mf_output(x, label)))
    return agg


def centroid(agg, x_values):
    """Defuzzifikasi centroid."""
    denom = np.sum(agg)
    return float(np.sum(x_values * agg) / denom) if denom > 0 else 0.5


def get_burnout_level(burn_rate):
    if burn_rate < 0.30: return 'LOW'
    if burn_rate < 0.55: return 'MODERATE'
    if burn_rate < 0.75: return 'HIGH'
    return 'SEVERE'


def mamdani_predict(fatigue, resource, designation, wfh, company_type, n_points=200):
    t0          = time.time()
    fuzz        = fuzzify_all(fatigue, resource, designation, wfh, company_type)
    fired_rules = evaluate_rules(fuzz)
    x_values    = np.linspace(0, 1, n_points)
    agg         = aggregate(fired_rules, x_values)
    burn_rate   = centroid(agg, x_values)
    return {
        'burn_rate':   round(burn_rate, 4),
        'level':       get_burnout_level(burn_rate),
        'fired_rules': fired_rules,
        'aggregated':  agg,
        'x_values':    x_values,
        'fuzz':        fuzz,
        'runtime':     round(time.time() - t0, 4)
    }


def mamdani_batch(df, sample_size=2000):
    """Evaluasi batch untuk MAE/MSE/RMSE."""
    sample = df.sample(n=min(sample_size, len(df)), random_state=42)
    preds  = []
    for _, row in sample.iterrows():
        r = mamdani_predict(row['Mental Fatigue Score'], row['Resource Allocation'],
                            row['Designation'], row['WFH_encoded'], row['Company_encoded'])
        preds.append(r['burn_rate'])
    return sample['Burn Rate'].values, np.array(preds)
