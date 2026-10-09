"""Semantic retrieval over the indexed corpus.

Embeds a natural-language question and returns the top-k most similar
chunks from Qdrant, with scores and source metadata.

Usage:
    python src/retrieve.py --query "How much does the Growth plan cost?"
    python src/retrieve.py --query "..." --top-k 3
"""

import argparse
import sys
import textwrap
from pathlib import Path

# Allow `python src/retrieve.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config
from src.embed import EmbeddingModel
from src.load import get_client


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search the indexed docs.")
    p.add_argument("--query", required=True, help="Natural-language question")
    p.add_argument("--top-k", type=int, default=config.DEFAULT_TOP_K)
    p.add_argument("--collection", default=config.COLLECTION_NAME)
    p.add_argument("--model", default=config.EMBEDDING_MODEL)
    p.add_argument("--qdrant-host", default=config.QDRANT_HOST)
    p.add_argument("--qdrant-port", type=int, default=config.QDRANT_PORT)
    return p.parse_args()


def search(client, collection: str, query_vector, top_k: int):
    """Return the top-k scored points for *query_vector*."""
    response = client.query_points(
        collection_name=collection,
        query=query_vector.tolist(),
        limit=top_k,
        with_payload=True,
    )
    return response.points


def format_result(rank: int, point, snippet_chars: int = 280) -> str:
    payload = point.payload or {}
    source = payload.get("source", "?")
    title = payload.get("title", "")
    section = payload.get("section", "")
    location = f"{title}" + (f" / {section}" if section else "")
    snippet = textwrap.shorten(
        payload.get("text", ""), width=snippet_chars, placeholder=" ..."
    )
    return (
        f"[{rank}] score={point.score:.4f} | {source} — {location}\n"
        f"    {snippet}"
    )


def main() -> None:
    args = parse_args()

    model = EmbeddingModel(args.model)
    query_vector = model.embed([args.query], show_progress=False)[0]

    client = get_client(host=args.qdrant_host, port=args.qdrant_port)
    points = search(client, args.collection, query_vector, args.top_k)

    print(f"\nQuery: {args.query}\n")
    print(f"Top {len(points)} results from collection '{args.collection}':\n")
    for rank, point in enumerate(points, start=1):
        print(format_result(rank, point))
        print()


if __name__ == "__main__":
    main()
