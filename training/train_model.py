"""Train and evaluate the NewsLens text classifier.

Example:
    python training/train_model.py --input data/raw/news.csv
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from nlp_utils import tokenize_text

ROOT = Path(__file__).resolve().parents[1]
LABEL_MAP = {"true": 0, "real": 0, "0": 0, "false": 1, "fake": 1, "1": 1}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the NewsLens fake-news classifier.")
    parser.add_argument("--input", type=Path, required=True, help="CSV with text and label columns")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output", type=Path, default=ROOT / "models" / "newslens.joblib")
    parser.add_argument("--test-size", type=float, default=0.2)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    if not arguments.input.exists():
        print(f"Dataset not found: {arguments.input}", file=sys.stderr)
        return 1
    frame = pd.read_csv(arguments.input).dropna(subset=[arguments.text_column, arguments.label_column])
    if len(frame) < 1000:
        print("Refusing to train: provide at least 1,000 reviewed rows for a meaningful experiment.", file=sys.stderr)
        return 1
    labels = frame[arguments.label_column].astype(str).str.strip().str.lower().map(LABEL_MAP)
    if labels.isna().any() or labels.nunique() != 2:
        print("Labels must map to two classes: true/false, real/fake, or 0/1.", file=sys.stderr)
        return 1
    texts = frame[arguments.text_column].astype(str)
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels.astype(int), test_size=arguments.test_size, random_state=42, stratify=labels
    )
    features = FeatureUnion([
        ("word", TfidfVectorizer(tokenizer=tokenize_text, token_pattern=None, ngram_range=(1, 2), min_df=2, max_df=0.98, sublinear_tf=True)),
        ("character", TfidfVectorizer(analyzer="char", ngram_range=(3, 5), min_df=3, max_features=80_000, sublinear_tf=True)),
    ])
    pipeline = Pipeline([
        ("features", features),
        ("classifier", LogisticRegression(max_iter=2_000, class_weight="balanced", random_state=42)),
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
        "class_distribution": labels.value_counts().to_dict(),
    }
    artifact = {
        "pipeline": pipeline,
        "metadata": {"created_at": datetime.now(timezone.utc).isoformat(), "dataset_sha256": hashlib.sha256(arguments.input.read_bytes()).hexdigest(), "metrics": metrics, "label_definition": {"0": "real/credible", "1": "fake/misleading"}},
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, arguments.output)
    arguments.output.with_suffix(".json").write_text(json.dumps(artifact["metadata"], indent=2, default=str), encoding="utf-8")
    print(json.dumps(metrics, indent=2, default=str))
    print(f"Saved model artifact to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
