from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from datetime import datetime
from model import predict_demo_risk

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "demo-only-change-this")
DB_PATH = os.path.join(os.path.dirname(__file__), "health_data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recorded_at TEXT NOT NULL,
                heart_rate REAL NOT NULL,
                spo2 REAL NOT NULL,
                temperature REAL NOT NULL,
                systolic_bp REAL NOT NULL,
                diastolic_bp REAL NOT NULL,
                risk_label TEXT NOT NULL,
                alerts TEXT NOT NULL
            )
        """)

def evaluate_alerts(hr, spo2, temp, sys_bp, dia_bp):
    alerts = []
    # Demo thresholds only; not intended for medical decisions.
    if hr < 50 or hr > 120:
        alerts.append("Heart rate is outside the demo range (50–120 bpm).")
    if spo2 < 94:
        alerts.append("SpO₂ is below the demo threshold (94%).")
    if temp < 35.0 or temp > 38.0:
        alerts.append("Temperature is outside the demo range (35–38 °C).")
    if sys_bp >= 140 or dia_bp >= 90:
        alerts.append("Blood pressure is high according to the demo threshold.")
    if sys_bp < 90 or dia_bp < 60:
        alerts.append("Blood pressure is low according to the demo threshold.")
    return alerts

@app.route("/")
def index():
    with get_db() as conn:
        readings = conn.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 10").fetchall()
        total = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
        alerts_count = conn.execute("SELECT COUNT(*) FROM readings WHERE alerts != ''").fetchone()[0]
    latest = readings[0] if readings else None
    return render_template("index.html", readings=readings, latest=latest, total=total, alerts_count=alerts_count)

@app.route("/add-reading", methods=["POST"])
def add_reading():
    try:
        hr = float(request.form["heart_rate"])
        spo2 = float(request.form["spo2"])
        temp = float(request.form["temperature"])
        sys_bp = float(request.form["systolic_bp"])
        dia_bp = float(request.form["diastolic_bp"])
        if not (20 <= hr <= 250 and 50 <= spo2 <= 100 and 25 <= temp <= 45 and 50 <= sys_bp <= 280 and 30 <= dia_bp <= 180):
            raise ValueError("Please enter plausible numeric values within the form limits.")
    except (ValueError, KeyError):
        flash("Invalid input. Please check all values and try again.", "error")
        return redirect(url_for("index"))

    alerts = evaluate_alerts(hr, spo2, temp, sys_bp, dia_bp)
    risk = predict_demo_risk(hr, spo2, temp, sys_bp, dia_bp)
    alert_text = " | ".join(alerts)
    with get_db() as conn:
        conn.execute("""INSERT INTO readings
            (recorded_at, heart_rate, spo2, temperature, systolic_bp, diastolic_bp, risk_label, alerts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now().strftime("%d %b %Y, %I:%M:%S %p"), hr, spo2, temp, sys_bp, dia_bp, risk, alert_text))
    flash("Reading saved successfully.", "success")
    return redirect(url_for("index"))

@app.route("/load-demo")
def load_demo():
    samples = [
        (76, 98, 36.7, 118, 78),
        (88, 97, 37.0, 124, 82),
        (126, 92, 38.4, 148, 96),
    ]
    with get_db() as conn:
        for hr, spo2, temp, sbp, dbp in samples:
            alerts = evaluate_alerts(hr, spo2, temp, sbp, dbp)
            risk = predict_demo_risk(hr, spo2, temp, sbp, dbp)
            conn.execute("""INSERT INTO readings
                (recorded_at, heart_rate, spo2, temperature, systolic_bp, diastolic_bp, risk_label, alerts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (datetime.now().strftime("%d %b %Y, %I:%M:%S %p"), hr, spo2, temp, sbp, dbp, risk, " | ".join(alerts)))
    flash("Three sample readings added for demonstration.", "success")
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear():
    with get_db() as conn:
        conn.execute("DELETE FROM readings")
    flash("Demo history cleared.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
