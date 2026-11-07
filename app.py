
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from pathlib import Path

st.set_page_config(
    page_title="BankGuard AI",
    page_icon="🛡️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

FEATURES = [
    "amount", "hour", "failed_logins", "new_device"
]

@st.cache_resource
def load_model():
    model_path = BASE_DIR / "fraud_model.pkl"
    return joblib.load(model_path)

st.title("🛡️ BankGuard AI")
st.caption("AI-Powered Banking Fraud & Cybersecurity Monitor")

st.sidebar.title("🛡️ BankGuard AI")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Fraud Detection", "Cybersecurity Monitor"]
)


if page == "Dashboard":

    st.header("Security Overview")
    st.caption("BankGuard AI | Demonstration Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", "3,000")
    col2.metric("Suspicious Transactions", "38")
    col3.metric("Security Alerts", "12")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Fraud Risk Distribution")

        risk_data = pd.DataFrame({
            "Risk Level": ["Low", "Medium", "High"],
            "Transactions": [2500, 350, 150]
        })

        fig = px.pie(
            risk_data,
            names="Risk Level",
            values="Transactions",
            hole=0.55,
            color="Risk Level",
            color_discrete_map={
                "Low": "#16a34a",
                "Medium": "#f59e0b",
                "High": "#dc2626"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Cybersecurity Alerts")

        alert_data = pd.DataFrame({
            "Threat Type": [
                "Failed Logins",
                "Unknown Devices",
                "Suspicious Access"
            ],
            "Alerts": [12, 7, 5]
        })

        fig2 = px.bar(
            alert_data,
            x="Threat Type",
            y="Alerts",
            color="Threat Type"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Recent Security Alerts")

    alerts = pd.DataFrame({
        "Account ID": [
            "ACC-1025",
            "ACC-1048",
            "ACC-1092"
        ],
        "Alert": [
            "Unusual Transaction",
            "Multiple Failed Logins",
            "Unrecognized Device"
        ],
        "Risk": [
            "High",
            "Medium",
            "Low"
        ]
    })

    st.dataframe(alerts, use_container_width=True)

    st.info(
        "All dashboard statistics and alerts are "
        "illustrative demonstration data."
    )


elif page == "Fraud Detection":

    st.header("AI Fraud Detection")

    st.write("Enter transaction details for AI risk analysis.")

    amount = st.number_input(
        "Transaction Amount (LKR)",
        min_value=0.0,
        value=10000.0
    )

    hour = st.slider(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=12
    )

    failed_logins = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        value=0
    )

    new_device = st.selectbox(
        "New Device?",
        ["No", "Yes"]
    )

    if st.button("Analyze Transaction", type="primary"):

        input_data = pd.DataFrame([{
            "amount": amount,
            "hour": hour,
            "failed_logins": failed_logins,
            "new_device": 1 if new_device == "Yes" else 0
        }], columns=FEATURES)

        try:
            model = load_model()

            prediction = model.predict(input_data)[0]

            probability = model.predict_proba(input_data)[0]

            fraud_index = list(model.classes_).index(1)
            risk_score = float(probability[fraud_index]) * 100

            st.subheader("AI Analysis Result")

            st.metric(
                "Model Fraud Risk Score",
                f"{risk_score:.1f}%"
            )

            if prediction == 1:
                st.error("Potentially Suspicious Transaction!")
            else:
                st.success("No Fraud Flag Detected by Model")

            st.progress(min(100, max(0, int(risk_score))))

            st.caption(
                "This is a synthetic-data model score, "
                "not a calibrated real-world fraud probability."
            )

            st.subheader("Risk Indicators")

            if amount > 200000:
                st.warning("Large transaction amount")

            if failed_logins >= 5:
                st.warning("Multiple failed login attempts")

            if new_device == "Yes":
                st.info("Transaction initiated from a new device")

            if hour < 5:
                st.info("Transaction occurred during early morning")

            st.caption(
                "These indicators are rule-based explanations, "
                "not explanations of the ML model itself."
            )

        except (FileNotFoundError, ValueError) as error:
            st.error(f"Unable to analyze transaction: {error}")
        except Exception:
            st.error(
                "The fraud model could not be loaded. "
                "Please verify fraud_model.pkl."
            )

elif page == "Cybersecurity Monitor":

    st.header("Cybersecurity Threat Monitor")

    failed_attempts = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        value=0
    )

    unfamiliar_device = st.checkbox(
        "Login From Unfamiliar Device"
    )

    if st.button("Check Security", type="primary"):

        if failed_attempts >= 5:
            st.error("Suspicious Login Activity Detected!")

        elif unfamiliar_device and failed_attempts >= 3:
            st.warning("Potential Account Security Threat!")

        elif unfamiliar_device:
            st.info("Unfamiliar device detected. Review recommended.")

        else:
            st.success("No configured security rule triggered.")

    st.caption(
        "This security monitor uses rule-based checks "
        "and manually entered demonstration data."
    )
