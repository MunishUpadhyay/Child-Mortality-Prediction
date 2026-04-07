import streamlit as st
import pandas as pd
import folium
import json
import os
from streamlit_folium import st_folium

# -------------------------
# PATHS
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "nfhs_with_risk_scores.csv")
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "raw", "india_states.geojson")

# -------------------------
# COLOR FUNCTION
# -------------------------
def get_color(risk):
    return {
        "Low": "#2ecc71",
        "Medium": "#f39c12",
        "High": "#e74c3c"
    }.get(risk, "#bdc3c7")

# -------------------------
# HUMAN FRIENDLY INSIGHT
# -------------------------
def get_insight(row):

    if row["risk_category"] == "High":
        return "Severe malnutrition & weak health conditions"
    elif row["risk_category"] == "Medium":
        return "Moderate health and nutrition concerns"
    else:
        return "Healthy conditions with low mortality risk"

# -------------------------
# MAIN FUNCTION
# -------------------------

def display_name(state):
    return {
        "Uttaranchal": "Uttarakhand",
        "Orissa": "Odisha"
    }.get(state, state)

def show_map():

    st.subheader("🌍 Child Mortality Risk Map")

    st.markdown("Hover over a state to understand risk level.")

    df = pd.read_csv(DATA_PATH)

    # -------------------------
    # STATE NAME FIXES
    # -------------------------
    df['state'] = df['state'].replace({
        "Jammu & Kashmir": "Jammu and Kashmir",
        "NCT of Delhi": "Delhi",
        "Odisha": "Orissa",
        "Uttarakhand": "Uttaranchal",
        "Maharastra": "Maharashtra",
        "Andaman & Nicobar Islands": "Andaman and Nicobar",
    })

    # -------------------------
    # LOAD GEOJSON
    # -------------------------
    with open(GEOJSON_PATH) as f:
        geojson = json.load(f)

    # -------------------------
    # INDIA-FOCUSED MAP
    # -------------------------
    m = folium.Map(
        location=[22.5, 80],
        zoom_start=5,
        min_zoom=5,
        max_zoom=6,
        tiles=None   # 🔥 IMPORTANT: removes world map tiles
    )

    # Light background instead of full world map
    folium.TileLayer(
        tiles="CartoDB positron",
        control=False
    ).add_to(m)

    # -------------------------
    # ADD STATES
    # -------------------------
    for feature in geojson["features"]:

        state_name = feature["properties"].get("NAME_1")
        state_data = df[df["state"] == state_name]

        if not state_data.empty:

            row = state_data.iloc[0]
            insight = get_insight(row)

            tooltip_text = f"""
            <b>{display_name(state_name)}</b><br>
            Risk Level: <b>{row['risk_category']}</b><br>
            {insight}
            """

            folium.GeoJson(
                feature,
                style_function=lambda x, color=get_color(row["risk_category"]): {
                    "fillColor": color,
                    "color": "#000000",
                    "weight": 1.5,
                    "fillOpacity": 0.85,
                },
                highlight_function=lambda x: {
                    "weight": 3,
                    "color": "#000000"
                },
                tooltip=folium.Tooltip(tooltip_text, sticky=False)
            ).add_to(m)

    # -------------------------
    # LOCK VIEW TO INDIA
    # -------------------------
    m.fit_bounds([[6, 68], [37, 97]])  # India bounding box

    # -------------------------
    # DISPLAY MAP
    # -------------------------
    st_folium(m, width=900, height=600)

    # -------------------------
    # LEGEND (IMPROVED)
    # -------------------------
    st.markdown("""
    ### 🗺️ Risk Interpretation

    - 🟢 **Low Risk** → Good healthcare, nutrition, and sanitation
    - 🟠 **Medium Risk** → Moderate issues requiring attention
    - 🔴 **High Risk** → Severe conditions needing urgent intervention
    """)

    # -------------------------
    # DISCLAIMER (YOU ASKED)
    # -------------------------
    st.markdown("---")
    st.warning("""
    ⚠️ **Disclaimer**

    This map uses publicly available geographic datasets.

    - Disputed regions (e.g., parts of Jammu & Kashmir, Ladakh) may not be fully represented.
    - Boundaries are for analytical and visualization purposes only.
    - This does not reflect official political boundaries.
    """)