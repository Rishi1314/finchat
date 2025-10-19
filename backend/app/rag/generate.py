# backend/app/rag/generate.py
from openai import OpenAI
from app.core.config import settings
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate(prompt: str, max_tokens: int = 220, temperature: float = 0.2):
    import traceback

    try:
        t0 = time.perf_counter()
        resp = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        latency_ms = int((time.perf_counter() - t0) * 1000)
        text = resp.choices[0].message.content.strip()
        return text, latency_ms
    except Exception as e:
        print("⚠️ OpenAI error:", e)
        traceback.print_exc()
        return "(model unavailable, internal error)", 0


# Quick test
if __name__ == "__main__":
    txt, ms = generate("Explain APR vs APY in one short paragraph.")
    print(txt, f"\n\nLatency: {ms} ms")
