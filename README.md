# Approach Documentation

## Firewall Log Anomaly Detection

### Problem Statement
The goal is to analyze firewall logs using AI/ML techniques to identify security incidents, threats, and suspicious traffic patterns. The final system detects anomalies, classifies threats, and presents results in an interactive dashboard.

---

### Solution Overview

#### 1. EDA
Conducted with Python (pandas, seaborn, matplotlib) to understand:
- Top destination ports (e.g., 3389)
- Session durations and byte distributions
- Unusual traffic patterns

#### 2. ML-based Anomaly Detection
Used `IsolationForest` to flag anomalies without requiring labeled data.

**Features used**:
- Bytes, Packets, Elapsed Time
- pkts_sent / pkts_received

#### 3. Threat Classification
Applied rule-based threat tagging:
- Port 3389 → RDP Access Attempt
- Bytes > 50,000 → Large Data Transfer
- pkts_received > 100 → High inbound traffic

#### 4. Streamlit Dashboard
Includes:
- Time filters: 1h / 12h / 24h
- Byte threshold filter
- Anomaly plot
- Threat type chart
- Export CSV

---
# How to Run It

## 1. Clone Repo

bash

git clone https://github.com/RaabiyahA/firewall_anomaly_detection.git
cd firewall_anomaly_detection


## 2. Create Virtual Environment

python3 -m venv .venv
source .venv/bin/activate

## 3. Install Dependencies

pip install -r requirements.txt

## 4. Run EDA Notebook

Open notebooks/1_eda.ipynb, run all cells.

## 5. Launch Dashboard

streamlit run dashboard/app.py

___

# Accuracy of Approach

This is an unsupervised system, so accuracy is measured using proxy indicators:

- Anomaly rate: ~5% of sessions flagged as anomalies
- Visual separation: Anomalies form clear outliers in scatter plots (e.g., Bytes vs Elapsed Time)
- Rule-based threat tags: Use logic like destination port and packet volume to categorize threats
- Further evaluation: Possible with labeled data to compute precision, recall, F1-score
