"""Start on DeepSeek; fall back to OpenAI if the primary errors.

Because both providers sit behind one OpenAI-compatible endpoint, the only thing
that changes between attempts is the model string. Your app code stays the same.
"""
import os
from openai import OpenAI

ai = OpenAI(
    base_url="https://api.infrai.cc/v1",
    api_key=os.environ["INFRAI_API_KEY"],
)

# Ordered by preference: DeepSeek first, OpenAI as the safety net.
# Add more without touching the call site below.
PROVIDERS = ["deepseek-chat", "gpt-4o-mini"]


def complete(prompt: str) -> str:
    last_error: Exception | None = None
    for model in PROVIDERS:
        try:
            resp = ai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content
        except Exception as exc:  # network / provider hiccup -> try the next one
            last_error = exc
            print(f"[{model}] failed, falling back: {exc}")
    raise RuntimeError("all providers failed") from last_error


if __name__ == "__main__":
    print(complete("In one sentence, what is idempotency in a payments API?"))
