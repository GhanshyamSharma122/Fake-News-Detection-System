"""Production entry point for the NewsLens inference service."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import joblib
from flask import Flask, jsonify, request, send_from_directory
from nlp_utils import count_tokens

ROOT = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("NEWSLENS_MODEL", ROOT / "models" / "newslens.joblib"))
MAX_TEXT_LENGTH = 10_000
app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
MODEL: dict[str, Any] | None = None


def load_model() -> dict[str, Any]:
    global MODEL
    if MODEL is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Model artifact not found at {MODEL_PATH}. Train one with training/train_model.py first.")
        MODEL = joblib.load(MODEL_PATH)
        if not isinstance(MODEL, dict) or "pipeline" not in MODEL or "metadata" not in MODEL:
            raise RuntimeError("Model artifact is invalid or incomplete.")
    return MODEL


def language_signals(text: str) -> list[dict[str, str]]:
    lower = text.lower()
    risk_terms = ["shocking", "secret", "miracle", "unbelievable", "guarantees", "share this", "urgent", "hidden"]
    evidence_terms = ["study", "research", "report", "data", "method", "published", "limitations", "official"]
    signals: list[dict[str, str]] = []
    found_risk = [term for term in risk_terms if term in lower]
    found_evidence = [term for term in evidence_terms if term in lower]
    if found_risk:
        signals.append({"type": "risk", "title": "Sensational vocabulary", "detail": ", ".join(found_risk[:4])})
    if text.count("!"):
        signals.append({"type": "risk", "title": "Emphasis pattern", "detail": f"{text.count('!')} exclamation mark(s)"})
    if found_evidence:
        signals.append({"type": "good", "title": "Evidence language", "detail": ", ".join(found_evidence[:4])})
    token_count = count_tokens(text)
    signals.append({"type": "neutral", "title": "Text statistics", "detail": f"{token_count} tokens · {len(re.findall(r'[.!?]+', text)) or 1} sentence(s)"})
    return signals


@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/health")
def health():
    try:
        artifact = load_model()
        return jsonify({"status": "ok", "model": "TF-IDF word+character features with Logistic Regression", "metadata": artifact["metadata"]})
    except RuntimeError as error:
        return jsonify({"status": "not_ready", "error": str(error)}), 503


@app.post("/api/analyze")
def analyze():
    body = request.get_json(silent=True) or {}
    text = body.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Please provide non-empty text."}), 400
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({"error": f"Text must be {MAX_TEXT_LENGTH} characters or fewer."}), 413
    try:
        artifact = load_model()
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503
    probability = float(artifact["pipeline"].predict_proba([text])[0][1])
    score = round(probability * 100)
    label = "High-risk language" if score >= 65 else "Needs verification" if score >= 38 else "Lower-risk language"
    description = (
        "The model found language patterns associated with misleading examples. Verify the original source before sharing."
        if score >= 65 else "The model found mixed or limited signals. Compare this claim with independent, reliable sources."
        if score >= 38 else "The model found fewer misleading-language patterns, but this does not prove the claim is true."
    )
    return jsonify({"score": score, "label": label, "description": description, "signals": language_signals(text), "model": "TF-IDF + Logistic Regression", "metrics": artifact["metadata"]["metrics"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
