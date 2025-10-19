# backend/app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.models.schema import AskRequest, AskResponse, Source
from app.rag.retriever import RETR
from app.rag.generate import generate

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    q = body.question.strip()
    if len(q) < 3:
        raise HTTPException(status_code=422, detail="Question too short.")

    # 1) Retrieve top chunks
    hits = RETR.topk(q, 4)
    context = "\n\n".join([f"[{h['source']}]\n{h['text']}" for h in hits])

    # 2) Build prompt for grounded answer
    sys_prompt = (
        "You are FinChat. Answer using ONLY the CONTEXT below. "
        "Cite claims using [filename]. If context is insufficient, ask a brief clarifying question."
    )
    prompt = f"{sys_prompt}\n\nCONTEXT:\n{context}\n\nQUESTION: {q}\n\nANSWER (concise, <=120 words):"

    # 3) Call OpenAI
    answer, latency_ms = generate(prompt)

    # 4) Simple confidence heuristic
    def conf_tag(text: str):
        t = text.lower()
        risky = any(w in t for w in ["always", "never", "guaranteed", "must"])
        return "low" if risky else "medium"

    return AskResponse(
        answer=answer,
        sources=[Source(source=h["source"], score=h.get("score")) for h in hits],
        confidence=conf_tag(answer),
        latency_ms=latency_ms,
    )
