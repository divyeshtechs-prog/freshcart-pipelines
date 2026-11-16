from sklearn.datasets import load_iris


@data_loader
def load_iris_data(*args, **kwargs):
    """
    Load the Iris dataset from scikit-learn.
    """
    iris = load_iris()

    return {
        "X": iris.data.tolist(),
        "y": iris.target.tolist(),
        "feature_names": iris.feature_names,
        "target_names": iris.target_names.tolist(),
    }