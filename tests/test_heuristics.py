from paper2repro.heuristics import find_hyperparameters, find_keywords, likely_framework


def test_find_keywords() -> None:
    text = "We evaluate on MNIST and CIFAR using accuracy and F1 against ResNet."
    assert "MNIST" in find_keywords(text, "datasets")
    assert "accuracy" in [x.lower() for x in find_keywords(text, "metrics")]
    assert "ResNet" in find_keywords(text, "baselines")


def test_find_hyperparameters() -> None:
    text = "We use Adam with learning rate 1e-3 and batch size 64 for 20 epochs."
    hp = find_hyperparameters(text)
    assert hp["learning_rate"] == "1e-3"
    assert hp["batch_size"] == "64"
    assert hp["optimizer"].lower() == "adam"


def test_likely_framework() -> None:
    assert likely_framework("implemented in PyTorch") == "pytorch"
    assert likely_framework("implemented in JAX") == "jax"
