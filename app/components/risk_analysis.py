import streamlit as st
import pandas as pd
from utils.config import DATA_PATH

def show_risk_analysis():
    df = pd.read_csv(DATA_PATH)

    st.subheader("🚨 High Risk States")

    high = df[df["risk_category"] == "High"] \
        .sort_values(by="weighted_risk_score", ascending=False) \
        .reset_index(drop=True)

    st.dataframe(high[["state", "weighted_risk_score"]], use_container_width=True)

    st.markdown("""
    These states show high mortality risk due to:
    - Malnutrition  
    - Poor sanitation  
    - Low literacy  
    """)