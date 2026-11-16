from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


@transformer
def transform(model_data, split_data, *args, **kwargs):
    model = model_data["model"]
    X_test = split_data["X_test"]
    y_test = split_data["y_test"]

    assert X_test is not None and y_test is not None

    predictions = model.predict(X_test)

    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(
            y_test, predictions, average="weighted"
        )),
        "recall": float(recall_score(
            y_test, predictions, average="weighted"
        )),
        "f1_score": float(f1_score(
            y_test, predictions, average="weighted"
        )),
        "confusion_matrix": confusion_matrix(
            y_test, predictions
        ).tolist(),
    }


@test
def test_output(output, *args) -> None:
    assert 0 <= output["accuracy"] <= 1
    assert 0 <= output["precision"] <= 1
    assert 0 <= output["recall"] <= 1
    assert 0 <= output["f1_score"] <= 1
    assert len(output["confusion_matrix"]) == 3