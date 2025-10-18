from pydantic import BaseModel, Field
from typing import List, Optional


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class Source(BaseModel):
    source: str
    score: Optional[float] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: Optional[str] = None
    latency_ms: Optional[int] = None
