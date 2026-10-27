# NewsLens — Fake News Detection System

NewsLens is an explainable, supervised NLP application for screening news language. It is designed as a serious college project: the web interface is backed by a versioned model artifact, a reproducible training script, evaluation metrics, input validation, and a deployment container. It does **not** claim to prove whether a story is true. Truth requires source verification and human judgement.

## Important data decision

The repository does not include a fabricated 20-row dataset. Put a real, legally obtained and labelled CSV in `data/raw/news.csv`, following the schema in `data/README.md`. Suitable choices include LIAR, FakeNewsNet, or an institution-approved dataset. Record the dataset source, licence, label definition, collection date, and known limitations in the final report.

The training script refuses fewer than 1,000 rows. This prevents a toy dataset from being presented as a production model.

## Run locally

On Windows, double-click `run.bat`. It creates the virtual environment, installs dependencies, trains the model if necessary, and starts the application.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Place the reviewed dataset at `data/raw/news.csv`, or use the included ISOT files in `data`, then train and evaluate:

```powershell
python training/train_model.py --input data
python server.py
```

Open `http://127.0.0.1:5000`. The health endpoint at `/api/health` reports model metadata, dataset hash, class balance, and held-out test metrics. The frontend calls `/api/analyze` and displays a probability-derived screening score plus understandable language signals. If the model is missing, the interface reports that it is unavailable; it never invents a prediction.

For deployment:

```powershell
docker build -t newslens .
docker run --rm -p 5000:5000 -v ${PWD}/models:/app/models newslens
```

The container expects a trained artifact at `models/newslens.joblib`. Never deploy without training and reviewing the artifact first.

## High-level design

```text
Reviewed dataset → validation → stratified train/test split
                                  ↓
          spaCy tokenization → bounded word TF-IDF
                                  ↓
                  balanced Logistic Regression model
                                  ↓
             versioned model artifact + evaluation report
                                  ↓
      Flask API → input validation → score + explanation
                                  ↓
                 human source verification before sharing
```

## NLP and machine-learning mechanisms

1. **Data validation:** required columns, non-empty text, two recognised classes, class balance, and minimum dataset size are checked.
2. **Preprocessing:** spaCy tokenizes English text. The pipeline preserves text semantics while keeping processing lightweight.
3. **Feature extraction:** bounded word-level TF-IDF captures informative unigrams while keeping memory and training time suitable for a college deployment.
4. **Classification:** balanced Logistic Regression estimates the probability of the misleading class. Class weighting reduces the effect of imbalance.
5. **Evaluation:** a stratified held-out split reports accuracy, precision, recall, F1-score, class distribution, and a full classification report.
6. **Inference:** the API validates JSON and length, loads a fixed artifact, and returns a score, label, model name, and signal explanation.
7. **Explainability:** additional signals identify sensational vocabulary, excessive emphasis, evidence vocabulary, and text statistics. These signals support review; they do not override the trained model.
8. **Operational safety:** the server does not train on startup, does not persist submitted articles, returns useful `400`, `413`, and `503` errors, and exposes readiness through `/api/health`.

## Why scikit-learn instead of TensorFlow and PyTorch?

The goal is a reliable, explainable system suitable for a college deployment. TF-IDF plus Logistic Regression is fast, auditable, inexpensive to host, and a strong baseline for text classification. TensorFlow or PyTorch would be justified only after a sufficiently large, high-quality dataset and a comparison experiment. Using all libraries merely to satisfy a checklist would make the system harder to operate without improving its evidence quality.

## Ethics and limitations

- A linguistic classifier detects patterns, not truth. A credible article can be flagged and a polished false claim can pass.
- Dataset source, annotation quality, political coverage, language, and publisher distribution can create bias.
- Do not use the output to censor, punish, deny services, or label people.
- Always show uncertainty and require a human to inspect the original source, author, date, evidence, and independent reporting.
- The current feature explanation is a transparency aid, not a formal causal explanation of the model.
- Before public deployment, add authentication, HTTPS, rate limiting, structured logging without article text, monitoring, model rollback, and an approved data-retention policy.

## AAT mapping

| Rubric | Project evidence |
|---|---|
| Scenario selection | Socially relevant misinformation-screening problem with a complete NLP pipeline |
| Integrity and ethics | No fabricated training claim, dataset provenance requirement, privacy, bias, uncertainty, and human review |
| Application | Working Flask API, trained artifact, frontend, validation, evaluation, and Docker deployment |
| Report | This document, data contract, architecture, mechanisms, metrics, and limitations |
| Presentation | Demonstrate training, `/api/health`, credible/misleading examples, confusion metrics, and error cases |
| Discussion | Explain data leakage, class imbalance, false positives, false negatives, and why the model is not a fact-checker |
