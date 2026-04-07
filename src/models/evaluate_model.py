import pandas as pd
from sklearn.model_selection import cross_val_score
from typing import Tuple


def evaluate_model(model, X, y, cv: int = 5) -> Tuple[list, float]:
    """
    Evaluate model using cross-validation.

    Returns:
    - scores (list)
    - mean accuracy (float)
    """

    scores = cross_val_score(model, X, y, cv=cv)

    return scores.tolist(), scores.mean()


def get_feature_importance(model, feature_names) -> pd.DataFrame:
    """
    Extract feature importance from trained model.
    """

    if not hasattr(model, "feature_importances_"):
        raise AttributeError("Model does not support feature importances")

    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)

    return importance_df


def print_evaluation_results(scores, mean_score):
    """
    Pretty print evaluation results.
    """

    print("Cross-validation scores:", scores)
    print(f"Mean accuracy: {mean_score:.4f}")


def summarize_feature_importance(importance_df: pd.DataFrame):
    """
    Print feature importance in readable format.
    """

    print("\nFeature Importance Ranking:\n")

    for i, row in enumerate(importance_df.itertuples(), 1):
        print(f"{i}. {row.feature}: {row.importance:.4f}")