
from sklearn.tree import DecisionTreeClassifier


@transformer
def transform(data, *args, **kwargs):
    X_train = data["X_train"]
    y_train = data["y_train"]

    # Read max_depth from Mage runtime variables (default: 3)
    # Read max_depth from Mage block variables
    configuration = kwargs.get("configuration", {})
    max_depth = int(configuration.get("max_depth", 3))
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    feature_names = data["feature_names"]

    return {
    "model": model,
    "max_depth": max_depth,
    "training_samples": len(X_train),
    "feature_names": feature_names,
}


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert output["model"] is not None
    assert output["training_samples"] == 120
    assert 1 <= output["max_depth"] <= 5
