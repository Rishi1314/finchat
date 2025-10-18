from pathlib import Path
import json, faiss
from sentence_transformers import SentenceTransformer

EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def chunk(txt: str, max_chars=700):
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


def ingest(data_dir="data", store_dir="store"):
    texts, meta = [], []
    Path(store_dir).mkdir(exist_ok=True)
    for p in Path(data_dir).glob("*.txt"):
        raw = p.read_text(encoding="utf-8")
        for c in chunk(raw):
            texts.append(c)
            meta.append({"source": p.name})
    print(f"Found {len(texts)} chunks before embedding")
    X = EMB.encode(texts, convert_to_numpy=True)
    print("Embedding shape:", X.shape)
    faiss.normalize_L2(X)
    idx = faiss.IndexFlatIP(X.shape[1])
    idx.add(X)
    faiss.write_index(idx, f"{store_dir}/faiss.index")
    Path(f"{store_dir}/meta.json").write_text(
        json.dumps({"texts": texts, "meta": meta})
    )
    print(f"Ingested {len(texts)} chunks into {store_dir}")


if __name__ == "__main__":
    ingest()
