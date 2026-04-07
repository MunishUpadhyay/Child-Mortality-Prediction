import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils.config import MODEL_PATH

def show_feature_importance():
    model = joblib.load(MODEL_PATH)

    features = ['immunization', 'stunting', 'wasting', 'female_literacy', 'sanitation']
    importance = model.feature_importances_

    df = pd.DataFrame({
        "Feature": features,
        "Importance": importance
    }).sort_values(by="Importance")

    st.subheader("📈 Key Drivers")

    fig = px.bar(df, x="Importance", y="Feature", orientation="h")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    👉 Stunting & wasting dominate risk  
    👉 Nutrition improvement is key  
    """)