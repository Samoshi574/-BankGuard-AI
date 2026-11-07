
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

from pathlib import Path
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BankGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

if "security_history" not in st.session_state:
    st.session_state.security_history = []

# =====================================================
# MODEL CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

FEATURES = [
    "amount",
    "hour",
    "failed_logins",
    "new_device"
]


@st.cache_resource
def load_model():
    model_path = BASE_DIR / "fraud_model.pkl"
    return joblib.load(model_path)


# =====================================================
# APPLICATION HEADER
# =====================================================

st.title("🛡️ BankGuard AI")
st.caption(
    "AI-Powered Banking Fraud Detection & "
    "Cybersecurity Monitoring Platform"
)

st.sidebar.title("🛡️ BankGuard AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Fraud Detection",
        "Cybersecurity Monitor"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Educational prototype using synthetic "
    "banking data and simulated security events."
)

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("## Security Command Center")
    st.caption(
        "Fraud Intelligence & Cybersecurity Overview"
    )

    history = st.session_state.transaction_history
    security_history = st.session_state.security_history

    total_transactions = len(history)

    fraud_alerts = sum(
        record["Prediction"] == "Suspicious"
        for record in history
    )

    transaction_login_alerts = sum(
        record["Failed Logins"] >= 5
        for record in history
    )

    monitored_login_alerts = sum(
        record["Status"] in ["High Risk", "Medium Risk"]
        for record in security_history
    )

    security_alerts = (
        transaction_login_alerts + monitored_login_alerts
    )

    st.divider()

    # KPI METRICS

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions Analyzed",
        total_transactions
    )

    col2.metric(
        "Fraud Alerts",
        fraud_alerts
    )

    col3.metric(
        "Login Security Alerts",
        security_alerts
    )

    col4.metric(
        "System Mode",
        "Demo"
    )

    st.divider()

    # =================================================
    # DYNAMIC ANALYTICS
    # =================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Transaction Risk Distribution")

        if history:

            history_df = pd.DataFrame(history)

            low_count = int(
                (history_df["Risk Score (%)"] < 30).sum()
            )

            medium_count = int(
                (
                    (history_df["Risk Score (%)"] >= 30)
                    & (history_df["Risk Score (%)"] < 70)
                ).sum()
            )

            high_count = int(
                (history_df["Risk Score (%)"] >= 70).sum()
            )

            risk_data = pd.DataFrame({
                "Risk Level": [
                    "Low",
                    "Medium",
                    "High"
                ],
                "Transactions": [
                    low_count,
                    medium_count,
                    high_count
                ]
            })

            risk_data = risk_data[
                risk_data["Transactions"] > 0
            ]

            fig = px.pie(
                risk_data,
                names="Risk Level",
                values="Transactions",
                hole=0.6,
                color="Risk Level",
                color_discrete_map={
                    "Low": "#21C7C7",
                    "Medium": "#F59E0B",
                    "High": "#EF4444"
                }
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#EAF2FF",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No transaction data available. "
                "Analyze a transaction to generate charts."
            )

    with right:

        st.subheader("Cyber Threat Analytics")

        if security_history:

            security_df = pd.DataFrame(
                security_history
            )

            threat_data = (
                security_df["Status"]
                .value_counts()
                .reset_index()
            )

            threat_data.columns = [
                "Threat Level",
                "Events"
            ]

            fig2 = px.bar(
                threat_data,
                x="Threat Level",
                y="Events",
                color="Threat Level",
                color_discrete_map={
                    "High Risk": "#EF4444",
                    "Medium Risk": "#F59E0B",
                    "Low Risk": "#21C7C7"
                }
            )

            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#EAF2FF",
                showlegend=False,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:

            st.info(
                "No security events analyzed yet. "
                "Use Cybersecurity Monitor to generate data."
            )

    # =================================================
    # TRANSACTION HISTORY
    # =================================================

    st.divider()

    st.subheader("Recent Analyzed Transactions")

    if history:

        history_df = pd.DataFrame(history)

        st.dataframe(
            history_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

        csv_data = history_df.to_csv(index=False)

        st.download_button(
            label="Download Transaction History",
            data=csv_data,
            file_name="bankguard_transactions.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No transactions analyzed yet."
        )

    # =================================================
    # CYBERSECURITY HISTORY
    # =================================================

    st.divider()

    st.subheader("Recent Cybersecurity Events")

    if security_history:

        security_df = pd.DataFrame(
            security_history
        )

        st.dataframe(
            security_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No cybersecurity events recorded yet."
        )

    st.divider()

    st.caption(
        "Dashboard results reflect analyses performed "
        "in this browser session. "
        "This is not a live banking monitoring service."
    )


# =====================================================
# FRAUD DETECTION PAGE
# =====================================================

elif page == "Fraud Detection":

    st.header("AI Fraud Detection")

    st.write(
        "Enter simulated transaction details "
        "to analyze potential fraud risk."
    )

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

    if st.button(
        "Analyze Transaction",
        type="primary"
    ):

        input_data = pd.DataFrame([{
            "amount": amount,
            "hour": hour,
            "failed_logins": failed_logins,
            "new_device": (
                1 if new_device == "Yes" else 0
            )
        }], columns=FEATURES)

        try:

            model = load_model()

            prediction = int(
                model.predict(input_data)[0]
            )

            probability = model.predict_proba(
                input_data
            )[0]

            fraud_index = list(
                model.classes_
            ).index(1)

            risk_score = (
                float(probability[fraud_index]) * 100
            )

            # =========================================
            # SAVE TRANSACTION
            # =========================================

            transaction_record = {
                "Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Amount (LKR)": amount,
                "Transaction Hour": hour,
                "Risk Score (%)": round(
                    risk_score, 2
                ),
                "Prediction": (
                    "Suspicious"
                    if prediction == 1
                    else "Normal"
                ),
                "Failed Logins": failed_logins,
                "New Device": new_device
            }

            st.session_state.transaction_history.append(
                transaction_record
            )

            # =========================================
            # ANALYSIS RESULTS
            # =========================================

            st.subheader("AI Analysis Result")

            st.metric(
                "Model Fraud Risk Score",
                f"{risk_score:.1f}%"
            )

            if prediction == 1:

                st.error(
                    "Potentially Suspicious Transaction!"
                )

            else:

                st.success(
                    "No Fraud Flag Detected by Model"
                )

            st.progress(
                min(
                    100,
                    max(0, int(risk_score))
                )
            )

            st.caption(
                "This model was trained on synthetic "
                "rule-generated labels. Its output is "
                "not a validated real-world fraud probability."
            )

            st.subheader("Risk Indicators")

            if amount > 200000:

                st.warning(
                    "Large transaction amount"
                )

            if failed_logins >= 5:

                st.warning(
                    "Multiple failed login attempts"
                )

            if new_device == "Yes":

                st.info(
                    "Transaction initiated "
                    "from a new device"
                )

            if hour < 5:

                st.info(
                    "Transaction occurred "
                    "during early morning"
                )

            st.caption(
                "Risk indicators use predefined rules "
                "rather than model-specific explanations."
            )

            st.success(
                "Transaction analysis saved "
                "to session history."
            )

        except (FileNotFoundError, ValueError) as error:

            st.error(
                f"Unable to analyze transaction: {error}"
            )

        except Exception:

            st.error(
                "The model could not be loaded "
                "or used. Check fraud_model.pkl "
                "and its dependencies."
            )


# =====================================================
# CYBERSECURITY MONITOR
# =====================================================

elif page == "Cybersecurity Monitor":

    st.header("Cybersecurity Threat Monitor")

    st.write(
        "Analyze simulated login events "
        "for suspicious security activity."
    )

    failed_attempts = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        value=0
    )

    unfamiliar_device = st.checkbox(
        "Login From Unfamiliar Device"
    )

    if st.button(
        "Check Security",
        type="primary"
    ):

        if failed_attempts >= 5:

            status = "High Risk"

            st.error(
                "Suspicious Login Activity Detected!"
            )

        elif unfamiliar_device and failed_attempts >= 3:

            status = "Medium Risk"

            st.warning(
                "Potential Account Security Threat!"
            )

        elif unfamiliar_device:

            status = "Low Risk"

            st.info(
                "Unfamiliar device detected. "
                "Review recommended."
            )

        else:

            status = "Low Risk"

            st.success(
                "No configured security rule triggered."
            )

        # =============================================
        # SAVE SECURITY EVENT
        # =============================================

        security_record = {
            "Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Failed Attempts": failed_attempts,
            "Unfamiliar Device": (
                "Yes" if unfamiliar_device else "No"
            ),
            "Status": status
        }

        st.session_state.security_history.append(
            security_record
        )

        st.success(
            "Security analysis saved "
            "to session history."
        )

    st.caption(
        "This monitor uses rule-based checks "
        "on manually entered demonstration data."
    )
