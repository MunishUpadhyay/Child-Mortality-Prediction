import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os

# -------------------------
# PATH
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "random_forest_model.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# -------------------------
# GAUGE
# -------------------------
def gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [0, 1]},
            'steps': [
                {'range': [0, 0.33], 'color': "#2ecc71"},
                {'range': [0.33, 0.66], 'color': "#f39c12"},
                {'range': [0.66, 1], 'color': "#e74c3c"}
            ]
        }
    ))
    return fig

# -------------------------
# CLASSIFICATION
# -------------------------
def classify(score):
    if score < 0.33:
        return "Low", "🟢", "Healthy conditions with low child mortality risk"
    elif score < 0.66:
        return "Medium", "🟠", "Moderate risk requiring attention"
    else:
        return "High", "🔴", "High risk – urgent intervention needed"

# -------------------------
# MAIN FUNCTION
# -------------------------
def show_prediction():

    st.subheader("🔮 Predict Child Mortality Risk")

    st.markdown("Adjust indicators to estimate risk level.")

    immunization = st.slider("Immunization (%)", 0, 100, 70)
    stunting = st.slider("Stunting (%)", 0, 100, 30)
    wasting = st.slider("Wasting (%)", 0, 100, 20)
    literacy = st.slider("Female Literacy (%)", 0, 100, 75)
    sanitation = st.slider("Sanitation (%)", 0, 100, 60)

    if st.button("Predict"):

        input_df = pd.DataFrame([{
            'immunization': immunization / 100,
            'stunting': stunting / 100,
            'wasting': wasting / 100,
            'female_literacy': literacy / 100,
            'sanitation': sanitation / 100
        }])

        # ML prediction (kept for reference)
        model_pred = model.predict(input_df)[0]

        # Weighted score (PRIMARY)
        score = (
            0.3 * input_df['stunting'][0] +
            0.3 * input_df['wasting'][0] +
            0.15 * (1 - input_df['immunization'][0]) +
            0.15 * (1 - input_df['female_literacy'][0]) +
            0.1 * (1 - input_df['sanitation'][0])
        )

        category, emoji, description = classify(score)

        # -------------------------
        # OUTPUT
        # -------------------------
        st.markdown("## 📊 Prediction Result")

        col1, col2 = st.columns(2)

        col1.metric("Risk Score", f"{score:.3f}")
        col2.metric("Model Prediction", model_pred)

        st.markdown(f"### {emoji} {category} Risk")
        st.info(description)

        # Gauge
        st.plotly_chart(gauge(score), use_container_width=True)

        # -------------------------
        # EXPLANATION
        # -------------------------
        st.markdown("### 🔍 Key Drivers")

        reasons = []

        if stunting > 30:
            reasons.append("High stunting (chronic malnutrition)")
        if wasting > 15:
            reasons.append("High wasting (acute malnutrition)")
        if immunization < 70:
            reasons.append("Low immunization coverage")
        if sanitation < 60:
            reasons.append("Poor sanitation conditions")
        if literacy < 70:
            reasons.append("Low female literacy")

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.success("All indicators are within healthy range")

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------
        st.markdown("### 💡 Recommendations")

        if category == "High":
            st.error("Focus on nutrition programs, sanitation, and maternal education urgently.")
        elif category == "Medium":
            st.warning("Improve awareness, healthcare access, and nutrition gradually.")
        else:
            st.success("Maintain current standards and monitor consistently.")