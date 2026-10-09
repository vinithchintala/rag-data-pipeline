"""Shared configuration for the RAG ingestion pipeline.

All tunables live here so the pipeline, retrieval, and eval scripts stay
consistent. Override via CLI flags where supported.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Qdrant ---------------------------------------------------------------
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "flowstack_docs"

# --- Embeddings -----------------------------------------------------------
# Local model: no API keys, runs on CPU. 384-dimensional output.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBED_BATCH_SIZE = 32

# --- Chunking -------------------------------------------------------------
# Word-based sliding window. 500 words ~= a few paragraphs; 100 words of
# overlap preserves context across chunk boundaries.
CHUNK_SIZE_WORDS = 500
CHUNK_OVERLAP_WORDS = 100

# --- Retrieval / eval -----------------------------------------------------
DEFAULT_TOP_K = 5
EVAL_MAX_K = 5

# --- Paths ----------------------------------------------------------------
DOCS_DIR = PROJECT_ROOT / "data" / "sample_docs"
EVAL_PATH = PROJECT_ROOT / "eval" / "questions.json"
