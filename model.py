"""
Educational demo model.
Synthetic data is generated only to demonstrate a machine-learning pipeline.
This model is NOT clinically validated and must not be used for diagnosis.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def _build_demo_model():
    rng = np.random.default_rng(42)
    n = 1600
    hr = rng.normal(78, 18, n).clip(35, 150)
    spo2 = rng.normal(97, 2.5, n).clip(82, 100)
    temp = rng.normal(36.8, 0.8, n).clip(34, 41)
    sbp = rng.normal(120, 18, n).clip(75, 210)
    dbp = rng.normal(79, 12, n).clip(40, 130)
    X = np.column_stack([hr, spo2, temp, sbp, dbp])
    y = ((hr < 50) | (hr > 120) | (spo2 < 94) | (temp > 38) |
         (temp < 35) | (sbp >= 140) | (dbp >= 90) | (sbp < 90) | (dbp < 60)).astype(int)
    model = RandomForestClassifier(n_estimators=80, random_state=42, class_weight="balanced")
    model.fit(X, y)
    return model

_MODEL = _build_demo_model()

def predict_demo_risk(hr, spo2, temp, systolic_bp, diastolic_bp):
    x = np.array([[hr, spo2, temp, systolic_bp, diastolic_bp]])
    pred = int(_MODEL.predict(x)[0])
    return "Needs Attention" if pred else "Within Demo Range"
