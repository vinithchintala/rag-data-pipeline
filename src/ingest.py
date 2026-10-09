"""Document ingestion.

Loads markdown / text files from a directory and extracts structured
documents with metadata (source filename, title, section). Markdown files
are split on H2 headings so each section keeps its own metadata — this
makes retrieval much more precise than one blob per file.
"""

import re
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt"}

# Matches markdown headings like "# Title" or "## Section"
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*?)\s*$")


@dataclass
class Document:
    """A single logical unit of source text with its metadata."""

    text: str       # raw text content
    source: str     # filename, e.g. "pricing.md"
    title: str      # document title (first H1, or filename stem)
    section: str    # section heading ("" when the doc has no sections)


def _parse_markdown(path: Path) -> list[Document]:
    """Split a markdown file into one Document per H2 section."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    title = path.stem.replace("-", " ").replace("_", " ").title()
    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:  # first H1 wins
            title = m.group(2).strip()
            break

    documents: list[Document] = []
    current_section = ""
    buffer: list[str] = []

    def flush() -> None:
        text = "\n".join(buffer).strip()
        if text:
            documents.append(
                Document(
                    text=text,
                    source=path.name,
                    title=title,
                    section=current_section,
                )
            )

    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:  # H2 starts a new section
            flush()
            current_section = m.group(2).strip()
            buffer = []
        elif m and len(m.group(1)) == 1:
            continue  # H1 title line: captured as metadata, not chunk text
        else:
            buffer.append(line)
    flush()

    # Fallback: file had no usable content split (e.g. no H2s) but is non-empty
    if not documents and raw.strip():
        documents.append(
            Document(text=raw.strip(), source=path.name, title=title, section="")
        )
    return documents


def _parse_text(path: Path) -> list[Document]:
    """Plain text files become a single Document."""
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    title = path.stem.replace("-", " ").replace("_", " ").title()
    return [Document(text=raw, source=path.name, title=title, section="")]


def load_documents(docs_dir: str | Path) -> list[Document]:
    """Load every supported file in *docs_dir* into Documents.

    Files are processed in sorted order for deterministic output.
    """
    docs_dir = Path(docs_dir)
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    documents: list[Document] = []
    for path in sorted(docs_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if path.suffix.lower() in {".md", ".markdown"}:
            documents.extend(_parse_markdown(path))
        else:
            documents.extend(_parse_text(path))
    return documents
