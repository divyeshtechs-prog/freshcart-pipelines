
import json
import os
from datetime import datetime


@transformer
def transform(data, data_2, *args, **kwargs):

    # Evaluation metrics
    evaluation_data = data

    # Model configuration
    model_data = data_2

    results = {
        "model": "DecisionTreeClassifier",
        "max_depth": model_data["max_depth"],
        "accuracy": evaluation_data["accuracy"],
        "precision": evaluation_data["precision"],
        "recall": evaluation_data["recall"],
        "f1_score": evaluation_data["f1_score"],
        "confusion_matrix": evaluation_data["confusion_matrix"],
        "evaluated_at": datetime.now().isoformat(),
    }

    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "iris_results.json")

    with open(output_path, "w") as file:
        json.dump(results, file, indent=4)

    return {
        "status": "success",
        "file_path": output_path,
        "results": results,
    }

@test
def test_output(output, *args) -> None:
    assert output["status"] == "success"
    assert output["results"]["model"] == "DecisionTreeClassifier"
    assert 0 <= output["results"]["accuracy"] <= 1
    assert os.path.exists(output["file_path"])
