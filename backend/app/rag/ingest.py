#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def chunk(txt: str, max_chars=700) -> List[str]:
    out, buf = [], ""
    for p in [p.strip() for p in txt.split("\n") if p.strip()]:
        if len(buf) + len(p) < max_chars:
            buf += (" " if buf else "") + p
        else:
            out.append(buf)
            buf = p
    if buf:
        out.append(buf)
    return out


DEFAULT_EXTS = {".txt", ".md", ".py", ".java", ".js", ".ts"}

def find_files(root: Path, extensions: List[str], recursive: bool) -> List[Path]:
    exts = {e if e.startswith(".") else f".{e}" for e in extensions}
    if recursive:
        return sorted([p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts])
    else:
        return sorted([p for p in root.glob("*") if p.is_file() and p.suffix.lower() in exts])

def load_text_file(p: Path) -> str:
    # Keep it simple: read as UTF-8 text; ignore errors
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def ingest(
    data_dir="data",
    store_dir="store",
    recursive=True,
    extensions=tuple(sorted(DEFAULT_EXTS)),
    max_chars=700,
    dry_run=False,
) -> Dict[str, int]:
    data_dir = Path(data_dir)
    store = Path(store_dir)
    store.mkdir(exist_ok=True)

    files = find_files(data_dir, list(extensions), recursive)
    if not files:
        print(f"No files found in '{data_dir.resolve()}' for extensions: {', '.join(extensions)}")
        return {"files": 0, "chunks": 0}

    texts, meta = [], []
    chunk_counts = {}  # per-file chunk count

    # Build chunks per file
    for p in files:
        raw = load_text_file(p)
        cs = chunk(raw, max_chars=max_chars)
        chunk_counts[str(p)] = len(cs)
        for c in cs:
            texts.append(c)
            meta.append({"source": str(p)})

    # Report per-file + totals
    total_chunks = sum(chunk_counts.values())
    print(f"Found {len(files)} file(s).")
    for f, n in chunk_counts.items():
        print(f"[OK] {f} | chunks={n}")
    print("\n---- SUMMARY ----")
    print(f"Files processed : {len(files)}")
    print(f"Total chunks    : {total_chunks}")

    # Always save counts for auditing
    (store / "chunk_counts.json").write_text(json.dumps(chunk_counts, indent=2))
    print(f"Wrote per-file counts -> {store/'chunk_counts.json'}")

    if dry_run or total_chunks == 0:
        print("(dry-run) Skipping embedding/index write." if dry_run else "No chunks to embed.")
        return {"files": len(files), "chunks": total_chunks}

    # Embed & index (same behavior you had)
    print("Embedding...")
    X = EMB.encode(texts, convert_to_numpy=True)
    print("Embedding shape:", X.shape)

    faiss.normalize_L2(X)  # cosine via inner product on normalized vectors
    idx = faiss.IndexFlatIP(X.shape[1])
    idx.add(X)

    faiss.write_index(idx, str(store / "faiss.index"))
    (store / "meta.json").write_text(json.dumps({"texts": texts, "meta": meta}))
    print(f"Ingested {total_chunks} chunks into {store_dir}")

    return {"files": len(files), "chunks": total_chunks}


def main():
    ap = argparse.ArgumentParser(description="Ingest files, count chunks, and build FAISS index.")
    ap.add_argument("--data-dir", default="data", help="Folder to read from")
    ap.add_argument("--store-dir", default="store", help="Folder to write index/meta/chunk counts")
    ap.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    ap.add_argument(
        "--exts",
        default=",".join(sorted(DEFAULT_EXTS)),
        help="Comma-separated list of extensions (e.g. .txt,.md,.py)",
    )
    ap.add_argument("--max-chars", type=int, default=700, help="Max chars per chunk")
    ap.add_argument("--dry-run", action="store_true", help="Count only; no embedding/index write")
    args = ap.parse_args()

    exts = [e.strip() for e in args.exts.split(",") if e.strip()]
    ingest(
        data_dir=args.data_dir,
        store_dir=args.store_dir,
        recursive=args.recursive,
        extensions=exts,
        max_chars=args.max_chars,
        dry_run=args.dry_run,
    )

if __name__ == "__main__":
    main()
