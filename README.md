# 🛡️ UIDAI Regional Identity Integrity Analytics Platform

A privacy-first analytics platform built for the UIDAI Database Hackathon to detect
regional anomalies and integrity risks in Aadhaar enrolment, demographic updates,
and biometric updates using aggregated data.

---

## 🚩 Problem Statement

UIDAI manages massive nationwide Aadhaar operations. Detecting abnormal patterns
in enrolments and updates early—without accessing individual Aadhaar data—is a
major governance and integrity challenge.

---

## ✅ Our Solution

We provide a **plug-and-play analytics platform** that allows uploading
**aggregated regional datasets** and instantly generates:

- Risk scores (Low / Medium / High)
- Anomaly detection using Machine Learning
- State-wise risk visualization
- Audit-ready downloadable reports

No Aadhaar numbers. No biometrics. No PII.

---

## 🧠 Key Features

- 📤 Upload enrolment, demographic & biometric datasets
- 🔐 Privacy-preserving (aggregated data only)
- 📊 Professional dashboard with KPIs
- 🧠 ML-based anomaly detection (Isolation Forest)
- 🗺️ State-wise risk visualization
- 📥 Exportable CSV audit reports

---

## 🏗️ Tech Stack

- Python 3.12
- Streamlit
- Pandas, NumPy
- Scikit-learn
- Plotly

---

## ▶️ How to Run

```bash
git clone https://github.com/<your-username>/uidai-regional-identity-integrity-analytics
cd uidai-regional-identity-integrity-analytics

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
