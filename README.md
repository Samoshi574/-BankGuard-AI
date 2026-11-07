
# 🛡️ BankGuard AI

### AI-Powered Banking Fraud Detection & Cybersecurity Monitor

BankGuard AI is a prototype web application designed to
demonstrate fraud risk analysis and basic cybersecurity monitoring
for simulated banking activities.

## Features

- Machine learning-based transaction risk classification
- Random Forest classification model
- Suspicious login activity detection
- Transaction risk scoring
- Security monitoring dashboard
- Interactive charts and alerts

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- Random Forest

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Train the model if fraud_model.pkl is not available:

   python train_model.py

5. Run the application:

   python -m streamlit run app.py

## Important Notes

This is an educational prototype.

- It uses synthetic transaction data.
- The model learns labels created by predefined rules.
- The risk score is not a validated real-world fraud probability.
- Cybersecurity monitoring currently uses rule-based checks.
- Dashboard charts use illustrative data.
- No real banking systems or customer accounts are connected.

## Project Purpose

To demonstrate Software Engineering, Machine Learning,
basic Cybersecurity monitoring, and data visualization skills.

## Developer

Software Engineering Portfolio Project
