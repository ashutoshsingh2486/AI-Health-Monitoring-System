# AI-Enabled Smart Health Monitoring & Prediction System

**B.Tech CSE (AI & ML) mini-project prototype**

A Flask-based educational prototype aligned with the project synopsis. It demonstrates health-reading input, validation/preprocessing, SQLite storage, a Random Forest demonstration model, configurable threshold alerts, and a web dashboard.

## Features
- Input heart rate, SpO₂, body temperature, systolic BP and diastolic BP.
- Basic numeric/range validation.
- Demo alerts for readings outside configurable thresholds.
- Random Forest classifier trained on generated synthetic data to demonstrate the ML pipeline.
- SQLite history of saved readings.
- Dashboard summary and sample-data loader.
- Clear history control.

## Tech stack
Python, Flask, scikit-learn, NumPy, SQLite, HTML, CSS.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.
7. Click **Load 3 sample readings** or enter a reading manually.

## Project flow
Data input → validation/preprocessing → demo ML model + threshold rules → SQLite database → dashboard/history.

## Important limitations
- This is an academic prototype, not a medical device or diagnostic system.
- It uses manual/sample data; ESP32, Raspberry Pi and physical sensors are not integrated.
- The classifier is trained on synthetic data solely to demonstrate a machine-learning workflow. It is not clinically validated and must not be used for health decisions.
- Thresholds are configurable demonstration values and are not personalized medical advice.

## Suggested viva explanation
"The application takes selected physiological values through a Flask web form. It validates the values, checks them against demonstration thresholds, and sends them to a Random Forest classifier trained on synthetic data for an educational ML demonstration. The result and any alerts are stored in SQLite and shown in the dashboard. Hardware sensor integration and validation on a real clinical dataset are future enhancements."

## GitHub upload
Create a new empty repository on GitHub. Then run these commands in this folder (replace the URL with your own repository URL):

```bash
git init
git add .
git commit -m "Initial commit: AI health monitoring mini project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

If Git says your identity is unknown, configure it once:
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```
