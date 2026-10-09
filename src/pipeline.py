"""End-to-end RAG ingestion pipeline.

Wires the stages together: ingest -> chunk -> embed -> load (Qdrant).

Usage:
    python src/pipeline.py [--docs-dir data/sample_docs] [--recreate]

The pipeline is idempotent: re-running it upserts over the same point IDs,
so the collection always reflects the current corpus without duplicates.
Pass --recreate to drop and rebuild the collection from scratch.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

# Allow `python src/pipeline.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config
from src.chunk import chunk_documents
from src.embed import EmbeddingModel
from src.ingest import load_documents
from src.load import ensure_collection, get_client, upsert_chunks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pipeline")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ingest docs, chunk, embed, load to Qdrant.")
    p.add_argument("--docs-dir", default=str(config.DOCS_DIR), help="Corpus directory")
    p.add_argument("--collection", default=config.COLLECTION_NAME, help="Qdrant collection")
    p.add_argument("--chunk-size", type=int, default=config.CHUNK_SIZE_WORDS)
    p.add_argument("--chunk-overlap", type=int, default=config.CHUNK_OVERLAP_WORDS)
    p.add_argument("--batch-size", type=int, default=config.EMBED_BATCH_SIZE)
    p.add_argument("--model", default=config.EMBEDDING_MODEL, help="Sentence-transformers model")
    p.add_argument("--qdrant-host", default=config.QDRANT_HOST)
    p.add_argument("--qdrant-port", type=int, default=config.QDRANT_PORT)
    p.add_argument("--recreate", action="store_true", help="Drop and rebuild the collection")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    started = time.time()

    # 1. Ingest -----------------------------------------------------------
    documents = load_documents(args.docs_dir)
    log.info("Ingested %d document sections from %s", len(documents), args.docs_dir)
    if not documents:
        log.warning("No documents found — nothing to do.")
        return

    # 2. Chunk ------------------------------------------------------------
    chunks = chunk_documents(
        documents, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    )
    log.info(
        "Created %d chunks (size=%d words, overlap=%d words)",
        len(chunks),
        args.chunk_size,
        args.chunk_overlap,
    )

    # 3. Embed ------------------------------------------------------------
    model = EmbeddingModel(args.model)
    log.info("Loading embedding model '%s' ...", args.model)
    embeddings = model.embed(
        [c.text for c in chunks], batch_size=args.batch_size, show_progress=True
    )
    log.info("Embedded %d chunks into %d-dim vectors", len(embeddings), model.dimension)

    # 4. Load -------------------------------------------------------------
    client = get_client(host=args.qdrant_host, port=args.qdrant_port)
    ensure_collection(
        client,
        collection_name=args.collection,
        vector_size=model.dimension,
        recreate=args.recreate,
    )
    log.info("Collection '%s' ready (recreate=%s)", args.collection, args.recreate)
    written = upsert_chunks(client, args.collection, chunks, embeddings)
    log.info("Upserted %d points to '%s'", written, args.collection)

    elapsed = time.time() - started
    log.info("Pipeline complete in %.1fs", elapsed)


if __name__ == "__main__":
    main()
