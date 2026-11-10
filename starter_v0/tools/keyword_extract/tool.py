from __future__ import annotations

import re
from collections import Counter
from typing import Any

from tools._shared import err


_STOPWORDS = {
    "about", "after", "again", "also", "and", "are", "because", "been", "before",
    "being", "but", "can", "could", "did", "does", "for", "from", "had", "has",
    "have", "her", "here", "him", "his", "how", "into", "its", "just", "more",
    "most", "not", "our", "out", "over", "she", "some", "such", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "this", "those",
    "through", "under", "was", "were", "what", "when", "where", "which", "who",
    "why", "will", "with", "would", "you", "your",
}


def extract_keywords(text: str = "", max_keywords: int = 5) -> dict[str, Any]:
    try:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if isinstance(max_keywords, bool) or not isinstance(max_keywords, int):
            raise TypeError("max_keywords must be an integer")
        if max_keywords < 1:
            raise ValueError("max_keywords must be at least 1")

        tokens = [
            token for token in re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)
            if len(token) > 2 and token not in _STOPWORDS
        ]
        ranked = sorted(Counter(tokens).items(), key=lambda item: (-item[1], item[0]))[:max_keywords]
        return {
            "tool": "extract_keywords",
            "text": text,
            "keywords": [{"term": term, "count": count} for term, count in ranked],
            "top_keywords": [term for term, _ in ranked],
        }
    except Exception as exc:
        return err("extract_keywords", exc)
