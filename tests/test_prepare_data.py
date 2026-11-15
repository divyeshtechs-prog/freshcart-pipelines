import pandas as pd

from iris_project.transformers.prepare_data import transform


def test_split_is_80_20():
    df = pd.DataFrame({
        "sepal length (cm)": range(150),
        "target": [0, 1, 2] * 50
    })

    result = transform(df)

    assert (result["split"] == "train").sum() == 120
    assert (result["split"] == "test").sum() == 30
