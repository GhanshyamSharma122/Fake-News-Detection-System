"""Shared, serializable NLP preprocessing used by training and inference."""

import spacy

NLP = spacy.blank("en")


def tokenize_text(text: str) -> list[str]:
    return [token.text for token in NLP(text.lower()) if not token.is_space and not token.is_punct]


def count_tokens(text: str) -> int:
    return sum(1 for token in NLP(text) if not token.is_space and not token.is_punct)
