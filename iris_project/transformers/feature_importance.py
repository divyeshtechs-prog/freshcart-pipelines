
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
    assert isinstance(output, list)
    assert len(output) == 4

    for item in output:
        assert isinstance(item, dict)
        assert "feature" in item
        assert "importance" in item
        assert 0 <= item["importance"] <= 1

    assert abs(sum(item["importance"] for item in output) - 1.0) < 1e-6