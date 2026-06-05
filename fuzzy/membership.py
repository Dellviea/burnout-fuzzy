import numpy as np


def trapezoid(x, a, b, c, d):
    x = float(x)
    if x <= a or x >= d: return 0.0
    if b <= x <= c:      return 1.0
    if a < x < b:        return (x - a) / (b - a)
    if c < x < d:        return (d - x) / (d - c)
    return 0.0


def triangle(x, a, b, c):
    x = float(x)
    if x <= a or x >= c: return 0.0
    if x == b:           return 1.0
    if a < x < b:        return (x - a) / (b - a)
    if b < x < c:        return (c - x) / (c - b)
    return 0.0


# --- Fuzzifikasi input ---

def fuzzify_mental_fatigue(val):
    return {
        'LOW':    trapezoid(val, 0, 0, 2, 4),
        'MEDIUM': triangle(val,  3, 5, 7),
        'HIGH':   trapezoid(val, 6, 8, 10, 10)
    }

def fuzzify_resource_allocation(val):
    return {
        'LOW':    trapezoid(val, 1, 1, 3, 5),
        'MEDIUM': triangle(val,  4, 5.5, 7),
        'HIGH':   trapezoid(val, 6, 8, 10, 10)
    }

def fuzzify_designation(val):
    return {
        'JUNIOR': trapezoid(val, 0, 0, 1.5, 2.5),
        'MID':    triangle(val,  2, 3, 4),
        'SENIOR': trapezoid(val, 3.5, 4.5, 5, 5)
    }

def fuzzify_wfh(val):
    val = float(val)
    return {'NO': 1.0 - val, 'YES': val}

def fuzzify_company_type(val):
    val = float(val)
    return {'SERVICE': 1.0 - val, 'PRODUCT': val}

def fuzzify_all(fatigue, resource, designation, wfh, company_type):
    return {
        'fatigue':  fuzzify_mental_fatigue(fatigue),
        'resource': fuzzify_resource_allocation(resource),
        'desig':    fuzzify_designation(designation),
        'wfh':      fuzzify_wfh(wfh),
        'company':  fuzzify_company_type(company_type)
    }


# --- MF output ---

def mf_output(x, label):
    mf = {
        'LOW':      lambda x: trapezoid(x, 0,    0,    0.20, 0.35),
        'MODERATE': lambda x: triangle(x,  0.25, 0.45, 0.60),
        'HIGH':     lambda x: triangle(x,  0.50, 0.65, 0.80),
        'SEVERE':   lambda x: trapezoid(x, 0.70, 0.85, 1.0,  1.0),
    }
    return mf.get(label, lambda x: 0.0)(x)


SUGENO_CONSTANTS = {
    'LOW': 0.15, 'MODERATE': 0.42, 'HIGH': 0.65, 'SEVERE': 0.88
}


def get_mf_curves():
    """Return data kurva MF untuk visualisasi."""
    x_f = np.linspace(0, 10, 300)
    x_r = np.linspace(1, 10, 300)
    x_d = np.linspace(0, 5,  300)
    x_o = np.linspace(0, 1,  300)
    return {
        'fatigue': {
            'x': x_f, 'xlabel': 'Mental Fatigue Score', 'range': (0, 10),
            'LOW':    [trapezoid(v, 0, 0, 2, 4)    for v in x_f],
            'MEDIUM': [triangle(v,  3, 5, 7)        for v in x_f],
            'HIGH':   [trapezoid(v, 6, 8, 10, 10)   for v in x_f],
        },
        'resource': {
            'x': x_r, 'xlabel': 'Resource Allocation', 'range': (1, 10),
            'LOW':    [trapezoid(v, 1, 1, 3, 5)    for v in x_r],
            'MEDIUM': [triangle(v,  4, 5.5, 7)      for v in x_r],
            'HIGH':   [trapezoid(v, 6, 8, 10, 10)   for v in x_r],
        },
        'designation': {
            'x': x_d, 'xlabel': 'Designation Level', 'range': (0, 5),
            'JUNIOR': [trapezoid(v, 0, 0, 1.5, 2.5)  for v in x_d],
            'MID':    [triangle(v,  2, 3, 4)           for v in x_d],
            'SENIOR': [trapezoid(v, 3.5, 4.5, 5, 5)   for v in x_d],
        },
        'output': {
            'x': x_o, 'xlabel': 'Output Burn Rate', 'range': (0, 1),
            'LOW':      [mf_output(v, 'LOW')      for v in x_o],
            'MODERATE': [mf_output(v, 'MODERATE') for v in x_o],
            'HIGH':     [mf_output(v, 'HIGH')     for v in x_o],
            'SEVERE':   [mf_output(v, 'SEVERE')   for v in x_o],
        },
    }
