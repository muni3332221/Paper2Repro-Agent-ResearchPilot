from __future__ import annotations

import re
from collections import OrderedDict

KEYWORDS = {
    "datasets": ["MNIST", "CIFAR", "ImageNet", "COCO", "SQuAD", "WikiText", "GLUE", "arXiv", "PubMed", "UCI"],
    "metrics": ["accuracy", "f1", "precision", "recall", "auc", "rmse", "mae", "bleu", "rouge", "perplexity", "mse"],
    "baselines": ["baseline", "BERT", "ResNet", "LSTM", "Transformer", "SVM", "Random Forest", "CNN", "MLP"],
}


def unique_keep_order(items: list[str]) -> list[str]:
    return list(OrderedDict.fromkeys([x.strip() for x in items if x.strip()]))


def sentences(text: str, limit: int = 8) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text))
    return [p.strip() for p in parts if len(p.strip()) > 40][:limit]


def find_keywords(text: str, category: str) -> list[str]:
    found: list[str] = []
    for kw in KEYWORDS[category]:
        if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
            found.append(kw)
    return unique_keep_order(found)


def find_hyperparameters(text: str) -> dict[str, str]:
    patterns = {
        "learning_rate": r"learning rate(?: of)?\s*[:=]?\s*([0-9.eE-]+)",
        "batch_size": r"batch size\s*[:=]?\s*([0-9]+)",
        "epochs": r"(?:trained for|epochs?)\s*[:=]?\s*([0-9]+)",
        "optimizer": r"\b(AdamW?|SGD|RMSProp)\b",
    }
    result: dict[str, str] = {}
    for name, pattern in patterns.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            result[name] = m.group(1)
    return result


def likely_framework(text: str) -> str:
    lower = text.lower()
    if "pytorch" in lower or "torch" in lower:
        return "pytorch"
    if "jax" in lower:
        return "jax"
    if "tensorflow" in lower or "keras" in lower:
        return "tensorflow"
    return "python"
