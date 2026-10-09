"""Qdrant collection management and vector loading.

Idempotency is a first-class concern here, as in any production load:
- Collections are created only if they do not already exist
  (or are explicitly recreated with --recreate).
- Point IDs are deterministic (UUID5 of "source#chunk_index"), so
  re-running the pipeline upserts over the same points instead of
  duplicating them.
"""

import uuid

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .chunk import Chunk


def get_client(host: str = "localhost", port: int = 6333) -> QdrantClient:
    """Connect to Qdrant. Assumes `docker compose up` is running."""
    return QdrantClient(host=host, port=port)


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
    recreate: bool = False,
) -> None:
    """Create the collection if missing; optionally drop and recreate it."""
    if recreate and client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def make_point_id(source: str, chunk_index: int) -> str:
    """Deterministic point ID so re-runs overwrite instead of duplicating."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}#{chunk_index}"))


def _chunk_to_point(chunk: Chunk, vector: np.ndarray) -> PointStruct:
    return PointStruct(
        id=make_point_id(chunk.source, chunk.chunk_index),
        vector=vector.tolist(),
        payload={
            "source": chunk.source,
            "title": chunk.title,
            "section": chunk.section,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
        },
    )


def upsert_chunks(
    client: QdrantClient,
    collection_name: str,
    chunks: list[Chunk],
    embeddings: np.ndarray,
    batch_size: int = 100,
) -> int:
    """Upsert chunks + vectors in batches. Returns the number of points written."""
    if len(chunks) != len(embeddings):
        raise ValueError(
            f"chunks ({len(chunks)}) and embeddings ({len(embeddings)}) must align"
        )
    total = 0
    for start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[start : start + batch_size]
        batch_vectors = embeddings[start : start + batch_size]
        points = [
            _chunk_to_point(chunk, vector)
            for chunk, vector in zip(batch_chunks, batch_vectors)
        ]
        client.upsert(collection_name=collection_name, points=points, wait=True)
        total += len(points)
    return total
