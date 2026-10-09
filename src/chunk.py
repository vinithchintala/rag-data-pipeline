"""Text cleaning and overlapping chunking.

Chunking strategy: word-based sliding window with configurable size and
overlap. Word boundaries are used (instead of raw characters) so chunks
never split mid-word, and the overlap preserves context that would
otherwise be lost at chunk edges — important for retrieval quality.
"""

import re
from dataclasses import dataclass

from .ingest import Document

_WHITESPACE_RE = re.compile(r"[ \t]+")


@dataclass
class Chunk:
    """A retrievable unit of text carrying its source metadata."""

    text: str        # chunk text
    source: str      # originating filename, e.g. "pricing.md"
    title: str       # document title
    section: str     # section heading within the document
    chunk_index: int  # position of this chunk within its document (0-based)
    word_start: int  # inclusive start offset in words
    word_end: int    # exclusive end offset in words


def clean_text(text: str) -> str:
    """Normalize whitespace: collapse runs of spaces/tabs and blank lines."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WHITESPACE_RE.sub(" ", text)
    # Collapse 3+ consecutive newlines to a paragraph break
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[tuple[str, int, int]]:
    """Split *text* into overlapping windows.

    Returns a list of (chunk_text, word_start, word_end) tuples.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap must satisfy 0 <= overlap < chunk_size")

    words = text.split()
    if not words:
        return []

    windows: list[tuple[str, int, int]] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        windows.append((" ".join(words[start:end]), start, end))
        if end == len(words):
            break
        start = end - chunk_overlap
    return windows


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Chunk]:
    """Clean and chunk every document, preserving metadata on each chunk."""
    chunks: list[Chunk] = []
    for doc in documents:
        cleaned = clean_text(doc.text)
        for i, (text, word_start, word_end) in enumerate(
            chunk_text(cleaned, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        ):
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    title=doc.title,
                    section=doc.section,
                    chunk_index=i,
                    word_start=word_start,
                    word_end=word_end,
                )
            )
    return chunks
