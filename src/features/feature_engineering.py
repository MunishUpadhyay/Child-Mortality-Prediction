import pandas as pd
from sklearn.preprocessing import MinMaxScaler


FEATURE_COLUMNS = [
    'immunization',
    'stunting',
    'wasting',
    'female_literacy',
    'sanitation'
]


def normalize_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize feature columns using Min-Max scaling (0–1).
    """

    df = df.copy()

    scaler = MinMaxScaler()
    df[FEATURE_COLUMNS] = scaler.fit_transform(df[FEATURE_COLUMNS])

    return df


def create_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create basic risk score.
    Higher score = higher risk.
    """

    df = df.copy()

    df['risk_score'] = (
        df['stunting'] +
        df['wasting'] +
        (1 - df['immunization']) +
        (1 - df['female_literacy']) +
        (1 - df['sanitation'])
    )

    return df


def create_weighted_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create weighted risk score based on domain knowledge.
    """

    df = df.copy()

    df['weighted_risk_score'] = (
        0.3 * df['stunting'] +
        0.3 * df['wasting'] +
        0.15 * (1 - df['immunization']) +
        0.15 * (1 - df['female_literacy']) +
        0.10 * (1 - df['sanitation'])
    )

    return df


def create_risk_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create categorical labels (Low, Medium, High risk).
    """

    df = df.copy()

    df['risk_category'] = pd.qcut(
        df['weighted_risk_score'],
        q=3,
        labels=['Low', 'Medium', 'High'],
        duplicates='drop'  # prevents crash if duplicate bins
    )

    return df


def feature_engineering_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline.
    """

    df = normalize_features(df)
    df = create_risk_score(df)
    df = create_weighted_risk_score(df)
    df = create_risk_category(df)

    return df