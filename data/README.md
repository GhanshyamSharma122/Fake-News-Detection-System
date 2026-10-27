# Dataset contract

The application deliberately does not ship with fabricated news examples. Before training, place a legally obtained, labelled dataset in `data/raw/news.csv` with these columns:

```csv
text,label
"The article text...",true
"Another article...",false
```

Accepted labels are `true`, `false`, `real`, `fake`, `1`, and `0` (case-insensitive). Use a genuine benchmark or institution-approved dataset, record its source and licence in your report, and do not upload private student data.

Recommended options for the project report are LIAR, FakeNewsNet, or a verified institutional dataset. Download and review the licence and class definitions yourself before use. The training script refuses tiny datasets and reports class balance so a toy dataset cannot be mistaken for a valid experiment.
