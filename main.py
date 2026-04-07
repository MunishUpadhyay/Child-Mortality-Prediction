import os
import joblib

# Data
from src.data.load_data import load_nfhs_data
from src.data.preprocess import preprocess_nfhs

# Features
from src.features.feature_engineering import feature_engineering_pipeline

# Models
from src.models.train_model import (
    train_random_forest,
    prepare_features_and_target
)

from src.models.evaluate_model import (
    evaluate_model,
    get_feature_importance,
    print_evaluation_results,
    summarize_feature_importance
)

# Visualization
from src.visualization.plots import (
    plot_feature_importance,
    plot_risk_distribution,
    plot_risk_category_count
)


# =========================
# CONFIG
# =========================

NFHS_PATH = "data/processed/state_factors_nfhs.csv"
MODEL_SAVE_PATH = "outputs/models/random_forest_model.pkl"

FIGURE_PATHS = {
    "feature_importance": "outputs/figures/comparisons/nfhs_feature_importance_final.png",
    "risk_distribution": "outputs/figures/distributions/nfhs_risk_distribution_final.png",
    "risk_category": "outputs/figures/distributions/nfhs_risk_category_final.png"
}


# =========================
# MAIN PIPELINE
# =========================

def main():
    print("\n🚀 Starting Child Mortality Analysis Pipeline...\n")

    # -------------------------
    # 1. Load Data
    # -------------------------
    print("📥 Loading data...")
    df = load_nfhs_data(NFHS_PATH)

    # -------------------------
    # 2. Preprocess
    # -------------------------
    print("🧹 Preprocessing data...")
    df = preprocess_nfhs(df)

    # -------------------------
    # 3. Feature Engineering
    # -------------------------
    print("⚙️ Performing feature engineering...")
    df = feature_engineering_pipeline(df)

    # -------------------------
    # 4. Prepare ML Data
    # -------------------------
    print("📊 Preparing features and target...")
    X, y = prepare_features_and_target(df)

    # -------------------------
    # 5. Train Model
    # -------------------------
    print("🤖 Training model...")
    model = train_random_forest(X, y)

    # -------------------------
    # 6. Evaluate Model
    # -------------------------
    print("📈 Evaluating model...")
    scores, mean_score = evaluate_model(model, X, y)

    print_evaluation_results(scores, mean_score)

    # -------------------------
    # 7. Feature Importance
    # -------------------------
    print("\n🔍 Extracting feature importance...")
    importance_df = get_feature_importance(model, X.columns)

    summarize_feature_importance(importance_df)

    # -------------------------
    # 8. Save Model
    # -------------------------
    print("\n💾 Saving model...")
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump(model, MODEL_SAVE_PATH)

    # -------------------------
    # 9. Generate Plots
    # -------------------------
    print("\n📊 Generating plots...")

    plot_feature_importance(
        importance_df,
        FIGURE_PATHS["feature_importance"]
    )

    plot_risk_distribution(
        df,
        FIGURE_PATHS["risk_distribution"]
    )

    plot_risk_category_count(
        df,
        FIGURE_PATHS["risk_category"]
    )

    print("\n✅ Pipeline completed successfully!\n")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main()