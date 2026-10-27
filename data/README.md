# Dataset contract

This folder contains the downloaded ISOT Fake News Dataset used by the project:

- `Fake.csv` — labelled fake-news articles
- `True.csv` — labelled real-news articles

The files were copied from the downloaded Kaggle archive and verified with SHA-256 before the original archive was removed. The dataset source is the [Kaggle Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download).

Train directly from this folder:

```powershell
python training/train_model.py --input data
```

The trainer combines each article title and body, assigns labels from the filenames, and saves the model under `models/newslens.joblib`.

For another dataset, place a legally obtained labelled CSV in `data/raw/news.csv` with these columns:

```csv
text,label
"The article text...",true
"Another article...",false
```

Accepted labels are `true`, `false`, `real`, `fake`, `1`, and `0` (case-insensitive). Use a genuine benchmark or institution-approved dataset, record its source and licence in your report, and do not upload private student data.

Record the source, licence, label definition, collection date, and known limitations in the report. Do not upload private student data. The training script refuses tiny datasets and reports class balance so a toy dataset cannot be mistaken for a valid experiment.
