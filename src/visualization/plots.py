import os
import matplotlib.pyplot as plt
import seaborn as sns


# Ensure consistent style
sns.set(style="whitegrid")


def _ensure_dir(path: str):
    """
    Ensure directory exists before saving.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def plot_feature_importance(importance_df, save_path: str):
    """
    Plot feature importance.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=importance_df,
        x='importance',
        y='feature'
    )

    plt.title("Feature Importance (Child Mortality Risk)")
    plt.xlabel("Importance")
    plt.ylabel("Feature")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_risk_distribution(df, save_path: str):
    """
    Plot distribution of weighted risk score.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(8, 5))

    sns.histplot(df['weighted_risk_score'], bins=10, kde=True)

    plt.title("Distribution of Risk Score")
    plt.xlabel("Risk Score")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_risk_category_count(df, save_path: str):
    """
    Plot count of risk categories.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(6, 4))

    sns.countplot(data=df, x='risk_category')

    plt.title("Risk Category Distribution")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_unicef_trend(df, save_path: str):
    """
    Plot UNICEF mortality trend.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df,
        x='year',
        y='u5mr',
        marker='o'
    )

    plt.title("Under-5 Mortality Trend (India)")
    plt.xlabel("Year")
    plt.ylabel("U5MR")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_srs_causes(df, save_path: str):
    """
    Plot SRS cause distribution.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x='percentage',
        y='cause'
    )

    plt.title("Major Causes of Child Death")
    plt.xlabel("Percentage")
    plt.ylabel("Cause")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_srs_category(df, save_path: str):
    """
    Plot SRS category distribution.
    """

    _ensure_dir(save_path)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=df,
        x='percentage',
        y='category'
    )

    plt.title("Child Death Causes by Category")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()