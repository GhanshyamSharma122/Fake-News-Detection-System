"""Train and evaluate the NewsLens text classifier.

Example:
    python training/train_model.py --input data/raw/news.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from nlp_utils import tokenize_text

ROOT = Path(__file__).resolve().parents[1]
LABEL_MAP = {"true": 0, "real": 0, "0": 0, "false": 1, "fake": 1, "1": 1}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the NewsLens fake-news classifier.")
    parser.add_argument("--input", type=Path, required=True, help="CSV with text and label columns, or an ISOT folder containing Fake.csv and True.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output", type=Path, default=ROOT / "models" / "newslens.joblib")
    parser.add_argument("--test-size", type=float, default=0.2)
    return parser.parse_args()


def load_csv(path: Path, text_column: str, label_column: str, forced_label: str | None = None) -> tuple[list[str], list[str]]:
    texts, labels = [], []
    with path.open(newline="", encoding="utf-8", errors="replace") as stream:
        for row in csv.DictReader(stream):
            text = row.get(text_column, "") if forced_label is None else f"{row.get('Title', row.get('title', ''))}\n{row.get('Text', row.get('text', ''))}"
            label = row.get(label_column, "") if forced_label is None else forced_label
            if text.strip() and label.strip():
                texts.append(text)
                labels.append(label)
    return texts, labels


def load_input(path: Path, text_column: str, label_column: str) -> tuple[list[str], list[str], str]:
    if path.is_dir() and (path / "Fake.csv").exists() and (path / "True.csv").exists():
        fake_texts, fake_labels = load_csv(path / "Fake.csv", text_column, label_column, "fake")
        true_texts, true_labels = load_csv(path / "True.csv", text_column, label_column, "true")
        return fake_texts + true_texts, fake_labels + true_labels, "ISOT Fake.csv + True.csv"
    texts, labels = load_csv(path, text_column, label_column)
    return texts, labels, str(path)


def input_hash(path: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path.glob("*.csv")) if path.is_dir() else [path]
    for file in files:
        digest.update(file.name.encode("utf-8"))
        with file.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    arguments = parse_arguments()
    if not arguments.input.exists():
        print(f"Dataset not found: {arguments.input}", file=sys.stderr)
        return 1
    texts, raw_labels, dataset_name = load_input(arguments.input, arguments.text_column, arguments.label_column)
    if len(texts) < 1000:
        print("Refusing to train: provide at least 1,000 reviewed rows for a meaningful experiment.", file=sys.stderr)
        return 1
    labels = [LABEL_MAP.get(label.strip().lower()) for label in raw_labels]
    if any(label is None for label in labels) or len(set(labels)) != 2:
        print("Labels must map to two classes: true/false, real/fake, or 0/1.", file=sys.stderr)
        return 1
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=arguments.test_size, random_state=42, stratify=labels
    )
    pipeline = Pipeline([
        ("features", TfidfVectorizer(tokenizer=tokenize_text, token_pattern=None, ngram_range=(1, 1), min_df=3, max_df=0.98, max_features=50_000, sublinear_tf=True)),
        ("classifier", LogisticRegression(solver="liblinear", max_iter=200, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit(train_texts, train_labels)
    predictions = pipeline.predict(test_texts)
    report = classification_report(test_labels, predictions, output_dict=True, zero_division=0)
    metrics = {
        "accuracy": round(float(accuracy_score(test_labels, predictions)), 4),
        "precision": round(float(precision_score(test_labels, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(test_labels, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(test_labels, predictions, zero_division=0)), 4),
        "classification_report": report,
        "training_rows": len(train_texts),
        "test_rows": len(test_texts),
        "class_distribution": dict(Counter(labels)),
    }
    artifact = {
        "pipeline": pipeline,
        "metadata": {"created_at": datetime.now(timezone.utc).isoformat(), "dataset": dataset_name, "dataset_sha256": input_hash(arguments.input), "metrics": metrics, "label_definition": {"0": "real/credible", "1": "fake/misleading"}},
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, arguments.output)
    arguments.output.with_suffix(".json").write_text(json.dumps(artifact["metadata"], indent=2, default=str), encoding="utf-8")
    print(json.dumps(metrics, indent=2, default=str))
    print(f"Saved model artifact to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
