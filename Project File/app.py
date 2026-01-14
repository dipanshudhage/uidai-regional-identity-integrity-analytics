import streamlit as st
import pandas as pd
import plotly.express as px

from feature_engineering import generate_features
from risk_engine import calculate_risk
from ml_engine import detect_anomalies

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="UIDAI Regional Integrity Analytics",
    page_icon="🛡️",
    layout="wide"
)

# ==================================================
# HEADER
# ==================================================
st.title("🛡️ UIDAI – Regional Identity Integrity Analytics Platform")
st.caption(
    "Upload aggregated Aadhaar enrolment, demographic update, and biometric update datasets "
    "to instantly detect regional risks and anomalies (privacy-first, policy-safe)."
)

st.markdown("---")

# ==================================================
# SIDEBAR – FILE UPLOAD
# ==================================================
st.sidebar.header("📤 Upload Datasets")

enrol_file = st.sidebar.file_uploader(
    "Enrolment Data (CSV)",
    type=["csv"]
)

demo_file = st.sidebar.file_uploader(
    "Demographic Update Data (CSV)",
    type=["csv"]
)

bio_file = st.sidebar.file_uploader(
    "Biometric Update Data (CSV)",
    type=["csv"]
)

# ==================================================
# COLUMN VALIDATION
# ==================================================
def validate_columns(df, required_cols):
    return all(col in df.columns for col in required_cols)

# ==================================================
# MAIN LOGIC
# ==================================================
if enrol_file and demo_file and bio_file:

    with st.spinner("📥 Reading uploaded files..."):
        enrol = pd.read_csv(enrol_file)
        demo  = pd.read_csv(demo_file)
        bio   = pd.read_csv(bio_file)

    # ---------------- VALIDATION ----------------
    if not validate_columns(
        enrol,
        ["state","district","pincode","age_0_5","age_5_17","age_18_greater"]
    ):
        st.error("❌ Enrolment file columns are incorrect")
        st.stop()

    if not validate_columns(
        demo,
        ["state","district","pincode","demo_age_5_17","demo_age_17_"]
    ):
        st.error("❌ Demographic update file columns are incorrect")
        st.stop()

    if not validate_columns(
        bio,
        ["state","district","pincode","bio_age_5_17","bio_age_17_"]
    ):
        st.error("❌ Biometric update file columns are incorrect")
        st.stop()

    # ---------------- PROCESSING ----------------
    with st.spinner("⚙️ Generating features, risk scores & anomalies..."):
        features = generate_features(enrol, demo, bio)
        risk = calculate_risk(features)
        risk = detect_anomalies(risk)

    # ==================================================
    # FILTERS
    # ==================================================
    st.sidebar.header("🔍 Filters")

    selected_states = st.sidebar.multiselect(
        "Select State(s)",
        sorted(risk["state"].unique())
    )

    if selected_states:
        risk = risk[risk["state"].isin(selected_states)]

    # ==================================================
    # KPIs
    # ==================================================
    st.markdown("## 📊 Key Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Regions", len(risk))
    c2.metric("High-Risk Regions", len(risk[risk["risk_level"] == "HIGH"]))
    c3.metric("Anomalous Regions", len(risk[risk["anomaly_flag"] == "ANOMALY"]))
    c4.metric("Average Risk Score", round(risk["risk_score"].mean(), 3))

    st.markdown("---")

    # ==================================================
    # RISK DISTRIBUTION
    # ==================================================
    st.markdown("## 📈 Risk Distribution")
    st.bar_chart(risk["risk_level"].value_counts())

    # ==================================================
    # STATE HEATMAP
    # ==================================================
    st.markdown("## 🗺️ State-wise Average Risk")

    state_risk = (
        risk.groupby("state", as_index=False)
        .agg(avg_risk=("risk_score", "mean"))
    )

    fig = px.bar(
        state_risk.sort_values("avg_risk", ascending=False),
        x="state",
        y="avg_risk",
        color="avg_risk",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # HIGH-RISK TABLE
    # ==================================================
    st.markdown("## 🚨 Top High-Risk Regions")

    st.dataframe(
        risk.sort_values("risk_score", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    # ==================================================
    # ANOMALY TABLE
    # ==================================================
    st.markdown("## 🧠 Detected Anomalies")

    st.dataframe(
        risk[risk["anomaly_flag"] == "ANOMALY"]
        .sort_values("risk_score", ascending=False)
        .reset_index(drop=True)
    )

    # ==================================================
    # EXPORT
    # ==================================================
    st.markdown("## 📥 Export Reports")

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "⬇️ Download Full Risk Report",
            data=risk.to_csv(index=False),
            file_name="uidai_full_risk_report.csv",
            mime="text/csv"
        )

    with c2:
        st.download_button(
            "⬇️ Download High-Risk Regions",
            data=risk[risk["risk_level"] == "HIGH"].to_csv(index=False),
            file_name="uidai_high_risk_regions.csv",
            mime="text/csv"
        )

    # ==================================================
    # AUTO INSIGHTS
    # ==================================================
    st.markdown("## 📝 Automated Insights")

    st.success(
        f"""
        ✔ {len(risk[risk["risk_level"]=="HIGH"])} regions show **HIGH integrity risk**  
        ✔ {len(risk[risk["anomaly_flag"]=="ANOMALY"])} regions exhibit **abnormal behaviour**  
        ✔ Minor (age 5–17) update ratios are a major risk contributor  
        ✔ Analysis is fully **aggregated & privacy-preserving**
        """
    )

else:
    st.info("👈 Upload **all three CSV files** from the sidebar to start analysis.")

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption(
    "UIDAI Database Hackathon Prototype | Privacy-first • Scalable • Explainable • Audit-ready"
)
