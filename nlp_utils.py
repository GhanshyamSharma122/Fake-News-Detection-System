"""Shared, serializable NLP preprocessing used by training and inference."""

import re

try:
    import spacy
except ImportError:
    spacy = None

NLP = spacy.blank("en") if spacy else None


def tokenize_text(text: str) -> list[str]:
    if NLP is None:
        return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())
    return [token.text for token in NLP(text.lower()) if not token.is_space and not token.is_punct]


def count_tokens(text: str) -> int:
    return len(tokenize_text(text))
