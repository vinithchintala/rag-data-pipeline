"""Retrieval evaluation: hit-rate@k over a labeled question set.

Each eval item pairs a question with the document expected to answer it
(eval/questions.json). A question scores a "hit" at k if the expected
source appears anywhere in the top-k retrieved chunks.

Usage:
    python src/evaluate.py [--eval-path eval/questions.json]
"""

import argparse
import json
import sys
from pathlib import Path

# Allow `python src/evaluate.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config
from src.embed import EmbeddingModel
from src.load import get_client
from src.retrieve import search

K_VALUES = (1, 3, 5)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate retrieval hit-rate@k.")
    p.add_argument("--eval-path", default=str(config.EVAL_PATH))
    p.add_argument("--collection", default=config.COLLECTION_NAME)
    p.add_argument("--model", default=config.EMBEDDING_MODEL)
    p.add_argument("--qdrant-host", default=config.QDRANT_HOST)
    p.add_argument("--qdrant-port", type=int, default=config.QDRANT_PORT)
    return p.parse_args()


def load_eval_items(eval_path: str | Path) -> list[dict]:
    with open(eval_path, encoding="utf-8") as f:
        items = json.load(f)
    for item in items:
        if "question" not in item or "expected_source" not in item:
            raise ValueError(f"Eval item missing keys: {item}")
    return items


def main() -> None:
    args = parse_args()
    items = load_eval_items(args.eval_path)
    print(f"Evaluating {len(items)} questions against '{args.collection}'...\n")

    model = EmbeddingModel(args.model)
    client = get_client(host=args.qdrant_host, port=args.qdrant_port)

    hits = {k: 0 for k in K_VALUES}
    rows: list[tuple[str, str, str, dict[int, str]]] = []

    for item in items:
        question = item["question"]
        expected = item["expected_source"]
        query_vector = model.embed([question], show_progress=False)[0]
        points = search(client, args.collection, query_vector, max(K_VALUES))
        ranked_sources = [(p.payload or {}).get("source", "?") for p in points]

        marks = {}
        for k in K_VALUES:
            hit = expected in ranked_sources[:k]
            hits[k] += int(hit)
            marks[k] = "HIT " if hit else "miss"
        rows.append((question, expected, ranked_sources[0] if ranked_sources else "?", marks))

    # Per-question table
    header = f"{'Question':<58} {'Expected':<24} {'Top-1':<24} {'@1':<5} {'@3':<5} {'@5':<5}"
    print(header)
    print("-" * len(header))
    for question, expected, top1, marks in rows:
        q = question if len(question) <= 56 else question[:53] + "..."
        print(
            f"{q:<58} {expected:<24} {top1:<24} "
            f"{marks[1]:<5} {marks[3]:<5} {marks[5]:<5}"
        )

    # Aggregate
    n = len(items)
    print("\n" + "=" * len(header))
    print("Summary (hit-rate@k):")
    for k in K_VALUES:
        print(f"  hit@{k}: {hits[k]}/{n} = {hits[k] / n:.1%}")


if __name__ == "__main__":
    main()
