
@transformer
def transform(data, *args, **kwargs):
    model = data["model"]
    feature_names = data["feature_names"]

    importance = model.feature_importances_

    results = [
        {
            "feature": name,
            "importance": float(score)
        }
        for name, score in zip(feature_names, importance)
    ]

    results.sort(key=lambda x: x["importance"], reverse=True)

    return results

@test
def test_output(output, *args) -> None:
    assert isinstance(output, dict)
    assert "feature" in output
    assert "importance" in output
    assert 0 <= output["importance"] <= 1