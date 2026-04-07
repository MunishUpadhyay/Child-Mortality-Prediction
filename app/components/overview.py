import streamlit as st
import pandas as pd
from utils.config import DATA_PATH

def show_overview():
    df = pd.read_csv(DATA_PATH)

    st.subheader("📊 Dataset Overview")

    st.markdown("""
    ### What this data represents:

    - **Immunization** → % vaccinated children  
    - **Stunting** → chronic malnutrition  
    - **Wasting** → acute malnutrition  
    - **Female Literacy** → education level  
    - **Sanitation** → hygiene access  
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Immunization", f"{df['immunization'].mean()*100:.1f}%")
    col2.metric("Avg Stunting", f"{df['stunting'].mean()*100:.1f}%")
    col3.metric("Avg Wasting", f"{df['wasting'].mean()*100:.1f}%")

    st.dataframe(df, use_container_width=True)