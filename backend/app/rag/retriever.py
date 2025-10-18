import json, faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path


class Retriever:
    def __init__(self, store_dir="store"):
        self.emb = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.idx = faiss.read_index(f"{store_dir}/faiss.index")
        obj = json.loads(Path(f"{store_dir}/meta.json").read_text())
        self.texts, self.meta = obj["texts"], obj["meta"]

    def topk(self, query: str, k=4):
        vec = self.emb.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(vec)
        D, I = self.idx.search(vec, k)
        hits = []
        for j, i in enumerate(I[0]):
            hits.append(
                {
                    "text": self.texts[i],
                    "source": self.meta[i]["source"],
                    "score": float(D[0][j]),
                }
            )
        return hits


RETR = Retriever()
