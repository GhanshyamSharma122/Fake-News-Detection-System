# NewsLens: Explainable Fake News Detection System

## Alternate Assessment Test (AAT) Report

**Institution:** BMS College of Engineering, Bengaluru  
**Department:** Computer Science and Engineering  
**Course:** Natural Language Processing  
**Academic year:** 2026  
**Team members:** *Add names, USNs, section, and guide name here*  

---

## Abstract

The rapid spread of misleading online news creates a need for tools that help readers identify content requiring verification. NewsLens is an explainable Natural Language Processing application that classifies the language of news headlines and articles using supervised machine learning. The system uses the ISOT Fake and Real News Dataset, spaCy-based tokenization, TF-IDF feature extraction, and Logistic Regression classification. It maintains separate models for short headlines and longer article text because these inputs have different linguistic characteristics.

The application exposes a Flask API and a responsive web interface. A user submits a headline or article, receives a cautious risk score, and can inspect supporting language signals. The system is designed as a verification aid rather than an autonomous fact-checker. It includes input validation, model metadata, evaluation metrics, ethical safeguards, and a human-in-the-loop workflow. On the current random stratified holdout, the article model achieved 99.31% accuracy and 99.34% F1-score, while the headline model achieved 96.16% accuracy and 96.29% F1-score. These results are reported with limitations because publisher and topic artefacts may make a random split optimistic.

**Keywords:** Natural Language Processing, fake news detection, text classification, tokenization, TF-IDF, Logistic Regression, explainable AI, misinformation, precision, recall, F1-score.

---

## 1. Introduction

News is increasingly consumed through social media, messaging platforms, and short online headlines. Misleading content can use emotional language, unsupported claims, imitation of legitimate reporting, or selective presentation of facts. Manually checking every claim is difficult, so NLP can assist by identifying language patterns associated with previously labelled examples.

NewsLens addresses this problem by converting text into numerical features and applying a trained binary classifier. The result is not presented as a definitive truth judgement. Instead, the system tells the reader that a text has lower-risk or higher-risk language patterns and encourages verification through reliable sources.

### 1.1 Problem statement

Design and implement an explainable NLP-based application that analyses a news headline or article and identifies whether its language resembles credible or misleading examples in a labelled dataset, while clearly communicating uncertainty and ethical limitations.

### 1.2 Motivation

The problem is suitable for an NLP AAT because it combines language preprocessing, feature engineering, supervised classification, model evaluation, explainability, web deployment, and responsible AI considerations in one practical scenario.

---

## 2. Objectives

1. Study how NLP can be applied to misinformation screening.
2. Use a genuine labelled news dataset rather than hand-written examples.
3. Build a reproducible training pipeline with a held-out evaluation set.
4. Implement separate handling for short headlines and longer article text.
5. Provide a web interface and API for end-to-end analysis.
6. Display understandable signals instead of an unexplained prediction.
7. Measure accuracy, precision, recall, and F1-score.
8. Discuss privacy, bias, false positives, false negatives, and human responsibility.

---

## 3. Scope of the project

### Included

- English news headline and article classification.
- Binary labels: real/credible and fake/misleading.
- spaCy tokenization with a deterministic fallback tokenizer.
- Word-level TF-IDF feature extraction.
- Logistic Regression classification.
- Separate headline and article model pipelines.
- Flask API and responsive HTML interface.
- Model metadata, dataset hash, metrics, and health endpoint.
- Ethical explanation and human verification guidance.

### Not included

- Automatic web fact-checking or live source verification.
- Detection of all types of satire, opinion, propaganda, or manipulated media.
- Multilingual classification.
- Social-network graph modelling.
- Autonomous content removal or user punishment.

---

## 4. Dataset and data preparation

### 4.1 Dataset selected

The project uses the ISOT Fake and Real News Dataset downloaded from Kaggle:

[https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download)

The dataset contains two files:

- `Fake.csv` — articles labelled fake.
- `True.csv` — articles labelled true.

The files contain title, article text, subject, and date fields. The project trainer combines title and body text for the article model and uses title text for the headline model. Labels are assigned from the source file names.

### 4.2 Dataset statistics

| Measure | Value |
|---|---:|
| Total usable articles | 44,898 |
| Real/credible articles | 21,417 |
| Fake/misleading articles | 23,481 |
| Training rows | 35,918 |
| Held-out test rows | 8,980 |
| Split method | Stratified random split, test size 20% |
| Random seed | 42 |

### 4.3 Data responsibility

The dataset source, licence, label definition, and known limitations must be recorded in the final submission. Dataset labels should not be interpreted as universal truth. They represent the labelling policy and source collection process used to build that dataset.

---

## 5. Core NLP concepts

### 5.1 Tokenization

Tokenization divides a text into smaller units such as words and punctuation. NewsLens uses spaCy’s English tokenizer when available. A deterministic regular-expression fallback is included so that the application can still operate in a restricted environment.

### 5.2 TF-IDF

Term Frequency-Inverse Document Frequency converts text into numerical vectors. A word receives a higher value when it appears frequently in one document but is not common throughout the complete dataset. This helps the classifier focus on informative vocabulary rather than only common words.

### 5.3 Supervised classification

The model learns from examples that already have labels. During training, it learns relationships between TF-IDF features and the two target classes. During inference, it estimates the probability that new text belongs to the fake/misleading class.

### 5.4 Logistic Regression

Logistic Regression is an interpretable and efficient binary classifier. It assigns a weight to each feature and converts the weighted result into a probability. The project uses class balancing so that differences in class frequency have less influence on learning.

### 5.5 Headline and article models

Headlines are short and often omit context, while full articles contain longer vocabulary and writing patterns. NewsLens trains two pipelines:

- Inputs of up to 60 words use the headline model.
- Longer inputs use the article model.

This routing is a practical improvement over applying an article model blindly to a short headline.

---

## 6. High-Level Design (HLD)

```text
                 ┌──────────────────────┐
                 │  User enters text    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Web interface       │
                 │  HTML/CSS/JavaScript │
                 └──────────┬───────────┘
                            │ POST /api/analyze
                            ▼
                 ┌──────────────────────┐
                 │  Flask API           │
                 │  Validate input      │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       Short input                    Long input
       Headline model                 Article model
              │                           │
              └─────────────┬─────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Score and explanation│
                 └──────────┬───────────┘
                            ▼
                 Human verifies sources
```

### 6.1 Major components

| Component | Responsibility |
|---|---|
| `index.html` | User-facing detector and project explanation |
| `app.js` | Sends analysis requests and renders results |
| `styles.css` | Responsive visual design |
| `server.py` | Flask API, validation, model loading, and inference |
| `nlp_utils.py` | Shared tokenization and token counting |
| `training/train_model.py` | Dataset loading, training, and evaluation |
| `models/newslens.joblib` | Saved article and headline model artifact |
| `data/Fake.csv` and `data/True.csv` | Training dataset |
| `developer-guide.html` | Setup, HLD, LLD, and developer documentation |

---

## 7. Low-Level Design (LLD)

### 7.1 Training flow

1. Read `Fake.csv` and `True.csv`.
2. Combine the title and body for article text.
3. Extract title text separately for the headline model.
4. Assign `fake` or `true` labels from the file name.
5. Validate that at least 1,000 rows and two classes are available.
6. Create a stratified 80/20 train-test split.
7. Tokenize text.
8. Fit bounded word-level TF-IDF features.
9. Train balanced Logistic Regression models.
10. Calculate metrics on unseen test rows.
11. Save both pipelines and metadata using Joblib.

### 7.2 Inference flow

1. Receive JSON at `POST /api/analyze`.
2. Check that the text is a non-empty string.
3. Reject text longer than 10,000 characters.
4. Select the headline model for text up to 60 words; otherwise select the article model.
5. Convert the text using the saved TF-IDF vocabulary.
6. Calculate the misleading-class probability.
7. Map the score to `Lower-risk language`, `Needs verification`, or `High-risk language`.
8. Return the score, model type, metrics, and language signals.

### 7.3 API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serves the web application |
| `GET` | `/api/health` | Reports model readiness and metadata |
| `POST` | `/api/analyze` | Analyses submitted text |

Example request:

```json
{
  "text": "SHOCKING secret cure doctors do not want you to know!!!"
}
```

Example response fields:

```json
{
  "score": 88,
  "label": "High-risk language",
  "input_mode": "headline",
  "model": "Headline TF-IDF + Logistic Regression"
}
```

---

## 8. Implementation and execution

### 8.1 Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 8.2 Training

```powershell
python training/train_model.py --input data
```

### 8.3 Starting the application

```powershell
python server.py
```

Open `http://127.0.0.1:5000` in a browser. Enter a headline or article, select **Analyse text**, and review the score and supporting signals.

### 8.4 Docker option

```powershell
docker build -t newslens .
docker run --rm -p 5000:5000 -v ${PWD}/models:/app/models newslens
```

---

## 9. Results and evaluation

### 9.1 Article model

| Metric | Result |
|---|---:|
| Accuracy | 99.31% |
| Precision | 99.57% |
| Recall | 99.11% |
| F1-score | 99.34% |

### 9.2 Headline model

| Metric | Result |
|---|---:|
| Accuracy | 96.16% |
| Precision | 97.32% |
| Recall | 95.27% |
| F1-score | 96.29% |

### 9.3 Smoke testing

Verified smoke-test headlines are stored in `data/test_cases.csv`. The file contains examples from the labelled dataset and the observed score from the current artifact. It is intended for demonstration, not as a replacement for formal evaluation.

### 9.4 Interpretation of results

The high random-split scores should not be presented as proof that the system can detect all real-world misinformation. The dataset may contain publisher, topic, date, and writing-style signals that are easier to learn than factual correctness. A stronger evaluation would use publisher-separated, time-separated, and out-of-domain test sets.

---

## 10. Ethics, integrity, and responsible use

1. **No certainty claim:** The system reports language risk, not truth.
2. **Human verification:** Users should inspect the source, author, date, evidence, and independent reporting.
3. **Bias awareness:** Political and publisher imbalance can produce unfair outcomes.
4. **Privacy:** Submitted text is not intentionally persisted by the application.
5. **No censorship:** The output must not be used alone to remove content or punish users.
6. **Transparent reporting:** Dataset provenance, labels, metrics, and limitations are disclosed.
7. **Error awareness:** False positives can harm credible journalism; false negatives can allow harmful claims to spread.

---

## 11. Limitations

- The system is English-language and dataset-dependent.
- A headline often lacks the context needed for fact checking.
- The ISOT dataset may not represent current news, Indian news, or all political viewpoints.
- Random train-test splitting may produce optimistic results when related articles share style or topics.
- A model can learn source or vocabulary shortcuts rather than factual evidence.
- The application does not retrieve citations or verify claims against external knowledge.
- The current explanation signals are helpful indicators, not causal explanations of the classifier.

---

## 12. Future enhancements

- Add publisher-separated and time-based evaluation.
- Add source metadata and evidence retrieval with citations.
- Compare Logistic Regression with a calibrated linear SVM or a transformer model.
- Add multilingual support for Indian languages.
- Add an annotation review interface for human fact-checkers.
- Add authentication, HTTPS, rate limiting, monitoring, and model rollback.
- Add a confusion-matrix dashboard and error analysis by topic and publisher.

---

## 13. AAT rubric mapping

| Criterion | Evidence in NewsLens |
|---|---|
| Selection of scenario — 8 marks | Real-world misinformation screening with preprocessing, feature extraction, classification, explanation, and source verification |
| Integrity and ethical behaviour — 8 marks | Genuine dataset, provenance, privacy, uncertainty, bias discussion, and human-in-the-loop design |
| Application development — 8 marks | Working training pipeline, two model routes, Flask API, web interface, validation, and saved artifact |
| Report — 8 marks | This report, developer guide, HLD, LLD, dataset details, metrics, and limitations |
| Oral communication — 4 marks | Demonstrable flow from dataset to model to API to result |
| Participation in discussions — 4 marks | Discussion points include leakage, class imbalance, generalisation, false positives, and ethics |

---

## 14. Conclusion

NewsLens demonstrates how NLP can support the early screening of potentially misleading news language. The project uses a genuine dataset, reproducible preprocessing, supervised classification, separate headline and article models, an API, a web interface, and explainable output. Its most important design decision is to avoid presenting a classifier as an autonomous fact-checker. The system is best used to prioritise content for careful human verification.

---

## References

1. ISOT Fake and Real News Dataset, Kaggle: [https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download)
2. Wang, William Yang. “Liar, Liar Pants on Fire: A New Benchmark Dataset for Fake News Detection.” ACL 2017: [https://aclanthology.org/P17-2067/](https://aclanthology.org/P17-2067/)
3. FakeNewsNet research repository: [https://github.com/KaiDMML/FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet)
