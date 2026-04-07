import pandas as pd


NUMERIC_COLS = [
    'immunization',
    'stunting',
    'wasting',
    'female_literacy',
    'sanitation'
]


def clean_nfhs_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean NFHS dataset:
    - Remove duplicates
    - Convert to numeric
    - Handle missing values
    - Validate ranges (0–100)
    """

    df = df.copy()

    # 1️⃣ Remove duplicates
    df = df.drop_duplicates()

    # 2️⃣ Convert columns to numeric
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3️⃣ Drop rows with missing values
    df = df.dropna(subset=NUMERIC_COLS)

    # 4️⃣ Validate value ranges (0–100)
    for col in NUMERIC_COLS:
        df = df[(df[col] >= 0) & (df[col] <= 100)]

    # 5️⃣ Clean state names (strip spaces)
    if 'state' in df.columns:
        df['state'] = df['state'].str.strip()

    # 6️⃣ Final reset index
    df = df.reset_index(drop=True)

    return df


def validate_nfhs_data(df: pd.DataFrame) -> None:
    """
    Perform sanity checks on cleaned data.
    Raises error if something is wrong.
    """

    if df.empty:
        raise ValueError("Dataset is empty after preprocessing")

    if df['state'].nunique() != len(df):
        raise ValueError("Duplicate or inconsistent state entries found")

    for col in NUMERIC_COLS:
        if df[col].isnull().any():
            raise ValueError(f"Null values found in column: {col}")

        if not ((df[col] >= 0) & (df[col] <= 100)).all():
            raise ValueError(f"Invalid values in column: {col}")


def preprocess_nfhs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full preprocessing pipeline for NFHS dataset.
    """

    df_clean = clean_nfhs_data(df)
    validate_nfhs_data(df_clean)

    return df_clean