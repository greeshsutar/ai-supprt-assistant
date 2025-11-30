# retriever.py
from pathlib import Path
import re


class FAQRetriever:
    def __init__(self, path: str = "data/faqs.txt"):
        # Load FAQ file
        text = Path(path).read_text(encoding="utf-8")

        # Split FAQs into blocks separated by blank lines
        self.chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

    def _tokens(self, s: str):
        # Simple tokenization to words
        return set(re.findall(r"\w+", s.lower()))

    def get_relevant(self, query: str, k: int = 3):
        q_tokens = self._tokens(query)

        scored = []
        for chunk in self.chunks:
            c_tokens = self._tokens(chunk)
            score = len(q_tokens & c_tokens)  # number of overlapping words
            scored.append((score, chunk))

        # sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        # take top k with score > 0
        top = [c for score, c in scored if score > 0][:k]

        # if nothing matches, just return one chunk so LLM has something
        if not top and self.chunks:
            top = [self.chunks[0]]

        return top
