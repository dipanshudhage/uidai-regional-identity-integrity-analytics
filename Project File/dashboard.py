import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def show_overview(enrol, demo, bio, risk):
    st.metric("Total Enrolments", len(enrol))
    st.metric("Demographic Updates", len(demo))
    st.metric("Biometric Updates", len(bio))
    st.metric("High Risk Identities", len(risk[risk["risk_level"]=="HIGH"]))

def show_risk_distribution(risk):
    st.subheader("Risk Level Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x="risk_level", data=risk, ax=ax)
    st.pyplot(fig)

def show_high_risk(risk):
    st.subheader("High Risk Aadhaar (Masked)")
    st.dataframe(
        risk[risk["risk_level"]=="HIGH"]
        .sort_values("risk_score", ascending=False)
    )
