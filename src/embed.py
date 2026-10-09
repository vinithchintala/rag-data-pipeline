"""Embedding generation with sentence-transformers.

Uses the all-MiniLM-L6-v2 model: it runs fully locally on CPU, needs no
API keys, and produces 384-dimensional vectors — a good quality/speed
tradeoff for a retrieval corpus of this size. The model is loaded lazily
so importing this module is cheap.
"""

import numpy as np


class EmbeddingModel:
    """Thin wrapper around SentenceTransformer with batched encoding."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    @property
    def dimension(self) -> int:
        """Embedding vector size (384 for all-MiniLM-L6-v2)."""
        return self.model.get_sentence_embedding_dimension()

    def embed(
        self,
        texts: list[str],
        batch_size: int = 32,
        show_progress: bool = True,
    ) -> np.ndarray:
        """Encode *texts* into a (n, dimension) float32 array."""
        if not texts:
            return np.zeros((0, self.dimension), dtype=np.float32)
        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype=np.float32)
