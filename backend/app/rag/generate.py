import os, time, requests
from app.core.config import settings

HF_TOKEN = settings.HF_TOKEN
MODEL = settings.HF_MODEL
URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


def generate(prompt: str, max_new_tokens=220, retries=2, timeout=60):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}
    for attempt in range(retries + 1):
        try:
            t0 = time.perf_counter()
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=timeout)
            r.raise_for_status()
            j = r.json()
            txt = (
                j[0]["generated_text"]
                if isinstance(j, list)
                else j.get("generated_text", "")
            )
            latency_ms = int((time.perf_counter() - t0) * 1000)
            return txt, latency_ms
        except Exception as e:
            time.sleep(1 + attempt)
    return "(model unavailable, try again)", 0
