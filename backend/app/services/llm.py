"""LLM call. Swap provider here without touching the rest of the app."""
import os
from anthropic import Anthropic  # or: from openai import OpenAI

_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
MODEL = os.environ.get("TUTOR_MODEL", "claude-sonnet-4-6")


def tutor_reply(system_prompt: str, history: list[dict], user_msg: str) -> str:
    """history is a list of {"role": "user"|"assistant", "content": str}."""
    messages = history + [{"role": "user", "content": user_msg}]
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )
    return "".join(b.text for b in resp.content if b.type == "text")
