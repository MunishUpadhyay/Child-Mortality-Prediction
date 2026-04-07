import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "nfhs_with_risk_scores.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "random_forest_model.pkl")
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "raw", "india_states.geojson")