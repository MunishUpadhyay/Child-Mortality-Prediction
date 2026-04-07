from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from typing import Tuple


def train_random_forest(
    X,
    y,
    n_estimators: int = 100,
    max_depth: int = None,
    random_state: int = 42
) -> RandomForestClassifier:
    """
    Train a Random Forest model.
    """

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )

    model.fit(X, y)

    return model


def train_decision_tree(
    X,
    y,
    max_depth: int = None,
    random_state: int = 42
) -> DecisionTreeClassifier:
    """
    Train a Decision Tree model.
    """

    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=random_state
    )

    model.fit(X, y)

    return model


def prepare_features_and_target(df) -> Tuple:
    """
    Extract features (X) and target (y) from dataframe.
    """

    X = df[
        [
            'immunization',
            'stunting',
            'wasting',
            'female_literacy',
            'sanitation'
        ]
    ]

    y = df['risk_category']

    return X, y