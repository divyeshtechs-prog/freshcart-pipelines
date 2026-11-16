
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    # Allows local pytest execution outside the Mage container.
    def transformer(func):
        return func

    def test(func):
        return func


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


@transformer
def transform(data, *args, **kwargs):
    """
    Prepare data for the Iris classification pipeline.

    Supports both Mage dictionary input and the standalone
    DataFrame input used by the CI test.
    """

    # Standalone CI test compatibility
    if isinstance(data, pd.DataFrame):
        result = data.copy()

        train_indices, test_indices = train_test_split(
            result.index,
            test_size=0.2,
            random_state=42,
            stratify=result["target"],
        )

        result["split"] = "train"
        result.loc[test_indices, "split"] = "test"

        return result

    # Mage pipeline execution
    X = np.array(data["X"])
    y = np.array(data["y"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    return {
        "X_train": X_train.tolist(),
        "X_test": X_test.tolist(),
        "y_train": y_train.tolist(),
        "y_test": y_test.tolist(),
        "feature_names": data["feature_names"],
    }


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output["X_train"]) == 120
    assert len(output["X_test"]) == 30
    assert len(output["y_train"]) == 120
    assert len(output["y_test"]) == 30
