import numpy as np
import time
from fuzzy.membership import fuzzify_all, SUGENO_CONSTANTS
from fuzzy.mamdani    import RULES, get_burnout_level


def evaluate_rules_sugeno(fuzz):
    """Evaluasi rule Sugeno, output = konstanta."""
    fired = []
    for i, rule in enumerate(RULES):
        fs = min(fuzz[var][lbl] for var, lbl in rule['conditions'])
        if fs > 0:
            label = rule['output']
            fired.append({
                'rule_idx':        i + 1,
                'conditions':      rule['conditions'],
                'output':          label,
                'output_value':    SUGENO_CONSTANTS[label],
                'firing_strength': round(fs, 4)
            })
    return fired


def weighted_average(fired_rules):
    """Defuzzifikasi weighted average."""
    if not fired_rules: return 0.5
    num   = sum(r['firing_strength'] * r['output_value'] for r in fired_rules)
    denom = sum(r['firing_strength'] for r in fired_rules)
    return float(num / denom) if denom > 0 else 0.5


def sugeno_predict(fatigue, resource, designation, wfh, company_type):
    t0          = time.time()
    fuzz        = fuzzify_all(fatigue, resource, designation, wfh, company_type)
    fired_rules = evaluate_rules_sugeno(fuzz)
    burn_rate   = weighted_average(fired_rules)
    return {
        'burn_rate':   round(burn_rate, 4),
        'level':       get_burnout_level(burn_rate),
        'fired_rules': fired_rules,
        'fuzz':        fuzz,
        'runtime':     round(time.time() - t0, 4)
    }


def sugeno_batch(df, sample_size=2000):
    """Evaluasi batch untuk MAE/MSE/RMSE."""
    sample = df.sample(n=min(sample_size, len(df)), random_state=42)
    preds  = []
    for _, row in sample.iterrows():
        r = sugeno_predict(row['Mental Fatigue Score'], row['Resource Allocation'],
                           row['Designation'], row['WFH_encoded'], row['Company_encoded'])
        preds.append(r['burn_rate'])
    return sample['Burn Rate'].values, np.array(preds)
