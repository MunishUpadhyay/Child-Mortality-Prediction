import pandas as pd
import os


def load_csv(path: str) -> pd.DataFrame:
    """
    Generic CSV loader with validation.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Error loading file {path}: {e}")

    return df


def load_nfhs_data(path: str) -> pd.DataFrame:
    """
    Load NFHS dataset.
    """
    df = load_csv(path)

    expected_cols = {
        'state',
        'immunization',
        'stunting',
        'wasting',
        'female_literacy',
        'sanitation'
    }

    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"NFHS dataset missing columns: {missing}")

    return df


def load_unicef_data(path: str) -> pd.DataFrame:
    """
    Load UNICEF trend dataset.
    """
    df = load_csv(path)

    expected_cols = {'year', 'u5mr'}
    missing = expected_cols - set(df.columns)

    if missing:
        raise ValueError(f"UNICEF dataset missing columns: {missing}")

    return df


def load_srs_data(causes_path: str, category_path: str):
    """
    Load SRS datasets.
    """
    df_causes = load_csv(causes_path)
    df_category = load_csv(category_path)

    # Basic validation
    if df_causes.empty or df_category.empty:
        raise ValueError("SRS datasets are empty")

    return df_causes, df_category