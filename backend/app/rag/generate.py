# backend/app/rag/generate.py
from openai import OpenAI
from app.core.config import settings
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


LOCAL_ANSWERS = (
    (
        ("emergency", "fund"),
        "An emergency fund is cash set aside for unexpected expenses, such as a job loss, medical bill, or urgent repair. Start with a small target, then build toward roughly three to six months of essential expenses. Keep it somewhere safe and easy to access, such as a savings account. [emergency_fund.txt]",
    ),
    (
        ("credit", "score"),
        "To support your credit score, pay every bill on time, keep credit utilization low, and avoid applying for unnecessary new credit. Credit utilization is the percentage of your available credit that you are using. [credit_score_basics.txt] [credit_utilization.txt]",
    ),
    (
        ("debt", "avalanche"),
        "The debt avalanche method prioritizes the debt with the highest interest rate, while the debt snowball method prioritizes the smallest balance. Avalanche usually minimizes interest; snowball can provide quicker motivational wins. [debt_avalanche_vs_snowball.txt]",
    ),
    (
        ("saving", "invest"),
        "Saving is generally for short-term goals and emergencies, while investing is for longer-term growth and carries market risk. Build a basic emergency fund before investing money you may need soon. [investing_basics.txt] [savings_accounts.txt]",
    ),
    (
        ("50/30/20",),
        "The 50/30/20 budgeting guideline divides take-home income into about 50% for needs, 30% for wants, and 20% for savings or debt repayment. Treat it as a flexible starting point rather than a strict rule. [budgeting_50_30_20.txt]",
    ),
)


def local_answer(question: str) -> str:
    normalized = question.lower()
    for keywords, answer in LOCAL_ANSWERS:
        if all(keyword in normalized for keyword in keywords):
            return answer
    return "I can answer questions about emergency funds, budgeting, credit scores, credit utilization, savings, investing, and debt payoff. Please ask about one of those topics."


def generate(
    prompt: str, question: str = "", max_tokens: int = 220, temperature: float = 0.2
):
    import traceback

    if client is None:
        return local_answer(question), 0

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
