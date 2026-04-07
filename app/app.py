import streamlit as st
st.cache_data.clear()
st.cache_resource.clear()

from components.overview import show_overview
from components.map_view import show_map
from components.feature_importance import show_feature_importance
from components.risk_analysis import show_risk_analysis
from components.prediction import show_prediction

st.set_page_config(page_title="Child Mortality Analysis", layout="wide")

st.title("👶 Child Mortality Risk Analysis (India)")

st.markdown("""
### 🧠 Key Insights

- Malnutrition (stunting & wasting) is the strongest driver  
- Improving nutrition has the highest impact  
- High-risk states need targeted intervention  
""")

section = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "India Risk Map",
        "Feature Importance",
        "Risk Analysis",
        "Prediction Tool"
    ]
)

if section == "Overview":
    show_overview()

elif section == "India Risk Map":
    show_map()

elif section == "Feature Importance":
    show_feature_importance()

elif section == "Risk Analysis":
    show_risk_analysis()

elif section == "Prediction Tool":
    show_prediction()