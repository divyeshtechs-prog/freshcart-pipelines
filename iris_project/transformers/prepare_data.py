import pandas as pd
from sklearn.model_selection import train_test_split


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a split column identifying training and testing records.

    Uses an 80:20 split with stratification to preserve
    the class distribution.
    """
    result = df.copy()

    train_indices, test_indices = train_test_split(
        result.index,
        test_size=0.2,
        random_state=42,
        stratify=result["target"]
    )

    result["split"] = "train"
    result.loc[test_indices, "split"] = "test"

    return result